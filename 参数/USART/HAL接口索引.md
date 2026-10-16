# HAL UART与USART接口索引

版本固定为v1.1.4与v1.1.10，按官方头文件声明逐项收录。这里区分异步UART模块（包括LIN、半双工、多处理器入口）与同步USART模块；相同外设硬件不意味着两个句柄及状态机可以互换。

[配置、句柄与状态编码](HAL配置句柄与状态.md)另列结构字段和常量。

本索引保存完整参数类型与顺序，避免按函数名猜测。const是两版间的真实声明差异；表示该形参类型的只读约束，不表示DMA或接收方向不会访问同一内存。Register/UnRegister回调声明受对应USE_HAL_*_REGISTER_CALLBACKS条件控制。

- Size为数据项数，9位无校验需要能容纳uint16_t项的缓冲；CPU访问的旧版缺陷见[数据宽度与版本边界](HAL数据宽度与版本边界.md)。DMA还需独立核对MSIZE、PSIZE、MINC。
- 阻塞入口的Timeout以HAL tick计时；返回类型列不是每个函数都能返回所有HAL状态的承诺。
- DMA启动、暂停、中止与回调的所有权边界见[DMA生命周期](DMA生命周期.md)。
- 新版ReceiveToIdle/RxEvent的Size与事件语义见[接收直到空闲](ReceiveToIdle与事件位置.md)。

按模块与版本：异步UART [v1.1.4](#v114) · [v1.1.10](#v1110)；同步USART [v1.1.4](#v114-1) · [v1.1.10](#v1110-1)。

## UART模块

固定v1.1.4声明40个名称，v1.1.10声明47个。此数包含条件回调声明，并非所有工程配置都编译出这些入口。

### v1.1.4

按任务：[初始化与MSP](#初始化与msp) · [模式控制](#模式控制) · [发送与接收](#发送与接收) · [DMA控制与传输中止](#dma控制与传输中止) · [中断入口与回调](#中断入口与回调) · [回调注册与条件编译](#回调注册与条件编译) · [状态与错误查询](#状态与错误查询)。

#### 初始化与MSP

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_UART_Init`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L677](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L677-L677)|
|`HAL_HalfDuplex_Init`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L678](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L678-L678)|
|`HAL_LIN_Init`|`UART_HandleTypeDef *huart, uint32_t BreakDetectLength`|`HAL_StatusTypeDef`|[L679](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L679-L679)|
|`HAL_MultiProcessor_Init`|`UART_HandleTypeDef *huart, uint8_t Address, uint32_t WakeUpMethod`|`HAL_StatusTypeDef`|[L680](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L680-L680)|
|`HAL_UART_DeInit`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L681](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L681-L681)|
|`HAL_UART_MspInit`|`UART_HandleTypeDef *huart`|`void`|[L682](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L682-L682)|
|`HAL_UART_MspDeInit`|`UART_HandleTypeDef *huart`|`void`|[L683](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L683-L683)|

#### 模式控制

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_LIN_SendBreak`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L735](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L735-L735)|
|`HAL_MultiProcessor_EnterMuteMode`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L736](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L736-L736)|
|`HAL_MultiProcessor_ExitMuteMode`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L737](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L737-L737)|
|`HAL_HalfDuplex_EnableTransmitter`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L738](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L738-L738)|
|`HAL_HalfDuplex_EnableReceiver`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L739](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L739-L739)|

#### 发送与接收

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_UART_Transmit`|`UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size, uint32_t Timeout`|`HAL_StatusTypeDef`|[L700](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L700-L700)|
|`HAL_UART_Receive`|`UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size, uint32_t Timeout`|`HAL_StatusTypeDef`|[L701](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L701-L701)|
|`HAL_UART_Transmit_IT`|`UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size`|`HAL_StatusTypeDef`|[L702](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L702-L702)|
|`HAL_UART_Receive_IT`|`UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size`|`HAL_StatusTypeDef`|[L703](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L703-L703)|
|`HAL_UART_Transmit_DMA`|`UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size`|`HAL_StatusTypeDef`|[L704](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L704-L704)|
|`HAL_UART_Receive_DMA`|`UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size`|`HAL_StatusTypeDef`|[L705](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L705-L705)|

#### DMA控制与传输中止

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_UART_DMAPause`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L706](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L706-L706)|
|`HAL_UART_DMAResume`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L707](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L707-L707)|
|`HAL_UART_DMAStop`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L708](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L708-L708)|
|`HAL_UART_Abort`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L710](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L710-L710)|
|`HAL_UART_AbortTransmit`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L711](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L711-L711)|
|`HAL_UART_AbortReceive`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L712](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L712-L712)|
|`HAL_UART_Abort_IT`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L713](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L713-L713)|
|`HAL_UART_AbortTransmit_IT`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L714](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L714-L714)|
|`HAL_UART_AbortReceive_IT`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L715](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L715-L715)|

