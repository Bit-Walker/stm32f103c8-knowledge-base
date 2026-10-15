# USART LL接口索引与配置结构

目标为STM32F103C8，固定v1.1.4源码；本表由已核对完整Git blob的头文件逐项定位，按功能重组。索引包含129个C8内联接口与5个独立初始化函数；API名称覆盖不表示所有并发组合或板级时序都已验证。

所有内联接口第一参数为 `USART_TypeDef *USARTx`，须指向C8的USART1/2/3。下表省略重复的实例参数；void表示无返回值，uint32_t/uint16_t/uint8_t分别为无符号32/16/8位类型。返回值究竟是0/1、编码字段、数据或地址，应按函数及寄存器说明解释，不把所有非零值统一当错误码。

- 使用前确认时钟、GPIO、模式和字段写入条件；LL调用不维护HAL句柄，不自动等待完成，也不提供事务锁。
- ClearFlag的SR→DR读序列会消耗数据并关联清标志；按[寄存器访问副作用](寄存器与访问副作用.md)及[硅勘误](硅勘误.md)处理。
- 模式辅助函数的准确清置范围、波特率截断和GetBaudRate边界见[初始化与模式契约](LL初始化与模式边界.md)。
- C8未定义USART_CR1_OVER8或USART_CR3_ONEBIT，排除对应五个接口；Set/GetBaudRate使用不含OverSampling参数的分支。保留在结构里的OverSampling字段不代表C8支持8倍采样。

## 基础配置与时钟

|接口|其他参数（按顺序）|返回类型|直接涉及的寄存器|固定源码|
|---|---|---|---|---|
|`LL_USART_Enable`|`无`|`void`|CR1|[L411–414](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L411-L414)|
|`LL_USART_Disable`|`无`|`void`|CR1|[L425–428](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L425-L428)|
|`LL_USART_IsEnabled`|`无`|`uint32_t`|CR1|[L436–439](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L436-L439)|
|`LL_USART_EnableDirectionRx`|`无`|`void`|CR1|[L447–450](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L447-L450)|
|`LL_USART_DisableDirectionRx`|`无`|`void`|CR1|[L458–461](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L458-L461)|
|`LL_USART_EnableDirectionTx`|`无`|`void`|CR1|[L469–472](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L469-L472)|
|`LL_USART_DisableDirectionTx`|`无`|`void`|CR1|[L480–483](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L480-L483)|
|`LL_USART_SetTransferDirection`|`uint32_t TransferDirection`|`void`|CR1|[L498–501](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L498-L501)|
|`LL_USART_GetTransferDirection`|`无`|`uint32_t`|CR1|[L514–517](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L514-L517)|
|`LL_USART_SetParity`|`uint32_t Parity`|`void`|CR1|[L533–536](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L533-L536)|
|`LL_USART_GetParity`|`无`|`uint32_t`|CR1|[L548–551](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L548-L551)|
|`LL_USART_SetWakeUpMethod`|`uint32_t Method`|`void`|CR1|[L562–565](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L562-L565)|
|`LL_USART_GetWakeUpMethod`|`无`|`uint32_t`|CR1|[L575–578](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L575-L578)|
|`LL_USART_SetDataWidth`|`uint32_t DataWidth`|`void`|CR1|[L589–592](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L589-L592)|
|`LL_USART_GetDataWidth`|`无`|`uint32_t`|CR1|[L602–605](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L602-L605)|
|`LL_USART_SetLastClkPulseOutput`|`uint32_t LastBitClockPulse`|`void`|CR2|[L647–650](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L647-L650)|
|`LL_USART_GetLastClkPulseOutput`|`无`|`uint32_t`|CR2|[L663–666](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L663-L666)|
|`LL_USART_SetClockPhase`|`uint32_t ClockPhase`|`void`|CR2|[L679–682](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L679-L682)|
|`LL_USART_GetClockPhase`|`无`|`uint32_t`|CR2|[L694–697](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L694-L697)|
|`LL_USART_SetClockPolarity`|`uint32_t ClockPolarity`|`void`|CR2|[L710–713](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L710-L713)|
|`LL_USART_GetClockPolarity`|`无`|`uint32_t`|CR2|[L725–728](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L725-L728)|
|`LL_USART_ConfigClock`|`uint32_t Phase, uint32_t Polarity, uint32_t LBCPOutput`|`void`|CR2|[L753–756](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L753-L756)|
|`LL_USART_EnableSCLKOutput`|`无`|`void`|CR2|[L766–769](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L766-L769)|
|`LL_USART_DisableSCLKOutput`|`无`|`void`|CR2|[L779–782](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L779-L782)|
|`LL_USART_IsEnabledSCLKOutput`|`无`|`uint32_t`|CR2|[L792–795](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L792-L795)|
|`LL_USART_SetStopBitsLength`|`uint32_t StopBits`|`void`|CR2|[L808–811](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L808-L811)|
|`LL_USART_GetStopBitsLength`|`无`|`uint32_t`|CR2|[L823–826](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L823-L826)|
|`LL_USART_ConfigCharacter`|`uint32_t DataWidth, uint32_t Parity, uint32_t StopBits`|`void`|CR1、CR2|[L853–858](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L853-L858)|
|`LL_USART_SetNodeAddress`|`uint32_t NodeAddress`|`void`|CR2|[L869–872](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L869-L872)|
|`LL_USART_GetNodeAddress`|`无`|`uint32_t`|CR2|[L881–884](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L881-L884)|
|`LL_USART_EnableRTSHWFlowCtrl`|`无`|`void`|CR3|[L894–897](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L894-L897)|
|`LL_USART_DisableRTSHWFlowCtrl`|`无`|`void`|CR3|[L907–910](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L907-L910)|
|`LL_USART_EnableCTSHWFlowCtrl`|`无`|`void`|CR3|[L920–923](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L920-L923)|
|`LL_USART_DisableCTSHWFlowCtrl`|`无`|`void`|CR3|[L933–936](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L933-L936)|
|`LL_USART_SetHWFlowCtrl`|`uint32_t HardwareFlowControl`|`void`|CR3|[L952–955](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L952-L955)|
|`LL_USART_GetHWFlowCtrl`|`无`|`uint32_t`|CR3|[L970–973](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L970-L973)|
|`LL_USART_SetBaudRate`|`uint32_t PeriphClk, uint32_t BaudRate`|`void`|BRR|[L1088–1091](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1088-L1091)|
|`LL_USART_GetBaudRate`|`uint32_t PeriphClk`|`uint32_t`|BRR|[L1102–1114](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1102-L1114)|

