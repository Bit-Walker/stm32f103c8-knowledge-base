# UART与同步USART的DMA生命周期

固定比较STM32F1 HAL v1.1.4（de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9）与v1.1.10（77fbb30b7a1d02533980400083e48c559aae5a4f）。UART是异步驱动，主要以gState/RxState分别表示发送和接收状态；同步USART使用单一State，不能将两者的停止或回调条件互换。

本页整合已核对的源代码路径。此前的主机模型记录仅支持控制流、状态、写寄存器意图等有限结论；本轮没有运行模型或实机。DMA总线时序、实际线上字符与中断抢占必须由目标系统独立验证。

## 1 启动返回值与缓冲所有权

两版UART Transmit_DMA，以及旧版Receive_DMA/新版UART_Start_Receive_DMA，均未向上传播HAL_DMA_Start_IT失败。同步USART的发送、接收与双向DMA入口也未按其底层返回值完整回滚。

因此可能出现外层已写新句柄指针、计数、回调和忙状态，底层DMA因忙或锁拒绝，仍保留原地址和计数，而外层开启请求并返回HAL_OK。RX启动还含SR→DR清ORE序列。HAL_OK不能单独证明底层已接受本次缓冲。

应在应用的单一所有者或等效串行化机制下确认所需DMA资源、方向和配置均可用；随后核对本次启动结果。不能在仍属旧事务的通道上强改State/Lock来强行提交新缓冲。

来源：[UART v1.1.10 RX helper L3271–3323](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L3271-L3323)、[同步USART v1.1.10 DMA入口 L1240–1498](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L1240-L1498)。

### 1.1 UART普通与循环完成的边界

以下以本页两版 `HAL_UART_Transmit_DMA` 已正确启动、DMA 模式一致，且没有并发停止、中止或错误收尾为前提。普通发送分两级完成：

1. TX DMA 的 IRQ 交给 `HAL_DMA_IRQHandler(huart->hdmatx)`，内部 `UART_DMATransmitCplt` 清 `DMAT`、开 `TCIE`；此时 `gState` 仍为 `BUSY_TX`，尚未调用用户发送完成回调。
2. USART 的 IRQ 交给 `HAL_UART_IRQHandler(huart)`；检测到 `USART_SR.TC` 且 `TCIE` 已开后，才关闭 `TCIE`、将 `gState` 置 `READY`，并调用 `TxCpltCallback` 或弱 `HAL_UART_TxCpltCallback`。

因此，仅接入 DMA IRQ 会留下“DMA 已完成，但 UART 仍忙且没有发送完成回调”的状态。DMA TC 表示最后一项已搬到数据寄存器；USART TC 才是该发送路径的线路结束条件。确认发送源不再被 DMA 读取，与等待最后一帧发完是两件事；不能在 DMA TC 时就据此关闭发送器、进入 Stop 或切换外部收发方向。

循环 UART TX 在每轮 DMA TC 中直接调用同名发送完成回调，不执行上述等待 USART TC 的收尾，也不清 `DMAT` 或将 `gState` 置 `READY`。HT/TC 通知只提供分段处理机会，循环 DMA 仍会再次读取发送缓冲。