#### 中断入口与回调

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_UART_IRQHandler`|`UART_HandleTypeDef *huart`|`void`|[L717](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L717-L717)|
|`HAL_UART_TxCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L718](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L718-L718)|
|`HAL_UART_TxHalfCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L719](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L719-L719)|
|`HAL_UART_RxCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L720](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L720-L720)|
|`HAL_UART_RxHalfCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L721](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L721-L721)|
|`HAL_UART_ErrorCallback`|`UART_HandleTypeDef *huart`|`void`|[L722](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L722-L722)|
|`HAL_UART_AbortCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L723](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L723-L723)|
|`HAL_UART_AbortTransmitCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L724](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L724-L724)|
|`HAL_UART_AbortReceiveCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L725](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L725-L725)|

#### 回调注册与条件编译

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_UART_RegisterCallback`|`UART_HandleTypeDef *huart, HAL_UART_CallbackIDTypeDef CallbackID, pUART_CallbackTypeDef pCallback`|`HAL_StatusTypeDef`|[L687](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L687-L687)|
|`HAL_UART_UnRegisterCallback`|`UART_HandleTypeDef *huart, HAL_UART_CallbackIDTypeDef CallbackID`|`HAL_StatusTypeDef`|[L688](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L688-L688)|

#### 状态与错误查询

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_UART_GetState`|`UART_HandleTypeDef *huart`|`HAL_UART_StateTypeDef`|[L748](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L748-L748)|
|`HAL_UART_GetError`|`UART_HandleTypeDef *huart`|`uint32_t`|[L749](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L749-L749)|

### v1.1.10

按任务：[初始化与MSP](#初始化与msp-1) · [模式控制](#模式控制-1) · [发送与接收](#发送与接收-1) · [DMA控制与传输中止](#dma控制与传输中止-1) · [中断入口与回调](#中断入口与回调-1) · [回调注册与条件编译](#回调注册与条件编译-1) · [状态与事件查询](#状态与事件查询)。

#### 初始化与MSP

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_UART_Init`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L722](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L722-L722)|
|`HAL_HalfDuplex_Init`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L723](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L723-L723)|
|`HAL_LIN_Init`|`UART_HandleTypeDef *huart, uint32_t BreakDetectLength`|`HAL_StatusTypeDef`|[L724](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L724-L724)|
|`HAL_MultiProcessor_Init`|`UART_HandleTypeDef *huart, uint8_t Address, uint32_t WakeUpMethod`|`HAL_StatusTypeDef`|[L725](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L725-L725)|
|`HAL_UART_DeInit`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L726](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L726-L726)|
|`HAL_UART_MspInit`|`UART_HandleTypeDef *huart`|`void`|[L727](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L727-L727)|
|`HAL_UART_MspDeInit`|`UART_HandleTypeDef *huart`|`void`|[L728](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L728-L728)|

#### 模式控制

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_LIN_SendBreak`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L794](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L794-L794)|
|`HAL_MultiProcessor_EnterMuteMode`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L795](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L795-L795)|
|`HAL_MultiProcessor_ExitMuteMode`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L796](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L796-L796)|
|`HAL_HalfDuplex_EnableTransmitter`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L797](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L797-L797)|
|`HAL_HalfDuplex_EnableReceiver`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L798](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L798-L798)|