## IrDA

|接口|其他参数（按顺序）|返回类型|直接涉及的寄存器|固定源码|
|---|---|---|---|---|
|`LL_USART_EnableIrda`|`无`|`void`|CR3|[L1133–1136](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1133-L1136)|
|`LL_USART_DisableIrda`|`无`|`void`|CR3|[L1146–1149](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1146-L1149)|
|`LL_USART_IsEnabledIrda`|`无`|`uint32_t`|CR3|[L1159–1162](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1159-L1162)|
|`LL_USART_SetIrdaPowerMode`|`uint32_t PowerMode`|`void`|CR3|[L1175–1178](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1175-L1178)|
|`LL_USART_GetIrdaPowerMode`|`无`|`uint32_t`|CR3|[L1190–1193](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1190-L1193)|
|`LL_USART_SetIrdaPrescaler`|`uint32_t PrescalerValue`|`void`|GTPR|[L1205–1208](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1205-L1208)|
|`LL_USART_GetIrdaPrescaler`|`无`|`uint32_t`|GTPR|[L1219–1222](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1219-L1222)|

## Smartcard

|接口|其他参数（按顺序）|返回类型|直接涉及的寄存器|固定源码|
|---|---|---|---|---|
|`LL_USART_EnableSmartcardNACK`|`无`|`void`|CR3|[L1240–1243](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1240-L1243)|
|`LL_USART_DisableSmartcardNACK`|`无`|`void`|CR3|[L1253–1256](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1253-L1256)|
|`LL_USART_IsEnabledSmartcardNACK`|`无`|`uint32_t`|CR3|[L1266–1269](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1266-L1269)|
|`LL_USART_EnableSmartcard`|`无`|`void`|CR3|[L1279–1282](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1279-L1282)|
|`LL_USART_DisableSmartcard`|`无`|`void`|CR3|[L1292–1295](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1292-L1295)|
|`LL_USART_IsEnabledSmartcard`|`无`|`uint32_t`|CR3|[L1305–1308](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1305-L1308)|
|`LL_USART_SetSmartcardPrescaler`|`uint32_t PrescalerValue`|`void`|GTPR|[L1320–1323](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1320-L1323)|
|`LL_USART_GetSmartcardPrescaler`|`无`|`uint32_t`|GTPR|[L1334–1337](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1334-L1337)|
|`LL_USART_SetSmartcardGuardTime`|`uint32_t GuardTime`|`void`|GTPR|[L1349–1352](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1349-L1352)|
|`LL_USART_GetSmartcardGuardTime`|`无`|`uint32_t`|GTPR|[L1363–1366](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1363-L1366)|

