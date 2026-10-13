# Smartcard 与 IrDA：DMA 启动、完成与错误边界
核查固定 ST HAL F1 v1.1.4（de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9）与 v1.1.10（77fbb30b7a1d02533980400083e48c559aae5a4f）。静态源码核查；没有新增运行或实机测试。下文注明已核对的完成/错误路径；尚未穷尽全部Abort重入、并发与循环传输交错。

## Smartcard RX 启动访问 TX DMA 句柄
两个版本的 HAL_SMARTCARD_Receive_DMA 均把 RX 完成、错误回调写入 hdmarx，却执行 hdmatx->XferAbortCallback = NULL。随后启动 hdmarx。
- 新版精确行：1026–1082，错误方向的访问在1054。
- 旧版精确行：1033–1089，错误方向的访问在1061。
- 入口检查 RxState、pData、Size 并加锁；该语句前没有 hdmatx 非空检查。
- 因此仅关联有效 RX DMA、TX 句柄为空的调用会到达空指针成员写入，属于未定义行为，存在故障风险；不声称所有构建都会产生同一种 HardFault。
- TX 句柄有效时，事实是其 Abort 回调被清空，RX Abort 回调未在此处清空。若两个指针别名，结论需按实际别名分析，不能以此推荐 TX/RX 共用句柄。
- 不据此声称任意后续 HAL Abort 必然调用旧回调：AbortReceive_IT、Abort_IT 和错误分支各自有重新安装回调的步骤。
- 源文件的 DMA 配置说明 L41–50 要求关联对应 Tx/Rx 通道，不能用含混的 Tx/Rx 措辞消除上述具体解引用风险。