#### 发送与接收

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_UART_Transmit`|`UART_HandleTypeDef *huart, const uint8_t *pData, uint16_t Size, uint32_t Timeout`|`HAL_StatusTypeDef`|[L749](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L749-L749)|
|`HAL_UART_Receive`|`UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size, uint32_t Timeout`|`HAL_StatusTypeDef`|[L750](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L750-L750)|
|`HAL_UART_Transmit_IT`|`UART_HandleTypeDef *huart, const uint8_t *pData, uint16_t Size`|`HAL_StatusTypeDef`|[L751](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L751-L751)|
|`HAL_UART_Receive_IT`|`UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size`|`HAL_StatusTypeDef`|[L752](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L752-L752)|
|`HAL_UART_Transmit_DMA`|`UART_HandleTypeDef *huart, const uint8_t *pData, uint16_t Size`|`HAL_StatusTypeDef`|[L753](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L753-L753)|
|`HAL_UART_Receive_DMA`|`UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size`|`HAL_StatusTypeDef`|[L754](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L754-L754)|
|`HAL_UARTEx_ReceiveToIdle`|`UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size, uint16_t *RxLen, uint32_t Timeout`|`HAL_StatusTypeDef`|[L759](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L759-L760)|
|`HAL_UARTEx_ReceiveToIdle_IT`|`UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size`|`HAL_StatusTypeDef`|[L761](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L761-L761)|
|`HAL_UARTEx_ReceiveToIdle_DMA`|`UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size`|`HAL_StatusTypeDef`|[L762](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L762-L762)|

#### DMA控制与传输中止

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_UART_DMAPause`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L755](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L755-L755)|
|`HAL_UART_DMAResume`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L756](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L756-L756)|
|`HAL_UART_DMAStop`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L757](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L757-L757)|
|`HAL_UART_Abort`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L767](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L767-L767)|
|`HAL_UART_AbortTransmit`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L768](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L768-L768)|
|`HAL_UART_AbortReceive`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L769](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L769-L769)|
|`HAL_UART_Abort_IT`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L770](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L770-L770)|
|`HAL_UART_AbortTransmit_IT`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L771](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L771-L771)|
|`HAL_UART_AbortReceive_IT`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L772](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L772-L772)|

#### 中断入口与回调

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_UART_IRQHandler`|`UART_HandleTypeDef *huart`|`void`|[L774](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L774-L774)|
|`HAL_UART_TxCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L775](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L775-L775)|
|`HAL_UART_TxHalfCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L776](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L776-L776)|
|`HAL_UART_RxCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L777](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L777-L777)|
|`HAL_UART_RxHalfCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L778](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L778-L778)|
|`HAL_UART_ErrorCallback`|`UART_HandleTypeDef *huart`|`void`|[L779](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L779-L779)|
|`HAL_UART_AbortCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L780](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L780-L780)|
|`HAL_UART_AbortTransmitCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L781](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L781-L781)|
|`HAL_UART_AbortReceiveCpltCallback`|`UART_HandleTypeDef *huart`|`void`|[L782](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L782-L782)|
|`HAL_UARTEx_RxEventCallback`|`UART_HandleTypeDef *huart, uint16_t Size`|`void`|[L784](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L784-L784)|

#### 回调注册与条件编译

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_UART_RegisterCallback`|`UART_HandleTypeDef *huart, HAL_UART_CallbackIDTypeDef CallbackID, pUART_CallbackTypeDef pCallback`|`HAL_StatusTypeDef`|[L732](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L732-L733)|
|`HAL_UART_UnRegisterCallback`|`UART_HandleTypeDef *huart, HAL_UART_CallbackIDTypeDef CallbackID`|`HAL_StatusTypeDef`|[L734](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L734-L734)|
|`HAL_UART_RegisterRxEventCallback`|`UART_HandleTypeDef *huart, pUART_RxEventCallbackTypeDef pCallback`|`HAL_StatusTypeDef`|[L736](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L736-L736)|
|`HAL_UART_UnRegisterRxEventCallback`|`UART_HandleTypeDef *huart`|`HAL_StatusTypeDef`|[L737](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L737-L737)|