## 单线半双工

|接口|其他参数（按顺序）|返回类型|直接涉及的寄存器|固定源码|
|---|---|---|---|---|
|`LL_USART_EnableHalfDuplex`|`无`|`void`|CR3|[L1384–1387](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1384-L1387)|
|`LL_USART_DisableHalfDuplex`|`无`|`void`|CR3|[L1397–1400](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1397-L1400)|
|`LL_USART_IsEnabledHalfDuplex`|`无`|`uint32_t`|CR3|[L1410–1413](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1410-L1413)|

## LIN

|接口|其他参数（按顺序）|返回类型|直接涉及的寄存器|固定源码|
|---|---|---|---|---|
|`LL_USART_SetLINBrkDetectionLen`|`uint32_t LINBDLength`|`void`|CR2|[L1434–1437](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1434-L1437)|
|`LL_USART_GetLINBrkDetectionLen`|`无`|`uint32_t`|CR2|[L1449–1452](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1449-L1452)|
|`LL_USART_EnableLIN`|`无`|`void`|CR2|[L1462–1465](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1462-L1465)|
|`LL_USART_DisableLIN`|`无`|`void`|CR2|[L1475–1478](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1475-L1478)|
|`LL_USART_IsEnabledLIN`|`无`|`uint32_t`|CR2|[L1488–1491](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1488-L1491)|

## 模式组合

|接口|其他参数（按顺序）|返回类型|直接涉及的寄存器|固定源码|
|---|---|---|---|---|
|`LL_USART_ConfigAsyncMode`|`无`|`void`|CR2、CR3|[L1526–1533](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1526-L1533)|
|`LL_USART_ConfigSyncMode`|`无`|`void`|CR2、CR3|[L1562–1571](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1562-L1571)|
|`LL_USART_ConfigLINMode`|`无`|`void`|CR2、CR3|[L1602–1611](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1602-L1611)|
|`LL_USART_ConfigHalfDuplexMode`|`无`|`void`|CR2、CR3|[L1640–1649](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1640-L1649)|
|`LL_USART_ConfigSmartcardMode`|`无`|`void`|CR2、CR3|[L1680–1692](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1680-L1692)|
|`LL_USART_ConfigIrdaMode`|`无`|`void`|CR2、CR3|[L1723–1732](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1723-L1732)|
|`LL_USART_ConfigMultiProcessMode`|`无`|`void`|CR2、CR3|[L1761–1768](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1761-L1768)|

## 状态标志

