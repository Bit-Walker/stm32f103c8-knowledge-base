# HAL配置、句柄与状态编码

以固定STM32F1 HAL v1.1.10头文件为本页基准，v1.1.4差异单独说明。目标STM32F103C8。字段存在、宏存在、函数声明存在，分别只证明该项被定义；仍需结合实现分支与硬件条件判断可用性。

## 1 初始化结构

以下字段均为uint32_t，参数值应使用对应UART_或USART_符号，不将其他系列的配置值移入F1。

|结构|字段|含义|
|---|---|---|
|UART_InitTypeDef与USART_InitTypeDef|BaudRate|目标波特率；非零、当前PCLK可表示范围与实现的舍入算法须分别检查|
|两者|WordLength|8/9位字长；PCE使最高字长位置用于校验|
|两者|StopBits|停止位编码；UART头文件提供1/2位，USART头文件另定义0.5/1.5位，硬件模式约束仍须满足|
|两者|Parity|无、偶或奇校验，对应PCE/PS|
|两者|Mode|RX、TX或TX_RX，对应RE/TE|
|仅UART_InitTypeDef|HwFlowCtl|无、RTS、CTS或二者，低有效握手|
|仅UART_InitTypeDef|OverSampling|C8使用16倍；不因通用结构字段或注释推断本芯片有OVER8|
|仅USART_InitTypeDef|CLKPolarity|同步CK空闲低/高|
|仅USART_InitTypeDef|CLKPhase|第一/第二转换边沿采样|
|仅USART_InitTypeDef|CLKLastBit|是否输出最后数据位对应的CK脉冲|

UART_InitTypeDef共7个字段，USART_InitTypeDef共8个。正常USART实例时钟为PCLK1或PCLK2，不套用TIM内核时钟倍频规则。参数断言及分频缺陷见[版本边界](HAL数据宽度与版本边界.md)。

来源：[UART结构 L46–78](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L46-L78)、[USART结构 L44–80](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L44-L80)。

## 2 UART与USART状态枚举

|语义后缀|HAL_UART_STATE_编码|HAL_USART_STATE_编码|
|---|---:|---:|
|RESET|0x00|0x00|
|READY|0x20|0x01|
|BUSY|0x24|0x02|
|BUSY_TX|0x21|0x12|
|BUSY_RX|0x22|0x22|
|BUSY_TX_RX|0x23|0x32|
|TIMEOUT|0xA0|0x03|
|ERROR|0xE0|0x04|

UART的gState存全局/发送状态，RxState存接收状态；BUSY_TX_RX是查询时按位或的组合结果，不应直接写入任一字段。同步USART只有State，且其编码不同。不要把两套枚举强制转换后当作统一状态。

状态名TIMEOUT/ERROR被定义，不代表每条超时或出错路径都会把状态置成对应枚举；不少路径会返回超时或设置ErrorCode后把状态恢复READY。状态查询也不证明DMA与线路均已收尾。

来源：[UART枚举 L115–138](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L115-L138)、[USART枚举 L86–98](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L86-L98)。

## 3 句柄的全部非回调字段

|字段|UART_HandleTypeDef|USART_HandleTypeDef|含义|
|---|---|---|---|
|Instance|USART_TypeDef *|同左|硬件寄存器实例|
|Init|UART_InitTypeDef|USART_InitTypeDef|配置副本，须与硬件实际配置协调|
|pTxBuffPtr|const uint8_t *|同左|v1.1.10发送缓冲当前位置；v1.1.4为uint8_t *|
|TxXferSize|uint16_t|同左|发送请求数据项总数|
|TxXferCount|__IO uint16_t|同左|驱动软件计数，含义和递减时机依路径|
|pRxBuffPtr|uint8_t *|同左|接收缓冲当前位置|
|RxXferSize|uint16_t|同左|接收请求数据项总数|
|RxXferCount|__IO uint16_t|同左|接收软件计数，不等同于DMA硬件CNDTR|
|ReceptionType|__IO HAL_UART_RxTypeTypeDef|无|新版UART接收类型|
|RxEventType|__IO HAL_UART_RxEventTypeTypeDef|无|新版UART可变事件类型字段|
|hdmatx|DMA_HandleTypeDef *|同左|关联发送DMA句柄|
|hdmarx|DMA_HandleTypeDef *|同左|关联接收DMA句柄|
|Lock|HAL_LockTypeDef|同左|HAL软件锁对象，不等同于系统级互斥锁|
|gState|__IO HAL_UART_StateTypeDef|无|全局/发送软件状态|
|RxState|__IO HAL_UART_StateTypeDef|无|接收软件状态|
|State|无|__IO HAL_USART_StateTypeDef|同步USART单一状态|
|ErrorCode|__IO uint32_t|同左|HAL错误位集合|

