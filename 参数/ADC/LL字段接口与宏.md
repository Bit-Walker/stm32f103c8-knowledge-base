# ADC LL 字段接口与辅助宏

依据 UM1850 Rev3 pp602～678 和 ST 固定 LL 源码 bd368aa335c529641d2e567574885e02deacc64a。接口按配置、启动、读数和状态管理分组；源码特定差异保留在对应接口处。

## 适用范围与硬件边界

本章按 UM1850 Rev 3（2020 年 2 月）整理，面向 STM32F103C8T6。C8 有 ADC1、ADC2，固定 12 位分辨率；外部模拟输入为 PA0–PA7 的通道 0–7 和 PB0–PB1 的通道 8–9。内部温度与 VREFINT 为 ADC1 的通道 16、17。只有 ADC1 能向 DMA1 通道 1 发请求，ADC2 的数据可在双 ADC 模式由 ADC1 合并搬运。

C8 的 ADC 模拟供电 VDDA 工作范围为 2.4–3.6 V，输入范围为 VREF− 到 VREF+。ADC 时钟来自 PCLK2 的分频，最高 14 MHz。GPIO 必须设模拟输入，电压不得超出器件允许的模拟输入范围；采样周期应满足信号源阻抗和内部通道最短采样时间。一次 12 位转换需要所选采样周期再加 12.5 个 ADC 时钟。内部通道使能后须等待稳定，温度传感器还须满足最短采样时间。

硬件 SR 有 EOC、JEOC、AWD、STRT、JSTRT；F1 不具有另一套独立的 EOS/JEOS 或硬件 OVR 标志。LL 使用 EOS/JEOS 名称映射 F1 的 EOC/JEOC；它们不是新增寄存器位。普通结果共用 DR，软件读取太慢会覆盖旧值；没有 OVR 中断替应用检测丢样。注入组使用独立 JDR1–JDR4。RM0008 的 EOC 位说明还包括注入组转换完成，因此单看 EOC=1 不能一概断定是规则组的新数据；应结合当前组状态、JEOC 和读数路径处理。

## 配置与运行约束

- 扫描是整个 ADC 共用属性。规则组长度 1–16，注入组 1–4，顺序由 Rank 决定，非通道编号大小。相同物理通道允许安排在多个 Rank。
- 通道采样时间属于物理通道；规则组最后一次配置会影响注入组的同通道，反之亦然。注入偏移按注入 Rank 配置，值为 0–4095，结果可为负。
- 规则连续转换与间断模式互斥；自动注入与两组间断模式不兼容。注入间断固定每次触发一个 Rank，规则间断每次触发 1–8 个 Rank。
- 外部触发只支持上升沿。选择触发源与开放触发是不同步骤。普通软件启动函数不能当成外部触发开放函数使用。
- 规则组多通道扫描优先使用 DMA；转换完成中断不能保证逐一取回整个序列。UM1850 只说扫描轮询改用“最大转换时间”等待，不能扩写成保证等待整个序列结束。所核对 HAL 实现的估算分支不逐 Rank 检查完成，也不确认外部触发已发生；扫描加单 Rank 间断可限制硬件每次转换数量，但仍不能使此 HAL 分支自动变成 EOC 轮询。具体条件见[规则组轮询接口](HAL轮询边界.md)。DMA 读取 DR 会清 EOC，因此不能让轮询与 DMA 竞争同一结束标志。
- 改序列、触发源、双模式和注入组公共属性前先停止转换；公共模式变化前停止 ADC1 与 ADC2。HAL 某些在线更新会跳过不允许修改的字段，不报错并不代表所有字段已经改变。
- ADC1/ADC2 共用中断向量；两个实例都在使用时，IRQ 应对相应句柄分别分发。DMA IRQ 应调用 HAL_DMA_IRQHandler，而不是把 ADC IRQ 处理函数填入 DMA 向量。原文该处为明显笔误。

## LL 初始化和状态管理

LL 不使用 HAL 句柄，不维护 HAL 状态位图，不提供超时、资源锁或弱回调。内联 Set/Enable 通常直接访问寄存器并返回 void；是否在合法状态调用、稳定等待和超时由应用负责。结构初始化函数通常属于完整 LL 驱动配置（USE_FULL_LL_DRIVER），编译时应包含相应实现文件；StructInit 只填结构默认值，不初始化时钟或 GPIO。

初始化应先配置 RCC/GPIO，在相关 ADC 禁用时设置公共模式、组序列、采样时间与看门狗；触发保持关闭。置 ADON 后等待稳定，并满足校准前已上电至少两个 ADC 周期，完成 RSTCAL/CAL 的启动与等待。校准完成后，先确认 DMA/NVIC 和结果接收路径已就绪，再按所选触发方式开放转换。若校准流程保留 ADON=1，不要再无条件调用 LL_ADC_Enable：这个内联函数直接对 ADON 写 1，F1 在该位已为 1 且 CR2 其它位没有同时改变时，会把再次写 1 作为启动转换的动作。若流程曾关闭 ADC，应重新上电并等待稳定。以上状态分支须由应用明确维护。[ADON 硬件语义：RM0008 Rev21 p243](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=243)

LL_ADC_StartCalibration 只置 CAL，不负责 ADON、RSTCAL、延时或超时。原文同时保留“校准前禁用”和“已经上电至少两个周期”的不一致说明；执行条件以 RM0008 的上电校准要求为依据，并区分 HAL 包装函数的入口条件。

CommonInit 要求公共组内 ADC1 与 ADC2 都禁用。Init、REG_Init、INJ_Init 要求所选 ADC 禁用；这些批量初始化不会代替每 Rank 的通道配置和采样时间配置。LL 触发 Stop 只屏蔽未来外部触发，并不立即取消正在进行的转换；结束连续运行需 LL_ADC_Disable。

