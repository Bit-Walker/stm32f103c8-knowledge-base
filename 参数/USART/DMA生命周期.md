# UART与同步USART的DMA生命周期

固定比较STM32F1 HAL v1.1.4（de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9）与v1.1.10（77fbb30b7a1d02533980400083e48c559aae5a4f）。UART是异步驱动，主要以gState/RxState分别表示发送和接收状态；同步USART使用单一State，不能将两者的停止或回调条件互换。

本页整合已核对的源代码路径。此前的主机模型记录仅支持控制流、状态、写寄存器意图等有限结论；本轮没有运行模型或实机。DMA总线时序、实际线上字符与中断抢占必须由目标系统独立验证。

## 1 启动返回值与缓冲所有权

两版UART Transmit_DMA，以及旧版Receive_DMA/新版UART_Start_Receive_DMA，均未向上传播HAL_DMA_Start_IT失败。同步USART的发送、接收与双向DMA入口也未按其底层返回值完整回滚。

因此可能出现外层已写新句柄指针、计数、回调和忙状态，底层DMA因忙或锁拒绝，仍保留原地址和计数，而外层开启请求并返回HAL_OK。RX启动还含SR→DR清ORE序列。HAL_OK不能单独证明底层已接受本次缓冲。

应在应用的单一所有者或等效串行化机制下确认所需DMA资源、方向和配置均可用；随后核对本次启动结果。不能在仍属旧事务的通道上强改State/Lock来强行提交新缓冲。

来源：[UART v1.1.10 RX helper L3271–3323](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L3271-L3323)、[同步USART v1.1.10 DMA入口 L1240–1498](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L1240-L1498)。

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
|UART DMAStop/Abort|分支依赖忙状态及DMAT/DMAR；Pause后请求位清零，后续Stop/Abort可能跳过实际DMA资源|
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
