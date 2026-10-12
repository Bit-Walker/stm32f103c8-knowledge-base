# ADC HAL 底层辅助函数与导出宏

这些条目补充公开HAL接口的内部依赖和宏行为。固定v1.1.4/v1.1.10，面向F103C8T6；应用应通过具备相应状态、锁及回调管理的公开接口组织事务。原文列出内部声明，不等于提供独立、完整的应用级生命周期契约。

## 1 内部辅助条目

|条目及签名|所核行为与边界|
|---|---|
|HAL_StatusTypeDef ADC_Enable(ADC_HandleTypeDef *hadc)|先判断是否已使能；仅未使能时置ADON、作基于SystemCoreClock的稳定估算循环并等待使能读回。已使能则直接返回OK，不重复置ADON。超时设置State和ErrorCode的INTERNAL错误，并执行句柄解锁；与无条件置位的宏行为不同。|
|HAL_StatusTypeDef ADC_ConversionStop_Disable(ADC_HandleTypeDef *hadc)|若仍使能，清ADON并等待禁用读回；超时写内部错误。函数不回收DMA、GPIO或NVIC，不取代完整Stop事务。|
|void ADC_StabilizationTime(uint32_t DelayUs)|UM及固定头文件保留声明；DelayUs单位µs。在本次所核两版ADC/ADCEx的C文件中未找到该函数定义或调用，不能仅凭声明认定其可链接、可用或具备精确延时契约。|
|void ADC_DMAConvCplt(DMA_HandleTypeDef *hdma)|经hdma->Parent取得ADC句柄。无INTERNAL/DMA错误State时置REG_EOC；软件触发且非连续等条件下归一化忙态，再调用户完成回调。已有相关错误State则转发DMA错误回调。|
|void ADC_DMAHalfConvCplt(DMA_HandleTypeDef *hdma)|经Parent取得ADC句柄并通知用户半完成；没有复用全完成的错误State门控。|
|void ADC_DMAError(DMA_HandleTypeDef *hdma)|经Parent取得ADC句柄，设置State.ERROR_DMA及ErrorCode.DMA，再调用用户错误回调。|

hadc、hdma分别为有效ADC与DMA句柄指针；DMA的Parent须指向真实所属ADC对象，其生命周期覆盖传输和回调。返回HAL_StatusTypeDef的条目报告函数状态；void条目无返回值。忙循环次数不等于经过测量的精确CPU周期，也不能单凭其注释证明校准前的ADC时钟等待条件。

完整DMA停止与恢复的差异见[ADC DMA生命周期](DMA生命周期与恢复.md)。用户完成、半完成、错误回调随USE_HAL_ADC_REGISTER_CALLBACKS选择句柄注册函数或弱符号入口；不能通过直接调用内部DMA回调模拟硬件已完成的证据。

固定定位：
- [v1.1.4辅助函数及DMA回调，L2224–2400](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L2224-L2400)
- [v1.1.10对应实现，L2232起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_adc.c#L2232)
- [v1.1.4内部声明，L977–979](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L977-L979)、[v1.1.10声明，L976–978](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_adc.h#L976-L978)

## 2 八个导出宏

|调用形态|具体行为|
|---|---|
|__HAL_ADC_ENABLE(h)|向h->Instance->CR2置ADON；不先判断旧值，也不内置稳定等待。已上电后重复写入可能启动规则转换，按RM的同次其它位变化条件解释。|
|__HAL_ADC_DISABLE(h)|清ADON，影响规则/注入转换和校准；宏自身不等待禁用读回，也不处理DMA所有权。|
|__HAL_ADC_ENABLE_IT(h, mask)|置CR1中指定中断使能位；还须独立满足NVIC和事件条件。|
|__HAL_ADC_DISABLE_IT(h, mask)|清所选CR1中断使能位，不等于清挂起事件或停止转换。|
|__HAL_ADC_GET_IT_SOURCE(h, mask)|比较(CR1 & mask)==mask；组合掩码要求全部所选位为1，返回真假表达式。|
|__HAL_ADC_GET_FLAG(h, mask)|比较(SR & mask)==mask；组合掩码要求全部所选标志置位。不能将返回真直接解释为一个特定新样本。|
|__HAL_ADC_CLEAR_FLAG(h, mask)|向SR写入掩码的按位反码；利用rc_w0语义将选中位写0清除、未选位写1保持。|
|__HAL_ADC_RESET_HANDLE_STATE(h)|总是设置State=RESET；若USE_HAL_ADC_REGISTER_CALLBACKS==1，还将MspInitCallback、MspDeInitCallback置NULL。|

h为有效ADC句柄指针。中断mask采用ADC_IT_EOC、ADC_IT_JEOC、ADC_IT_AWD的合法组合；标志mask采用ADC_FLAG_STRT、JSTRT、EOC、JEOC、AWD的合法组合。mask是无量纲位掩码；查询表达式使用零掩码会恒真，不能据此证明任何事件。宏不提供普通函数的类型和运行时范围检查，不应传入带副作用的表达式。

RESET_HANDLE_STATE不会关闭ADC、停止DMA或清ErrorCode、Lock、Init和所有转换回调。回调注册启用时，它清除两个MSP入口的行为会影响后续Init/DeInit选用的回调，不能概括成“只改State”。下一次RESET态初始化还可能重设其它默认回调，须结合[初始化边界](HAL初始化边界.md)使用。

来源：[v1.1.4宏，L508–597](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L508-L597)、[v1.1.10宏，L507–596](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_adc.h#L507-L596)；[RM0008 Rev21 SR与ADON，pp237–243](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=237)。