#### 状态与事件查询

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_UARTEx_GetRxEventType`|`UART_HandleTypeDef *huart`|`HAL_UART_RxEventTypeTypeDef`|[L764](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L764-L764)|
|`HAL_UART_GetState`|`const UART_HandleTypeDef *huart`|`HAL_UART_StateTypeDef`|[L807](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L807-L807)|
|`HAL_UART_GetError`|`const UART_HandleTypeDef *huart`|`uint32_t`|[L808](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L808-L808)|

名称增加：HAL_UARTEx_GetRxEventType、HAL_UARTEx_ReceiveToIdle、HAL_UARTEx_ReceiveToIdle_DMA、HAL_UARTEx_ReceiveToIdle_IT、HAL_UARTEx_RxEventCallback、HAL_UART_RegisterRxEventCallback、HAL_UART_UnRegisterRxEventCallback。名称删除：无。

## USART模块

固定v1.1.4声明30个名称，v1.1.10声明30个。此数包含条件回调声明，并非所有工程配置都编译出这些入口。

### v1.1.4

按任务：[初始化与MSP](#初始化与msp-2) · [同步收发](#同步收发) · [DMA控制与传输中止](#dma控制与传输中止-2) · [中断入口与回调](#中断入口与回调-2) · [回调注册与条件编译](#回调注册与条件编译-2) · [状态与错误查询](#状态与错误查询-1)。

#### 初始化与MSP

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_USART_Init`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L492](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L492-L492)|
|`HAL_USART_DeInit`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L493](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L493-L493)|
|`HAL_USART_MspInit`|`USART_HandleTypeDef *husart`|`void`|[L494](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L494-L494)|
|`HAL_USART_MspDeInit`|`USART_HandleTypeDef *husart`|`void`|[L495](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L495-L495)|

#### 同步收发

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_USART_Transmit`|`USART_HandleTypeDef *husart, uint8_t *pTxData, uint16_t Size, uint32_t Timeout`|`HAL_StatusTypeDef`|[L511](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L511-L511)|
|`HAL_USART_Receive`|`USART_HandleTypeDef *husart, uint8_t *pRxData, uint16_t Size, uint32_t Timeout`|`HAL_StatusTypeDef`|[L512](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L512-L512)|
|`HAL_USART_TransmitReceive`|`USART_HandleTypeDef *husart, uint8_t *pTxData, uint8_t *pRxData, uint16_t Size, uint32_t Timeout`|`HAL_StatusTypeDef`|[L513](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L513-L513)|
|`HAL_USART_Transmit_IT`|`USART_HandleTypeDef *husart, uint8_t *pTxData, uint16_t Size`|`HAL_StatusTypeDef`|[L514](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L514-L514)|
|`HAL_USART_Receive_IT`|`USART_HandleTypeDef *husart, uint8_t *pRxData, uint16_t Size`|`HAL_StatusTypeDef`|[L515](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L515-L515)|
|`HAL_USART_TransmitReceive_IT`|`USART_HandleTypeDef *husart, uint8_t *pTxData, uint8_t *pRxData, uint16_t Size`|`HAL_StatusTypeDef`|[L516](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L516-L516)|
|`HAL_USART_Transmit_DMA`|`USART_HandleTypeDef *husart, uint8_t *pTxData, uint16_t Size`|`HAL_StatusTypeDef`|[L517](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L517-L517)|
|`HAL_USART_Receive_DMA`|`USART_HandleTypeDef *husart, uint8_t *pRxData, uint16_t Size`|`HAL_StatusTypeDef`|[L518](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L518-L518)|
|`HAL_USART_TransmitReceive_DMA`|`USART_HandleTypeDef *husart, uint8_t *pTxData, uint8_t *pRxData, uint16_t Size`|`HAL_StatusTypeDef`|[L519](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L519-L519)|

#### DMA控制与传输中止

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_USART_DMAPause`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L520](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L520-L520)|
|`HAL_USART_DMAResume`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L521](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L521-L521)|
|`HAL_USART_DMAStop`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L522](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L522-L522)|
|`HAL_USART_Abort`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L524](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L524-L524)|
|`HAL_USART_Abort_IT`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L525](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L525-L525)|