__IO为CMSIS的易变访问限定，不把多个字段的读写变成原子快照。ReceptionType与RxEventType是v1.1.10相对固定v1.1.4的新增字段。应按本次DMA事务的映射关联正确hdmatx/hdmarx和各DMA句柄的Parent；内部回调经Parent恢复UART/USART句柄，不能仅填一个同名指针便认定关联正确。

来源：[UART句柄 L159–213](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L159-L213)、[USART句柄 L104–153](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L104-L153)；DMA关联与资源要求见[DMA生命周期](DMA生命周期.md)。

## 4 错误码与接收事件

两模块以各自HAL_UART_ERROR_或HAL_USART_ERROR_前缀定义以下数值；不能把SR原始位图直接当这个错误码。

|后缀|值|含义|
|---|---:|---|
|NONE|0x00|未记录错误|
|PE|0x01|校验错误|
|NE|0x02|噪声错误|
|FE|0x04|帧错误|
|ORE|0x08|接收覆盖错误|
|DMA|0x10|DMA传输错误|
|INVALID_CALLBACK|0x20|回调参数错误，仅对应动态回调注册开启时定义|

例如硬件SR.FE为bit1、SR.NE为bit2，而HAL_ERROR_FE/NE的数值按上表排列，需要逐项映射。ErrorCode还可能被后续API清零或重写，恢复前应保存需要的诊断信息。

v1.1.10 UART另有：HAL_UART_RECEPTION_STANDARD=0、HAL_UART_RECEPTION_TOIDLE=1；HAL_UART_RXEVENT_TC=0、HAL_UART_RXEVENT_HT=1、HAL_UART_RXEVENT_IDLE=2。RxEventType定义为uint32_t类型；它不是不可变事件队列，模式控制也可写它。

来源：[UART错误码及事件定义](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L140-L157)、[UART错误码 L253–266](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L253-L266)、[USART错误码 L193–208](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L193-L208)。

## 5 条件回调字段与声明/实现差异

动态回调启用时，UART句柄含TxHalfCpltCallback、TxCpltCallback、RxHalfCpltCallback、RxCpltCallback、ErrorCallback、AbortCpltCallback、AbortTransmitCpltCallback、AbortReceiveCpltCallback、WakeupCallback、RxEventCallback、MspInitCallback、MspDeInitCallback。RxEventCallback为新版新增，额外参数uint16_t Pos是事件位置；其余这些字段为只接收句柄参数、返回void的函数指针。

USART句柄含TxHalfCpltCallback、TxCpltCallback、RxHalfCpltCallback、RxCpltCallback、TxRxCpltCallback、ErrorCallback、AbortCpltCallback、MspInitCallback、MspDeInitCallback，均为句柄参数、void返回。两个句柄的回调布局和ID编码不可混用。

两份固定UART头文件都定义WakeupCallback字段和HAL_UART_WAKEUP_CB_ID=0x08，但所核对的两份UART.c中均未引用该字段或该ID；Register/UnRegister的switch没有对应case，会按default处理为无效回调。不能只根据头文件字段存在就声称该驱动支持一个可注册、可触发的Wakeup回调。

来源：[v1.1.10 UART字段/ID L197–234](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L197-L234)、[注册实现 L764–976](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L764-L976)、[USART字段及ID L136–180](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L136-L180)。

|回调ID语义|HAL_UART_…_CB_ID|HAL_USART_…_CB_ID|
|---|---|---|
|TX_HALFCOMPLETE|0x00|0x00|
|TX_COMPLETE|0x01|0x01|
|RX_HALFCOMPLETE|0x02|0x02|
|RX_COMPLETE|0x03|0x03|
|TX_RX_COMPLETE|无此ID|0x04|
|ERROR|0x04|0x05|
|ABORT_COMPLETE|0x05|0x06|
|ABORT_TRANSMIT_COMPLETE|0x06|无此ID|
|ABORT_RECEIVE_COMPLETE|0x07|无此ID|
|WAKEUP|0x08，固定实现不接受|无此ID|
|MSPINIT|0x0B|0x07|
|MSPDEINIT|0x0C|0x08|

RxEventCallback通过专用HAL_UART_RegisterRxEventCallback注册，不能为它补造上述通用ID。表中“无此ID”限定于所核对的固定头文件。