|接口|其他参数（按顺序）|返回类型|直接涉及的寄存器|固定源码|
|---|---|---|---|---|
|`LL_USART_IsActiveFlag_PE`|`无`|`uint32_t`|SR|[L1784–1787](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1784-L1787)|
|`LL_USART_IsActiveFlag_FE`|`无`|`uint32_t`|SR|[L1795–1798](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1795-L1798)|
|`LL_USART_IsActiveFlag_NE`|`无`|`uint32_t`|SR|[L1806–1809](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1806-L1809)|
|`LL_USART_IsActiveFlag_ORE`|`无`|`uint32_t`|SR|[L1817–1820](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1817-L1820)|
|`LL_USART_IsActiveFlag_IDLE`|`无`|`uint32_t`|SR|[L1828–1831](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1828-L1831)|
|`LL_USART_IsActiveFlag_RXNE`|`无`|`uint32_t`|SR|[L1839–1842](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1839-L1842)|
|`LL_USART_IsActiveFlag_TC`|`无`|`uint32_t`|SR|[L1850–1853](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1850-L1853)|
|`LL_USART_IsActiveFlag_TXE`|`无`|`uint32_t`|SR|[L1861–1864](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1861-L1864)|
|`LL_USART_IsActiveFlag_LBD`|`无`|`uint32_t`|SR|[L1874–1877](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1874-L1877)|
|`LL_USART_IsActiveFlag_nCTS`|`无`|`uint32_t`|SR|[L1887–1890](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1887-L1890)|
|`LL_USART_IsActiveFlag_SBK`|`无`|`uint32_t`|CR1|[L1898–1901](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1898-L1901)|
|`LL_USART_IsActiveFlag_RWU`|`无`|`uint32_t`|CR1|[L1909–1912](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1909-L1912)|
|`LL_USART_ClearFlag_PE`|`无`|`void`|DR、SR|[L1924–1931](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1924-L1931)|
|`LL_USART_ClearFlag_FE`|`无`|`void`|DR、SR|[L1943–1950](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1943-L1950)|
|`LL_USART_ClearFlag_NE`|`无`|`void`|DR、SR|[L1962–1969](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1962-L1969)|
|`LL_USART_ClearFlag_ORE`|`无`|`void`|DR、SR|[L1981–1988](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1981-L1988)|
|`LL_USART_ClearFlag_IDLE`|`无`|`void`|DR、SR|[L2000–2007](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2000-L2007)|
|`LL_USART_ClearFlag_TC`|`无`|`void`|SR|[L2015–2018](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2015-L2018)|
|`LL_USART_ClearFlag_RXNE`|`无`|`void`|SR|[L2026–2029](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2026-L2029)|
|`LL_USART_ClearFlag_LBD`|`无`|`void`|SR|[L2039–2042](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2039-L2042)|
|`LL_USART_ClearFlag_nCTS`|`无`|`void`|SR|[L2052–2055](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2052-L2055)|

## 中断使能

|接口|其他参数（按顺序）|返回类型|直接涉及的寄存器|固定源码|
|---|---|---|---|---|
|`LL_USART_EnableIT_IDLE`|`无`|`void`|CR1|[L2071–2074](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2071-L2074)|
|`LL_USART_EnableIT_RXNE`|`无`|`void`|CR1|[L2082–2085](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2082-L2085)|
|`LL_USART_EnableIT_TC`|`无`|`void`|CR1|[L2093–2096](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2093-L2096)|
|`LL_USART_EnableIT_TXE`|`无`|`void`|CR1|[L2104–2107](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2104-L2107)|
|`LL_USART_EnableIT_PE`|`无`|`void`|CR1|[L2115–2118](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2115-L2118)|
|`LL_USART_EnableIT_LBD`|`无`|`void`|CR2|[L2128–2131](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2128-L2131)|
|`LL_USART_EnableIT_ERROR`|`无`|`void`|CR3|[L2143–2146](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2143-L2146)|
|`LL_USART_EnableIT_CTS`|`无`|`void`|CR3|[L2156–2159](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2156-L2159)|
|`LL_USART_DisableIT_IDLE`|`无`|`void`|CR1|[L2167–2170](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2167-L2170)|
|`LL_USART_DisableIT_RXNE`|`无`|`void`|CR1|[L2178–2181](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2178-L2181)|
|`LL_USART_DisableIT_TC`|`无`|`void`|CR1|[L2189–2192](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2189-L2192)|
|`LL_USART_DisableIT_TXE`|`无`|`void`|CR1|[L2200–2203](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2200-L2203)|
|`LL_USART_DisableIT_PE`|`无`|`void`|CR1|[L2211–2214](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2211-L2214)|
|`LL_USART_DisableIT_LBD`|`无`|`void`|CR2|[L2224–2227](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2224-L2227)|
|`LL_USART_DisableIT_ERROR`|`无`|`void`|CR3|[L2239–2242](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2239-L2242)|
|`LL_USART_DisableIT_CTS`|`无`|`void`|CR3|[L2252–2255](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2252-L2255)|
|`LL_USART_IsEnabledIT_IDLE`|`无`|`uint32_t`|CR1|[L2263–2266](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2263-L2266)|
|`LL_USART_IsEnabledIT_RXNE`|`无`|`uint32_t`|CR1|[L2274–2277](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2274-L2277)|
|`LL_USART_IsEnabledIT_TC`|`无`|`uint32_t`|CR1|[L2285–2288](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2285-L2288)|
|`LL_USART_IsEnabledIT_TXE`|`无`|`uint32_t`|CR1|[L2296–2299](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2296-L2299)|
|`LL_USART_IsEnabledIT_PE`|`无`|`uint32_t`|CR1|[L2307–2310](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2307-L2310)|
|`LL_USART_IsEnabledIT_LBD`|`无`|`uint32_t`|CR2|[L2320–2323](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2320-L2323)|
|`LL_USART_IsEnabledIT_ERROR`|`无`|`uint32_t`|CR3|[L2331–2334](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2331-L2334)|
|`LL_USART_IsEnabledIT_CTS`|`无`|`uint32_t`|CR3|[L2344–2347](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2344-L2347)|