来源：[新版RX启动](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_smartcard.c#L1026-L1082)、[旧版RX启动](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_smartcard.c#L1033-L1089)。

## 底层启动结果没有向上传递
已读两模块的 TX/RX DMA 入口：先改句柄状态及回调，再调用 HAL_DMA_Start_IT，调用结果未保存/检查，随后使能 USART DMA 请求并返回 HAL_OK。故外层 HAL_OK 不足以证明 DMA 已接受这一次启动。必须分别满足句柄、通道、Parent、状态、配置和缓冲所有权前提。
v1.1.10 HAL_DMA_Start_IT L361–406 在 DMA 状态非 READY 时返回 HAL_BUSY；专用外层没有对应回滚分支。

## Smartcard HT 回调字段保留
Smartcard 两个 DMA 入口没有赋值 XferHalfCpltCallback；IrDA 入口明确安装本模块 Half 回调。结合固定 v1.1.10 DMA Start_IT L385–393：半完成回调非空时会启用 HT 中断；IRQ L607–625 在事件到达且中断开启时调用该字段。
因此复用 DMA 句柄且残留非空半完成回调时，Smartcard 启动不会自动清除它，可能继续产生旧回调调用。全新且该字段为空的句柄不满足此条件；不宣称默认必然触发。需把句柄复用清理作为独立前提，不在活动传输上随意清除回调。

来源：[固定DMA启动](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_dma.c#L361-L406)、[固定DMA半完成IRQ](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_dma.c#L607-L625)。


## 完成事件
|路径|Smartcard|IrDA|
|---|---|---|
|TX DMA TC|无 CIRC 分支；计数归零、清 DMAT、开 TCIE，等 USART TC 路径|读硬件 CCR.CIRC；普通模式清 DMAT、开 TCIE；循环模式直接调用 TxCplt 回调，维持传输|
|RX DMA TC|无 CIRC 分支；计数归零、关 RXNE/PE/EIE、清 DMAR、RxState READY 后调用回调|普通模式计数归零、关 PE/EIE、清 DMAR、RxState READY；循环模式保留请求与状态；两种模式均调用 RxCplt|

Smartcard 不能从外层没有拒绝 DMA_CIRCULAR 推导出连续环形接收契约：其完成函数到第一次 DMA TC 即清请求，并且它本身不负责清 DMA CCR.EN。事件到达、DMA硬件停止、串口请求关闭、软件 READY、缓冲所有权交回必须分别判断。
IrDA 循环 TX 回调对应 DMA 一轮数据搬运，不等于最后一位已离开串口；普通 TX 路径则经 TCIE 等 USART TC。IrDA 循环 RX 回调并不冻结缓冲区。
Smartcard 也不能仅凭 DMA TC 当作线上发送结束；还需 USART TC，包括硬件 Smartcard guard-time 对 TC 的影响。

## DMA 错误回调
两模块均依据串口状态与 DMAT/DMAR 是否开启，调用各自 EndTxTransfer / EndRxTransfer，再调用用户 Error 回调。
这些 End 函数只处理串口中断与软件状态；未清 CR3.DMAT/DMAR，未停止另一 DMA 通道。不要把函数注释“Stop ... DMA request”直接抄成已实际清请求的结论。
- Smartcard 无条件把 RX/TX 两个计数归零，并将 ErrorCode 赋为 HAL_SMARTCARD_ERROR_DMA，可能覆盖已有错误位。
- IrDA 仅在各方向 BUSY 且对应请求开启时归零该方向计数；ErrorCode 用按位或保留已有错误位。
- 到达用户 Error 回调或串口状态 READY 不构成另一方向 DMA 已停、缓冲可重用的充分证据。完整安全恢复还需核对 DMA IRQ 自身及调用方的清理步骤；此稿没有完成所有错误/Abort 重入交错分析。

来源（固定新版；本文列出的十对完成/错误/End函数体与旧版逐对一致）：
- [Smartcard 完成与错误 L1832–1913](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_smartcard.c#L1832-L1913)
- [Smartcard End 函数 L1959–1983](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_smartcard.c#L1959-L1983)
- [IrDA 完成 L2085–2166](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_irda.c#L2085-L2166)
- [IrDA 错误 L2193–2223](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_irda.c#L2193-L2223)
- [IrDA End L2268–2290](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_irda.c#L2268-L2290)


## Abort 调用中的同步回调

固定 v1.1.10 的 HAL_DMA_Abort_IT 在 DMA 为 BUSY 时于函数返回前直接调用 XferAbortCallback。Smartcard 与 IrDA 的 HAL_*_Abort_IT 均先处理 TX，再重新读取 DMAR 决定是否处理 RX。因此用户 Abort 完成回调有可能在外层函数仍未返回时运行；在该回调内立即开启新一代接收，必须审查外层后续 RX 分支是否再次消费新传输。这里指出可重入控制流边界，没有宣称所有调用均发生重启后中止。

来源：[DMA Abort_IT L456–491](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_dma.c#L456-L491)、[Smartcard Abort_IT L1246–1359](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_smartcard.c#L1246-L1359)、[IrDA Abort_IT L1457–1548](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_irda.c#L1457-L1548)。

DMA IRQ错误分支处理的是触发该IRQ的DMA句柄；其清中断、置READY、解锁和错误回调顺序不能自动证明另一个DMA句柄已停止。见[固定DMA IRQ L654–680](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_dma.c#L654-L680)。

配套：[CPU数据宽度与初始化](Smartcard与IrDA数据宽度及初始化.md)、[UART/USART DMA生命周期](DMA生命周期.md)、[来源身份](../../来源/驱动实现.md#src-usart-dedicated-fixed-boundaries)。

IrDA启动路径来源：[TX/RX DMA L1040–1170](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_irda.c#L1040-L1170)。

## 严格前提下的回调重启接收路径

以下进一步追踪固定v1.1.10两模块，属于静态控制流分析，没有新增固件执行或实机故障复现。

### 需要同时满足的前提
- 调用 HAL_*_Abort_IT 前 DMAT=1、DMAR=0。
- TX DMA 句柄有效且 State=BUSY；RX DMA 是另一个有效、可启动的句柄，外层handle及Parent正确。
- 原用户 Abort 完成回调同步调用 HAL_*_Receive_DMA，并成功启动新的RX DMA；回调结束前DMAR仍为1、RX DMA仍BUSY。
- 不存在其它抢占、用户回调或寄存器写入改变以下路径；若新RX已完成、失败或被别处中止，不能套用本轨迹。

### 控制流顺序
1. 外层 Abort_IT 初始化回调：TX安装TxAbortCallback，因旧DMAR=0而将RX Abort回调置NULL。
2. 外层清DMAT并调用 HAL_DMA_Abort_IT(TX)。
3. DMA Abort_IT在原调用栈内关闭该DMA并置READY，调用TX Abort回调。
4. 模块TX Abort回调清自身回调，看到RX Abort回调为NULL，将串口两状态置READY，然后调用用户Abort完成回调。
5. 用户立即启动新RX，接收入口设置RxState=BUSY_RX，启动RX DMA并置DMAR。
   - IrDA Receive_DMA把RX Abort回调置NULL。
   - Smartcard Receive_DMA误清TX Abort回调；RX仍保留步骤1的NULL。
6. 用户回调返回，TX DMA Abort_IT返回HAL_OK，外层AbortCplt置0。
7. 外层随后重新读取DMAR，看到新RX的请求位，清DMAR并Abort新RX DMA。
8. 新RX DMA Abort成功，因其XferAbortCallback为NULL，不再调用模块RX Abort辅助函数；外层AbortCplt仍0，跳过最终状态恢复块而返回。
9. 在这些严格前提下，静态路径留下RX DMA READY、DMAR=0，但串口RxState仍BUSY_RX。具体硬件数据已搬运多少未由本分析确定。

此轨迹说明在“完成回调”内立即重启不一定跨越了外层函数的资源操作边界。应用需将新传输启动延后到外层Abort调用返回之后，并以本应用对传输代次、句柄和缓冲所有权的同步规则确认；此建议仅排除本条同步嵌套路径，不能代替完整中断并发证明。


来源：[Smartcard TX Abort回调 L2120–2153](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_smartcard.c#L2120-L2153)、[IrDA TX Abort回调 L2321–2355](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_irda.c#L2321-L2355)；外层Abort与DMA同步回调来源见上一节；Receive_DMA来源见启动边界节。

[专用HAL接口与版本原型](Smartcard与IrDA_HAL接口索引.md)。
