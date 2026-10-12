# ADC HAL 符号参考

基于固定v1.1.4 ADC及ADCEx头文件；168 个保留符号已逐项核对名称、固定头文件位置及 C8 适用语义；硬件适用范围为STM32F103C8T6。

固定版本：[de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/tree/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9)。下列位置指对应头文件的定义行，符号存在不代表每个系列具备相应硬件。

## 通用ADC符号

|符号|含义及边界|固定头文件定义|
|---|---|---|
|`ADC_ANALOGWATCHDOG_NONE`|看门狗：关闭|[stm32f1xx_hal_adc.h:353](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L353)|
|`ADC_ANALOGWATCHDOG_SINGLE_REG`|看门狗：单通道规则组|[stm32f1xx_hal_adc.h:354](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L354)|
|`ADC_ANALOGWATCHDOG_SINGLE_INJEC`|看门狗：单通道注入组|[stm32f1xx_hal_adc.h:355](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L355)|
|`ADC_ANALOGWATCHDOG_SINGLE_REGINJEC`|看门狗：单通道两组|[stm32f1xx_hal_adc.h:356](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L356)|
|`ADC_ANALOGWATCHDOG_ALL_REG`|看门狗：全通道规则组|[stm32f1xx_hal_adc.h:357](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L357)|
|`ADC_ANALOGWATCHDOG_ALL_INJEC`|看门狗：全通道注入组|[stm32f1xx_hal_adc.h:358](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L358)|
|`ADC_ANALOGWATCHDOG_ALL_REGINJEC`|看门狗：全通道两组|[stm32f1xx_hal_adc.h:359](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L359)|
|`ADC_CHANNEL_0`|ADC 通道 0，C8 外部模拟输入|[stm32f1xx_hal_adc.h:287](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L287)|
|`ADC_CHANNEL_1`|ADC 通道 1，C8 外部模拟输入|[stm32f1xx_hal_adc.h:288](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L288)|
|`ADC_CHANNEL_2`|ADC 通道 2，C8 外部模拟输入|[stm32f1xx_hal_adc.h:289](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L289)|
|`ADC_CHANNEL_3`|ADC 通道 3，C8 外部模拟输入|[stm32f1xx_hal_adc.h:290](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L290)|
|`ADC_CHANNEL_4`|ADC 通道 4，C8 外部模拟输入|[stm32f1xx_hal_adc.h:291](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L291)|
|`ADC_CHANNEL_5`|ADC 通道 5，C8 外部模拟输入|[stm32f1xx_hal_adc.h:292](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L292)|
|`ADC_CHANNEL_6`|ADC 通道 6，C8 外部模拟输入|[stm32f1xx_hal_adc.h:293](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L293)|
|`ADC_CHANNEL_7`|ADC 通道 7，C8 外部模拟输入|[stm32f1xx_hal_adc.h:294](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L294)|
|`ADC_CHANNEL_8`|ADC 通道 8，C8 外部模拟输入|[stm32f1xx_hal_adc.h:295](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L295)|
|`ADC_CHANNEL_9`|ADC 通道 9，C8 外部模拟输入|[stm32f1xx_hal_adc.h:296](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L296)|
|`ADC_CHANNEL_10`|ADC 通道 10 的合法寄存器编码，但 C8 LQFP48 没有对应外部模拟输入脚|[stm32f1xx_hal_adc.h:297](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L297)|
|`ADC_CHANNEL_11`|ADC 通道 11 的合法寄存器编码，但 C8 LQFP48 没有对应外部模拟输入脚|[stm32f1xx_hal_adc.h:298](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L298)|
|`ADC_CHANNEL_12`|ADC 通道 12 的合法寄存器编码，但 C8 LQFP48 没有对应外部模拟输入脚|[stm32f1xx_hal_adc.h:299](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L299)|
|`ADC_CHANNEL_13`|ADC 通道 13 的合法寄存器编码，但 C8 LQFP48 没有对应外部模拟输入脚|[stm32f1xx_hal_adc.h:300](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L300)|
|`ADC_CHANNEL_14`|ADC 通道 14 的合法寄存器编码，但 C8 LQFP48 没有对应外部模拟输入脚|[stm32f1xx_hal_adc.h:301](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L301)|
|`ADC_CHANNEL_15`|ADC 通道 15 的合法寄存器编码，但 C8 LQFP48 没有对应外部模拟输入脚|[stm32f1xx_hal_adc.h:302](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L302)|
|`ADC_CHANNEL_16`|通道 16；ADC1 连接温度传感器，ADC2 的该通道接地，不作为温度采集源|[stm32f1xx_hal_adc.h:303](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L303)|
|`ADC_CHANNEL_17`|通道 17；ADC1 连接 VREFINT，ADC2 的该通道接地，不作为内部参考采集源|[stm32f1xx_hal_adc.h:304](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L304)|
|`ADC_CHANNEL_TEMPSENSOR`|ADC1 内部温度传感器通道/通路|[stm32f1xx_hal_adc.h:306](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L306)|
|`ADC_CHANNEL_VREFINT`|ADC1 内部参考电压通道/通路|[stm32f1xx_hal_adc.h:307](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L307)|
|`ADC_CONVERSIONCLOCKCYCLES_SAMPLETIME_1CYCLE5`|值 14，单位 ADC 时钟周期；对应采样档位加 12.5 周期转换阶段，不含触发延迟或序列求和|[stm32f1xx_hal_adc.h:423](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L423)|
|`ADC_CONVERSIONCLOCKCYCLES_SAMPLETIME_7CYCLES5`|值 20，单位 ADC 时钟周期；对应采样档位加 12.5 周期转换阶段，不含触发延迟或序列求和|[stm32f1xx_hal_adc.h:424](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L424)|
|`ADC_CONVERSIONCLOCKCYCLES_SAMPLETIME_13CYCLES5`|值 26，单位 ADC 时钟周期；对应采样档位加 12.5 周期转换阶段，不含触发延迟或序列求和|[stm32f1xx_hal_adc.h:425](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L425)|
|`ADC_CONVERSIONCLOCKCYCLES_SAMPLETIME_28CYCLES5`|值 41，单位 ADC 时钟周期；对应采样档位加 12.5 周期转换阶段，不含触发延迟或序列求和|[stm32f1xx_hal_adc.h:426](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L426)|
|`ADC_CONVERSIONCLOCKCYCLES_SAMPLETIME_41CYCLES5`|值 54，单位 ADC 时钟周期；对应采样档位加 12.5 周期转换阶段，不含触发延迟或序列求和|[stm32f1xx_hal_adc.h:427](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L427)|
|`ADC_CONVERSIONCLOCKCYCLES_SAMPLETIME_55CYCLES5`|值 68，单位 ADC 时钟周期；对应采样档位加 12.5 周期转换阶段，不含触发延迟或序列求和|[stm32f1xx_hal_adc.h:428](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L428)|
|`ADC_CONVERSIONCLOCKCYCLES_SAMPLETIME_71CYCLES5`|值 84，单位 ADC 时钟周期；对应采样档位加 12.5 周期转换阶段，不含触发延迟或序列求和|[stm32f1xx_hal_adc.h:429](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L429)|
|`ADC_CONVERSIONCLOCKCYCLES_SAMPLETIME_239CYCLES5`|值 252，单位 ADC 时钟周期；对应采样档位加 12.5 周期转换阶段，不含触发延迟或序列求和|[stm32f1xx_hal_adc.h:430](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L430)|
|`ADC_REGULAR_GROUP`|转换组：规则组|[stm32f1xx_hal_adc.h:367](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L367)|
|`ADC_INJECTED_GROUP`|转换组：注入组|[stm32f1xx_hal_adc.h:368](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L368)|
|`ADC_REGULAR_INJECTED_GROUP`|转换组：两组|[stm32f1xx_hal_adc.h:369](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L369)|
|`ADC_DATAALIGN_RIGHT`|数据右对齐|[stm32f1xx_hal_adc.h:255](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L255)|
|`ADC_DATAALIGN_LEFT`|数据左对齐|[stm32f1xx_hal_adc.h:256](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L256)|
|`HAL_ADC_ERROR_NONE`|无错误|[stm32f1xx_hal_adc.h:238](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L238)|
|`HAL_ADC_ERROR_INTERNAL`|时钟、使能/禁用或状态相关内部错误|[stm32f1xx_hal_adc.h:239](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L239)|
|`HAL_ADC_ERROR_DMA`|ADC 关联 DMA 的错误码，包括已核版本中 DMA 传输错误与部分停止/中止失败路径|[stm32f1xx_hal_adc.h:242](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L242)|
|`ADC_AWD_EVENT`|模拟看门狗越界事件|[stm32f1xx_hal_adc.h:377](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L377)|
|`ADC_AWD1_EVENT`|同一看门狗事件的跨系列兼容别名|[stm32f1xx_hal_adc.h:379](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L379)|
|`HAL_ADC_STATE_RESET`|尚未初始化/已复位|[stm32f1xx_hal_adc.h:140](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L140)|
|`HAL_ADC_STATE_READY`|HAL 软件 READY 位；不能单独证明 ADC/DMA 已停止、已校准或缓冲区可复用|[stm32f1xx_hal_adc.h:141](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L141)|
|`HAL_ADC_STATE_BUSY_INTERNAL`|初始化或校准等内部处理忙|[stm32f1xx_hal_adc.h:142](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L142)|
|`HAL_ADC_STATE_TIMEOUT`|曾发生超时|[stm32f1xx_hal_adc.h:143](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L143)|
|`HAL_ADC_STATE_ERROR_INTERNAL`|内部操作错误|[stm32f1xx_hal_adc.h:146](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L146)|
|`HAL_ADC_STATE_ERROR_CONFIG`|配置错误|[stm32f1xx_hal_adc.h:147](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L147)|
|`HAL_ADC_STATE_ERROR_DMA`|ADC 软件 DMA 错误状态位；与 ErrorCode 字段分别维护，重新启动未必清除|[stm32f1xx_hal_adc.h:148](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L148)|
|`HAL_ADC_STATE_REG_BUSY`|规则转换正在运行或已武装待触发|[stm32f1xx_hal_adc.h:151](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L151)|
|`HAL_ADC_STATE_REG_EOC`|HAL 规则完成路径记录的软件状态位；规则轮询估算路径及 EOC 中断来源均须另核，不单独证明 DR 已更新|[stm32f1xx_hal_adc.h:153](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L153)|
|`HAL_ADC_STATE_INJ_BUSY`|注入转换正在运行或待触发|[stm32f1xx_hal_adc.h:158](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L158)|
|`HAL_ADC_STATE_INJ_EOC`|HAL 注入完成路径记录的软件状态位；注入轮询的估算路径也会设置，不单独证明 JDR 已更新|[stm32f1xx_hal_adc.h:160](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L160)|
|`HAL_ADC_STATE_AWD1`|模拟看门狗越界|[stm32f1xx_hal_adc.h:164](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L164)|
|`HAL_ADC_STATE_MULTIMODE_SLAVE`|双模式从 ADC 由主 ADC 控制|[stm32f1xx_hal_adc.h:169](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L169)|
|`ADC_EXTERNALTRIGCONVEDGE_NONE`|关闭外部触发|[stm32f1xx_hal_adc.h:276](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L276)|
|`ADC_EXTERNALTRIGCONVEDGE_RISING`|仅上升沿触发|[stm32f1xx_hal_adc.h:277](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L277)|
|`ADC_EXTERNALTRIGCONV_T1_CC1`|规则组外部触发：T1_CC1；仅本章保留的 C8 事件源|[stm32f1xx_hal_adc_ex.h:170](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L170)|
|`ADC_EXTERNALTRIGCONV_T1_CC2`|规则组外部触发：T1_CC2；仅本章保留的 C8 事件源|[stm32f1xx_hal_adc_ex.h:171](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L171)|
|`ADC_EXTERNALTRIGCONV_T2_CC2`|规则组外部触发：T2_CC2；仅本章保留的 C8 事件源|[stm32f1xx_hal_adc_ex.h:172](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L172)|
|`ADC_EXTERNALTRIGCONV_T3_TRGO`|规则组外部触发：T3_TRGO；仅本章保留的 C8 事件源|[stm32f1xx_hal_adc_ex.h:173](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L173)|
|`ADC_EXTERNALTRIGCONV_T4_CC4`|规则组外部触发：T4_CC4；仅本章保留的 C8 事件源|[stm32f1xx_hal_adc_ex.h:174](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L174)|
|`ADC_EXTERNALTRIGCONV_EXT_IT11`|规则组外部触发：EXT_IT11；仅本章保留的 C8 事件源|[stm32f1xx_hal_adc_ex.h:175](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L175)|
|`ADC_EXTERNALTRIGCONV_T1_CC3`|规则组外部触发：TIM1_CC3，硬件有效；固定版本中等容量断言列表漏列，见配置契约|[stm32f1xx_hal_adc_ex.h:187](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L187)|
|`ADC_SOFTWARE_START`|规则组软件触发|[stm32f1xx_hal_adc_ex.h:203](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L203)|
|`ADC_FLAG_STRT`|规则组启动状态位|[stm32f1xx_hal_adc.h:397](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L397)|
|`ADC_FLAG_JSTRT`|注入组启动状态位|[stm32f1xx_hal_adc.h:398](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L398)|
|`ADC_FLAG_EOC`|EOC硬件状态位；规则或注入结束均可能置位，须结合模式与结果寄存器判断数据来源。|[stm32f1xx_hal_adc.h:399](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L399)|
|`ADC_FLAG_JEOC`|注入组完成 JEOC状态位|[stm32f1xx_hal_adc.h:400](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L400)|
|`ADC_FLAG_AWD`|看门狗越界状态位|[stm32f1xx_hal_adc.h:401](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L401)|
|`ADC_IT_EOC`|EOC中断使能位；事件边界按硬件EOC语义解释，不能据此断言只有规则转换来源。|[stm32f1xx_hal_adc.h:387](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L387)|
|`ADC_IT_JEOC`|注入组完成 JEOC中断使能位|[stm32f1xx_hal_adc.h:388](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L388)|
|`ADC_IT_AWD`|看门狗越界中断使能位|[stm32f1xx_hal_adc.h:389](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L389)|
|`IS_ADC_RANGE`|检查 12 位数值 0–4095|[stm32f1xx_hal_adc.h:857](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L857)|
|`IS_ADC_REGULAR_DISCONT_NUMBER`|检查规则间断数量 1–8|[stm32f1xx_hal_adc.h:873](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L873)|
|`IS_ADC_REGULAR_NB_CONV`|检查规则序列长度 1–16|[stm32f1xx_hal_adc.h:865](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L865)|
|`ADC_REGULAR_RANK_1`|规则组序列位置 1|[stm32f1xx_hal_adc.h:330](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L330)|
|`ADC_REGULAR_RANK_2`|规则组序列位置 2|[stm32f1xx_hal_adc.h:331](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L331)|
|`ADC_REGULAR_RANK_3`|规则组序列位置 3|[stm32f1xx_hal_adc.h:332](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L332)|
|`ADC_REGULAR_RANK_4`|规则组序列位置 4|[stm32f1xx_hal_adc.h:333](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L333)|
|`ADC_REGULAR_RANK_5`|规则组序列位置 5|[stm32f1xx_hal_adc.h:334](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L334)|
|`ADC_REGULAR_RANK_6`|规则组序列位置 6|[stm32f1xx_hal_adc.h:335](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L335)|
|`ADC_REGULAR_RANK_7`|规则组序列位置 7|[stm32f1xx_hal_adc.h:336](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L336)|
|`ADC_REGULAR_RANK_8`|规则组序列位置 8|[stm32f1xx_hal_adc.h:337](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L337)|
|`ADC_REGULAR_RANK_9`|规则组序列位置 9|[stm32f1xx_hal_adc.h:338](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L338)|
|`ADC_REGULAR_RANK_10`|规则组序列位置 10|[stm32f1xx_hal_adc.h:339](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L339)|
|`ADC_REGULAR_RANK_11`|规则组序列位置 11|[stm32f1xx_hal_adc.h:340](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L340)|
|`ADC_REGULAR_RANK_12`|规则组序列位置 12|[stm32f1xx_hal_adc.h:341](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L341)|
|`ADC_REGULAR_RANK_13`|规则组序列位置 13|[stm32f1xx_hal_adc.h:342](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L342)|
|`ADC_REGULAR_RANK_14`|规则组序列位置 14|[stm32f1xx_hal_adc.h:343](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L343)|
|`ADC_REGULAR_RANK_15`|规则组序列位置 15|[stm32f1xx_hal_adc.h:344](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L344)|
|`ADC_REGULAR_RANK_16`|规则组序列位置 16|[stm32f1xx_hal_adc.h:345](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L345)|
|`ADC_SAMPLETIME_1CYCLE_5`|采样时间 1.5 个 ADC 时钟|[stm32f1xx_hal_adc.h:315](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L315)|
|`ADC_SAMPLETIME_7CYCLES_5`|采样时间 7.5 个 ADC 时钟|[stm32f1xx_hal_adc.h:316](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L316)|
|`ADC_SAMPLETIME_13CYCLES_5`|采样时间 13.5 个 ADC 时钟|[stm32f1xx_hal_adc.h:317](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L317)|
|`ADC_SAMPLETIME_28CYCLES_5`|采样时间 28.5 个 ADC 时钟|[stm32f1xx_hal_adc.h:318](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L318)|
|`ADC_SAMPLETIME_41CYCLES_5`|采样时间 41.5 个 ADC 时钟|[stm32f1xx_hal_adc.h:319](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L319)|
|`ADC_SAMPLETIME_55CYCLES_5`|采样时间 55.5 个 ADC 时钟|[stm32f1xx_hal_adc.h:320](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L320)|
|`ADC_SAMPLETIME_71CYCLES_5`|采样时间 71.5 个 ADC 时钟|[stm32f1xx_hal_adc.h:321](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L321)|
|`ADC_SAMPLETIME_239CYCLES_5`|采样时间 239.5 个 ADC 时钟|[stm32f1xx_hal_adc.h:322](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L322)|
|`ADC_SAMPLETIME_ALLCHANNELS_SMPR2BIT2`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:438](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L438)|
|`ADC_SAMPLETIME_ALLCHANNELS_SMPR1BIT2`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:442](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L442)|
|`ADC_SAMPLETIME_ALLCHANNELS_SMPR2BIT1`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:446](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L446)|
|`ADC_SAMPLETIME_ALLCHANNELS_SMPR1BIT1`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:450](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L450)|
|`ADC_SAMPLETIME_ALLCHANNELS_SMPR2BIT0`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:454](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L454)|
|`ADC_SAMPLETIME_ALLCHANNELS_SMPR1BIT0`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:458](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L458)|
|`ADC_SAMPLETIME_1CYCLE5_SMPR2ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:462](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L462)|
|`ADC_SAMPLETIME_7CYCLES5_SMPR2ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:463](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L463)|
|`ADC_SAMPLETIME_13CYCLES5_SMPR2ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:464](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L464)|
|`ADC_SAMPLETIME_28CYCLES5_SMPR2ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:465](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L465)|
|`ADC_SAMPLETIME_41CYCLES5_SMPR2ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:466](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L466)|
|`ADC_SAMPLETIME_55CYCLES5_SMPR2ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:467](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L467)|
|`ADC_SAMPLETIME_71CYCLES5_SMPR2ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:468](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L468)|
|`ADC_SAMPLETIME_239CYCLES5_SMPR2ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:469](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L469)|
|`ADC_SAMPLETIME_1CYCLE5_SMPR1ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:471](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L471)|
|`ADC_SAMPLETIME_7CYCLES5_SMPR1ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:472](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L472)|
|`ADC_SAMPLETIME_13CYCLES5_SMPR1ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:473](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L473)|
|`ADC_SAMPLETIME_28CYCLES5_SMPR1ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:474](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L474)|
|`ADC_SAMPLETIME_41CYCLES5_SMPR1ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:475](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L475)|
|`ADC_SAMPLETIME_55CYCLES5_SMPR1ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:476](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L476)|
|`ADC_SAMPLETIME_71CYCLES5_SMPR1ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:477](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L477)|
|`ADC_SAMPLETIME_239CYCLES5_SMPR1ALLCHANNELS`|批量设置 SMPR 采样时间的驱动内部位模式；不作为单通道 SamplingTime 参数|[stm32f1xx_hal_adc.h:478](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L478)|
|`ADC_SCAN_DISABLE`|ADC 共用扫描关闭|[stm32f1xx_hal_adc.h:267](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L267)|
|`ADC_SCAN_ENABLE`|ADC 共用扫描开启|[stm32f1xx_hal_adc.h:268](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L268)|

## ADC扩展符号

|符号|含义及边界|固定头文件定义|
|---|---|---|
|`ADC_MODE_INDEPENDENT`|ADC1/ADC2 独立工作|[stm32f1xx_hal_adc_ex.h:256](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L256)|
|`ADC_DUALMODE_REGSIMULT_INJECSIMULT`|双 ADC：规则和注入均同步|[stm32f1xx_hal_adc_ex.h:257](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L257)|
|`ADC_DUALMODE_REGSIMULT_ALTERTRIG`|双 ADC：规则同步、注入交替触发|[stm32f1xx_hal_adc_ex.h:258](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L258)|
|`ADC_DUALMODE_INJECSIMULT_INTERLFAST`|双 ADC：注入同步、规则快速交错|[stm32f1xx_hal_adc_ex.h:259](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L259)|
|`ADC_DUALMODE_INJECSIMULT_INTERLSLOW`|双 ADC：注入同步、规则慢速交错|[stm32f1xx_hal_adc_ex.h:260](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L260)|
|`ADC_DUALMODE_INJECSIMULT`|双 ADC：仅注入同步|[stm32f1xx_hal_adc_ex.h:261](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L261)|
|`ADC_DUALMODE_REGSIMULT`|双 ADC：仅规则同步|[stm32f1xx_hal_adc_ex.h:262](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L262)|
|`ADC_DUALMODE_INTERLFAST`|双 ADC：规则快速交错，间隔 7 个 ADC 周期|[stm32f1xx_hal_adc_ex.h:263](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L263)|
|`ADC_DUALMODE_INTERLSLOW`|双 ADC：规则慢速交错，间隔 14 个 ADC 周期|[stm32f1xx_hal_adc_ex.h:264](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L264)|
|`ADC_DUALMODE_ALTERTRIG`|双 ADC：注入交替触发|[stm32f1xx_hal_adc_ex.h:265](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L265)|
|`ADC_EXTERNALTRIGINJECCONV_EDGE_NONE`|关闭外部触发|[stm32f1xx_hal_adc_ex.h:157](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L157)|
|`ADC_EXTERNALTRIGINJECCONV_EDGE_RISING`|仅上升沿触发|[stm32f1xx_hal_adc_ex.h:158](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L158)|
|`ADC_EXTERNALTRIGINJECCONV_T2_TRGO`|注入组外部触发：T2_TRGO；仅本章保留的 C8 事件源|[stm32f1xx_hal_adc_ex.h:215](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L215)|
|`ADC_EXTERNALTRIGINJECCONV_T2_CC1`|注入组外部触发：T2_CC1；仅本章保留的 C8 事件源|[stm32f1xx_hal_adc_ex.h:216](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L216)|
|`ADC_EXTERNALTRIGINJECCONV_T3_CC4`|注入组外部触发：T3_CC4；仅本章保留的 C8 事件源|[stm32f1xx_hal_adc_ex.h:217](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L217)|
|`ADC_EXTERNALTRIGINJECCONV_T4_TRGO`|注入组外部触发：T4_TRGO；仅本章保留的 C8 事件源|[stm32f1xx_hal_adc_ex.h:218](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L218)|
|`ADC_EXTERNALTRIGINJECCONV_EXT_IT15`|注入组外部触发：EXT_IT15；仅本章保留的 C8 事件源|[stm32f1xx_hal_adc_ex.h:219](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L219)|
|`ADC_EXTERNALTRIGINJECCONV_T1_CC4`|注入组外部触发：T1_CC4；仅本章保留的 C8 事件源|[stm32f1xx_hal_adc_ex.h:230](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L230)|
|`ADC_EXTERNALTRIGINJECCONV_T1_TRGO`|注入组外部触发：T1_TRGO；仅本章保留的 C8 事件源|[stm32f1xx_hal_adc_ex.h:231](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L231)|
|`ADC_INJECTED_SOFTWARE_START`|注入组软件触发|[stm32f1xx_hal_adc_ex.h:247](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L247)|
|`IS_ADC_INJECTED_NB_CONV`|检查注入序列长度 1–4|[stm32f1xx_hal_adc_ex.h:516](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L516)|
|`ADC_INJECTED_RANK_1`|注入组序列位置 1|[stm32f1xx_hal_adc_ex.h:146](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L146)|
|`ADC_INJECTED_RANK_2`|注入组序列位置 2|[stm32f1xx_hal_adc_ex.h:147](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L147)|
|`ADC_INJECTED_RANK_3`|注入组序列位置 3|[stm32f1xx_hal_adc_ex.h:148](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L148)|
|`ADC_INJECTED_RANK_4`|注入组序列位置 4|[stm32f1xx_hal_adc_ex.h:149](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L149)|
|`ADC1_2_EXTERNALTRIGINJEC_T2_TRGO`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:327](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L327)|
|`ADC1_2_EXTERNALTRIGINJEC_T2_CC1`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:328](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L328)|
|`ADC1_2_EXTERNALTRIGINJEC_T3_CC4`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:329](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L329)|
|`ADC1_2_EXTERNALTRIGINJEC_T4_TRGO`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:330](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L330)|
|`ADC1_2_EXTERNALTRIGINJEC_EXT_IT15`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:331](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L331)|
|`ADC1_2_3_EXTERNALTRIGINJEC_T1_TRGO`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:348](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L348)|
|`ADC1_2_3_EXTERNALTRIGINJEC_T1_CC4`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:349](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L349)|
|`ADC1_2_3_JSWSTART`|注入组软件启动源的 JEXTSEL 编码；选择源与设置实际启动/触发使能位须区分|[stm32f1xx_hal_adc_ex.h:350](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L350)|
|`ADC1_2_EXTERNALTRIG_T1_CC1`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:290](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L290)|
|`ADC1_2_EXTERNALTRIG_T1_CC2`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:291](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L291)|
|`ADC1_2_EXTERNALTRIG_T2_CC2`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:292](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L292)|
|`ADC1_2_EXTERNALTRIG_T3_TRGO`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:293](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L293)|
|`ADC1_2_EXTERNALTRIG_T4_CC4`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:294](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L294)|
|`ADC1_2_EXTERNALTRIG_EXT_IT11`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:295](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L295)|
|`ADC1_2_3_EXTERNALTRIG_T1_CC3`|ADC1/ADC2 的触发选择内部编码；Tn_CCm/TRGO 或 EXTI 对应指定事件，不建议应用直接替代公开触发常量|[stm32f1xx_hal_adc_ex.h:313](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L313)|
|`ADC1_2_3_SWSTART`|规则组软件启动源的 EXTSEL 编码；选择源与设置实际启动/触发使能位须区分|[stm32f1xx_hal_adc_ex.h:314](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L314)|

## 硬件与条件编译边界

- HAL_ADC_ERROR_OVR、HAL_ADC_STATE_REG_OVR、HAL_ADC_STATE_REG_EOSMP、HAL_ADC_STATE_INJ_JQOVF、HAL_ADC_STATE_AWD2/3为头文件跨系列兼容名字；F103没有对应硬件检测资源，不能用于证明丢样检测或额外看门狗存在。
- C8没有TIM8，不采用ADC_EXTERNALTRIGCONV_T8_TRGO及TIM8注入触发重映射。
- USE_HAL_ADC_REGISTER_CALLBACKS==1时的七个回调ID、七个附加句柄字段及HAL_ADC_ERROR_INVALID_CALLBACK见[HAL配置字段](HAL配置字段.md)。
- 配置结构没有ExternalTrigConvEdge、ExternalTrigInjecConvEdge等其他系列字段；头文件触发边沿符号存在不意味着这些字段存在。
- HAL软件State、硬件SR、DMA完成标志和数据缓冲区有效性分别核对。

## 状态与配置解释边界

State 为可组合的软件位图，ErrorCode 是另一字段；不能仅按 READY、REG_EOC 或 INJ_EOC 的名称推出硬件状态和数据新鲜性。具体轮询分支及估算宏的通道 8/9 掩码缺口见[轮询实现契约](HAL轮询边界.md)。

本表保留原整理的 168 项，不能据此宣称是完整头文件 API 清单。USE_HAL_ADC_REGISTER_CALLBACKS==1 时的七个回调 ID、字段及 HAL_ADC_ERROR_INVALID_CALLBACK 见[条件回调结构](HAL配置字段.md)。头文件还保留 F1 不支持的跨系列状态名，例如 REG_OVR、REG_EOSMP、INJ_JQOVF、AWD2/3；这些名称不意味着 C8 增加对应硬件功能。
