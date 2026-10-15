# UART ReceiveToIdle 与事件位置

本页仅对应 STM32F1 HAL v1.1.10，固定提交 77fbb30b7a1d02533980400083e48c559aae5a4f，适用 C8 异步 UART 接收。v1.1.4 的对应头文件没有下列 ReceiveToIdle/RxEvent 接口；不能把新版处理器行为直接写进旧版调用说明。以下为固定源码静态核查，未模拟真实中断、DMA请求、寄存器清标志或线上的数据流。

## 1 接口与计数单位

|接口|主要参数|结果或通知|
|---|---|---|
|HAL_UARTEx_ReceiveToIdle|huart、pData、uint16_t Size、uint16_t *RxLen、uint32_t Timeout|阻塞接收，返回HAL_StatusTypeDef；RxLen记录已经写入缓冲的项数|
|HAL_UARTEx_ReceiveToIdle_IT|huart、pData、uint16_t Size|启动中断接收，后续由RxEvent回调报告|
|HAL_UARTEx_ReceiveToIdle_DMA|huart、pData、uint16_t Size|启动DMA接收，HT、TC和符合条件的IDLE均可能报告RxEvent|
|HAL_UARTEx_GetRxEventType|huart|返回句柄中的HAL_UART_RxEventTypeTypeDef字段|
|HAL_UARTEx_RxEventCallback|huart、uint16_t Size|默认弱回调，返回void；Size的事件含义见下表|
|HAL_UART_RegisterRxEventCallback|huart、pUART_RxEventCallbackTypeDef pCallback|启用动态回调注册时，设置RxEvent回调，返回HAL_StatusTypeDef|
|HAL_UART_UnRegisterRxEventCallback|huart|启用动态回调注册时恢复默认弱回调，返回HAL_StatusTypeDef|

huart为UART_HandleTypeDef指针，pData为uint8_t指针形式的数据区入口。Size和RxLen均按数据项计数。9位且无校验时，轮询/IT按uint16_t元素保存数据；其他所述帧格式按uint8_t元素保存，校验占位另按有效数据掩码处理。DMA的外设及内存宽度仍由关联DMA配置决定，指针的C类型不自动配置宽度；连续保存整段结果还需要MINC=1及相应容量、对齐。

Timeout单位为HAL毫秒tick；HAL_MAX_DELAY代表不检查该有限超时条件。RxLen必须指向可写uint16_t存储；固定阻塞实现检查pData和Size，但没有在解引用前检查RxLen是否为空。所有异步缓冲、句柄和关联DMA资源必须保持有效。

来源：[接口声明，头文件L748–764](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L748-L764)、[阻塞实现，L1591–1706](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L1591-L1706)。

## 2 RxEvent 的 Size 是位置或累计进度

下表适用于已正确启动、请求长度固定的 `ReceiveToIdle_DMA` 事务。请求长度记为 $N$，即本次传入的 `Size`，单位为数据项；$\mathrm{CNDTR}$ 为读取时 DMA 剩余项数。表中的 TC 是接收达到 $N$ 项时的 HAL 接收事件，不是 `USART_SR.TC` 发送完成标志。

使用下表前，须保证 DMA 句柄的 `Init.Mode` 与硬件 `CCR.CIRC` 一致。IDLE 收尾按前者分支，DMA 完整回调按后者分支；修改其中一处不能保证另一处自动同步。

表内回调数值均以数据项为单位。$\lfloor N/2\rfloor$ 表示 $N$ 除以 2 后向下取整，即整数商；$N-\mathrm{CNDTR}$ 表示本次长度减去读取时剩余项数。

|事件|回调 `Size` 实参|普通 DMA|循环 DMA|
|---|---|---|---|
|HT|$\lfloor N/2\rfloor$|继续接收|继续接收|
|TC|$N$|关闭接收 DMA 请求及相应中断，`RxState` 置 `READY`|继续接收，保留忙状态|
|IDLE，且 $0<\mathrm{CNDTR}<N$|$N-\mathrm{CNDTR}$|清请求、关闭相关接收中断，调用 DMA Abort 并报告|保留接收，报告当前环内进度|
|IDLE，但 $\mathrm{CNDTR}=0$ 或 $\mathrm{CNDTR}=N$|该 IDLE 分支不调用 RxEvent|完整完成由 DMA 完成路径报告|未报告 IDLE 不代表没有数据；还须结合 TC 及回卷时序判断|

### 2.1 重复位置与环尾位置

`Size` 表示位置或累计进度，不是距上一次回调新增的数据项数。例如，$N$ 为正偶数时，HT 报告 $N/2$ 项；随后发生 IDLE，若读取时进度未变，仍可报告同一位置。把两次 `Size` 相加会重复计数。

循环 DMA 的 TC 报告 $N$，表示本轮环尾位置，不能直接当作 0。应用可以在明确的游标规则中处理环尾，但须保留相应代际和未消费区段。

### 2.2 中断延迟与回卷

软件在处理 IDLE 时才读取 `CNDTR`；硬件不会在 IDLE 事件发生时替软件锁存这个长度。中断延迟期间可能又有数据到达，相同的位置值也可能对应已经回卷一圈或多圈的状态。

HT、TC、IDLE 应交给同一个串行化的消费机制处理，并按最早覆盖时刻安排处理预算。单个事件标志或位置值不能证明多圈数据没有丢失。