#### 中断入口与回调

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_USART_IRQHandler`|`USART_HandleTypeDef *husart`|`void`|[L527](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L527-L527)|
|`HAL_USART_TxCpltCallback`|`USART_HandleTypeDef *husart`|`void`|[L528](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L528-L528)|
|`HAL_USART_TxHalfCpltCallback`|`USART_HandleTypeDef *husart`|`void`|[L529](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L529-L529)|
|`HAL_USART_RxCpltCallback`|`USART_HandleTypeDef *husart`|`void`|[L530](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L530-L530)|
|`HAL_USART_RxHalfCpltCallback`|`USART_HandleTypeDef *husart`|`void`|[L531](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L531-L531)|
|`HAL_USART_TxRxCpltCallback`|`USART_HandleTypeDef *husart`|`void`|[L532](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L532-L532)|
|`HAL_USART_ErrorCallback`|`USART_HandleTypeDef *husart`|`void`|[L533](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L533-L533)|
|`HAL_USART_AbortCpltCallback`|`USART_HandleTypeDef *husart`|`void`|[L534](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L534-L534)|

#### 回调注册与条件编译

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_USART_RegisterCallback`|`USART_HandleTypeDef *husart, HAL_USART_CallbackIDTypeDef CallbackID, pUSART_CallbackTypeDef pCallback`|`HAL_StatusTypeDef`|[L499](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L499-L499)|
|`HAL_USART_UnRegisterCallback`|`USART_HandleTypeDef *husart, HAL_USART_CallbackIDTypeDef CallbackID`|`HAL_StatusTypeDef`|[L500](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L500-L500)|

#### 状态与错误查询

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_USART_GetState`|`USART_HandleTypeDef *husart`|`HAL_USART_StateTypeDef`|[L543](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L543-L543)|
|`HAL_USART_GetError`|`USART_HandleTypeDef *husart`|`uint32_t`|[L544](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L544-L544)|

### v1.1.10

按任务：[初始化与MSP](#初始化与msp-3) · [同步收发](#同步收发-1) · [DMA控制与传输中止](#dma控制与传输中止-3) · [中断入口与回调](#中断入口与回调-3) · [回调注册与条件编译](#回调注册与条件编译-3) · [状态与错误查询](#状态与错误查询-2)。

#### 初始化与MSP

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_USART_Init`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L492](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L492-L492)|
|`HAL_USART_DeInit`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L493](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L493-L493)|
|`HAL_USART_MspInit`|`USART_HandleTypeDef *husart`|`void`|[L494](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L494-L494)|
|`HAL_USART_MspDeInit`|`USART_HandleTypeDef *husart`|`void`|[L495](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L495-L495)|

#### 同步收发

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_USART_Transmit`|`USART_HandleTypeDef *husart, const uint8_t *pTxData, uint16_t Size, uint32_t Timeout`|`HAL_StatusTypeDef`|[L512](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L512-L512)|
|`HAL_USART_Receive`|`USART_HandleTypeDef *husart, uint8_t *pRxData, uint16_t Size, uint32_t Timeout`|`HAL_StatusTypeDef`|[L513](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L513-L513)|
|`HAL_USART_TransmitReceive`|`USART_HandleTypeDef *husart, const uint8_t *pTxData, uint8_t *pRxData, uint16_t Size, uint32_t Timeout`|`HAL_StatusTypeDef`|[L514](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L514-L515)|
|`HAL_USART_Transmit_IT`|`USART_HandleTypeDef *husart, const uint8_t *pTxData, uint16_t Size`|`HAL_StatusTypeDef`|[L516](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L516-L516)|
|`HAL_USART_Receive_IT`|`USART_HandleTypeDef *husart, uint8_t *pRxData, uint16_t Size`|`HAL_StatusTypeDef`|[L517](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L517-L517)|
|`HAL_USART_TransmitReceive_IT`|`USART_HandleTypeDef *husart, const uint8_t *pTxData, uint8_t *pRxData, uint16_t Size`|`HAL_StatusTypeDef`|[L518](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L518-L519)|
|`HAL_USART_Transmit_DMA`|`USART_HandleTypeDef *husart, const uint8_t *pTxData, uint16_t Size`|`HAL_StatusTypeDef`|[L520](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L520-L520)|
|`HAL_USART_Receive_DMA`|`USART_HandleTypeDef *husart, uint8_t *pRxData, uint16_t Size`|`HAL_StatusTypeDef`|[L521](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L521-L521)|
|`HAL_USART_TransmitReceive_DMA`|`USART_HandleTypeDef *husart, const uint8_t *pTxData, uint8_t *pRxData, uint16_t Size`|`HAL_StatusTypeDef`|[L522](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L522-L523)|

#### DMA控制与传输中止

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_USART_DMAPause`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L524](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L524-L524)|
|`HAL_USART_DMAResume`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L525](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L525-L525)|
|`HAL_USART_DMAStop`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L526](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L526-L526)|
|`HAL_USART_Abort`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L528](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L528-L528)|
|`HAL_USART_Abort_IT`|`USART_HandleTypeDef *husart`|`HAL_StatusTypeDef`|[L529](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L529-L529)|