来源：[UART v1.1.4 DMA完成，L2542–2569](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_uart.c#L2542-L2569)、[v1.1.4 TC收尾，L2967–2984](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_uart.c#L2967-L2984)、[v1.1.10 DMA完成，L2988–3015](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L2988-L3015)、[v1.1.10 TC分发，L2578–2582](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L2578-L2582)、[UART_EndTransmit_IT，L3569–3585](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L3569-L3585)、[RM0008 Rev21 §27.3.13，p813](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=813)。

### 1.2 接收完成与同步USART须分别判断

已正确启动且配置一致时，两版普通 `HAL_UART_Receive_DMA` 的 DMA TC 路径会清 `DMAR`、关闭接收错误相关中断、将 `RxState` 置 `READY`，再调用接收完成回调；循环路径保留接收请求和忙状态。接收回调不等待 `USART_SR.TC`，也不表示同一 UART 上独立运行的发送已经完成。v1.1.10 的 `ReceiveToIdle_DMA` 改用 RxEvent 通知，具体位置、事件与结束条件见[ReceiveToIdle与事件位置](ReceiveToIdle与事件位置.md)；v1.1.4 不提供该接口。

同步 `HAL_USART_Transmit_DMA` 的普通单发送路径也会在 DMA 完成后打开 `TCIE`，由 `HAL_USART_IRQHandler` 完成线路 TC 收尾，但这段分支要求 `State==BUSY_TX`。不能将它套到 `BUSY_TX_RX` 的双向传输或用于提供时钟的伴随 TX DMA；这两类接收完成行为见 §4。

来源：[UART v1.1.4接收完成，L2596–2622](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_uart.c#L2596-L2622)、[UART v1.1.10接收完成，L3042–3096](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L3042-L3096)、[同步USART v1.1.4 TX完成，L2083–2114](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_usart.c#L2083-L2114)、[v1.1.10 TX完成，L2120–2151](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L2120-L2151)、[v1.1.10 TC收尾，L2532–2550](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L2532-L2550)。

## 2 同步Receive_DMA还读取同一缓冲来发送

两版HAL_USART_Receive_DMA均把pRxData同时放入接收和发送缓冲指针，并启动两路DMA：RX从USART_DR写入该缓冲，TX从同一缓冲读出并写USART_DR，为从机提供同步时钟。TX的完成/半完成用户回调被设为NULL，错误回调仍存在。

这意味着pRxData的要求包括可被DMA读取与写入；不能把本接口的发送值理解为固定dummy常数。CPU轮询/IT接收写DUMMY_DATA产生时钟的行为，不可直接套用到这个DMA实现。

若从设备要求确定的dummy值，应选择显式发送缓冲的双向接口并提供合适的数据与资源配置。循环模式、相同缓冲的覆盖顺序以及实际线上发送内容均取决于DMA配置和访问时序；此处不承诺每次发出的数据等于缓冲的哪一代内容。

Size仍是DMA数据项数。连续历史缓冲需要正确的MINC、MSIZE、PSIZE及容量；9位无校验须保留第9位，不可仅因入口指针类型为uint8_t就按字节推定配置。

来源：[v1.1.4 Receive_DMA L1280–1365](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_usart.c#L1280-L1365)、[v1.1.10 Receive_DMA L1307–1390](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L1307-L1390)。

## 3 暂停、停止与中止

|路径|固定实现的关键边界|
|---|---|
|UART DMAPause|关闭外设请求并处理相关中断，不等于DMA通道禁用或状态回收|
|UART DMAStop|各方向分支同时检查对应忙状态和DMAT/DMAR；Pause后请求位清零，可能跳过实际DMA资源|
|UART Abort/Abort_IT|是否中止底层DMA由DMAT/DMAR门控；Pause后可能已回报UART READY或中止完成，但DMA资源仍未回收|
|UART普通TX DMA完成到线路TC之间|DMAT已清，gState仍BUSY_TX，TCIE仍开；此时DMAStop可返回OK而不完成线路收尾|
|同步USART DMAStop，BUSY_TX_RX|仅精确匹配BUSY_TX或BUSY_RX，双向状态可使两个分支都不执行，仍返回OK|
|同步USART Receive_DMA后DMAStop|接收分支只终止RX并清DMAR；句柄READY时伴随TX DMA和DMAT仍可能保留|
|同步USART DMAPause后回收|Pause仅清DMAT，保留DMAR，不禁用DMA通道；后续按DMAT门控的TX中止分支可能跳过，RX仍需另行核对|

恢复时应检查本事务拥有的两路DMA EN、State、Lock、待处理中断/回调以及USART请求位。暂停后不要为了让某个Abort分支识别而贸然重新打开DMA请求。释放内存与协议线路收尾分别验收；READY或HAL_OK不足以替代这两类证据。

同步USART的DMAResume也只设置DMAT，不对残余计数、两路DMA状态或接收请求进行完整重建。Pause/Resume是请求位操作，不能当作重新启动一笔完整同步事务。

来源：[同步USART Pause/Resume L1496–1528](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L1496-L1528)、[UART v1.1.10暂停/恢复/停止 L1471–1580](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L1471-L1580)、[UART Abort L1859–2190](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L1859-L2190)、[同步USART v1.1.10停止 L1536–1580](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L1536-L1580)。

## 4 同步USART普通与循环完成

普通RX DMA完成会清DMAR和DMAT、关接收错误相关中断；它不会另行调用HAL_DMA_Abort回收伴随TX句柄。两个DMA的IRQ处理先后与真实数据搬运先后不同：即使双方计数都已经到0，若先服务RX IRQ，TX的HAL State/Lock仍可能等待TX IRQ清理。TX用户完成回调为NULL也不能省略DMA IRQ路由。

完成回调分派还有版本差异：

- v1.1.4先把USART State写READY，再比较它是否BUSY_RX，因此普通Receive_DMA走TxRxCpltCallback。
- v1.1.10先按原忙状态分派，Receive_DMA走RxCpltCallback，然后才写READY；回调执行期间仍BUSY_RX，立即再次Receive_DMA会返回HAL_BUSY。
- 循环RX分支有意保持请求和忙状态，Receive模式调用RxCplt，双向模式调用TxRxCplt。循环分段回调不表示整体事务结束。

来源：[v1.1.4 L2141–2210](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_usart.c#L2141-L2210)、[v1.1.10 L2178–2245](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L2178-L2245)。

## 5 同步USART错误回调不证明双方均已停止

DMA自身传输错误经过DMA IRQ和USART_DMAError：出错方向的DMA状态会收尾，USART上层可READY并通知ErrorCallback；两个请求位及另一方向DMA可能仍保留。USART_DMAError不统一Abort伴随方向。

USART线路ORE等走另一条路径：在DMA接收活跃时结束接收、清DMAR并Abort RX，仍可留下TX DMA与DMAT。这个路径不能与DMA自身TE混为同一种资源结果。真实剩余时钟/数据还受通道计数及外设时序影响，不根据EN残留就声称无限持续发送。

来源：[v1.1.10 DMA完成/错误 L2118–2301](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L2118-L2301)、[线路错误IRQ L1784–1930](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L1784-L1930)、[EndRx及错误回调 L2369–2403](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L2369-L2403)。

## 6 Abort_IT回调可能早于外层返回

F1的HAL_DMA_Abort_IT在BUSY分支直接执行非空XferAbortCallback。由UART_Abort_IT调用时，用户完成回调可能在外层函数返回前发生。已核对的单TX活动场景中，回调内启动新Receive_DMA，外层返回前继续检查新DMAR，可能将这笔新RX中止。

因此回调名含IT不表示回调一定延迟到另一次IRQ。回调可先记录事件，待外层退出并核验资源后再由事务所有者提交下一笔；这是针对该重入关系的处理原则，不是对任意多线程/IRQ场景的完整安全证明。

来源：[UART v1.1.10 Abort_IT范围](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L2047-L2190)、[F1 DMA Abort_IT L455–495](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_dma.c#L455-L495)。

## 7 UART错误与缓冲交接

本节针对异步 UART，两版都有以下区别；它与 §5 的同步 USART 状态机分别核对。

- **DMA 自身传输错误。** `HAL_DMA_IRQHandler` 处理出错通道的 TE 后进入 `UART_DMAError`。后者按各方向的忙状态与 `DMAT/DMAR` 条件调用 `UART_EndTxTransfer` / `UART_EndRxTransfer`，但这些 helper 不清两个 DMA 请求位，也不 Abort 另一方向 DMA。若 TX、RX 同时活跃，错误回调可能已经看到两个 UART 状态均为 `READY`，而未出错方向仍可访问其缓冲。不能因为句柄已就绪就释放两个方向的缓冲。
- **UART 接收线路错误。** IRQ 按已使能的错误源记入 `ErrorCode`；接收 DMA 请求 `DMAR` 仍开时，该错误路径结束接收、清 `DMAR`，并对关联 RX DMA 调用 `HAL_DMA_Abort_IT`，随后通知 `ErrorCallback`。它不会一并中止独立 TX DMA；即使错误 helper 把 `TxXferCount` 清零，也不代表 TX 通道已经停止。DMA Abort 失败时还有直接通知错误回调的路径，故异常状态下仍需核验实际资源。

停止、错误和中止后的缓冲交接，应确认本事务各方向的 DMA 不再访问旧内存，并处理仍可能引用旧事务的中断、回调及待消费数据，再释放或重新提交缓冲。`READY`、错误回调和中止回调都不能单独替代这些条件；§3 的请求位门控和 §6 的同步重入边界仍然适用。

来源：[UART v1.1.4 DMA错误及EndTransfer，L2649–2744](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_uart.c#L2649-L2744)、[v1.1.4线路错误，L2041–2144](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_uart.c#L2041-L2144)、[UART v1.1.10 DMA错误，L3143–3172](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L3143-L3172)、[v1.1.10 EndTransfer与错误通知，L3321–3372](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L3321-L3372)、[v1.1.10线路错误，L2370–2475](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L2370-L2475)、[DMA TE收尾，L653–678](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_dma.c#L653-L678)。