若采用前后半区模型，$N$ 应为正偶数。表中的 $N/2$ 整数商只说明源码传给回调的数值，不保证奇数长度时的硬件半传输边界。

来源：[IRQ中的IDLE分支，L2478–2582](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L2478-L2582)、[DMA完整/半完整回调，L3042–3140](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L3042-L3140)。

## 3 事件类型是可变句柄字段

HAL_UARTEx_GetRxEventType直接返回huart中的RxEventType，没有读取硬件事件队列。固定实现可写入HAL_UART_RXEVENT_HT、TC或IDLE；调用说明建议在RxEvent回调内取得此次事件类型。缓存回调参数、事件类型与自己的事务代际时，还须处理UART和DMA中断之间的并发，不能在较晚时刻读该字段后断言它仍属于某个旧回调。

IT模式通过TC或IDLE结束接收，不产生DMA半传输事件。DMA模式的HT不结束普通接收，循环模式的HT/TC/IDLE都不会仅因该事件而结束接收。错误分支另行处理，不能从“循环模式”推出发生错误后仍持续接收。

固定v1.1.10的HAL_MultiProcessor_EnterMuteMode与ExitMuteMode也会把RxEventType写成HAL_UART_RXEVENT_TC。因此在回调后执行其他控制API，再查询GetRxEventType，结果未必仍表示刚才那一次DMA/IDLE通知。需要在相应回调的受控上下文保存事件类型和位置，并协调同一句柄的其他操作。

来源：[v1.1.10模式控制 L2780–2829](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L2780-L2829)。

来源：[事件类型说明与GetRxEventType，L1814–1845](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L1814-L1845)。

## 4 启动与停止的检查边界

ReceiveToIdle_DMA先检查RxState、pData及非零Size，设置接收类型和事件字段，再调用UART_Start_Receive_DMA。后者会改写DMA回调和UART状态，调用HAL_DMA_Start_IT，却不检查其返回值，之后清ORE并开放接收请求。因此外层HAL_OK不能单独证明DMA已经接受本次地址和长度；资源独占、正确关联、通道状态和入口串行化仍是前提。

外层根据ReceptionType是否仍为TOIDLE判断是否继续清IDLE并开放IDLEIE；已经发生错误而结束接收可能改变该字段。清ORE和清IDLE都涉及SR→DR读取，可能影响已有接收数据，因此接收应在允许对端发送之前准备好，不能依赖启动动作保存先到的首字节。

普通DMA的部分IDLE分支先关闭接收请求及相关中断、将RxState置READY，再调用HAL_DMA_Abort，且不传播Abort返回值。回调与READY不构成对所有异常入口状态的硬件停止认证；尤其在先前错误、暂停或资源状态不一致时，仍须分别核实DMA与缓冲归属。不能通过手改State绕过这些条件。

来源：[ReceiveToIdle_DMA，L1776–1811](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L1776-L1811)、[UART_Start_Receive_DMA，L3271–3318](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L3271-L3318)、[普通DMA的IDLE收尾，L2501–2545](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L2501-L2545)。

## 5 阻塞接收的IDLE与超时顺序

固定阻塞实现每轮先检查并清IDLE，再检查RXNE、读取数据，最后检查超时。没有收到任何数据时，IDLE被清除但不会令函数成功结束；已有数据时，符合IDLE分支会先返回HAL_OK。IDLE清除可能读取DR，不能把它视为不接触数据的纯状态查询。

超时基准从本次调用开始计时，不会每收一个字符就重新开始。Timeout=0仍可能先读取一个已经就绪的数据项，然后返回HAL_TIMEOUT；若该项恰好填满本次Size，仍会先执行这一轮的超时判断。因此HAL_TIMEOUT不等于RxLen必为0，也不等于缓冲没有被修改。有限超时依赖HAL_GetTick推进，不是含全部抢占延迟的硬实时上限。

这段轮询主体没有逐项检查PE、FE、NE、ORE并据此返回错误的分支。HAL_OK只描述此函数的长度或IDLE结束路径，不额外证明每个字符都无硬件错误。应用的错误保存和协议校验仍需明确；本页不凭静态分支推断特定错误发生概率。

来源：[ReceiveToIdle轮询主体，L1591–1706](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L1591-L1706)。

## 6 动态注册不提供接收事务隔离

动态注册接口在USE_HAL_UART_REGISTER_CALLBACKS启用时提供。Register拒绝空pCallback；进入锁保护主体后，Register和UnRegister以gState==READY作为更改条件，没有同时要求RxState==READY。gState和RxState分别承担不同状态，因此“注册成功”不能证明接收闲置。

已在进行的RX事务应保持回调归属稳定，在受控停机和资源交接后再替换。UnRegister恢复默认弱HAL_UARTEx_RxEventCallback，并非把指针设空。锁宏及应用重入行为需要按实际工程另核，不能从此处的gState条件推导跨中断事务安全。

来源：[Register/UnRegisterRxEventCallback，L981–1041](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L981-L1041)。


## 7 芯片层面的IDLE与校验限制

ReceiveToIdle还须结合[USART硅勘误](硅勘误.md)。ES096 Rev15 §2.9.2明确存在接收时钟偏差导致IDLE不置位的情形；驱动提供这个接口不消除该硬件边界。§2.9.1与§2.9.3分别约束PE清除时机及全双工发送路径的副作用。
