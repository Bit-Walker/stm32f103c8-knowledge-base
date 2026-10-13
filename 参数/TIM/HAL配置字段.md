# TIM HAL 配置结构

适用STM32F103C8T6，固定来源整合。字段表由既有资料迁移，基础HAL字段参考固定de129f1头文件；Hall结构的四个uint32_t字段已逐项核对保留的[UM1850 Rev3 §37.1.1 p532原文](https://www.st.com/resource/en/user_manual/um1850-description-of-stm32f1-hal-and-lowlayer-drivers-stmicroelectronics.pdf#page=532)，并与固定实现访问字段交叉核对；此处不宣称已核对TIMEx头文件。参数及返回状态边界另见[HAL初始化](HAL初始化边界.md)和[扩展接口](HAL扩展接口.md)。


### `TIM_Base_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t Prescaler` | TIM 16 位 PSC，0–65535；实际计数时钟除以 PSC+1。PSC 有缓冲，更新事件后新值生效。 |
| `uint32_t CounterMode` | 向上、向下、中心对齐 1/2/3；中心与边沿对齐互换应先复位定时器，避免 DIR 只读语义导致异常方向。 |
| `uint32_t Period` | 自动重装 ARR，C8 的 TIM1–4 均为 16 位，0–65535；ARR=0 阻止正常计数。更新时机受 ARR 预装载控制。 |
| `uint32_t ClockDivision` | CKD 分频 DIV1/DIV2/DIV4，用于数字滤波和死区采样基准；不直接替代 PSC。 |
| `uint32_t RepetitionCounter` | TIM1 的 RCR，0–255；更新允许且排除软件UG/从模式额外事件时，周期性更新每RCR+1个边沿对齐周期或中心对齐半周期产生一次；TIM2–4 不具备此功能。 |
| `uint32_t AutoReloadPreload` | ARR 预装载开关；启用后 ARR 写入缓冲，在更新事件装入有效寄存器。 |

### `TIM_OC_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t OCMode` | 输出比较模式：冻结、匹配置有效/无效、翻转、强制有效/无效、PWM1/PWM2；选择与通道用途一致的模式。 |
| `uint32_t Pulse` | 写入 CCR 的比较值，C8 为 0–65535；PWM 的占空效果还取决于 ARR、计数模式和极性。 |
| `uint32_t OCPolarity` | 主输出有效极性，高或低。 |
| `uint32_t OCNPolarity` | 互补输出有效极性，仅 TIM1 的 CH1N–CH3N。 |
| `uint32_t OCFastMode` | PWM1/PWM2 快速模式开关，用于减少触发到输出响应的延迟。 |
| `uint32_t OCIdleState` | TIM1 主输出空闲电平，SET 或 RESET；配合 MOE、OSSI 和刹车设置解释。 |
| `uint32_t OCNIdleState` | TIM1 互补输出空闲电平，SET 或 RESET；仅支持互补的 CH1–CH3。 |

### `TIM_OnePulse_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t OCMode` | 输出比较模式：冻结、匹配置有效/无效、翻转、强制有效/无效、PWM1/PWM2；选择与通道用途一致的模式。 |
| `uint32_t Pulse` | 写入 CCR 的比较值，C8 为 0–65535；PWM 的占空效果还取决于 ARR、计数模式和极性。 |
| `uint32_t OCPolarity` | 主输出有效极性，高或低。 |
| `uint32_t OCNPolarity` | 互补输出有效极性，仅 TIM1 的 CH1N–CH3N。 |
| `uint32_t OCIdleState` | TIM1 主输出空闲电平，SET 或 RESET；配合 MOE、OSSI 和刹车设置解释。 |
| `uint32_t OCNIdleState` | TIM1 互补输出空闲电平，SET 或 RESET；仅支持互补的 CH1–CH3。 |
| `uint32_t ICPolarity` | 输入捕获有效边沿/极性；C8 使用 RISING 或 FALLING。编码器路径需按相位方向选择极性，不能将双边沿选项当成普遍可用。 |
| `uint32_t ICSelection` | 输入映射：直接 TI、间接 TI 或 TRC；需结合通道配对和从模式触发路径选择。 |
| `uint32_t ICFilter` | 输入数字滤波编码，HAL 为 0–15；LL 采用 FDIV 和 N 命名常量。滤波增加识别延迟，N 为连续一致采样数。 |

### `TIM_IC_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t ICPolarity` | 输入捕获有效边沿/极性；C8 使用 RISING 或 FALLING。编码器路径需按相位方向选择极性，不能将双边沿选项当成普遍可用。 |
| `uint32_t ICSelection` | 输入映射：直接 TI、间接 TI 或 TRC；需结合通道配对和从模式触发路径选择。 |
| `uint32_t ICPrescaler` | 输入捕获事件分频 DIV1/DIV2/DIV4/DIV8；与基本时基 PSC 不同。 |
| `uint32_t ICFilter` | 输入数字滤波编码，HAL 为 0–15；LL 采用 FDIV 和 N 命名常量。滤波增加识别延迟，N 为连续一致采样数。 |

### `TIM_Encoder_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t EncoderMode` | 编码器x2/x4模式；必须按实际写入的SMS位解释，TI1/TI2库符号名与原文边沿描述存在冲突，见[编码器符号冲突](LL辅助宏.md#编码器-x2-模式的文档符号冲突)。 |
| `uint32_t IC1Polarity` | 输入捕获有效边沿/极性；C8 使用 RISING 或 FALLING。编码器路径需按相位方向选择极性，不能将双边沿选项当成普遍可用。 |
| `uint32_t IC1Selection` | 输入映射：直接 TI、间接 TI 或 TRC；需结合通道配对和从模式触发路径选择。 |
| `uint32_t IC1Prescaler` | 输入捕获事件分频 DIV1/DIV2/DIV4/DIV8；与基本时基 PSC 不同。 |
| `uint32_t IC1Filter` | 输入数字滤波编码，HAL 为 0–15；LL 采用 FDIV 和 N 命名常量。滤波增加识别延迟，N 为连续一致采样数。 |
| `uint32_t IC2Polarity` | 输入捕获有效边沿/极性；C8 使用 RISING 或 FALLING。编码器路径需按相位方向选择极性，不能将双边沿选项当成普遍可用。 |
| `uint32_t IC2Selection` | 输入映射：直接 TI、间接 TI 或 TRC；需结合通道配对和从模式触发路径选择。 |
| `uint32_t IC2Prescaler` | 输入捕获事件分频 DIV1/DIV2/DIV4/DIV8；与基本时基 PSC 不同。 |
| `uint32_t IC2Filter` | 输入数字滤波编码，HAL 为 0–15；LL 采用 FDIV 和 N 命名常量。滤波增加识别延迟，N 为连续一致采样数。 |

### `TIM_ClockConfigTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t ClockSource` | 内部时钟、ETR 外部模式 1/2、TI 输入或 ITR；依所选路径配置极性、预分频和滤波。 |
| `uint32_t ClockPolarity` | 所选外部时钟、触发或清除输入的极性；TI 边沿与 ETR 反相选项按路径使用。 |
| `uint32_t ClockPrescaler` | 外部输入预分频 DIV1/DIV2/DIV4/DIV8；只对相应 ETR 路径有效。 |
| `uint32_t ClockFilter` | 所选输入数字滤波，HAL 编码 0–15，含义与 RM0008 的滤波表一致。 |

### `TIM_ClearInputConfigTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t ClearInputState` | 使能或关闭 OCREF 外部清除。 |
| `uint32_t ClearInputSource` | 清除源为 ETR 或 NONE；不能作为普通 GPIO 软件清零功能使用。 |
| `uint32_t ClearInputPolarity` | 所选外部时钟、触发或清除输入的极性；TI 边沿与 ETR 反相选项按路径使用。 |
| `uint32_t ClearInputPrescaler` | OCREF 清除使用 ETR 时必须为 0，即 TIM_CLEARINPUTPRESCALER_DIV1，禁止 ETR 预分频；不能使用此枚举族的 DIV2/4/8。 |
| `uint32_t ClearInputFilter` | 所选输入数字滤波，HAL 编码 0–15，含义与 RM0008 的滤波表一致。 |

### `TIM_MasterConfigTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t MasterOutputTrigger` | TRGO 来源：复位、使能、更新、比较脉冲或 OC1REF–OC4REF。 |
| `uint32_t MasterSlaveMode` | MSM 主从同步开关；使能后延迟 TRGI 事件的作用，以便本定时器与经 TRGO 连接的从定时器同步。定时器同步并非一律必须使能 MSM。 |

### `TIM_SlaveConfigTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t SlaveMode` | 从模式关闭、复位、门控、触发或外部时钟模式 1。 |
| `uint32_t InputTrigger` | TRGI 来源 ITR0–ITR3、TI1 边沿检测、TI1FP1、TI2FP2 或 ETRF；ITR 编号对应的源定时器必须查互联表。 |
| `uint32_t TriggerPolarity` | 所选外部时钟、触发或清除输入的极性；TI 边沿与 ETR 反相选项按路径使用。 |
| `uint32_t TriggerPrescaler` | 外部输入预分频 DIV1/DIV2/DIV4/DIV8；只对相应 ETR 路径有效。 |
| `uint32_t TriggerFilter` | 所选输入数字滤波，HAL 编码 0–15，含义与 RM0008 的滤波表一致。 |

### `TIM_BreakDeadTimeConfigTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t OffStateRunMode` | TIM1 运行状态下的关闭态选择 OSSR；LOCK≥2 后不能更改。 |
| `uint32_t OffStateIDLEMode` | TIM1 空闲状态下的关闭态选择 OSSI；LOCK≥2 后不能更改。 |
| `uint32_t LockLevel` | TIM1 LOCK OFF/1/2/3；BDTR首次写入后LOCK字段冻结至外设复位；首次写入时应完成等级及受保护字段配置。 |
| `uint32_t DeadTime` | TIM1 DTG 死区编码 0–255，非线性编码；不是直接的纳秒数。LOCK≥1 保护该字段。 |
| `uint32_t BreakState` | TIM1 刹车输入使能；LOCK≥1 后受保护。 |
| `uint32_t BreakPolarity` | TIM1 BKIN 有效电平高/低；LOCK≥1 后受保护。 |
| `uint32_t AutomaticOutput` | TIM1 AOE 自动输出恢复；刹车无效时允许在更新事件置 MOE，不要求此前发生过刹车。LOCK≥1 后受保护。 |

### `TIM_HandleTypeDef`

下表列出固定旧版的六个无条件字段；启用动态注册后的27个函数指针字段及回调ID映射见[回调登记表](HAL生命周期与DMA.md#回调-id句柄字段与默认函数)。

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `TIM_TypeDef* Instance` | TIM 寄存器基地址，C8 为 TIM1–TIM4；按所选实例确认高级输出等能力。 |
| `TIM_Base_InitTypeDef Init` | TIM_Base_InitTypeDef 基本时基初始化参数。 |
| `HAL_TIM_ActiveChannel Channel` | 当前活动回调通道 HAL_TIM_ActiveChannel；不等同于 TIM_CHANNEL_x 配置参数，驱动在回调分发时维护。 |
| `DMA_HandleTypeDef* hdma[7]` | TIM 的 7 个 DMA 句柄指针数组，按 UPDATE、CC1–CC4、COMMUTATION、TRIGGER 索引关联。 |
| `HAL_LockTypeDef Lock` | HAL 软件锁对象；驱动维护，不能替代 RTOS 互斥锁。 |
| `__IO HAL_TIM_StateTypeDef State` | HAL_TIM_StateTypeDef 软件状态枚举，由驱动维护。 |


### `TIM_HallSensor_InitTypeDef`

| 字段类型与名称 | 中文含义与约束 |
|---|---|
| `uint32_t IC1Polarity` | 输入捕获有效边沿/极性；C8 使用 RISING 或 FALLING。编码器路径需按相位方向选择极性，不能将双边沿选项当成普遍可用。 |
| `uint32_t IC1Prescaler` | 输入捕获事件分频 DIV1/DIV2/DIV4/DIV8；与基本时基 PSC 不同。 |
| `uint32_t IC1Filter` | 输入数字滤波编码，HAL 为 0–15；LL 采用 FDIV 和 N 命名常量。滤波增加识别延迟，N 为连续一致采样数。 |
| `uint32_t Commutation_Delay` | 霍尔输入变化后产生 TRGO 换相事件的延迟比较值，写 CCR2，0–65535。 |


[返回定时器主题](../../知识库/06_定时器PWM与同步.md) · [图形关系与来源](图形关系与来源.md)