#### 中断入口与回调

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_USART_IRQHandler`|`USART_HandleTypeDef *husart`|`void`|[L531](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L531-L531)|
|`HAL_USART_TxCpltCallback`|`USART_HandleTypeDef *husart`|`void`|[L532](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L532-L532)|
|`HAL_USART_TxHalfCpltCallback`|`USART_HandleTypeDef *husart`|`void`|[L533](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L533-L533)|
|`HAL_USART_RxCpltCallback`|`USART_HandleTypeDef *husart`|`void`|[L534](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L534-L534)|
|`HAL_USART_RxHalfCpltCallback`|`USART_HandleTypeDef *husart`|`void`|[L535](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L535-L535)|
|`HAL_USART_TxRxCpltCallback`|`USART_HandleTypeDef *husart`|`void`|[L536](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L536-L536)|
|`HAL_USART_ErrorCallback`|`USART_HandleTypeDef *husart`|`void`|[L537](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L537-L537)|
|`HAL_USART_AbortCpltCallback`|`USART_HandleTypeDef *husart`|`void`|[L538](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L538-L538)|

#### 回调注册与条件编译

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_USART_RegisterCallback`|`USART_HandleTypeDef *husart, HAL_USART_CallbackIDTypeDef CallbackID, pUSART_CallbackTypeDef pCallback`|`HAL_StatusTypeDef`|[L499](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L499-L500)|
|`HAL_USART_UnRegisterCallback`|`USART_HandleTypeDef *husart, HAL_USART_CallbackIDTypeDef CallbackID`|`HAL_StatusTypeDef`|[L501](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L501-L501)|

#### 状态与错误查询

|接口|参数（完整顺序）|返回类型|固定声明|
|---|---|---|---|
|`HAL_USART_GetState`|`const USART_HandleTypeDef *husart`|`HAL_USART_StateTypeDef`|[L547](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L547-L547)|
|`HAL_USART_GetError`|`const USART_HandleTypeDef *husart`|`uint32_t`|[L548](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L548-L548)|

名称增加：无。名称删除：无。


## 模式控制入口的状态副作用（固定v1.1.10）

HAL_HalfDuplex_EnableTransmitter将TE/RE改为TE=1、RE=0；EnableReceiver改为TE=0、RE=1。它们加锁后把gState设BUSY，写CR1，再把gState设READY并解锁。主体没有等待TC、检查当前gState/RxState是否存在传输、停止DMA或改写RxState的步骤。传输方向的切换时机及已有事务收尾由应用协调，不能用这两个入口的HAL_OK证明当前字符已安全结束。

HAL_MultiProcessor_EnterMuteMode / ExitMuteMode直接设置/清除RWU，也暂时改gState并恢复READY；固定v1.1.10还将RxEventType写为TC。它们没有等待RXNE=0后再写RWU的步骤；硬件对RWU的写入条件依然有效。HAL_LIN_SendBreak写SBK后即恢复gState并返回，不等待Break发送完毕，也不消除CTS相关硅勘误。

来源：[v1.1.10控制入口 L2753–2898](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L2753-L2898)。

## 状态查询的含义

固定v1.1.10 HAL_UART_GetState返回先后读取的gState与RxState的按位或；HAL_UART_GetError返回句柄ErrorCode。它们不直接读取DMA剩余数、线路状态，也不原子冻结整个事务。HAL_USART_GetState则返回同步句柄的单一State。状态字段可能被初始化、模式控制、错误或回调收尾改写，查询结果只具有对应驱动实现的语义。

来源：[UART查询 L2928–2948](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L2928-L2948)、[USART查询 L2068–2084](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L2068-L2084)。
