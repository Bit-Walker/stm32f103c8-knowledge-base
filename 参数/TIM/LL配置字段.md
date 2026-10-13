# TIM LL 配置结构

适用STM32F103C8T6的固定de129f1驱动，固定来源整合。六个结构的原有字段表保留，实际初始化动作、返回路径、StructInit默认值及Hall状态依赖见[初始化约束](LL初始化边界.md)。结构值的合法范围不代表函数会对任意输入自动限幅。


### `LL_TIM_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint16_t Prescaler` | TIM 16 位 PSC，0–65535；实际计数时钟除以 PSC+1。PSC 有缓冲，更新事件后新值生效。 |
| `uint32_t CounterMode` | 向上、向下、中心对齐 1/2/3；中心与边沿对齐互换应先复位定时器，避免 DIR 只读语义导致异常方向。 |
| `uint32_t Autoreload` | 自动重装 ARR，C8 的 TIM1–4 均为 16 位，0–65535；ARR=0 阻止正常计数。更新时机受 ARR 预装载控制。 |
| `uint32_t ClockDivision` | CKD 分频 DIV1/DIV2/DIV4，用于数字滤波和死区采样基准；不直接替代 PSC。 |
| `uint8_t RepetitionCounter` | TIM1 的 RCR，0–255；更新允许且排除软件UG/从模式额外事件时，周期性更新每RCR+1个边沿对齐周期或中心对齐半周期产生一次；TIM2–4 不具备此功能。 |

### `LL_TIM_OC_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t OCMode` | 输出比较模式：冻结、匹配置有效/无效、翻转、强制有效/无效、PWM1/PWM2；选择与通道用途一致的模式。 |
| `uint32_t OCState` | 主输出通道使能状态，LL_TIM_OCSTATE_ENABLE 或 DISABLE。 |
| `uint32_t OCNState` | 互补输出通道使能状态，仅 TIM1 CH1N–CH3N。 |
| `uint32_t CompareValue` | 写入 CCR 的比较值，C8 为 0–65535；PWM 的占空效果还取决于 ARR、计数模式和极性。 |
| `uint32_t OCPolarity` | 主输出有效极性，高或低。 |
| `uint32_t OCNPolarity` | 互补输出有效极性，仅 TIM1 的 CH1N–CH3N。 |
| `uint32_t OCIdleState` | TIM1主输出空闲电平，LL_TIM_OCIDLESTATE_HIGH或LL_TIM_OCIDLESTATE_LOW；配合 MOE、OSSI 和刹车设置解释。 |
| `uint32_t OCNIdleState` | TIM1互补输出空闲电平，LL_TIM_OCIDLESTATE_HIGH或LL_TIM_OCIDLESTATE_LOW；仅支持互补的 CH1–CH3。 |

### `LL_TIM_IC_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t ICPolarity` | 输入捕获有效边沿/极性；C8 使用 RISING 或 FALLING。编码器路径需按相位方向选择极性，不能将双边沿选项当成普遍可用。 |
| `uint32_t ICActiveInput` | 输入映射：直接 TI、间接 TI 或 TRC；需结合通道配对和从模式触发路径选择。 |
| `uint32_t ICPrescaler` | 输入捕获事件分频 DIV1/DIV2/DIV4/DIV8；与基本时基 PSC 不同。 |
| `uint32_t ICFilter` | 输入数字滤波编码，HAL 为 0–15；LL 采用 FDIV 和 N 命名常量。滤波增加识别延迟，N 为连续一致采样数。 |

### `LL_TIM_ENCODER_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t EncoderMode` | 编码器x2/x4模式；必须按实际写入的SMS位解释，TI1/TI2库符号名与原文边沿描述存在冲突，见[编码器符号冲突](LL辅助宏.md#编码器-x2-模式的文档符号冲突)。 |
| `uint32_t IC1Polarity` | 输入捕获有效边沿/极性；C8 使用 RISING 或 FALLING。编码器路径需按相位方向选择极性，不能将双边沿选项当成普遍可用。 |
| `uint32_t IC1ActiveInput` | 输入映射：直接 TI、间接 TI 或 TRC；需结合通道配对和从模式触发路径选择。 |
| `uint32_t IC1Prescaler` | 输入捕获事件分频 DIV1/DIV2/DIV4/DIV8；与基本时基 PSC 不同。 |
| `uint32_t IC1Filter` | 输入数字滤波编码，HAL 为 0–15；LL 采用 FDIV 和 N 命名常量。滤波增加识别延迟，N 为连续一致采样数。 |
| `uint32_t IC2Polarity` | 输入捕获有效边沿/极性；C8 使用 RISING 或 FALLING。编码器路径需按相位方向选择极性，不能将双边沿选项当成普遍可用。 |
| `uint32_t IC2ActiveInput` | 输入映射：直接 TI、间接 TI 或 TRC；需结合通道配对和从模式触发路径选择。 |
| `uint32_t IC2Prescaler` | 输入捕获事件分频 DIV1/DIV2/DIV4/DIV8；与基本时基 PSC 不同。 |
| `uint32_t IC2Filter` | 输入数字滤波编码，HAL 为 0–15；LL 采用 FDIV 和 N 命名常量。滤波增加识别延迟，N 为连续一致采样数。 |

### `LL_TIM_HALLSENSOR_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t IC1Polarity` | 输入捕获有效边沿/极性；C8 使用 RISING 或 FALLING。编码器路径需按相位方向选择极性，不能将双边沿选项当成普遍可用。 |
| `uint32_t IC1Prescaler` | 输入捕获事件分频 DIV1/DIV2/DIV4/DIV8；与基本时基 PSC 不同。 |
| `uint32_t IC1Filter` | 输入数字滤波编码，HAL 为 0–15；LL 采用 FDIV 和 N 命名常量。滤波增加识别延迟，N 为连续一致采样数。 |
| `uint32_t CommutationDelay` | 霍尔输入变化后产生 TRGO 换相事件的延迟比较值，写 CCR2，0–65535。 |

### `LL_TIM_BDTR_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t OSSRState` | TIM1 运行状态下的关闭态选择 OSSR；LOCK≥2 后不能更改。 |
| `uint32_t OSSIState` | TIM1 空闲状态下的关闭态选择 OSSI；LOCK≥2 后不能更改。 |
| `uint32_t LockLevel` | TIM1 LOCK OFF/1/2/3；BDTR首次写入后LOCK字段冻结，直至外设复位；应在首次写入时完成所需等级及受保护字段配置。 |
| `uint8_t DeadTime` | TIM1 DTG 死区编码 0–255，非线性编码；不是直接的纳秒数。LOCK≥1 保护该字段。 |
| `uint16_t BreakState` | TIM1 刹车输入使能；LOCK≥1 后受保护。 |
| `uint32_t BreakPolarity` | TIM1 BKIN 有效电平高/低；LOCK≥1 后受保护。 |
| `uint32_t AutomaticOutput` | TIM1 AOE 自动输出恢复；刹车无效时允许在更新事件置 MOE，不要求此前发生过刹车。LOCK≥1 后受保护。 |


来源：[固定LL TIM头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h)。

[返回定时器主题](../../知识库/06_定时器PWM与同步.md) · [图形关系与来源](图形关系与来源.md)
