# ADC HAL 配置结构及条件编译字段

依据 UM1850 Rev3 与固定 v1.1.4 源码。先选配置对象，再查字段；较长的时序和状态条件紧接对应表格说明。

- [公共与规则组初始化](#adc_inittypedef)
- [规则通道配置](#adc_channelconftypedef)
- [模拟看门狗](#adc_analogwdgconftypedef)
- [ADC 句柄](#__adc_handletypedef)
- [注入组配置](#adc_injectionconftypedef)
- [双 ADC 模式](#adc_multimodetypedef)
- [条件回调字段](#回调注册配置下的附加字段)

## `ADC_InitTypeDef`

[UM1850 Rev3 p56,57](https://www.st.com/resource/en/user_manual/um1850-description-of-stm32f1-hal-and-lowlayer-drivers-stmicroelectronics.pdf#page=56)。

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t DataAlign` | 规则组与注入组的数据对齐方式，见下方说明。 |
| `uint32_t ScanConvMode` | 规则组与注入组共用扫描开关；禁用时只转换 Rank 1，序列长度配置失效。 |
| `FunctionalState ContinuousConvMode` | 规则组连续转换开关：启用后首次触发启动，后续序列自动重复；与间断转换互斥。 |
| `uint32_t NbrOfConversion` | 规则组序列长度，1–16；多 Rank 要同时启用扫描。 |
| `FunctionalState DiscontinuousConvMode` | 规则组间断转换开关，只在扫描且非连续方式有效。 |
| `uint32_t NbrOfDiscConversion` | 每次触发执行的规则组间断转换个数，1–8；间断关闭时忽略。 |
| `uint32_t ExternalTrigConv` | 规则组触发源，软件触发或 TIM1 CC1/CC2/CC3、TIM2 CC2、TIM3 TRGO、TIM4 CC4、EXTI11；外部触发仅上升沿。 |

### 数据对齐

规则数据右对齐为 DR[11:0]、左对齐为 DR[15:4]。注入组执行偏移减法：右对齐 JDR[11:0] 为数据、[15:12] 为符号扩展；左对齐 JDR[14:3] 为数据、bit15 为符号、[2:0]=0。注入结果不能按规则组的无符号 0–4095 处理。

## `ADC_ChannelConfTypeDef`

[UM1850 Rev3 p57](https://www.st.com/resource/en/user_manual/um1850-description-of-stm32f1-hal-and-lowlayer-drivers-stmicroelectronics.pdf#page=57)。

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t Channel` | ADC 通道；C8 外部通道 0–9，内部通道 16/温度、17/VREFINT 仅 ADC1 可用。 |
| `uint32_t Rank` | 规则组位置，ADC_REGULAR_RANK_1 至 ADC_REGULAR_RANK_16；同一 Rank 再配置将覆盖原通道；移除末尾 Rank 也可缩短 NbrOfConversion，不能只停止为该 Rank 调用配置函数。 |
| `uint32_t SamplingTime` | 采样窗口的 ADC 周期数；档位、内部通道条件见下方说明。 |

### 采样时间与内部通道

每通道采样周期取 1.5、7.5、13.5、28.5、41.5、55.5、71.5、239.5 个 ADC 时钟；总转换时间再加 12.5 周期。同一通道规则组和注入组共享采样时间。内部通道采样条件须按DS5319 Table12/51及RM§11.10确定：VREFINT采样5.1µs为典型栏值、17.1µs为Max栏值；温度采样RM推荐17.1µs，不能把通用HAL注释的约5–17.1µs直接当成统一保证最小值。

## `ADC_AnalogWDGConfTypeDef`

[UM1850 Rev3 p57,58](https://www.st.com/resource/en/user_manual/um1850-description-of-stm32f1-hal-and-lowlayer-drivers-stmicroelectronics.pdf#page=57)。

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t WatchdogMode` | 模拟看门狗关闭、单通道或全通道；可监视规则组、注入组或两组。 |
| `uint32_t Channel` | 选择看门狗监视的 ADC 通道；仅 WatchdogMode 为单通道模式时有效，ADC1 内部通道及 C8 外部通道限制同上。 |
| `FunctionalState ITMode` | ENABLE 采用看门狗中断；DISABLE 只设置状态供轮询。 |
| `uint32_t HighThreshold` | 模拟看门狗上阈值，0–4095；应不小于下阈值。 |
| `uint32_t LowThreshold` | 模拟看门狗下阈值，0–4095；比较结果低于下阈值或高于上阈值时触发。 |
| `uint32_t WatchdogNumber` | 原文保留字段，置 0；C8 仅有一个模拟看门狗。 |

## `__ADC_HandleTypeDef`

[UM1850 Rev3 p58](https://www.st.com/resource/en/user_manual/um1850-description-of-stm32f1-hal-and-lowlayer-drivers-stmicroelectronics.pdf#page=58)。

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `ADC_TypeDef* Instance` | ADC 实例寄存器基地址，为 ADC1 或 ADC2；DMA 和内部通道仍受各实例能力限制。 |
| `ADC_InitTypeDef Init` | 本 ADC 的 ADC_InitTypeDef 初始化结构。 |
| `DMA_HandleTypeDef* DMA_Handle` | 关联的 DMA 句柄指针；C8 独立 ADC DMA 仅 ADC1，使用 DMA1 通道 1。 |
| `HAL_LockTypeDef Lock` | HAL 软件锁对象；驱动维护，不能替代 RTOS 互斥锁。 |
| `__IO uint32_t State` | ADC 驱动状态位图，可组合检测 HAL_ADC_STATE_*；由驱动维护。 |
| `__IO uint32_t ErrorCode` | 错误位图；NONE/INTERNAL/DMA及启用回调注册时的INVALID_CALLBACK分别解释。头文件OVR兼容符号不证明F103具有硬件OVR。 |

## `ADC_InjectionConfTypeDef`

[UM1850 Rev3 p80,81](https://www.st.com/resource/en/user_manual/um1850-description-of-stm32f1-hal-and-lowlayer-drivers-stmicroelectronics.pdf#page=80)。

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t InjectedChannel` | ADC 通道；C8 外部通道 0–9，内部通道 16/温度、17/VREFINT 仅 ADC1 可用。 |
| `uint32_t InjectedRank` | 注入组顺序，满足 1≤InjectedRank≤InjectedNbrOfConversion≤4；扫描关闭时仅 Rank 1。改变长度后须重建完整序列，由驱动处理 JSQR 布局。 |
| `uint32_t InjectedSamplingTime` | 每通道采样周期取 1.5、7.5、13.5、28.5、41.5、55.5、71.5、239.5 个 ADC 时钟；总转换时间再加 12.5 周期。同一通道规则组和注入组共享采样时间。内部通道采样条件见DS5319 Table12/51与RM§11.10，保留原表Typ/Max和RM推荐值的区别。 |
| `uint32_t InjectedOffset` | 从注入原始转换结果减去的偏移，0–4095；减法结果可能为负。 |
| `uint32_t InjectedNbrOfConversion` | 注入组序列长度，1–4；同组所有通道配置必须一致，长度改变会影响已有 Rank。 |
| `FunctionalState InjectedDiscontinuousConvMode` | 注入组间断模式开关，每次触发固定推进一个 Rank；ScanConvMode 关闭时该字段被忽略；ContinuousConvMode 开启时原文规定忽略；自动注入时不得启用。此字段对整个注入组生效。 |
| `FunctionalState AutoInjectedConv` | 规则序列结束后的自动注入开关，配置与停止条件见下方说明。 |
| `uint32_t ExternalTrigInjecConv` | 注入触发源：软件或 TIM1 TRGO/CC4、TIM2 TRGO/CC1、TIM3 CC4、TIM4 TRGO、EXTI15；仅上升沿。修改前关闭 ADC，否则 HAL 可能跳过该项而不报错。 |

### 自动注入的配置与停止条件

规则序列结束后自动执行注入组；采用自动注入时关闭两组间断模式，注入触发设软件/独立外部触发关闭。UM1850 原说明称普通 DMA 完成会停止 JAUTO、要持续应使用循环 DMA；已核固定实现的 DMA 完成回调不直接清 JAUTO 或 ADON，不能当作 ADC 硬件自行停机保证。重复配置 AutoInjectedConv=DISABLE 也不保证清除已有 JAUTO，见配置契约。

## `ADC_MultiModeTypeDef`

[UM1850 Rev3 p81](https://www.st.com/resource/en/user_manual/um1850-description-of-stm32f1-hal-and-lowlayer-drivers-stmicroelectronics.pdf#page=81)。

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t Mode` | 独立或双 ADC 模式；ADC1 为主、ADC2 为从。同步采样的两通道采样时间应相同；交错模式须满足采样阶段不重叠的限制。 |

## 回调注册配置下的附加字段

[v1.1.4固定头文件第189–220行](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L189-L220)。只有USE_HAL_ADC_REGISTER_CALLBACKS==1时出现以下字段；每个字段的类型均为void (*)(struct __ADC_HandleTypeDef *hadc)。hadc为回调所处理的ADC句柄，无返回值。

|字段|事件或用途|
|---|---|
|ConvCpltCallback|转换完成回调|
|ConvHalfCpltCallback|DMA半传输完成回调|
|LevelOutOfWindowCallback|模拟看门狗越界回调|
|ErrorCallback|错误回调|
|InjectedConvCpltCallback|注入组转换完成回调|
|MspInitCallback|底层初始化回调|
|MspDeInitCallback|底层反初始化回调|

这些字段不替代硬件和数据有效性条件；转换完成回调也不自动证明外设停止、所有DMA资源回收或规则DR新鲜。接口注册状态、回调ID和错误行为另按固定实现核查。

### 回调ID与注册接口

以下ID和值属于同一固定v1.1.4头文件的USE_HAL_ADC_REGISTER_CALLBACKS==1分支，不与DMA驱动的回调ID混用。

|ID|数值|对应句柄字段|
|---|---|---|
|HAL_ADC_CONVERSION_COMPLETE_CB_ID|0x00|ConvCpltCallback|
|HAL_ADC_CONVERSION_HALF_CB_ID|0x01|ConvHalfCpltCallback|
|HAL_ADC_LEVEL_OUT_OF_WINDOW_1_CB_ID|0x02|LevelOutOfWindowCallback|
|HAL_ADC_ERROR_CB_ID|0x03|ErrorCallback|
|HAL_ADC_INJ_CONVERSION_COMPLETE_CB_ID|0x04|InjectedConvCpltCallback|
|HAL_ADC_MSPINIT_CB_ID|0x09|MspInitCallback|
|HAL_ADC_MSPDEINIT_CB_ID|0x0A|MspDeInitCallback|

`HAL_ADC_RegisterCallback(hadc, CallbackID, pCallback)`与`HAL_ADC_UnRegisterCallback(hadc, CallbackID)`返回HAL_StatusTypeDef。hadc类型为ADC_HandleTypeDef*，CallbackID类型为HAL_ADC_CallbackIDTypeDef，pCallback类型为pADC_CallbackTypeDef（void (*)(ADC_HandleTypeDef*)）。

[固定v1.1.4实现第830–1022行](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L830-L1022)的分支如下：

- Register在pCallback==NULL时置ErrorCode中的HAL_ADC_ERROR_INVALID_CALLBACK并返回HAL_ERROR。
- State包含READY位时，可以注册/解除表列全部七种有效ID。检查表达式是位包含测试，不是State严格等于READY。
- State严格等于RESET时，仅接受MSPINIT和MSPDEINIT两个ID。
- 其他状态或不被当前分支接受的ID置INVALID_CALLBACK并返回HAL_ERROR；该错误位在所核头文件中为0x10。
- UnRegister将对应函数指针恢复到默认弱回调，而非置NULL。
- 这两段固定实现没有在函数体内获取HAL锁，也未检查hadc是否NULL；有效句柄与并发串行化由调用方保证。接口成功不代表转换/中断硬件已停止，不能在仍被调用的路径上任意换回调。

上述仅针对固定实现，不将错误处理或锁行为外推到其他HAL模块或所有版本。

## 配置与实现的配套约束

- TIM1_CC3 是 C8 的合法规则触发源，但所核两版的中等容量 IS_ADC_EXTTRIG 断言列表漏列此项。
- JAUTO/JDISCEN 的 DISABLE 更新、内部温度通道启动等待以及配置失败后的部分写入，见[配置更新与读数契约](HAL配置与读数.md)。
- HighThreshold 与 LowThreshold 应形成有效窗口；驱动没有独立检查两者大小关系。