## DMA请求

|接口|其他参数（按顺序）|返回类型|直接涉及的寄存器|固定源码|
|---|---|---|---|---|
|`LL_USART_EnableDMAReq_RX`|`无`|`void`|CR3|[L2363–2366](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2363-L2366)|
|`LL_USART_DisableDMAReq_RX`|`无`|`void`|CR3|[L2374–2377](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2374-L2377)|
|`LL_USART_IsEnabledDMAReq_RX`|`无`|`uint32_t`|CR3|[L2385–2388](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2385-L2388)|
|`LL_USART_EnableDMAReq_TX`|`无`|`void`|CR3|[L2396–2399](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2396-L2399)|
|`LL_USART_DisableDMAReq_TX`|`无`|`void`|CR3|[L2407–2410](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2407-L2410)|
|`LL_USART_IsEnabledDMAReq_TX`|`无`|`uint32_t`|CR3|[L2418–2421](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2418-L2421)|
|`LL_USART_DMA_GetRegAddr`|`无`|`uint32_t`|DR|[L2430–2434](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2430-L2434)|

## 数据读写

|接口|其他参数（按顺序）|返回类型|直接涉及的寄存器|固定源码|
|---|---|---|---|---|
|`LL_USART_ReceiveData8`|`无`|`uint8_t`|DR|[L2450–2453](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2450-L2453)|
|`LL_USART_ReceiveData9`|`无`|`uint16_t`|DR|[L2461–2464](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2461-L2464)|
|`LL_USART_TransmitData8`|`uint8_t Value`|`void`|DR|[L2473–2476](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2473-L2476)|
|`LL_USART_TransmitData9`|`uint16_t Value`|`void`|DR|[L2485–2488](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2485-L2488)|

## Break与静默请求

|接口|其他参数（按顺序）|返回类型|直接涉及的寄存器|固定源码|
|---|---|---|---|---|
|`LL_USART_RequestBreakSending`|`无`|`void`|CR1|[L2504–2507](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2504-L2507)|
|`LL_USART_RequestEnterMuteMode`|`无`|`void`|CR1|[L2515–2518](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2515-L2518)|
|`LL_USART_RequestExitMuteMode`|`无`|`void`|CR1|[L2526–2529](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2526-L2529)|

## 独立初始化函数

以下函数及两个配置结构需要USE_FULL_LL_DRIVER对应声明/实现支持；链接独立源文件及其依赖不由内联头文件自动完成。