LL 的 EOS/JEOS 与 F1 硬件 EOC/JEOC 对应。查询标志返回 0/1；查询中断使能与查询事件是否发生是不同操作。读取 DR 清 EOC；对 JEOC 按手册的 SR 清除机制处理，不依赖 JDR 读取自动清标志的跨系列注释。双ADC的状态须按实际实例地址检查：固定版本三个SLV包装函数存在读到ADC1_CR1的偏移问题，不能按名称认定它们读取ADC2事件，详见[从标志地址核查](LL固定实现边界.md#从-adc-状态查询的地址偏移与接口说明不一致)。内部温度/VREFINT通路仍只由ADC1可测量。

固定版本的批量初始化、复位范围和返回值差异见[LL 实现边界](LL固定实现边界.md)。

### 公共实例约定

ADCx 表示 ADC1 或 ADC2 的寄存器实例；DMA、内部通道及双 ADC 等接口仍按各节明确的实例限制使用。

ADCxy_COMMON 表示 ADC1/ADC2 公共配置入口，可用 __LL_ADC_COMMON_INSTANCE(ADCx) 取得。公共控制使用现有 ADC 寄存器映射，没有额外独立的公共 ADC 外设块；具体实例限制仍以各接口说明为准。

## 配置结构逐字段参考

### `LL_ADC_CommonInitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t Multimode` | 独立或双 ADC 模式；ADC1 为主、ADC2 为从。同步采样的两通道采样时间应相同；交错模式须满足采样阶段不重叠的限制。 |

### `LL_ADC_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t DataAlignment` | 规则数据右对齐 DR[11:0]、左对齐 DR[15:4]；注入右对齐 JDR[11:0] 和 [15:12] 符号扩展，左对齐 JDR[14:3] 和 bit15 符号。注入减去偏移后可能为负。 |
| `uint32_t SequencersScanMode` | 规则组与注入组共用扫描开关；禁用时只转换 Rank 1，序列长度配置失效。 |

### `LL_ADC_REG_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t TriggerSource` | 规则组 TriggerSource，使用 LL_ADC_REG_TRIG_* 集合，外部仅上升沿。 |
| `uint32_t SequencerLength` | 取 `LL_ADC_REG_SEQ_SCAN_DISABLE`（1 Rank）或 `LL_ADC_REG_SEQ_SCAN_ENABLE_2RANKS` 至 `LL_ADC_REG_SEQ_SCAN_ENABLE_16RANKS` 的编码，不直接填整数长度 1–16；扫描关闭时仅执行 Rank 1。 |
| `uint32_t SequencerDiscont` | 取 `LL_ADC_REG_SEQ_DISCONT_DISABLE`，或 `LL_ADC_REG_SEQ_DISCONT_1RANK` 至 `LL_ADC_REG_SEQ_DISCONT_8RANKS` 的编码，不直接填 Rank 个数；启用时每次触发 1–8 Rank，只在序列至少 2 Rank 时生效，不得同时启用连续转换或自动注入。 |
| `uint32_t ContinuousMode` | 规则组连续转换开关：启用后首次触发启动，后续序列自动重复；与间断转换互斥。 |
| `uint32_t DMATransfer` | 规则组 DMA 请求开关/方式；C8 仅 ADC1 能发出 ADC DMA 请求，实际单次或循环缓冲还取决于 DMA 配置。 |

### `LL_ADC_INJ_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t TriggerSource` | 注入组 TriggerSource，使用 LL_ADC_INJ_TRIG_* 集合，外部仅上升沿。 |
| `uint32_t SequencerLength` | 取 `LL_ADC_INJ_SEQ_SCAN_DISABLE`（1 Rank）或 `LL_ADC_INJ_SEQ_SCAN_ENABLE_2RANKS` 至 `LL_ADC_INJ_SEQ_SCAN_ENABLE_4RANKS` 的编码，不直接填整数长度 1–4；扫描关闭时仅执行 Rank 1。 |
| `uint32_t SequencerDiscont` | 取 `LL_ADC_INJ_SEQ_DISCONT_DISABLE` 或 `LL_ADC_INJ_SEQ_DISCONT_1RANK`；开启时每次触发固定 1 Rank，只在序列至少 2 Rank 时生效，不得与自动注入同用。 |
| `uint32_t TrigAuto` | 规则序列结束后自动执行注入组；采用自动注入时关闭两组间断模式，注入触发设软件/独立外部触发关闭。若注入触发源为外部事件，TrigAuto 必须为独立注入。LL 本身没有 HAL 的 DMA 完成状态管理，不能从 DMA 非循环传输结束推断 JAUTO 或 ADC 自动停止。 |

## 函数接口逐项参考

- [公共配置与数据格式](#公共配置与数据格式)
- [规则组配置](#规则组配置)
- [注入组配置](#注入组配置)
- [采样时间与模拟看门狗](#采样时间与模拟看门狗)
- [双 ADC 模式](#双-adc-模式)
- [ADC 使能与校准](#adc-使能与校准)
- [规则组启动与读数](#规则组启动与读数)
- [注入组启动与读数](#注入组启动与读数)
- [转换与看门狗状态标志](#转换与看门狗状态标志)
- [中断使能与查询](#中断使能与查询)
- [批量初始化与结构默认值](#批量初始化与结构默认值)

以下保留原文 C 原型；`__STATIC_INLINE` 表示 LL 头文件内联接口。重复的时钟、状态与实例约束已在本章开头集中说明，仍适用于每个接口。HAL/LL 的枚举编码不能交叉传入。

### 公共配置与数据格式

#### `LL_ADC_DMA_GetRegAddr`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1600)

```c
__STATIC_INLINE uint32_t LL_ADC_DMA_GetRegAddr (ADC_TypeDef * ADCx, uint32_t Register);
```

取得 ADC 数据寄存器的地址供 DMA 配置使用；C8 的独立和双 ADC DMA 均以 ADC1 为入口。

- `Register`：需要取得地址的规则数据或双 ADC 数据寄存器类别。
  - 可用编码：`LL_ADC_DMA_REG_REGULAR_DATA`、`LL_ADC_DMA_REG_REGULAR_DATA_MULTI`。

返回：uint32_t 数据寄存器地址，用于 DMA 外设端地址。

#### `LL_ADC_SetCommonPathInternalCh`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1658)

```c
__STATIC_INLINE void LL_ADC_SetCommonPathInternalCh (ADC_Common_TypeDef * ADCxy_COMMON, uint32_t PathInternal);
```

设置ADC1 内部温度传感器和 VREFINT 的公共测量通路。

- `ADCxy_COMMON`：公共配置入口，见本页[公共实例约定](#公共实例约定)。
- `PathInternal`：内部温度/VREFINT 通路位组合，打开后等待稳定。
  - 可用编码：`LL_ADC_PATH_INTERNAL_NONE`、`LL_ADC_PATH_INTERNAL_VREFINT`、`LL_ADC_PATH_INTERNAL_TEMPSENSOR`。

返回：无返回值。

- 内部通路只供 ADC1 采样；使能后须满足稳定时间和内部通道采样时间。


PathInternal 可按位组合。使能后按数据手册等待，原文引用 LL_ADC_DELAY_TEMPSENSOR_STAB_US；等待稳定与满足最短采样时间是两个条件。F1 的两内部通路共用 TSVREFE，不能认为能分别独立关闭。

#### `LL_ADC_GetCommonPathInternalCh`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1677)

```c
__STATIC_INLINE uint32_t LL_ADC_GetCommonPathInternalCh (ADC_Common_TypeDef * ADCxy_COMMON);
```

读取ADC1 内部温度传感器和 VREFINT 的公共测量通路。

- `ADCxy_COMMON`：公共配置入口，见本页[公共实例约定](#公共实例约定)。

返回：uint32_t，零表示共同通路关闭；非零为 TSVREFE 位。VREFINT 与 TEMPSENSOR 两个常量在 F1 上数值相同，读回不能区分独立使能。

- 内部通路只供 ADC1 采样；使能后须满足稳定时间和内部通道采样时间。


返回通路编码或组合；F1 两内部通路由同一 TSVREFE 控制。

#### `LL_ADC_SetDataAlignment`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1701)

```c
__STATIC_INLINE void LL_ADC_SetDataAlignment (ADC_TypeDef * ADCx, uint32_t DataAlignment);
```

设置转换数据左/右对齐方式。

- `DataAlignment`：转换数据左对齐或右对齐。
  - 可用编码：`LL_ADC_DATA_ALIGN_RIGHT`、`LL_ADC_DATA_ALIGN_LEFT`。

返回：无返回值。

#### `LL_ADC_GetDataAlignment`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1716)

```c
__STATIC_INLINE uint32_t LL_ADC_GetDataAlignment (ADC_TypeDef * ADCx);
```

读取转换数据左/右对齐方式。


返回：uint32_t，返回编码：`LL_ADC_DATA_ALIGN_RIGHT`、`LL_ADC_DATA_ALIGN_LEFT`。

#### `LL_ADC_SetSequencersScanMode`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1742)

```c
__STATIC_INLINE void LL_ADC_SetSequencersScanMode (ADC_TypeDef * ADCx, uint32_t ScanMode);
```

设置规则组和注入组共用的扫描开关。

- `ScanMode`：整个 ADC 的序列扫描开关。
  - 可用编码：`LL_ADC_SEQ_SCAN_DISABLE`、`LL_ADC_SEQ_SCAN_ENABLE`。

返回：无返回值。

#### `LL_ADC_GetSequencersScanMode`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1767)

```c
__STATIC_INLINE uint32_t LL_ADC_GetSequencersScanMode (ADC_TypeDef * ADCx);
```

读取规则组和注入组共用的扫描开关。


返回：uint32_t，返回编码：`LL_ADC_SEQ_SCAN_DISABLE`、`LL_ADC_SEQ_SCAN_ENABLE`。

### 规则组配置

#### `LL_ADC_REG_SetTriggerSource`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1814)

```c
__STATIC_INLINE void LL_ADC_REG_SetTriggerSource (ADC_TypeDef * ADCx, uint32_t TriggerSource);
```

设置规则组触发源。

- `TriggerSource`：所在组的软件/外部触发来源。
  - 可用编码：`LL_ADC_REG_TRIG_SOFTWARE`、`LL_ADC_REG_TRIG_EXT_TIM1_CH3`、`LL_ADC_REG_TRIG_EXT_TIM1_CH1`、`LL_ADC_REG_TRIG_EXT_TIM1_CH2`、`LL_ADC_REG_TRIG_EXT_TIM2_CH2`、`LL_ADC_REG_TRIG_EXT_TIM3_TRGO`、`LL_ADC_REG_TRIG_EXT_TIM4_CH4`、`LL_ADC_REG_TRIG_EXT_EXTI_LINE11`。

返回：无返回值。

原文另列 `LL_ADC_REG_TRIG_EXT_TIM8_TRGO`、`LL_ADC_REG_TRIG_EXT_TIM8_TRGO_ADC3`、`LL_ADC_REG_TRIG_EXT_TIM3_CH1`、`LL_ADC_REG_TRIG_EXT_TIM2_CH3`、`LL_ADC_REG_TRIG_EXT_TIM8_CH1`、`LL_ADC_REG_TRIG_EXT_TIM5_CH1`、`LL_ADC_REG_TRIG_EXT_TIM5_CH3`；它们属于其它密度器件的 TIM8 或 ADC3/TIM5 路由，不是 C8 的 ADC1/ADC2 可选事件。TIM2/3/4 即使存在，也不能把 ADC3 专用触发连线套给 ADC1/ADC2。

#### `LL_ADC_REG_GetTriggerSource`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1861)

```c
__STATIC_INLINE uint32_t LL_ADC_REG_GetTriggerSource (ADC_TypeDef * ADCx);
```

读取规则组触发源。


返回：uint32_t，返回编码：`LL_ADC_REG_TRIG_SOFTWARE`、`LL_ADC_REG_TRIG_EXT_TIM1_CH3`、`LL_ADC_REG_TRIG_EXT_TIM1_CH1`、`LL_ADC_REG_TRIG_EXT_TIM1_CH2`、`LL_ADC_REG_TRIG_EXT_TIM2_CH2`、`LL_ADC_REG_TRIG_EXT_TIM3_TRGO`、`LL_ADC_REG_TRIG_EXT_TIM4_CH4`、`LL_ADC_REG_TRIG_EXT_EXTI_LINE11`。


原文另列 `LL_ADC_REG_TRIG_EXT_TIM8_TRGO`、`LL_ADC_REG_TRIG_EXT_TIM8_TRGO_ADC3`、`LL_ADC_REG_TRIG_EXT_TIM3_CH1`、`LL_ADC_REG_TRIG_EXT_TIM2_CH3`、`LL_ADC_REG_TRIG_EXT_TIM8_CH1`、`LL_ADC_REG_TRIG_EXT_TIM5_CH1`、`LL_ADC_REG_TRIG_EXT_TIM5_CH3`；它们属于其它密度器件的 TIM8 或 ADC3/TIM5 路由，不是 C8 的 ADC1/ADC2 可选事件。TIM2/3/4 即使存在，也不能把 ADC3 专用触发连线套给 ADC1/ADC2。

#### `LL_ADC_REG_IsTriggerSourceSWStart`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1877)

```c
__STATIC_INLINE uint32_t LL_ADC_REG_IsTriggerSourceSWStart (ADC_TypeDef * ADCx);
```

判断规则组触发源是否为软件触发；1 表示软件触发。


返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

#### `LL_ADC_REG_SetSequencerLength`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1939)

```c
__STATIC_INLINE void LL_ADC_REG_SetSequencerLength (ADC_TypeDef * ADCx, uint32_t SequencerNbRanks);
```

设置规则组 1–16 个 Rank 的序列长度。

- `SequencerNbRanks`：规则组 1–16 个 Rank 的编码值。
  - 可用编码：`LL_ADC_REG_SEQ_SCAN_DISABLE`、`LL_ADC_REG_SEQ_SCAN_ENABLE_2RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_3RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_4RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_5RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_6RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_7RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_8RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_9RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_10RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_11RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_12RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_13RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_14RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_15RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_16RANKS`。

返回：无返回值。

本函数只配置规则组长度；Rank 与通道绑定另用 LL_ADC_REG_SetSequencerRanks。执行顺序为 Rank 1 到 Rank n，与通道编号无关；全局扫描关闭时只执行 Rank 1，SEQ_SCAN_DISABLE 也表示一 Rank。

#### `LL_ADC_REG_GetSequencerLength`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1999)

```c
__STATIC_INLINE uint32_t LL_ADC_REG_GetSequencerLength (ADC_TypeDef * ADCx);
```

读取规则组 1–16 个 Rank 的序列长度。


返回：uint32_t，返回编码：`LL_ADC_REG_SEQ_SCAN_DISABLE`、`LL_ADC_REG_SEQ_SCAN_ENABLE_2RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_3RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_4RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_5RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_6RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_7RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_8RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_9RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_10RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_11RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_12RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_13RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_14RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_15RANKS`、`LL_ADC_REG_SEQ_SCAN_ENABLE_16RANKS`。


返回规则组长度编码，非十进制个数。全局扫描关闭时即使读回较长配置，硬件仍只执行 Rank 1。

#### `LL_ADC_REG_SetSequencerDiscont`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2027)

```c
__STATIC_INLINE void LL_ADC_REG_SetSequencerDiscont (ADC_TypeDef * ADCx, uint32_t SeqDiscont);
```

设置规则组间断模式及每次触发的 1–8 次转换数。

- `SeqDiscont`：规则组每次触发 1–8 Rank 的间断转换编码。
  - 可用编码：`LL_ADC_REG_SEQ_DISCONT_DISABLE`、`LL_ADC_REG_SEQ_DISCONT_1RANK`、`LL_ADC_REG_SEQ_DISCONT_2RANKS`、`LL_ADC_REG_SEQ_DISCONT_3RANKS`、`LL_ADC_REG_SEQ_DISCONT_4RANKS`、`LL_ADC_REG_SEQ_DISCONT_5RANKS`、`LL_ADC_REG_SEQ_DISCONT_6RANKS`、`LL_ADC_REG_SEQ_DISCONT_7RANKS`、`LL_ADC_REG_SEQ_DISCONT_8RANKS`。

返回：无返回值。

规则组间断模式不能与规则连续转换同时启用，也不能与自动注入同时启用。每次触发转换 SeqDiscont 指定个数；最后不足一段时完成剩余 Rank。

#### `LL_ADC_REG_GetSequencerDiscont`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2050)

```c
__STATIC_INLINE uint32_t LL_ADC_REG_GetSequencerDiscont (ADC_TypeDef * ADCx);
```

读取规则组间断模式及每次触发的 1–8 次转换数。


返回：uint32_t，返回编码：`LL_ADC_REG_SEQ_DISCONT_DISABLE`、`LL_ADC_REG_SEQ_DISCONT_1RANK`、`LL_ADC_REG_SEQ_DISCONT_2RANKS`、`LL_ADC_REG_SEQ_DISCONT_3RANKS`、`LL_ADC_REG_SEQ_DISCONT_4RANKS`、`LL_ADC_REG_SEQ_DISCONT_5RANKS`、`LL_ADC_REG_SEQ_DISCONT_6RANKS`、`LL_ADC_REG_SEQ_DISCONT_7RANKS`、`LL_ADC_REG_SEQ_DISCONT_8RANKS`。

#### `LL_ADC_REG_SetSequencerRanks`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2130)

```c
__STATIC_INLINE void LL_ADC_REG_SetSequencerRanks (ADC_TypeDef * ADCx, uint32_t Rank, uint32_t Channel);
```

设置规则组指定 Rank 对应的通道。

- `Rank`：规则组 Rank 1–16 的枚举。
  - 可用编码：`LL_ADC_REG_RANK_1`、`LL_ADC_REG_RANK_2`、`LL_ADC_REG_RANK_3`、`LL_ADC_REG_RANK_4`、`LL_ADC_REG_RANK_5`、`LL_ADC_REG_RANK_6`、`LL_ADC_REG_RANK_7`、`LL_ADC_REG_RANK_8`、`LL_ADC_REG_RANK_9`、`LL_ADC_REG_RANK_10`、`LL_ADC_REG_RANK_11`、`LL_ADC_REG_RANK_12`、`LL_ADC_REG_RANK_13`、`LL_ADC_REG_RANK_14`、`LL_ADC_REG_RANK_15`、`LL_ADC_REG_RANK_16`。
- `Channel`：所选通道或 Rank 映射的通道；采用下面列出的同一驱动常量，不能混用 HAL 和 LL 编码。
  - 通道符号见[通道编码](#通道编码)，内部通道还须满足 ADC1 与通路使能条件。

返回：无返回值。

任何有效通道都可安排到任一有效 Rank，重复通道也允许。内部通道还须 LL_ADC_SetCommonPathInternalCh 开通通路；通道 10–15 编码不等于 C8 存在可接线输入脚。

#### `LL_ADC_REG_GetSequencerRanks`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2224)

```c
__STATIC_INLINE uint32_t LL_ADC_REG_GetSequencerRanks (ADC_TypeDef * ADCx, uint32_t Rank);
```

读取规则组指定 Rank 对应的通道。

- `Rank`：规则组 Rank 1–16 的枚举。
  - 可用编码：`LL_ADC_REG_RANK_1`、`LL_ADC_REG_RANK_2`、`LL_ADC_REG_RANK_3`、`LL_ADC_REG_RANK_4`、`LL_ADC_REG_RANK_5`、`LL_ADC_REG_RANK_6`、`LL_ADC_REG_RANK_7`、`LL_ADC_REG_RANK_8`、`LL_ADC_REG_RANK_9`、`LL_ADC_REG_RANK_10`、`LL_ADC_REG_RANK_11`、`LL_ADC_REG_RANK_12`、`LL_ADC_REG_RANK_13`、`LL_ADC_REG_RANK_14`、`LL_ADC_REG_RANK_15`、`LL_ADC_REG_RANK_16`。

返回：uint32_t，当前通道配置的 LL 编码。有效测量通道见[通道编码](#通道编码)；读取配置不验证外部接线。


返回编码只含通道定义的部分格式，不能不经转换就传给另一 LL 通道配置函数。用 __LL_ADC_CHANNEL_TO_DECIMAL_NB 得到编号，再选择完整 LL_ADC_CHANNEL_* 常量；与内部通道常量比较时先用 __LL_ADC_CHANNEL_INTERNAL_TO_EXTERNAL 去掉内部标记。

#### `LL_ADC_REG_SetContinuousMode`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2249)

```c
__STATIC_INLINE void LL_ADC_REG_SetContinuousMode (ADC_TypeDef * ADCx, uint32_t Continuous);
```

设置规则组单次或连续转换方式。

- `Continuous`：单次或连续规则转换。
  - 可用编码：`LL_ADC_REG_CONV_SINGLE`、`LL_ADC_REG_CONV_CONTINUOUS`。

返回：无返回值。


SINGLE 每次触发执行一次已配置的规则序列；CONTINUOUS 首次触发后连续重复。连续模式不能与规则间断模式同时启用。

#### `LL_ADC_REG_GetContinuousMode`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2266)

```c
__STATIC_INLINE uint32_t LL_ADC_REG_GetContinuousMode (ADC_TypeDef * ADCx);
```

读取规则组单次或连续转换方式。


返回：uint32_t，返回编码：`LL_ADC_REG_CONV_SINGLE`、`LL_ADC_REG_CONV_CONTINUOUS`。


返回单次/连续模式编码；单次是每次触发一个已配置序列，连续是首次触发后自动重复。

#### `LL_ADC_REG_SetDMATransfer`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2298)

```c
__STATIC_INLINE void LL_ADC_REG_SetDMATransfer (ADC_TypeDef * ADCx, uint32_t DMATransfer);
```

设置规则组 DMA 请求方式。

- `DMATransfer`：规则 DMA 请求模式；ADC2 无独立 DMA。
  - 可用编码：`LL_ADC_REG_DMA_TRANSFER_NONE`、`LL_ADC_REG_DMA_TRANSFER_UNLIMITED`。

返回：无返回值。


F1 只有 NONE/UNLIMITED，原文关于 LIMITED 及 DMA 停止后产生 OVR 的跨系列说明不适用。DMA 非循环模式达到长度后自身停止，但 ADC 可继续覆盖 DR；选择循环 DMA 才能持续接收。用 LL_ADC_DMA_GetRegAddr 取得外设端地址。

#### `LL_ADC_REG_GetDMATransfer`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2329)

```c
__STATIC_INLINE uint32_t LL_ADC_REG_GetDMATransfer (ADC_TypeDef * ADCx);
```

读取规则组 DMA 请求方式。


返回：uint32_t，返回编码：`LL_ADC_REG_DMA_TRANSFER_NONE`、`LL_ADC_REG_DMA_TRANSFER_UNLIMITED`。


此函数读 ADC 的 DMA 请求配置，不读 DMA 控制器 CIRC/计数状态。F1 没有 LIMITED 请求模式或硬件 OVR；DMA 非循环耗尽后 ADC 数据可能丢失。

### 注入组配置

#### `LL_ADC_INJ_SetTriggerSource`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2375)

```c
__STATIC_INLINE void LL_ADC_INJ_SetTriggerSource (ADC_TypeDef * ADCx, uint32_t TriggerSource);
```

设置注入组触发源。

- `TriggerSource`：所在组的软件/外部触发来源。
  - 可用编码：`LL_ADC_INJ_TRIG_SOFTWARE`、`LL_ADC_INJ_TRIG_EXT_TIM1_TRGO`、`LL_ADC_INJ_TRIG_EXT_TIM1_CH4`、`LL_ADC_INJ_TRIG_EXT_TIM2_TRGO`、`LL_ADC_INJ_TRIG_EXT_TIM2_CH1`、`LL_ADC_INJ_TRIG_EXT_TIM3_CH4`、`LL_ADC_INJ_TRIG_EXT_TIM4_TRGO`、`LL_ADC_INJ_TRIG_EXT_EXTI_LINE15`。

返回：无返回值。

原文另列 `LL_ADC_INJ_TRIG_EXT_TIM8_CH4`、`LL_ADC_INJ_TRIG_EXT_TIM8_CH4_ADC3`、`LL_ADC_INJ_TRIG_EXT_TIM4_CH3`、`LL_ADC_INJ_TRIG_EXT_TIM8_CH2`、`LL_ADC_INJ_TRIG_EXT_TIM5_TRGO`、`LL_ADC_INJ_TRIG_EXT_TIM5_CH4`；它们属于其它密度器件的 TIM8 或 ADC3/TIM5 路由，不是 C8 的 ADC1/ADC2 可选事件。TIM2/3/4 即使存在，也不能把 ADC3 专用触发连线套给 ADC1/ADC2。

#### `LL_ADC_INJ_GetTriggerSource`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2421)

```c
__STATIC_INLINE uint32_t LL_ADC_INJ_GetTriggerSource (ADC_TypeDef * ADCx);
```

读取注入组触发源。


返回：uint32_t，返回编码：`LL_ADC_INJ_TRIG_SOFTWARE`、`LL_ADC_INJ_TRIG_EXT_TIM1_TRGO`、`LL_ADC_INJ_TRIG_EXT_TIM1_CH4`、`LL_ADC_INJ_TRIG_EXT_TIM2_TRGO`、`LL_ADC_INJ_TRIG_EXT_TIM2_CH1`、`LL_ADC_INJ_TRIG_EXT_TIM3_CH4`、`LL_ADC_INJ_TRIG_EXT_TIM4_TRGO`、`LL_ADC_INJ_TRIG_EXT_EXTI_LINE15`。


原文另列 `LL_ADC_INJ_TRIG_EXT_TIM8_CH4`、`LL_ADC_INJ_TRIG_EXT_TIM8_CH4_ADC3`、`LL_ADC_INJ_TRIG_EXT_TIM4_CH3`、`LL_ADC_INJ_TRIG_EXT_TIM8_CH2`、`LL_ADC_INJ_TRIG_EXT_TIM5_TRGO`、`LL_ADC_INJ_TRIG_EXT_TIM5_CH4`；它们属于其它密度器件的 TIM8 或 ADC3/TIM5 路由，不是 C8 的 ADC1/ADC2 可选事件。TIM2/3/4 即使存在，也不能把 ADC3 专用触发连线套给 ADC1/ADC2。

#### `LL_ADC_INJ_IsTriggerSourceSWStart`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2437)

```c
__STATIC_INLINE uint32_t LL_ADC_INJ_IsTriggerSourceSWStart (ADC_TypeDef * ADCx);
```

判断注入组触发源是否为软件触发；1 表示软件触发。


返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

#### `LL_ADC_INJ_SetSequencerLength`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2465)

```c
__STATIC_INLINE void LL_ADC_INJ_SetSequencerLength (ADC_TypeDef * ADCx, uint32_t SequencerNbRanks);
```

设置注入组 1–4 个 Rank 的序列长度。

- `SequencerNbRanks`：注入组 1–4 个 Rank 的编码值。
  - 可用编码：`LL_ADC_INJ_SEQ_SCAN_DISABLE`、`LL_ADC_INJ_SEQ_SCAN_ENABLE_2RANKS`、`LL_ADC_INJ_SEQ_SCAN_ENABLE_3RANKS`、`LL_ADC_INJ_SEQ_SCAN_ENABLE_4RANKS`。

返回：无返回值。

本函数只配置注入组长度；执行顺序为 Rank 1 到 Rank n，通道绑定另用 LL_ADC_INJ_SetSequencerRanks。全局扫描关闭时只执行 Rank 1，SEQ_SCAN_DISABLE 也表示一 Rank。

#### `LL_ADC_INJ_GetSequencerLength`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2492)

```c
__STATIC_INLINE uint32_t LL_ADC_INJ_GetSequencerLength (ADC_TypeDef * ADCx);
```

读取注入组 1–4 个 Rank 的序列长度。


返回：uint32_t，返回编码：`LL_ADC_INJ_SEQ_SCAN_DISABLE`、`LL_ADC_INJ_SEQ_SCAN_ENABLE_2RANKS`、`LL_ADC_INJ_SEQ_SCAN_ENABLE_3RANKS`、`LL_ADC_INJ_SEQ_SCAN_ENABLE_4RANKS`。


返回注入组长度编码，非十进制个数。全局扫描关闭时即使读回较长配置，硬件仍只执行 Rank 1。

#### `LL_ADC_INJ_SetSequencerDiscont`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2510)

```c
__STATIC_INLINE void LL_ADC_INJ_SetSequencerDiscont (ADC_TypeDef * ADCx, uint32_t SeqDiscont);
```

设置注入组逐 Rank 间断转换方式。

- `SeqDiscont`：注入组间断开关；开启时每次固定 1 Rank。
  - 可用编码：`LL_ADC_INJ_SEQ_DISCONT_DISABLE`、`LL_ADC_INJ_SEQ_DISCONT_1RANK`。

返回：无返回值。

注入组间断模式不能与自动注入同时启用；每次触发只推进一个 Rank，不能传规则组的 2–8 Rank 编码。

#### `LL_ADC_INJ_GetSequencerDiscont`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2525)

```c
__STATIC_INLINE uint32_t LL_ADC_INJ_GetSequencerDiscont (ADC_TypeDef * ADCx);
```

读取注入组逐 Rank 间断转换方式。


返回：uint32_t，返回编码：`LL_ADC_INJ_SEQ_DISCONT_DISABLE`、`LL_ADC_INJ_SEQ_DISCONT_1RANK`。

#### `LL_ADC_INJ_SetSequencerRanks`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2574)

```c
__STATIC_INLINE void LL_ADC_INJ_SetSequencerRanks (ADC_TypeDef * ADCx, uint32_t Rank, uint32_t Channel);
```

设置注入组指定 Rank 对应的通道。

- `Rank`：使用注入组 Rank 枚举，且位置不得超过当前 JSQR.JL+1。先设置长度，再配置/查询对应的有效位置。
  - 可用编码：`LL_ADC_INJ_RANK_1`、`LL_ADC_INJ_RANK_2`、`LL_ADC_INJ_RANK_3`、`LL_ADC_INJ_RANK_4`。
- `Channel`：所选通道或 Rank 映射的通道；采用下面列出的同一驱动常量，不能混用 HAL 和 LL 编码。
  - 通道符号见[通道编码](#通道编码)，内部通道还须满足 ADC1 与通路使能条件。

返回：无返回值。

内部通道还须 LL_ADC_SetCommonPathInternalCh 开通通路。注入组长度影响 JSQR 中实际位置，先确定长度再配置 Rank；通道 10–15 编码不等于 C8 存在可接线输入脚。

#### `LL_ADC_INJ_GetSequencerRanks`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2640)

```c
__STATIC_INLINE uint32_t LL_ADC_INJ_GetSequencerRanks (ADC_TypeDef * ADCx, uint32_t Rank);
```

读取注入组指定 Rank 对应的通道。

- `Rank`：使用注入组 Rank 枚举，且位置不得超过当前 JSQR.JL+1。先设置长度，再配置/查询对应的有效位置。
  - 可用编码：`LL_ADC_INJ_RANK_1`、`LL_ADC_INJ_RANK_2`、`LL_ADC_INJ_RANK_3`、`LL_ADC_INJ_RANK_4`。

返回：uint32_t，当前通道配置的 LL 编码。有效测量通道见[通道编码](#通道编码)；读取配置不验证外部接线。


返回编码只含通道定义的部分格式，不能不经转换就传给另一 LL 通道配置函数。用 __LL_ADC_CHANNEL_TO_DECIMAL_NB 得到编号，再选择完整 LL_ADC_CHANNEL_* 常量；与内部通道常量比较时先用 __LL_ADC_CHANNEL_INTERNAL_TO_EXTERNAL 去掉内部标记。

#### `LL_ADC_INJ_SetTrigAuto`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2676)

```c
__STATIC_INLINE void LL_ADC_INJ_SetTrigAuto (ADC_TypeDef * ADCx, uint32_t TrigAuto);
```

设置规则组结束后自动注入或独立注入触发方式。

- `TrigAuto`：独立注入或规则组结束后自动注入。
  - 可用编码：`LL_ADC_INJ_TRIG_INDEPENDENT`、`LL_ADC_INJ_TRIG_FROM_GRP_REGULAR`。

返回：无返回值。

自动注入仅与注入软件触发源相容，之后注入开始/停止由规则组控制，无须再单独触发注入；不得与间断模式同时启用。可利用规则 DR 和四个 JDR 共五个数据寄存器保存一次组合采样的结果。

#### `LL_ADC_INJ_GetTrigAuto`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2690)

```c
__STATIC_INLINE uint32_t LL_ADC_INJ_GetTrigAuto (ADC_TypeDef * ADCx);
```

读取规则组结束后自动注入或独立注入触发方式。


返回：uint32_t，返回编码：`LL_ADC_INJ_TRIG_INDEPENDENT`、`LL_ADC_INJ_TRIG_FROM_GRP_REGULAR`。

#### `LL_ADC_INJ_SetOffset`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2720)

```c
__STATIC_INLINE void LL_ADC_INJ_SetOffset (ADC_TypeDef * ADCx, uint32_t Rank, uint32_t OffsetLevel);
```

设置指定注入 Rank 的 12 位减法偏移量。 偏移不能单独使能/禁用，写 0 即等效关闭减法；F1 固定 12 位，不采用其他分辨率的移位示例。

- `Rank`：注入组 Rank 1–4 的枚举。
  - 可用编码：`LL_ADC_INJ_RANK_1`、`LL_ADC_INJ_RANK_2`、`LL_ADC_INJ_RANK_3`、`LL_ADC_INJ_RANK_4`。
- `OffsetLevel`：注入减法偏移，0–4095。

返回：无返回值。

#### `LL_ADC_INJ_GetOffset`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2747)

```c
__STATIC_INLINE uint32_t LL_ADC_INJ_GetOffset (ADC_TypeDef * ADCx, uint32_t Rank);
```

读取指定注入 Rank 的 12 位减法偏移量。

- `Rank`：注入组 Rank 1–4 的枚举。
  - 可用编码：`LL_ADC_INJ_RANK_1`、`LL_ADC_INJ_RANK_2`、`LL_ADC_INJ_RANK_3`、`LL_ADC_INJ_RANK_4`。

返回：`uint32_t`，具体数值/位域含义见上方功能说明；Get 类不表示操作成功状态。

### 采样时间与模拟看门狗

#### `LL_ADC_SetChannelSamplingTime`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2836)

```c
__STATIC_INLINE void LL_ADC_SetChannelSamplingTime (ADC_TypeDef * ADCx, uint32_t Channel, uint32_t SamplingTime);
```

设置指定通道采样周期，规则组和注入组共享同一通道设置。

- `Channel`：所选通道或 Rank 映射的通道；采用下面列出的同一驱动常量，不能混用 HAL 和 LL 编码。
  - 通道符号见[通道编码](#通道编码)，内部通道还须满足 ADC1 与通路使能条件。
- `SamplingTime`：ADC 采样周期编码；同通道两组共用。
  - 可用编码：`LL_ADC_SAMPLINGTIME_1CYCLE_5`、`LL_ADC_SAMPLINGTIME_7CYCLES_5`、`LL_ADC_SAMPLINGTIME_13CYCLES_5`、`LL_ADC_SAMPLINGTIME_28CYCLES_5`、`LL_ADC_SAMPLINGTIME_41CYCLES_5`、`LL_ADC_SAMPLINGTIME_55CYCLES_5`、`LL_ADC_SAMPLINGTIME_71CYCLES_5`、`LL_ADC_SAMPLINGTIME_239CYCLES_5`。

返回：无返回值。

#### `LL_ADC_GetChannelSamplingTime`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L2909)

```c
__STATIC_INLINE uint32_t LL_ADC_GetChannelSamplingTime (ADC_TypeDef * ADCx, uint32_t Channel);
```

读取指定通道采样周期，规则组和注入组共享同一通道设置。

- `Channel`：所选通道或 Rank 映射的通道；采用下面列出的同一驱动常量，不能混用 HAL 和 LL 编码。
  - 通道符号见[通道编码](#通道编码)，内部通道还须满足 ADC1 与通路使能条件。

返回：uint32_t，返回编码：`LL_ADC_SAMPLINGTIME_1CYCLE_5`、`LL_ADC_SAMPLINGTIME_7CYCLES_5`、`LL_ADC_SAMPLINGTIME_13CYCLES_5`、`LL_ADC_SAMPLINGTIME_28CYCLES_5`、`LL_ADC_SAMPLINGTIME_41CYCLES_5`、`LL_ADC_SAMPLINGTIME_55CYCLES_5`、`LL_ADC_SAMPLINGTIME_71CYCLES_5`、`LL_ADC_SAMPLINGTIME_239CYCLES_5`。

#### `LL_ADC_SetAnalogWDMonitChannels`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3016)

```c
__STATIC_INLINE void LL_ADC_SetAnalogWDMonitChannels (ADC_TypeDef * ADCx, uint32_t AWDChannelGroup);
```

设置模拟看门狗监视的通道和转换组组合。

- `AWDChannelGroup`：看门狗监视的通道及规则/注入组组合。
  - 可用监视组合见[看门狗监视编码](#看门狗监视编码)。

返回：无返回值。


选择非 DISABLE 的监视组合即启用对应监视。若从序列通道编码构造单通道配置，可用 __LL_ADC_ANALOGWD_CHANNEL_GROUP。C8 只有 AWD1，可监视一个或所有通道及规则/注入/两组。

#### `LL_ADC_GetAnalogWDMonitChannels`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3109)

```c
__STATIC_INLINE uint32_t LL_ADC_GetAnalogWDMonitChannels (ADC_TypeDef * ADCx);
```

读取模拟看门狗监视的通道和转换组组合。


返回：uint32_t，当前看门狗监视配置的编码；对应符号见[看门狗监视编码](#看门狗监视编码)。


只有单通道监视模式才可把返回值中的通道部分交给 __LL_ADC_CHANNEL_TO_DECIMAL_NB 解析；原文提醒该通道部分不是完整 LL_ADC_CHANNEL_* 格式，再传入通道配置接口前须重建完整编码。全通道/关闭模式不得这样解析。

#### `LL_ADC_SetAnalogWDThresholds`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3133)

```c
__STATIC_INLINE void LL_ADC_SetAnalogWDThresholds (ADC_TypeDef * ADCx, uint32_t AWDThresholdsHighLow, uint32_t AWDThresholdValue);
```

设置模拟看门狗指定上/下阈值，12 位无符号范围 0–4095。

- `AWDThresholdsHighLow`：选择高阈值或低阈值。
  - 可用编码：`LL_ADC_AWD_THRESHOLD_HIGH`、`LL_ADC_AWD_THRESHOLD_LOW`。
- `AWDThresholdValue`：12 位阈值，0–4095。

返回：无返回值。

#### `LL_ADC_GetAnalogWDThresholds`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3156)

```c
__STATIC_INLINE uint32_t LL_ADC_GetAnalogWDThresholds (ADC_TypeDef * ADCx, uint32_t AWDThresholdsHighLow);
```

读取模拟看门狗指定上/下阈值，12 位无符号范围 0–4095。

- `AWDThresholdsHighLow`：选择高阈值或低阈值。
  - 可用编码：`LL_ADC_AWD_THRESHOLD_HIGH`、`LL_ADC_AWD_THRESHOLD_LOW`。

返回：`uint32_t`，具体数值/位域含义见上方功能说明；Get 类不表示操作成功状态。

### 双 ADC 模式

#### `LL_ADC_SetMultimode`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3194)

```c
__STATIC_INLINE void LL_ADC_SetMultimode (ADC_Common_TypeDef * ADCxy_COMMON, uint32_t Multimode);
```

设置ADC1 主、ADC2 从的双 ADC 工作模式。

- `ADCxy_COMMON`：公共配置入口，见本页[公共实例约定](#公共实例约定)。
- `Multimode`：ADC1/ADC2 独立或双转换模式。
  - 可用编码：`LL_ADC_MULTI_INDEPENDENT`、`LL_ADC_MULTI_DUAL_REG_SIMULT`、`LL_ADC_MULTI_DUAL_REG_INTERL_FAST`、`LL_ADC_MULTI_DUAL_REG_INTERL_SLOW`、`LL_ADC_MULTI_DUAL_INJ_SIMULT`、`LL_ADC_MULTI_DUAL_INJ_ALTERN`、`LL_ADC_MULTI_DUAL_REG_SIM_INJ_SIM`、`LL_ADC_MULTI_DUAL_REG_SIM_INJ_ALT`、`LL_ADC_MULTI_DUAL_REG_INTFAST_INJ_SIM`、`LL_ADC_MULTI_DUAL_REG_INTSLOW_INJ_SIM`。

返回：无返回值。

#### `LL_ADC_GetMultimode`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3220)

```c
__STATIC_INLINE uint32_t LL_ADC_GetMultimode (ADC_Common_TypeDef * ADCxy_COMMON);
```

读取ADC1 主、ADC2 从的双 ADC 工作模式。

- `ADCxy_COMMON`：公共配置入口，见本页[公共实例约定](#公共实例约定)。

返回：uint32_t，返回编码：`LL_ADC_MULTI_INDEPENDENT`、`LL_ADC_MULTI_DUAL_REG_SIMULT`、`LL_ADC_MULTI_DUAL_REG_INTERL_FAST`、`LL_ADC_MULTI_DUAL_REG_INTERL_SLOW`、`LL_ADC_MULTI_DUAL_INJ_SIMULT`、`LL_ADC_MULTI_DUAL_INJ_ALTERN`、`LL_ADC_MULTI_DUAL_REG_SIM_INJ_SIM`、`LL_ADC_MULTI_DUAL_REG_SIM_INJ_ALT`、`LL_ADC_MULTI_DUAL_REG_INTFAST_INJ_SIM`、`LL_ADC_MULTI_DUAL_REG_INTSLOW_INJ_SIM`。

### ADC 使能与校准

#### `LL_ADC_Enable`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3244)

```c
__STATIC_INLINE void LL_ADC_Enable (ADC_TypeDef * ADCx);
```

直接执行 CR2.ADON 置 1。ADON 原为 0 时使 ADC 上电，随后须等待稳定；ADON 已为 1 时，再写 1 且 CR2 其它位未同时改变会启动转换。因此本接口不具有“重复调用仅保持使能”的幂等保证。出处：RM0008 Rev21 pp218、243；固定实现只执行 SET_BIT，没有先判断当前 ADON。


返回：无返回值。

#### `LL_ADC_Disable`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3255)

```c
__STATIC_INLINE void LL_ADC_Disable (ADC_TypeDef * ADCx);
```

关闭 ADC，终止连续转换；也会影响正在进行的注入组。


返回：无返回值。

#### `LL_ADC_IsEnabled`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3266)

```c
__STATIC_INLINE uint32_t LL_ADC_IsEnabled (ADC_TypeDef * ADCx);
```

读取 ADC 使能状态，返回 0 或 1。


返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

#### `LL_ADC_StartCalibration`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3286)

```c
__STATIC_INLINE void LL_ADC_StartCalibration (ADC_TypeDef * ADCx);
```

置位 CAL 启动校准；该内联函数不替代完整的上电、稳定等待和校准完成轮询过程。


返回：无返回值。


UM1850 同时写“校准前禁用”并引用 LL_ADC_DELAY_DISABLE_CALIB_ADC_CYCLES，又写“已上电至少两个 ADC 周期”，两条不能直接作为同一置 CAL 时刻的条件。RM0008 §11.4 要求 ADC 上电至少两个周期后校准；此接口只置 CAL，不负责 ADON、RSTCAL、稳定延时或等待完成。按实际 LL 头文件和 RM 的上电校准流程执行。

#### `LL_ADC_IsCalibrationOnGoing`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3297)

```c
__STATIC_INLINE uint32_t LL_ADC_IsCalibrationOnGoing (ADC_TypeDef * ADCx);
```

查询 CAL 是否仍置位；1 表示校准尚未结束。


返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

### 规则组启动与读数

#### `LL_ADC_REG_StartConversionSWStart`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3326)

```c
__STATIC_INLINE void LL_ADC_REG_StartConversionSWStart (ADC_TypeDef * ADCx);
```

软件启动规则组；须预先选择软件触发源并使能 ADC。


返回：无返回值。

#### `LL_ADC_REG_StartConversionExtTrig`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3345)

```c
__STATIC_INLINE void LL_ADC_REG_StartConversionExtTrig (ADC_TypeDef * ADCx, uint32_t ExternalTriggerEdge);
```

开放规则组外部触发，在下一有效上升沿启动转换。

- `ExternalTriggerEdge`：外部触发边沿，F1 仅上升沿。
  - 可用编码：`LL_ADC_REG_TRIG_EXT_RISING`。

返回：无返回值。

#### `LL_ADC_REG_StopConversionExtTrig`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3363)

```c
__STATIC_INLINE void LL_ADC_REG_StopConversionExtTrig (ADC_TypeDef * ADCx);
```

禁止后续外部触发启动规则组；已开始的转换仍会完成，停止连续转换须关闭 ADC。


返回：无返回值。

#### `LL_ADC_REG_ReadConversionData32`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3377)

```c
__STATIC_INLINE uint32_t LL_ADC_REG_ReadConversionData32 (ADC_TypeDef * ADCx);
```

以 uint32_t 容器返回本 ADC 的规则数据；名字中的 32 不表示得到双 ADC 组合字或 32 位分辨率。F103C8 转换分辨率固定 12 位，数据对齐仍影响数值位置。


返回：`uint32_t`，具体数值/位域含义见上方功能说明；Get 类不表示操作成功状态。

#### `LL_ADC_REG_ReadConversionData12`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3392)

```c
__STATIC_INLINE uint16_t LL_ADC_REG_ReadConversionData12 (ADC_TypeDef * ADCx);
```

取得规则组 12 位转换数据路径的寄存器值；必须结合左/右对齐设置解释。


返回：`uint16_t`，具体数值/位域含义见上方功能说明；Get 类不表示操作成功状态。

#### `LL_ADC_REG_ReadMultiConversionData32`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3419)

```c
__STATIC_INLINE uint32_t LL_ADC_REG_ReadMultiConversionData32 (ADC_TypeDef * ADCx, uint32_t ConversionData);
```

读取双 ADC 主值、从值或主从组合值，ConversionData 指定返回部分。

- `ADCx`：取主 ADC1 寄存器入口，或用 __LL_ADC_COMMON_INSTANCE(ADCx) 得到所属公共入口；不能直接读 ADC2_DR 而期待其中存在主从组合。
- `ConversionData`：选取双 ADC 的主数据、从数据或主从组合字。
  - 可用编码：`LL_ADC_MULTI_MASTER`、`LL_ADC_MULTI_SLAVE`、`LL_ADC_MULTI_MASTER_SLAVE`。

按 UM1850 原接口契约返回：`uint32_t`，MASTER/SLAVE 选择相应 ADC 的数据，MASTER_SLAVE 返回 ADC1 低半字、ADC2 高半字的组合字，原文给定容器范围 0x00000000–0xFFFFFFFF。可用 __LL_ADC_MULTI_CONV_DATA_MASTER_SLAVE 从组合字再取主/从数据；ADCx 应取主 ADC1 公共入口。

**组合数据有效条件：**按 RM0008 §11.9，通过 ADC1_DR 读取主从组合结果时，必须置 ADC1_CR2.DMA=1，即使采用 CPU 轮询读取而未使用 DMA 控制器也一样；否则不能把高 16 位当作有效 ADC2 结果。该位条件与是否启用 DMA1 通道是不同概念。

版本核验：2026-10-10 读取 [ST 官方 LL ADC 头文件固定快照](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h)，REG_ReadConversionData32 实际掩码为 ADC_DR_DATA（低 16 位）；ReadMultiConversionData32 的实现却固定先掩 ADC_DR_ADC2DATA（高 16 位）再按 ConversionData 移位，与上述“主/从/组合”文档契约不一致，会丢失主半字。使用本接口前必须核对工程固定版本的实际实现，不能只因传 MASTER_SLAVE 就保证得到完整组合字。这里保留 UM1850 原契约与所见实现差异，不把新版本源码当作原手册内容，也未修改库文件。

### 注入组启动与读数

#### `LL_ADC_INJ_StartConversionSWStart`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3452)

```c
__STATIC_INLINE void LL_ADC_INJ_StartConversionSWStart (ADC_TypeDef * ADCx);
```

软件启动注入组；须预先选择软件触发源并使能 ADC。


返回：无返回值。

#### `LL_ADC_INJ_StartConversionExtTrig`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3471)

```c
__STATIC_INLINE void LL_ADC_INJ_StartConversionExtTrig (ADC_TypeDef * ADCx, uint32_t ExternalTriggerEdge);
```

开放注入组外部触发，在下一有效上升沿开始转换。

- `ExternalTriggerEdge`：外部触发边沿，F1 仅上升沿。
  - 可用编码：`LL_ADC_INJ_TRIG_EXT_RISING`。

返回：无返回值。

#### `LL_ADC_INJ_StopConversionExtTrig`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3489)

```c
__STATIC_INLINE void LL_ADC_INJ_StopConversionExtTrig (ADC_TypeDef * ADCx);
```

禁止后续外部触发启动注入组；不强制中断已开始的转换。


返回：无返回值。


只关闭未来外部触发；已开始转换会完成。需要中止正在运行的转换或整个连续工作过程时，使用 LL_ADC_Disable，注意同时影响规则组。

#### `LL_ADC_INJ_ReadConversionData32`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3511)

```c
__STATIC_INLINE uint32_t LL_ADC_INJ_ReadConversionData32 (ADC_TypeDef * ADCx, uint32_t Rank);
```

以 32 位读出指定注入 Rank 的 JDR 数据；注意注入偏移后可能为负。

- `Rank`：注入组 Rank 1–4 的枚举。
  - 可用编码：`LL_ADC_INJ_RANK_1`、`LL_ADC_INJ_RANK_2`、`LL_ADC_INJ_RANK_3`、`LL_ADC_INJ_RANK_4`。

返回：`uint32_t`，具体数值/位域含义见上方功能说明；Get 类不表示操作成功状态。

#### `LL_ADC_INJ_ReadConversionData12`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3538)

```c
__STATIC_INLINE uint16_t LL_ADC_INJ_ReadConversionData12 (ADC_TypeDef * ADCx, uint32_t Rank);
```

读取指定注入 Rank 的数据寄存器；按对齐方式和注入偏移进行有符号解释。

- `Rank`：注入组 Rank 1–4 的枚举。
  - 可用编码：`LL_ADC_INJ_RANK_1`、`LL_ADC_INJ_RANK_2`、`LL_ADC_INJ_RANK_3`、`LL_ADC_INJ_RANK_4`。

返回：`uint16_t`，具体数值/位域含义见上方功能说明；Get 类不表示操作成功状态。

### 转换与看门狗状态标志

#### `LL_ADC_IsActiveFlag_EOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3561)

```c
__STATIC_INLINE uint32_t LL_ADC_IsActiveFlag_EOS (ADC_TypeDef * ADCx);
```

查询硬件 EOC 状态；LL 命名 EOS，注入组结束也可置位，不能单独据此认定规则 DR 已更新。


返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

#### `LL_ADC_IsActiveFlag_JEOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3577)

```c
__STATIC_INLINE uint32_t LL_ADC_IsActiveFlag_JEOS (ADC_TypeDef * ADCx);
```

查询注入组结束标志 JEOC。


返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

#### `LL_ADC_IsActiveFlag_AWD1`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3592)

```c
__STATIC_INLINE uint32_t LL_ADC_IsActiveFlag_AWD1 (ADC_TypeDef * ADCx);
```

查询模拟看门狗 AWD 越界标志。


返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

#### `LL_ADC_ClearFlag_EOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3603)

```c
__STATIC_INLINE void LL_ADC_ClearFlag_EOS (ADC_TypeDef * ADCx);
```

按 SR 的写零清除机制清除 EOC。EOC 也可能由注入组结束置位，清除动作本身不区分事件来源。


返回：无返回值。

#### `LL_ADC_ClearFlag_JEOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3619)

```c
__STATIC_INLINE void LL_ADC_ClearFlag_JEOS (ADC_TypeDef * ADCx);
```

清除注入组结束标志 JEOC。


返回：无返回值。

#### `LL_ADC_ClearFlag_AWD1`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3634)

```c
__STATIC_INLINE void LL_ADC_ClearFlag_AWD1 (ADC_TypeDef * ADCx);
```

清除模拟看门狗 AWD 越界标志。


返回：无返回值。

#### `LL_ADC_IsActiveFlag_MST_EOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3647)

```c
__STATIC_INLINE uint32_t LL_ADC_IsActiveFlag_MST_EOS (ADC_Common_TypeDef * ADCxy_COMMON);
```

查询主 ADC1 的 EOC，返回 0 或 1；注入组结束也可能置位。

- `ADCxy_COMMON`：公共配置入口，见本页[公共实例约定](#公共实例约定)。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

#### `LL_ADC_IsActiveFlag_SLV_EOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3663)

```c
__STATIC_INLINE uint32_t LL_ADC_IsActiveFlag_SLV_EOS (ADC_Common_TypeDef * ADCxy_COMMON);
```

查询从 ADC2 的 EOC，返回 0 或 1；注入组结束也可能置位。

- `ADCxy_COMMON`：公共配置入口，见本页[公共实例约定](#公共实例约定)。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

**固定版本差异：**本接口实际由公共 SR 地址加 4 字节读取 ADC1_CR1，未读到 ADC2_SR；本节上方为接口意图，其返回不能用于确认 ADC2 事件。地址推导与对应位号见[LL 实现边界](LL固定实现边界.md#从-adc-状态查询的地址偏移与接口说明不一致)。

#### `LL_ADC_IsActiveFlag_MST_JEOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3683)

```c
__STATIC_INLINE uint32_t LL_ADC_IsActiveFlag_MST_JEOS (ADC_Common_TypeDef * ADCxy_COMMON);
```

查询双模式中主 ADC1的注入组结束标志 JEOC，返回 0 或 1。

- `ADCxy_COMMON`：公共配置入口，见本页[公共实例约定](#公共实例约定)。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

#### `LL_ADC_IsActiveFlag_SLV_JEOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3699)

```c
__STATIC_INLINE uint32_t LL_ADC_IsActiveFlag_SLV_JEOS (ADC_Common_TypeDef * ADCxy_COMMON);
```

查询双模式中从 ADC2的注入组结束标志 JEOC，返回 0 或 1。

- `ADCxy_COMMON`：公共配置入口，见本页[公共实例约定](#公共实例约定)。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

**固定版本差异：**本接口实际由公共 SR 地址加 4 字节读取 ADC1_CR1，未读到 ADC2_SR；本节上方为接口意图，其返回不能用于确认 ADC2 事件。地址推导与对应位号见[LL 实现边界](LL固定实现边界.md#从-adc-状态查询的地址偏移与接口说明不一致)。

#### `LL_ADC_IsActiveFlag_MST_AWD1`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3718)

```c
__STATIC_INLINE uint32_t LL_ADC_IsActiveFlag_MST_AWD1 (ADC_Common_TypeDef * ADCxy_COMMON);
```

查询双模式中主 ADC1的模拟看门狗 AWD 越界标志，返回 0 或 1。

- `ADCxy_COMMON`：公共配置入口，见本页[公共实例约定](#公共实例约定)。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

#### `LL_ADC_IsActiveFlag_SLV_AWD1`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3730)

```c
__STATIC_INLINE uint32_t LL_ADC_IsActiveFlag_SLV_AWD1 (ADC_Common_TypeDef * ADCxy_COMMON);
```

查询双模式中从 ADC2的模拟看门狗 AWD 越界标志，返回 0 或 1。

- `ADCxy_COMMON`：公共配置入口，见本页[公共实例约定](#公共实例约定)。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

**固定版本差异：**本接口实际由公共 SR 地址加 4 字节读取 ADC1_CR1，未读到 ADC2_SR；本节上方为接口意图，其返回不能用于确认 ADC2 事件。地址推导与对应位号见[LL 实现边界](LL固定实现边界.md#从-adc-状态查询的地址偏移与接口说明不一致)。

### 中断使能与查询

#### `LL_ADC_EnableIT_EOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3753)

```c
__STATIC_INLINE void LL_ADC_EnableIT_EOS (ADC_TypeDef * ADCx);
```

使能 CR1.EOCIE，允许 EOC 事件产生中断；EOC 事件来源还包括注入组结束。


返回：无返回值。

#### `LL_ADC_EnableIT_JEOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3769)

```c
__STATIC_INLINE void LL_ADC_EnableIT_JEOS (ADC_TypeDef * ADCx);
```

开放注入组结束标志 JEOC对应中断。


返回：无返回值。

#### `LL_ADC_EnableIT_AWD1`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3784)

```c
__STATIC_INLINE void LL_ADC_EnableIT_AWD1 (ADC_TypeDef * ADCx);
```

开放模拟看门狗 AWD 越界标志对应中断。


返回：无返回值。

#### `LL_ADC_DisableIT_EOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3795)

```c
__STATIC_INLINE void LL_ADC_DisableIT_EOS (ADC_TypeDef * ADCx);
```

禁止规则组结束标志 EOC对应中断。


返回：无返回值。

#### `LL_ADC_DisableIT_JEOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3811)

```c
__STATIC_INLINE void LL_ADC_DisableIT_JEOS (ADC_TypeDef * ADCx);
```

禁止注入组结束标志 JEOC对应中断。


返回：无返回值。

#### `LL_ADC_DisableIT_AWD1`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3826)

```c
__STATIC_INLINE void LL_ADC_DisableIT_AWD1 (ADC_TypeDef * ADCx);
```

禁止模拟看门狗 AWD 越界标志对应中断。


返回：无返回值。

#### `LL_ADC_IsEnabledIT_EOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3838)

```c
__STATIC_INLINE uint32_t LL_ADC_IsEnabledIT_EOS (ADC_TypeDef * ADCx);
```

查询是否使能 CR1.EOCIE，允许 EOC 事件产生中断；EOC 事件来源还包括注入组结束。


返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

#### `LL_ADC_IsEnabledIT_JEOS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3855)

```c
__STATIC_INLINE uint32_t LL_ADC_IsEnabledIT_JEOS (ADC_TypeDef * ADCx);
```

查询是否开放注入组结束标志 JEOC对应中断。


返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

#### `LL_ADC_IsEnabledIT_AWD1`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3871)

```c
__STATIC_INLINE uint32_t LL_ADC_IsEnabledIT_AWD1 (ADC_TypeDef * ADCx);
```

查询是否开放模拟看门狗 AWD 越界标志对应中断。


返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

### 批量初始化与结构默认值

#### `LL_ADC_CommonDeInit`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_adc.c#L279)

```c
ErrorStatus LL_ADC_CommonDeInit (ADC_Common_TypeDef * ADCxy_COMMON);
```

UM1850 p650 描述为公共组内全部 ADC 复位；所核固定实现仅请求 ADC1 的 RCC 复位，不能据此承诺 ADC2 全部寄存器也已复位。具体调用、掩码与影响见[LL 实现边界](LL固定实现边界.md)。

- `ADCxy_COMMON`：公共配置入口，见本页[公共实例约定](#公共实例约定)。

返回：固定实现无条件返回 SUCCESS，没有复位效果验证；UM1850 原文注明 ERROR 不适用。ADC1 的公共双模式控制变化可能影响 ADC2，使用前按两实例的资源所有权停机。

#### `LL_ADC_CommonInit`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_adc.c#L308)

```c
ErrorStatus LL_ADC_CommonInit (ADC_Common_TypeDef * ADCxy_COMMON, LL_ADC_CommonInitTypeDef * ADC_CommonInitStruct);
```

初始化 ADC1/ADC2 公共双模式；要求两实例均已禁用。

- `ADCxy_COMMON`：公共配置入口，见本页[公共实例约定](#公共实例约定)。
- `ADC_CommonInitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：`SUCCESS` 或 `ERROR`；不会替应用配置 RCC、GPIO 或 NVIC。

#### `LL_ADC_CommonStructInit`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_adc.c#L366)

```c
void LL_ADC_CommonStructInit (LL_ADC_CommonInitTypeDef * ADC_CommonInitStruct);
```

把公共配置结构置为默认值，不访问硬件。

- `ADC_CommonInitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：无返回值。

#### `LL_ADC_DeInit`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_adc.c#L388)

```c
ErrorStatus LL_ADC_DeInit (ADC_TypeDef * ADCx);
```

尝试禁用指定 ADC，并在读 ADON=0 后清理寄存器；固定实现即使未进入清理分支也不改写 SUCCESS 返回值。清理分支会清 DUALMOD、将 HTR 设为0xFFF，详见[LL 实现边界](LL固定实现边界.md)。


返回：所核固定实现始终返回 SUCCESS；它不能单独证明寄存器清理完成，不回收应用 DMA/GPIO/NVIC 资源。

#### `LL_ADC_Init`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_adc.c#L555)

```c
ErrorStatus LL_ADC_Init (ADC_TypeDef * ADCx, LL_ADC_InitTypeDef * ADC_InitStruct);
```

初始化整个 ADC 实例的对齐及扫描设置；要求 ADC 禁用，随后仍须配置组、Rank 和采样时间。

- `ADC_InitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：`SUCCESS` 或 `ERROR`；不会替应用配置 RCC、GPIO 或 NVIC。

#### `LL_ADC_StructInit`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_adc.c#L599)

```c
void LL_ADC_StructInit (LL_ADC_InitTypeDef * ADC_InitStruct);
```

把 ADC 实例配置结构置为默认值，不启动硬件。

- `ADC_InitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：无返回值。

#### `LL_ADC_REG_Init`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_adc.c#L645)

```c
ErrorStatus LL_ADC_REG_Init (ADC_TypeDef * ADCx, LL_ADC_REG_InitTypeDef * ADC_REG_InitStruct);
```

初始化规则组触发、序列长度、间断、连续和 DMA 设置；要求 ADC 禁用。

- `ADC_REG_InitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：`SUCCESS` 或 `ERROR`；不会替应用配置 RCC、GPIO 或 NVIC。


尚须 LL_ADC_REG_SetSequencerRanks 逐 Rank 绑定通道和 LL_ADC_SetChannelSamplingTime 配置采样时间；此函数不完成这些步骤。

固定实现会把 SequencerLength 的 SQR1.L 编码额外写入 CR1，可能涉及看门狗使能和保留位；不能只看序列长度最后已写入 SQR1 就忽略前面的副作用。见[LL 初始化写入边界](LL固定实现边界.md)。

#### `LL_ADC_REG_StructInit`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_adc.c#L738)

```c
void LL_ADC_REG_StructInit (LL_ADC_REG_InitTypeDef * ADC_REG_InitStruct);
```

把规则组配置结构置为默认值。

- `ADC_REG_InitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：无返回值。

#### `LL_ADC_INJ_Init`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_adc.c#L784)

```c
ErrorStatus LL_ADC_INJ_Init (ADC_TypeDef * ADCx, LL_ADC_INJ_InitTypeDef * ADC_INJ_InitStruct);
```

初始化注入组触发、序列长度、间断和自动注入设置；要求 ADC 禁用。

- `ADC_INJ_InitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：`SUCCESS` 或 `ERROR`；不会替应用配置 RCC、GPIO 或 NVIC。


尚须 LL_ADC_INJ_SetSequencerRanks 逐 Rank 绑定通道和 LL_ADC_SetChannelSamplingTime 配置采样时间；此函数不完成这些步骤。

#### `LL_ADC_INJ_StructInit`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_adc.c#L865)

```c
void LL_ADC_INJ_StructInit (LL_ADC_INJ_InitTypeDef * ADC_INJ_InitStruct);
```

把注入组配置结构置为默认值。

- `ADC_INJ_InitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：无返回值。

## 导出宏与辅助计算

宏不是带类型检查的普通函数。不要把带自增等副作用的表达式作为参数；读写寄存器仍须满足本章状态和实例限制。

### 通道编码辅助宏

#### `__LL_ADC_CHANNEL_TO_DECIMAL_NB`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1002)

调用形态：`__LL_ADC_CHANNEL_TO_DECIMAL_NB(__CHANNEL__)`。

把 LL 通道编码转换为十进制通道编号；输入 LL_ADC_CHANNEL_*，也接受通道读回接口给出的部分格式，返回编号，不访问硬件。原文举通道 4 返回数字 4；其返回范围写 0–18，但 F1 本章仅列通道 0–17，不能据此使用不存在的通道 18。若输入是位图格式，只能选一个通道位。

#### `__LL_ADC_DECIMAL_NB_TO_CHANNEL`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1039)

调用形态：`__LL_ADC_DECIMAL_NB_TO_CHANNEL(__DECIMAL_NB__)`。

把十进制通道编号转换成 LL 通道编码；例如 4 得到 LL_ADC_CHANNEL_4。本章 F1 编码 0–17；10–15 在 C8 LQFP48 没有外部引脚，内部 16/17 仍须遵守 ADC1 与通路使能限制。

#### `__LL_ADC_IS_CHANNEL_INTERNAL`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1095)

调用形态：`__LL_ADC_IS_CHANNEL_INTERNAL(__CHANNEL__)`。

按驱动字面常量中的内部通道标记判断：外部编码返回 0，LL_ADC_CHANNEL_VREFINT/TEMPSENSOR 等内部编码返回 1。不能传通道寄存器读回的裸编号，因硬件编号本身不能区分驱动的内部标记；例如数字形式 CHANNEL_16 与 TEMPSENSOR 的编码用途不同。

#### `__LL_ADC_CHANNEL_INTERNAL_TO_EXTERNAL`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1154)

调用形态：`__LL_ADC_CHANNEL_INTERNAL_TO_EXTERNAL(__CHANNEL__)`。

去除内部通道编码中的内部标记，取得对应硬件通道编码；不会把芯片内部通路接到外部引脚。

#### `__LL_ADC_IS_CHANNEL_INTERNAL_AVAILABLE`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1179)

调用形态：`__LL_ADC_IS_CHANNEL_INTERNAL_AVAILABLE(__ADC_INSTANCE__, __CHANNEL__)`。

给定 ADC 实例及带内部标记的 LL_ADC_CHANNEL_VREFINT/TEMPSENSOR，支持返回 1，否则 0；C8 仅 ADC1 支持。不能用外部通道常量或寄存器读回的裸编号代替内部常量。

### 看门狗辅助宏

#### `__LL_ADC_ANALOGWD_CHANNEL_GROUP`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1296)

调用形态：`__LL_ADC_ANALOGWD_CHANNEL_GROUP(__CHANNEL__, __GROUP__)`。

把 LL 通道（编码表 0–17、VREFINT/TEMPSENSOR，受封装/实例限制）与 LL_ADC_GROUP_REGULAR、LL_ADC_GROUP_INJECTED 或 LL_ADC_GROUP_REGULAR_INJECTED 组合成看门狗监视编码，供 LL_ADC_SetAnalogWDMonitChannels 使用。原示例误多传 LL_ADC_AWD1，并把 LL_ADC_CHANNEL_4 写成 LL_ADC_CHANNEL4；本章实际 SetAnalogWDMonitChannels 原型只有 ADCx、AWDChannelGroup 两个参数。

#### `__LL_ADC_ANALOGWD_SET_THRESHOLD_RESOLUTION`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1325)

调用形态：`__LL_ADC_ANALOGWD_SET_THRESHOLD_RESOLUTION(__ADC_RESOLUTION__, __AWD_THRESHOLD__)`。

C8 固定实现把阈值实参左移 0 位，不改变数值、不检查范围，并忽略分辨率实参；合法阈值为 0–4095，使用 LL_ADC_RESOLUTION_12B。

#### `__LL_ADC_ANALOGWD_GET_THRESHOLD_RESOLUTION`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1347)

调用形态：`__LL_ADC_ANALOGWD_GET_THRESHOLD_RESOLUTION(__ADC_RESOLUTION__, __AWD_THRESHOLD_12_BITS__)`。

C8 固定实现直接返回阈值实参，不缩放、不检查范围，并忽略分辨率实参；合法阈值仍由调用者保证在 0–4095。

### 双 ADC 与公共实例辅助宏

#### `__LL_ADC_MULTI_CONV_DATA_MASTER_SLAVE`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1364)

调用形态：`__LL_ADC_MULTI_CONV_DATA_MASTER_SLAVE(__ADC_MULTI_MASTER_SLAVE__, __ADC_MULTI_CONV_DATA__)`。

参数为主/从选择与 32 位组合字，返回选定半字数据；原文把组合输入范围写成 0xFFF 是模板错误，DMA 组合字包含两路结果。

#### `__LL_ADC_COMMON_INSTANCE`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1398-L1400)

调用形态：`__LL_ADC_COMMON_INSTANCE(__ADCx__)`。

C8 分支直接展开为 ADC12_COMMON，并不求值或验证实参；ADC1 代表 ADC1/ADC2 的公共控制入口，没有额外独立公共寄存器块。应用仍须只传合法实例，不能把该宏当作实例合法性检查。

#### `__LL_ADC_IS_ENABLED_ALL_COMMON_INSTANCE`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1442-L1445)

调用形态：`__LL_ADC_IS_ENABLED_ALL_COMMON_INSTANCE(__ADCXY_COMMON__)`。

C8 分支读取 ADC1、ADC2 的 ADON 并作按位或：两者均关闭时返回 0，至少一个使能时返回 1。该分支不求值或验证公共入口实参。

### 数据与温度换算宏

#### `__LL_ADC_DIGITAL_SCALE`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1461)

调用形态：`__LL_ADC_DIGITAL_SCALE(__ADC_RESOLUTION__)`。

参数为 LL_ADC_RESOLUTION_12B，返回数字满量程 4095；不是毫伏值。原文 Return value 把它标成 mV，与其数字满量程用途不符。固定实现忽略分辨率实参，直接展开为 0xFFFU；不会检查传入了哪种分辨率符号。

#### `__LL_ADC_CALC_DATA_TO_VOLTAGE`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1477)

调用形态：`__LL_ADC_CALC_DATA_TO_VOLTAGE(__VREFANALOG_VOLTAGE__, __ADC_DATA__, __ADC_RESOLUTION__)`。

参数依次为参考电压 mV、右对齐 ADC 数字值（0–4095）、LL_ADC_RESOLUTION_12B；以非负整数实参调用时，按 floor(Vref×data/4095) 作整数换算，结果单位 mV，丢弃不足 1 mV 的小数。此宏没有固定返回类型或强制把全部实参转成整数；传入浮点实参会改变表达式类型和舍入路径。参考电压必须可靠已知；C8 合法电压范围内的 mV×12 位数据乘积不会超过 uint32_t。不要把左对齐 DR、带符号的注入减偏移结果、双 ADC 组合字或以 µV 表示的参考电压直接传入该接口。

#### `__LL_ADC_CALC_TEMPERATURE_TYP_PARAMS`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1525)

调用形态：`__LL_ADC_CALC_TEMPERATURE_TYP_PARAMS(__TEMPSENSOR_TYP_AVGSLOPE__, __TEMPSENSOR_TYP_CALX_V__, __TEMPSENSOR_CALX_TEMP__, __VREFANALOG_VOLTAGE__, __TEMPSENSOR_ADC_DATA__, __ADC_RESOLUTION__)`。

依次输入典型斜率 µV/°C、典型校准点电压 mV、校准点温度 °C、参考电压 mV、温度通道 ADC 数据、12 位分辨率；返回 °C。采用典型而非逐芯片校准参数，精度受器件散差限制。原文将校准点温度参数单位误写为 mV；正确为 °C。物理换算式为 T=(Vcal_mV−Vref_mV×ADC/4095)×1000/AvgSlope_µV_per_°C+Tcal_°C；核对的 [ST 官方固定快照](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L1525-L1541) 宏在 ADC 数据和参考电压均为整数实参时，先经整数除法把 ADC 电压截断为整数 mV，再换算为 µV 作差并除以斜率；整数结果的除法向零截断。浮点实参会改变中间除法和截断位置，不能把整数路径的误差分析无条件套用。斜率须为正且非零；温差可能为负，改写公式时必须保留有符号算术，并检查传入参数的 C 整数类型不会把负温差提升成无符号数。输入 ADC 数据应为右对齐的 12 位量，参考电压需可靠已知，不能把其它芯片的工厂温度校准宏直接套到 C8。

### 直接寄存器访问宏

#### `LL_ADC_WriteReg`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L951)

调用形态：`LL_ADC_WriteReg(__INSTANCE__, __REG__, __VALUE__)`。

参数为 ADC 实例、寄存器成员名、写入值；直接写寄存器，无返回，不做状态检查。

#### `LL_ADC_ReadReg`

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L959)

调用形态：`LL_ADC_ReadReg(__INSTANCE__, __REG__)`。

参数为 ADC 实例、寄存器成员名；返回寄存器值，读 DR 等寄存器可能产生清标志副作用。

## 常量与枚举编码

传参使用下列符号，具体字段宽度和状态要求见各接口。通道表列出本器件可用于测量的输入；原始字段读回不构成引脚或测量配置有效性的保证。

### 看门狗监视编码

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_ADC_AWD_DISABLE` | 看门狗监视：关闭 |
| `LL_ADC_AWD_ALL_CHANNELS_REG` | 看门狗监视：全通道；REG=规则组，INJ=注入组，REG_INJ=两组 |
| `LL_ADC_AWD_ALL_CHANNELS_INJ` | 看门狗监视：全通道；REG=规则组，INJ=注入组，REG_INJ=两组 |
| `LL_ADC_AWD_ALL_CHANNELS_REG_INJ` | 看门狗监视：全通道；REG=规则组，INJ=注入组，REG_INJ=两组 |
| `LL_ADC_AWD_CHANNEL_0_REG` | ADC 通道 0，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_0_INJ` | ADC 通道 0，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_0_REG_INJ` | ADC 通道 0，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_1_REG` | ADC 通道 1，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_1_INJ` | ADC 通道 1，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_1_REG_INJ` | ADC 通道 1，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_2_REG` | ADC 通道 2，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_2_INJ` | ADC 通道 2，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_2_REG_INJ` | ADC 通道 2，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_3_REG` | ADC 通道 3，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_3_INJ` | ADC 通道 3，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_3_REG_INJ` | ADC 通道 3，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_4_REG` | ADC 通道 4，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_4_INJ` | ADC 通道 4，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_4_REG_INJ` | ADC 通道 4，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_5_REG` | ADC 通道 5，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_5_INJ` | ADC 通道 5，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_5_REG_INJ` | ADC 通道 5，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_6_REG` | ADC 通道 6，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_6_INJ` | ADC 通道 6，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_6_REG_INJ` | ADC 通道 6，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_7_REG` | ADC 通道 7，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_7_INJ` | ADC 通道 7，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_7_REG_INJ` | ADC 通道 7，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_8_REG` | ADC 通道 8，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_8_INJ` | ADC 通道 8，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_8_REG_INJ` | ADC 通道 8，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_9_REG` | ADC 通道 9，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_9_INJ` | ADC 通道 9，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_9_REG_INJ` | ADC 通道 9，C8 外部模拟输入；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_16_REG` | ADC1 通道16连接温度；ADC2通道16接VSS；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_16_INJ` | ADC1 通道16连接温度；ADC2通道16接VSS；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_16_REG_INJ` | ADC1 通道16连接温度；ADC2通道16接VSS；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_17_REG` | ADC1 通道17连接VREFINT；ADC2通道17接VSS；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_17_INJ` | ADC1 通道17连接VREFINT；ADC2通道17接VSS；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CHANNEL_17_REG_INJ` | ADC1 通道17连接VREFINT；ADC2通道17接VSS；监视组由 REG/INJ 后缀确定 |
| `LL_ADC_AWD_CH_VREFINT_REG` | ADC1 内部参考电压看门狗监视组合 |
| `LL_ADC_AWD_CH_VREFINT_INJ` | ADC1 内部参考电压看门狗监视组合 |
| `LL_ADC_AWD_CH_VREFINT_REG_INJ` | ADC1 内部参考电压看门狗监视组合 |
| `LL_ADC_AWD_CH_TEMPSENSOR_REG` | ADC1 内部温度传感器看门狗监视组合 |
| `LL_ADC_AWD_CH_TEMPSENSOR_INJ` | ADC1 内部温度传感器看门狗监视组合 |
| `LL_ADC_AWD_CH_TEMPSENSOR_REG_INJ` | ADC1 内部温度传感器看门狗监视组合 |
| `LL_ADC_AWD1` | 唯一模拟看门狗实例 |
| `LL_ADC_AWD_THRESHOLD_HIGH` | 选择上阈值 |
| `LL_ADC_AWD_THRESHOLD_LOW` | 选择下阈值 |

### 通道编码

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_ADC_CHANNEL_0` | ADC 通道 0，C8 外部模拟输入 |
| `LL_ADC_CHANNEL_1` | ADC 通道 1，C8 外部模拟输入 |
| `LL_ADC_CHANNEL_2` | ADC 通道 2，C8 外部模拟输入 |
| `LL_ADC_CHANNEL_3` | ADC 通道 3，C8 外部模拟输入 |
| `LL_ADC_CHANNEL_4` | ADC 通道 4，C8 外部模拟输入 |
| `LL_ADC_CHANNEL_5` | ADC 通道 5，C8 外部模拟输入 |
| `LL_ADC_CHANNEL_6` | ADC 通道 6，C8 外部模拟输入 |
| `LL_ADC_CHANNEL_7` | ADC 通道 7，C8 外部模拟输入 |
| `LL_ADC_CHANNEL_8` | ADC 通道 8，C8 外部模拟输入 |
| `LL_ADC_CHANNEL_9` | ADC 通道 9，C8 外部模拟输入 |
| `LL_ADC_CHANNEL_16` | ADC1 通道16连接温度；ADC2通道16接VSS |
| `LL_ADC_CHANNEL_17` | ADC1 通道17连接VREFINT；ADC2通道17接VSS |
| `LL_ADC_CHANNEL_VREFINT` | ADC1 内部参考电压通道/通路 |
| `LL_ADC_CHANNEL_TEMPSENSOR` | ADC1 内部温度传感器通道/通路 |

### 采样时间编码

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_ADC_SAMPLINGTIME_1CYCLE_5` | 采样时间 1.5 个 ADC 时钟 |
| `LL_ADC_SAMPLINGTIME_7CYCLES_5` | 采样时间 7.5 个 ADC 时钟 |
| `LL_ADC_SAMPLINGTIME_13CYCLES_5` | 采样时间 13.5 个 ADC 时钟 |
| `LL_ADC_SAMPLINGTIME_28CYCLES_5` | 采样时间 28.5 个 ADC 时钟 |
| `LL_ADC_SAMPLINGTIME_41CYCLES_5` | 采样时间 41.5 个 ADC 时钟 |
| `LL_ADC_SAMPLINGTIME_55CYCLES_5` | 采样时间 55.5 个 ADC 时钟 |
| `LL_ADC_SAMPLINGTIME_71CYCLES_5` | 采样时间 71.5 个 ADC 时钟 |
| `LL_ADC_SAMPLINGTIME_239CYCLES_5` | 采样时间 239.5 个 ADC 时钟 |

### 内部通路与数据对齐

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_ADC_PATH_INTERNAL_NONE` | 关闭内部测量通路 |
| `LL_ADC_PATH_INTERNAL_VREFINT` | ADC1 内部参考电压通道/通路 |
| `LL_ADC_PATH_INTERNAL_TEMPSENSOR` | ADC1 内部温度传感器通道/通路 |
| `LL_ADC_DATA_ALIGN_RIGHT` | 数据右对齐 |
| `LL_ADC_DATA_ALIGN_LEFT` | 数据左对齐 |

### 状态与中断编码

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_ADC_FLAG_STRT` | 规则组启动状态位 |
| `LL_ADC_FLAG_EOS` | 硬件 EOC 状态位（LL 命名 EOS）；规则或注入结束均可能置位 |
| `LL_ADC_FLAG_JSTRT` | 注入组启动状态位 |
| `LL_ADC_FLAG_JEOS` | 注入组完成 JEOC（LL 命名 JEOS）状态位 |
| `LL_ADC_FLAG_AWD1` | 唯一看门狗越界状态位 |
| `LL_ADC_FLAG_EOS_MST` | 主 ADC1 的硬件 EOC 状态；含注入完成来源，须读取正确实例 |
| `LL_ADC_FLAG_EOS_SLV` | 从 ADC2 的硬件 EOC 状态；含注入完成来源，须读取正确实例 |
| `LL_ADC_FLAG_JEOS_MST` | 主 ADC1 的注入组完成 JEOC（LL 命名 JEOS）状态 |
| `LL_ADC_FLAG_JEOS_SLV` | 从 ADC2 的注入组完成 JEOC（LL 命名 JEOS）状态 |
| `LL_ADC_FLAG_AWD1_MST` | 主 ADC1 的唯一看门狗越界状态 |
| `LL_ADC_FLAG_AWD1_SLV` | 从 ADC2 的唯一看门狗越界状态 |
| `LL_ADC_IT_EOS` | 硬件 EOC 的中断使能位；事件范围按 F1 EOC 语义解释 |
| `LL_ADC_IT_JEOS` | 注入组完成 JEOC（LL 命名 JEOS）中断使能位 |
| `LL_ADC_IT_AWD1` | 唯一看门狗越界中断使能位 |

### 组选择与稳定时间

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_ADC_GROUP_REGULAR` | 转换组：规则组 |
| `LL_ADC_GROUP_INJECTED` | 转换组：注入组 |
| `LL_ADC_GROUP_REGULAR_INJECTED` | 转换组：两组 |
| `LL_ADC_DELAY_TEMPSENSOR_STAB_US` | 固定值 10 µs，温度传感器启动等待；不会自动执行延时 |
| `LL_ADC_DELAY_DISABLE_CALIB_ADC_CYCLES` | 固定值 2 个 ADC 周期；保留的旧名称/注释不能用作 ADON=0 时开始校准的依据，见校准说明 |
| `LL_ADC_DELAY_ENABLE_CALIB_ADC_CYCLES` | 固定值 2 个 ADC 周期，从 ADC 上电到校准开始的等待下限；另满足 tSTAB |

### 注入组配置编码

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_ADC_INJ_SEQ_DISCONT_DISABLE` | 间断转换：关闭 |
| `LL_ADC_INJ_SEQ_DISCONT_1RANK` | 间断转换：每次触发 1 个 Rank |
| `LL_ADC_INJ_RANK_1` | 注入组序列位置 1 |
| `LL_ADC_INJ_RANK_2` | 注入组序列位置 2 |
| `LL_ADC_INJ_RANK_3` | 注入组序列位置 3 |
| `LL_ADC_INJ_RANK_4` | 注入组序列位置 4 |
| `LL_ADC_INJ_SEQ_SCAN_DISABLE` | 序列长度为 1 的编码；该常量本身不修改公共 CR1.SCAN |
| `LL_ADC_INJ_SEQ_SCAN_ENABLE_2RANKS` | 序列长度 2 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_INJ_SEQ_SCAN_ENABLE_3RANKS` | 序列长度 3 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_INJ_SEQ_SCAN_ENABLE_4RANKS` | 序列长度 4 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_INJ_TRIG_EXT_RISING` | 仅上升沿触发 |
| `LL_ADC_INJ_TRIG_SOFTWARE` | 软件触发 |
| `LL_ADC_INJ_TRIG_EXT_TIM1_TRGO` | 注入组外部触发：TIM1_TRGO；仅本章保留的 C8 事件源 |
| `LL_ADC_INJ_TRIG_EXT_TIM1_CH4` | 注入组外部触发：TIM1_CH4；仅本章保留的 C8 事件源 |
| `LL_ADC_INJ_TRIG_EXT_TIM2_TRGO` | 注入组外部触发：TIM2_TRGO；仅本章保留的 C8 事件源 |
| `LL_ADC_INJ_TRIG_EXT_TIM2_CH1` | 注入组外部触发：TIM2_CH1；仅本章保留的 C8 事件源 |
| `LL_ADC_INJ_TRIG_EXT_TIM3_CH4` | 注入组外部触发：TIM3_CH4；仅本章保留的 C8 事件源 |
| `LL_ADC_INJ_TRIG_EXT_TIM4_TRGO` | 注入组外部触发：TIM4_TRGO；仅本章保留的 C8 事件源 |
| `LL_ADC_INJ_TRIG_EXT_EXTI_LINE15` | 注入组外部触发：EXTI_LINE15；仅本章保留的 C8 事件源 |
| `LL_ADC_INJ_TRIG_INDEPENDENT` | 注入组独立触发 |
| `LL_ADC_INJ_TRIG_FROM_GRP_REGULAR` | 规则序列完成后自动注入 |

### 双 ADC 配置编码

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_ADC_MULTI_MASTER` | 选择主 ADC1 数据 |
| `LL_ADC_MULTI_SLAVE` | 选择从 ADC2 数据 |
| `LL_ADC_MULTI_MASTER_SLAVE` | 选择主从组合数据 |
| `LL_ADC_MULTI_INDEPENDENT` | 两 ADC 独立工作 |
| `LL_ADC_MULTI_DUAL_REG_SIMULT` | 双 ADC：规则同步 |
| `LL_ADC_MULTI_DUAL_REG_INTERL_FAST` | 双 ADC：规则快速交错 |
| `LL_ADC_MULTI_DUAL_REG_INTERL_SLOW` | 双 ADC：规则慢速交错 |
| `LL_ADC_MULTI_DUAL_INJ_SIMULT` | 双 ADC：注入同步 |
| `LL_ADC_MULTI_DUAL_INJ_ALTERN` | 双 ADC：注入交替 |
| `LL_ADC_MULTI_DUAL_REG_SIM_INJ_SIM` | 双 ADC：规则同步与注入同步 |
| `LL_ADC_MULTI_DUAL_REG_SIM_INJ_ALT` | 双 ADC：规则同步与注入交替 |
| `LL_ADC_MULTI_DUAL_REG_INTFAST_INJ_SIM` | 双 ADC：规则快速交错与注入同步 |
| `LL_ADC_MULTI_DUAL_REG_INTSLOW_INJ_SIM` | 双 ADC：规则慢速交错与注入同步 |

### DMA 数据地址编码

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_ADC_DMA_REG_REGULAR_DATA` | 规则组 DR 地址 |
| `LL_ADC_DMA_REG_REGULAR_DATA_MULTI` | 双 ADC 组合结果地址（ADC1 DR） |

### 规则组配置编码

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_ADC_REG_CONV_SINGLE` | 规则转换单次 |
| `LL_ADC_REG_CONV_CONTINUOUS` | 规则转换连续 |
| `LL_ADC_REG_DMA_TRANSFER_NONE` | 不产生规则 DMA 请求 |
| `LL_ADC_REG_DMA_TRANSFER_UNLIMITED` | 转换持续产生 DMA 请求；DMA 单次/循环另行设置 |
| `LL_ADC_REG_SEQ_DISCONT_DISABLE` | 间断转换：关闭 |
| `LL_ADC_REG_SEQ_DISCONT_1RANK` | 间断转换：每次触发 1 个 Rank |
| `LL_ADC_REG_SEQ_DISCONT_2RANKS` | 间断转换：每次触发 2 个 Rank |
| `LL_ADC_REG_SEQ_DISCONT_3RANKS` | 间断转换：每次触发 3 个 Rank |
| `LL_ADC_REG_SEQ_DISCONT_4RANKS` | 间断转换：每次触发 4 个 Rank |
| `LL_ADC_REG_SEQ_DISCONT_5RANKS` | 间断转换：每次触发 5 个 Rank |
| `LL_ADC_REG_SEQ_DISCONT_6RANKS` | 间断转换：每次触发 6 个 Rank |
| `LL_ADC_REG_SEQ_DISCONT_7RANKS` | 间断转换：每次触发 7 个 Rank |
| `LL_ADC_REG_SEQ_DISCONT_8RANKS` | 间断转换：每次触发 8 个 Rank |
| `LL_ADC_REG_RANK_1` | 规则组序列位置 1 |
| `LL_ADC_REG_RANK_2` | 规则组序列位置 2 |
| `LL_ADC_REG_RANK_3` | 规则组序列位置 3 |
| `LL_ADC_REG_RANK_4` | 规则组序列位置 4 |
| `LL_ADC_REG_RANK_5` | 规则组序列位置 5 |
| `LL_ADC_REG_RANK_6` | 规则组序列位置 6 |
| `LL_ADC_REG_RANK_7` | 规则组序列位置 7 |
| `LL_ADC_REG_RANK_8` | 规则组序列位置 8 |
| `LL_ADC_REG_RANK_9` | 规则组序列位置 9 |
| `LL_ADC_REG_RANK_10` | 规则组序列位置 10 |
| `LL_ADC_REG_RANK_11` | 规则组序列位置 11 |
| `LL_ADC_REG_RANK_12` | 规则组序列位置 12 |
| `LL_ADC_REG_RANK_13` | 规则组序列位置 13 |
| `LL_ADC_REG_RANK_14` | 规则组序列位置 14 |
| `LL_ADC_REG_RANK_15` | 规则组序列位置 15 |
| `LL_ADC_REG_RANK_16` | 规则组序列位置 16 |
| `LL_ADC_REG_SEQ_SCAN_DISABLE` | 序列长度为 1 的编码；该常量本身不修改公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_2RANKS` | 序列长度 2 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_3RANKS` | 序列长度 3 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_4RANKS` | 序列长度 4 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_5RANKS` | 序列长度 5 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_6RANKS` | 序列长度 6 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_7RANKS` | 序列长度 7 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_8RANKS` | 序列长度 8 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_9RANKS` | 序列长度 9 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_10RANKS` | 序列长度 10 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_11RANKS` | 序列长度 11 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_12RANKS` | 序列长度 12 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_13RANKS` | 序列长度 13 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_14RANKS` | 序列长度 14 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_15RANKS` | 序列长度 15 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_SEQ_SCAN_ENABLE_16RANKS` | 序列长度 16 的字段编码；须另使能公共 CR1.SCAN |
| `LL_ADC_REG_TRIG_EXT_RISING` | 仅上升沿触发 |
| `LL_ADC_REG_TRIG_SOFTWARE` | 软件触发 |
| `LL_ADC_REG_TRIG_EXT_TIM1_CH3` | 规则组外部触发：TIM1_CH3；仅本章保留的 C8 事件源 |
| `LL_ADC_REG_TRIG_EXT_TIM1_CH1` | 规则组外部触发：TIM1_CH1；仅本章保留的 C8 事件源 |
| `LL_ADC_REG_TRIG_EXT_TIM1_CH2` | 规则组外部触发：TIM1_CH2；仅本章保留的 C8 事件源 |
| `LL_ADC_REG_TRIG_EXT_TIM2_CH2` | 规则组外部触发：TIM2_CH2；仅本章保留的 C8 事件源 |
| `LL_ADC_REG_TRIG_EXT_TIM3_TRGO` | 规则组外部触发：TIM3_TRGO；仅本章保留的 C8 事件源 |
| `LL_ADC_REG_TRIG_EXT_TIM4_CH4` | 规则组外部触发：TIM4_CH4；仅本章保留的 C8 事件源 |
| `LL_ADC_REG_TRIG_EXT_EXTI_LINE11` | 规则组外部触发：EXTI_LINE11；仅本章保留的 C8 事件源 |

### 分辨率与扫描编码

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_ADC_RESOLUTION_12B` | F1 固定 12 位分辨率 |
| `LL_ADC_SEQ_SCAN_DISABLE` | 序列扫描：关闭（单 Rank） |
| `LL_ADC_SEQ_SCAN_ENABLE` | 序列扫描：开启 |

## 与相邻章节配合

HAL 与 ADCEx 接口见[HAL 接口参考](HAL接口.md)，本页为 LL 参考。同一实例混用 HAL 与 LL 时，直接寄存器写入不会自动同步 HAL 句柄状态；应明确资源所有权和停止/重配边界。