|接口|参数|返回|边界|
|---|---|---|---|
|`LL_USART_DeInit`|`USART_TypeDef *USARTx`|`ErrorStatus`|按实例执行APB复位，涉及整个USART；不能替代DMA所有权回收；[L128–187](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_usart.c#L128-L187)|
|`LL_USART_Init`|`USART_TypeDef *USARTx, LL_USART_InitTypeDef *USART_InitStruct`|`ErrorStatus`|要求UE=0；部分配置写入后仍可能因时钟/波特率参数返回ERROR；[L202–322](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_usart.c#L202-L322)|
|`LL_USART_StructInit`|`LL_USART_InitTypeDef *USART_InitStruct`|`void`|填写默认配置；C8的未使用OverSampling字段不保证被写入；[L331–343](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_usart.c#L331-L343)|
|`LL_USART_ClockInit`|`USART_TypeDef *USARTx, LL_USART_ClockInitTypeDef *USART_ClockInitStruct`|`ErrorStatus`|要求UE=0；禁用时钟分支仅清CLKEN，保留CPOL/CPHA/LBCL；[L357–408](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_usart.c#L357-L408)|
|`LL_USART_ClockStructInit`|`LL_USART_ClockInitTypeDef *USART_ClockInitStruct`|`void`|填入时钟配置默认值；[L416–423](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_usart.c#L416-L423)|

来源：[固定LL实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_usart.c)。

## 配置结构的全部字段

|结构|uint32_t字段|含义|
|---|---|---|
|LL_USART_InitTypeDef|BaudRate|目标波特率，需合法非零并可由当前PCLK实现|
|同上|DataWidth|字长M字段；校验占据所选字长最高位|
|同上|StopBits|STOP编码对应的停止位长度|
|同上|Parity|PCE/PS组合|
|同上|TransferDirection|TE/RE方向组合|
|同上|HardwareFlowControl|RTSE/CTSE组合|
|同上|OverSampling|结构保留字段；C8不使用对应OVER8分支|
|LL_USART_ClockInitTypeDef|ClockOutput|CLKEN同步时钟输出使能|
|同上|ClockPolarity|CPOL空闲极性|
|同上|ClockPhase|CPHA采样边沿选择|
|同上|LastBitClockPulse|LBCL最后数据位时钟输出选择|

来源：[固定头文件结构 L71–145](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L71-L145)。结构默认值和适用写入条件见初始化契约；配置符号组见下节。

## 通用读写宏

LL_USART_WriteReg(USARTx, Reg, Value)直接写指定寄存器；LL_USART_ReadReg(USARTx, Reg)直接读。Reg为寄存器成员标识符，Value为写值。它们不对保留位、W0C语义或读DR副作用进行保护，也不是带检查的收发API。

## C8配置符号与编码

下表完整列出该固定头文件的C8配置符号组；标志/中断掩码另列。组合值由原字段按位或形成，不能把不同寄存器的编码混用。

|组|符号后缀（均以LL_USART_开头）|编码及意义|
|---|---|---|
|方向|DIRECTION_NONE / RX / TX / TX_RX|0 / CR1.RE / CR1.TE / TE与RE|
|校验|PARITY_NONE / EVEN / ODD|0 / CR1.PCE / PCE与PS|
|唤醒|WAKEUP_IDLELINE / ADDRESSMARK|0 / CR1.WAKE；分别为空闲和地址标记唤醒|
|字长|DATAWIDTH_8B / 9B|0 / CR1.M；PCE开启时最高位由校验占用|
|过采样|OVERSAMPLING_16|0；C8固定16倍，结构中的字段在本芯片路径不使用|
|同步CK|CLOCK_DISABLE / ENABLE|0 / CR2.CLKEN；这两个符号在USE_FULL_LL_DRIVER下提供|
|末位CK|LASTCLKPULSE_NO_OUTPUT / OUTPUT|0 / CR2.LBCL|
|时钟相位|PHASE_1EDGE / 2EDGE|0 / CR2.CPHA；第一/第二转换边沿采样|
|时钟极性|POLARITY_LOW / HIGH|0 / CR2.CPOL；空闲低/高|
|停止位|STOPBITS_1 / 0_5 / 2 / 1_5|STOP=00 / 01 / 10 / 11；模式适用性见硬件页|
|硬件流控|HWCONTROL_NONE / RTS / CTS / RTS_CTS|0 / CR3.RTSE / CR3.CTSE / RTSE与CTSE|
|IrDA功耗|IRDA_POWER_NORMAL / LOW|0 / CR3.IRLP|
|LIN Break检测|LINBREAK_DETECT_10B / 11B|0 / CR2.LBDL|

标志掩码均为同名硬件字段的别名：LL_USART_SR_PE、FE、NE、ORE、IDLE、RXNE、TC、TXE、LBD、CTS（后九个也有LL_USART_SR_前缀）。中断掩码为LL_USART_CR1_IDLEIE、RXNEIE、TCIE、TXEIE、PEIE，以及LL_USART_CR2_LBDIE、LL_USART_CR3_EIE、CTSIE；省略项沿用同组前缀。它们是掩码，读取标志或设置使能后仍须按硬件条件解释。

来源：[固定头文件常量 L158–334](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L158-L334)。

16倍波特率helper组包含 __LL_USART_DIV_SAMPLING16_100、__LL_USART_DIVMANT_SAMPLING16、__LL_USART_DIVFRAQ_SAMPLING16、__LL_USART_DIV_SAMPLING16。它们分别形成百分倍中间量、整数部分、舍入分数和BRR编码，参数均为外设时钟与目标波特率。输入非零、整数中间量范围、参数重复求值及最终16位截断仍需核对；不向有副作用的宏参数表达式作安全保证。头文件虽然也提供SAMPLING8 helper定义，C8没有OVER8硬件，不能借这些宏启用8倍采样。

来源：[固定helper L366–385](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L366-L385)。

## 数据读取、清标志和参数范围的具体边界

以下逐项核过固定 v1.1.4 与 v1.1.10 的函数体；新版部分只读接口把 USARTx 参数改为 const，寄存器读取的硬件副作用仍然存在。

- ReceiveData8 读取 DR 并转换为 uint8_t；ReceiveData9 读取 DR[8:0] 并转换为 uint16_t。两者都不读取 CR1.M/PCE 来自动剔除校验位。例如 M=0、PCE=1 的 7 位载荷仍须用 0x7F 提取；9 位无校验用 ReceiveData8 会丢掉第 9 位。
- TransmitData8 将 uint8_t 值写入 DR；TransmitData9 先用 0x1FF 掩码再写 DR。函数名中的 8/9 表示数据值的处理方式，不保证生成 8/16 位外设总线访问；DR 在 CMSIS 结构中的类型及编译器生成的访问应另行区分。
- ClearFlag_PE/FE/NE/ORE/IDLE 均执行先读 SR、再读 DR，关联清除多个接收状态并消耗可读数据。不能为了分别清五个状态而连续调用五次，假定每次只影响名称中的那一个标志。
- ClearFlag_TC/RXNE/LBD/nCTS 向 SR 写入对应位取反的掩码，使用写零清除语义。ClearFlag_RXNE 不返回数据，不能当接收数据读取函数。
- IsActiveFlag_nCTS 返回 SR.CTS 变化事件标志，不能用它读取 CTS 引脚当前高低电平；IsActiveFlag_SBK/RWU 读取的是 CR1 中的请求/静默状态。
- RequestBreakSending 只置 SBK，不等待 Break 结束；RequestEnterMuteMode 只置 RWU，没有等待 RXNE=0 的步骤。调用者仍须满足寄存器的写入前提。

来源：[v1.1.4 状态与清除 L1779–2059](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1779-L2059)、[数据与请求 L2443–2533](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L2443-L2533)、[v1.1.10 对应数据路径 L2444–2534](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_ll_usart.h#L2444-L2534)。

### Smartcard 与 IrDA 预分频读取不构成有效性检查

SetSmartcardPrescaler 注释给出 0～31，SetIrdaPrescaler 给出 0～255，但 RM0008 的 GTPR 定义将 0 列为保留值。合法配置仍需满足：Smartcard 的有效 PSC[4:0] 为 1～31，IrDA 低功耗 PSC[7:0] 为 1～255，普通 IrDA 必须为 1。两个 setter 的函数体都没有参数断言或错误返回。

GetSmartcardPrescaler 虽注释返回 0～31，实际读取掩码是 USART_GTPR_PSC=0xFF；它不把返回值截成低 5 位。Smartcard 模式的 PSC[7:5] 对卡时钟分频无效，但软件读出的整个低字节可能包含这些位。因此跨模式保存/恢复 GTPR 时，应分别核对实际 PSC 位域与目标模式约束，不能把该 getter 的非零返回值当作合法卡时钟证明。

来源：[v1.1.4 IrDA预分频 L1197–1222](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1197-L1222)、[Smartcard L1310–1338](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1310-L1338)、[v1.1.10 对应 Smartcard 实现 L1311–1339](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_ll_usart.h#L1311-L1339)、[固定器件头文件 PSC 掩码 L9583–9597](https://github.com/STMicroelectronics/cmsis-device-f1/blob/c8e9a4a4f16b6d2cb2a2083cbe5161025280fb22/Include/stm32f103xb.h#L9583-L9597)、[RM0008 Rev21 GTPR](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=826)。
