# TIM HAL 符号与适用限制

适用STM32F103C8T6，固定来源整合。以固定de129f1头文件核对符号存在性；运行模式、合法组合及字段效果须按接口与手册分别核查。BOTHEDGE、TI1F_ED与通道路由的区别见[HAL宏边界](HAL辅助宏.md)。


下表保留原文符号名，不臆造手册未给出的数值编码；传参使用符号而非自行猜测数值。寄存器字段宽度与合法取值在结构和函数表中说明。

| 符号 | 中文含义与适用限制 |
|---|---|
| `TIM_AUTOMATICOUTPUT_DISABLE` | TIM1 自动恢复 MOE：关闭 |
| `TIM_AUTOMATICOUTPUT_ENABLE` | TIM1 自动恢复 MOE：开启 |
| `TIM_AUTORELOAD_PRELOAD_DISABLE` | ARR 预装载：关闭 |
| `TIM_AUTORELOAD_PRELOAD_ENABLE` | ARR 预装载：开启 |
| `TIM_BREAK_ENABLE` | TIM1 刹车：开启 |
| `TIM_BREAK_DISABLE` | TIM1 刹车：关闭 |
| `TIM_BREAKPOLARITY_LOW` | BKIN 有效极性：低有效/低电平 |
| `TIM_BREAKPOLARITY_HIGH` | BKIN 有效极性：高有效/高电平 |
| `TIM_CHANNEL_1` | 选择通道1；只接受该接口支持的通道，CH4无互补N路 |
| `TIM_CHANNEL_2` | 选择通道2；只接受该接口支持的通道，CH4无互补N路 |
| `TIM_CHANNEL_3` | 选择通道3；只接受该接口支持的通道，CH4无互补N路 |
| `TIM_CHANNEL_4` | 选择通道4；只接受该接口支持的通道，CH4无互补N路 |
| `TIM_CHANNEL_ALL` | 仅在明确接受ALL的API中使用；不能传给任意单通道接口或宏来表示全通道 |
| `TIM_CLEARINPUTPOLARITY_INVERTED` | OCREF 清除输入极性：反相 |
| `TIM_CLEARINPUTPOLARITY_NONINVERTED` | OCREF 清除输入极性：不反相 |
| `TIM_CLEARINPUTPRESCALER_DIV1` | OCREF 清除输入预分频：除以 1 |
| `TIM_CLEARINPUTPRESCALER_DIV2` | 原文枚举保留：除以 2；使用 ETR 的 OCREF 清除时不允许选择，须 DIV1 |
| `TIM_CLEARINPUTPRESCALER_DIV4` | 原文枚举保留：除以 4；使用 ETR 的 OCREF 清除时不允许选择，须 DIV1 |
| `TIM_CLEARINPUTPRESCALER_DIV8` | 原文枚举保留：除以 8；使用 ETR 的 OCREF 清除时不允许选择，须 DIV1 |
| `TIM_CLEARINPUTSOURCE_NONE` | OCREF 清除输入源：不选择/关闭 |
| `TIM_CLEARINPUTSOURCE_ETR` | OCREF 清除输入源：滤波后的外部 ETR 输入 |
| `TIM_CLOCKDIVISION_DIV1` | CKD 滤波/死区时钟分频：除以 1 |
| `TIM_CLOCKDIVISION_DIV2` | CKD 滤波/死区时钟分频：除以 2 |
| `TIM_CLOCKDIVISION_DIV4` | CKD 滤波/死区时钟分频：除以 4 |
| `TIM_CLOCKPOLARITY_INVERTED` | 外部计数时钟极性：反相 |
| `TIM_CLOCKPOLARITY_NONINVERTED` | 外部计数时钟极性：不反相 |
| `TIM_CLOCKPOLARITY_RISING` | 外部计数时钟极性：上升沿 |
| `TIM_CLOCKPOLARITY_FALLING` | 外部计数时钟极性：下降沿 |
| `TIM_CLOCKPOLARITY_BOTHEDGE` | 库极性编码；本符号本身不选择TI1F_ED路由。C8按具体输入路径与硬件极性限制核对，不能作普通双边沿捕获保证 |
| `TIM_CLOCKPRESCALER_DIV1` | 外部计数时钟预分频：除以 1 |
| `TIM_CLOCKPRESCALER_DIV2` | 外部计数时钟预分频：除以 2 |
| `TIM_CLOCKPRESCALER_DIV4` | 外部计数时钟预分频：除以 4 |
| `TIM_CLOCKPRESCALER_DIV8` | 外部计数时钟预分频：除以 8 |
| `TIM_CLOCKSOURCE_ETRMODE2` | 计数时钟源：ETR 外部时钟模式 2 |
| `TIM_CLOCKSOURCE_INTERNAL` | 计数时钟源：内部时钟 |
| `TIM_CLOCKSOURCE_ITR0` | 计数时钟源：内部触发 0，核对互联表 |
| `TIM_CLOCKSOURCE_ITR1` | 计数时钟源：内部触发 1，核对互联表 |
| `TIM_CLOCKSOURCE_ITR2` | 计数时钟源：内部触发 2，核对互联表 |
| `TIM_CLOCKSOURCE_ITR3` | 计数时钟源：内部触发 3，核对互联表 |
| `TIM_CLOCKSOURCE_TI1ED` | 计数时钟源：TI1 双边沿检测 |
| `TIM_CLOCKSOURCE_TI1` | 计数时钟源：TI1 过滤/极性选择后的输入边沿；外部时钟模式1，不能套用编码器x2/x4倍率 |
| `TIM_CLOCKSOURCE_TI2` | 计数时钟源：TI2 过滤/极性选择后的输入边沿；外部时钟模式1，不能套用编码器x2/x4倍率 |
| `TIM_CLOCKSOURCE_ETRMODE1` | 计数时钟源：ETR 外部时钟模式 1 |
| `TIM_COMMUTATION_TRGI` | TIM1 换相来源：触发输入 |
| `TIM_COMMUTATION_SOFTWARE` | TIM1 换相来源：软件事件 |
| `TIM_COUNTERMODE_UP` | 计数模式：向上 |
| `TIM_COUNTERMODE_DOWN` | 计数模式：向下 |
| `TIM_COUNTERMODE_CENTERALIGNED1` | 计数模式：中心对齐 1（比较中断对应向下） |
| `TIM_COUNTERMODE_CENTERALIGNED2` | 计数模式：中心对齐 2（比较中断对应向上） |
| `TIM_COUNTERMODE_CENTERALIGNED3` | 计数模式：中心对齐 3（比较中断对应双向） |
| `TIM_DMABASE_CR1` | DMA 突发起始寄存器 CR1；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_CR2` | DMA 突发起始寄存器 CR2；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_SMCR` | DMA 突发起始寄存器 SMCR；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_DIER` | DMA 突发起始寄存器 DIER；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_SR` | DMA 突发起始寄存器 SR；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_EGR` | DMA 突发起始寄存器 EGR；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_CCMR1` | DMA 突发起始寄存器 CCMR1；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_CCMR2` | DMA 突发起始寄存器 CCMR2；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_CCER` | DMA 突发起始寄存器 CCER；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_CNT` | DMA 突发起始寄存器 CNT；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_PSC` | DMA 突发起始寄存器 PSC；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_ARR` | DMA 突发起始寄存器 ARR；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_RCR` | DMA 突发起始寄存器 RCR；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_CCR1` | DMA 突发起始寄存器 CCR1；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_CCR2` | DMA 突发起始寄存器 CCR2；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_CCR3` | DMA 突发起始寄存器 CCR3；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_CCR4` | DMA 突发起始寄存器 CCR4；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_BDTR` | DMA 突发起始寄存器 BDTR；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_DCR` | DMA 突发起始寄存器 DCR；RCR/BDTR 仅 TIM1 |
| `TIM_DMABASE_DMAR` | DMA 突发起始寄存器 DMAR；RCR/BDTR 仅 TIM1 |
| `TIM_DMABURSTLENGTH_1TRANSFER` | 一次 DMA 突发 1 项传输的编码 |
| `TIM_DMABURSTLENGTH_2TRANSFERS` | 一次 DMA 突发 2 项传输的编码 |
| `TIM_DMABURSTLENGTH_3TRANSFERS` | 一次 DMA 突发 3 项传输的编码 |
| `TIM_DMABURSTLENGTH_4TRANSFERS` | 一次 DMA 突发 4 项传输的编码 |
| `TIM_DMABURSTLENGTH_5TRANSFERS` | 一次 DMA 突发 5 项传输的编码 |
| `TIM_DMABURSTLENGTH_6TRANSFERS` | 一次 DMA 突发 6 项传输的编码 |
| `TIM_DMABURSTLENGTH_7TRANSFERS` | 一次 DMA 突发 7 项传输的编码 |
| `TIM_DMABURSTLENGTH_8TRANSFERS` | 一次 DMA 突发 8 项传输的编码 |
| `TIM_DMABURSTLENGTH_9TRANSFERS` | 一次 DMA 突发 9 项传输的编码 |
| `TIM_DMABURSTLENGTH_10TRANSFERS` | 一次 DMA 突发 10 项传输的编码 |
| `TIM_DMABURSTLENGTH_11TRANSFERS` | 一次 DMA 突发 11 项传输的编码 |
| `TIM_DMABURSTLENGTH_12TRANSFERS` | 一次 DMA 突发 12 项传输的编码 |
| `TIM_DMABURSTLENGTH_13TRANSFERS` | 一次 DMA 突发 13 项传输的编码 |
| `TIM_DMABURSTLENGTH_14TRANSFERS` | 一次 DMA 突发 14 项传输的编码 |
| `TIM_DMABURSTLENGTH_15TRANSFERS` | 一次 DMA 突发 15 项传输的编码 |
| `TIM_DMABURSTLENGTH_16TRANSFERS` | 一次 DMA 突发 16 项传输的编码 |
| `TIM_DMABURSTLENGTH_17TRANSFERS` | 一次 DMA 突发 17 项传输的编码 |
| `TIM_DMABURSTLENGTH_18TRANSFERS` | 一次 DMA 突发 18 项传输的编码 |
| `TIM_DMA_UPDATE` | 更新DMA 请求源 |
| `TIM_DMA_CC1` | 通道 1 捕获/比较DMA 请求源 |
| `TIM_DMA_CC2` | 通道 2 捕获/比较DMA 请求源 |
| `TIM_DMA_CC3` | 通道 3 捕获/比较DMA 请求源 |
| `TIM_DMA_CC4` | 通道 4 捕获/比较DMA 请求源 |
| `TIM_DMA_COM` | TIM1 换相DMA 请求源 |
| `TIM_DMA_TRIGGER` | 触发DMA 请求源 |
| `TIM_ENCODERMODE_TI1` | 官方头文件编码SMS=001；按RM0008在TI2边沿计数，方向由TI1电平决定，见版本冲突说明 |
| `TIM_ENCODERMODE_TI2` | 官方头文件编码SMS=010；按RM0008在TI1边沿计数，方向由TI2电平决定，见版本冲突说明 |
| `TIM_ENCODERMODE_TI12` | x4 编码器模式，两路边沿均计数，方向由另一输入电平决定 |
| `TIM_ETRPOLARITY_INVERTED` | ETR 极性：反相 |
| `TIM_ETRPOLARITY_NONINVERTED` | ETR 极性：不反相 |
| `TIM_ETRPRESCALER_DIV1` | ETR 预分频：除以 1 |
| `TIM_ETRPRESCALER_DIV2` | ETR 预分频：除以 2 |
| `TIM_ETRPRESCALER_DIV4` | ETR 预分频：除以 4 |
| `TIM_ETRPRESCALER_DIV8` | ETR 预分频：除以 8 |
| `TIM_EVENTSOURCE_UPDATE` | 更新软件事件 |
| `TIM_EVENTSOURCE_CC1` | 通道 1 捕获/比较软件事件 |
| `TIM_EVENTSOURCE_CC2` | 通道 2 捕获/比较软件事件 |
| `TIM_EVENTSOURCE_CC3` | 通道 3 捕获/比较软件事件 |
| `TIM_EVENTSOURCE_CC4` | 通道 4 捕获/比较软件事件 |
| `TIM_EVENTSOURCE_COM` | TIM1 换相软件事件 |
| `TIM_EVENTSOURCE_TRIGGER` | 触发软件事件 |
| `TIM_EVENTSOURCE_BREAK` | TIM1 刹车软件事件 |
| `TIM_FLAG_UPDATE` | 更新状态标志 |
| `TIM_FLAG_CC1` | 通道 1 捕获/比较状态标志 |
| `TIM_FLAG_CC2` | 通道 2 捕获/比较状态标志 |
| `TIM_FLAG_CC3` | 通道 3 捕获/比较状态标志 |
| `TIM_FLAG_CC4` | 通道 4 捕获/比较状态标志 |
| `TIM_FLAG_COM` | TIM1 换相状态标志 |
| `TIM_FLAG_TRIGGER` | 触发状态标志 |
| `TIM_FLAG_BREAK` | TIM1 刹车状态标志 |
| `TIM_FLAG_CC1OF` | 通道 1 过捕获状态标志 |
| `TIM_FLAG_CC2OF` | 通道 2 过捕获状态标志 |
| `TIM_FLAG_CC3OF` | 通道 3 过捕获状态标志 |
| `TIM_FLAG_CC4OF` | 通道 4 过捕获状态标志 |
| `TIM_ICPOLARITY_RISING` | 捕获有效边沿：上升沿 |
| `TIM_ICPOLARITY_FALLING` | 捕获有效边沿：下降沿 |
| `TIM_ICPSC_DIV1` | 捕获事件预分频：除以 1 |
| `TIM_ICPSC_DIV2` | 捕获事件预分频：除以 2 |
| `TIM_ICPSC_DIV4` | 捕获事件预分频：除以 4 |
| `TIM_ICPSC_DIV8` | 捕获事件预分频：除以 8 |
| `TIM_ICSELECTION_DIRECTTI` | 捕获映射：IC1←TI1、IC2←TI2、IC3←TI3、IC4←TI4 |
| `TIM_ICSELECTION_INDIRECTTI` | 捕获映射：IC1←TI2、IC2←TI1、IC3←TI4、IC4←TI3 |
| `TIM_ICSELECTION_TRC` | 捕获映射：内部触发控制信号 |
| `TIM_INPUTCHANNELPOLARITY_RISING` | 单脉冲输入极性：上升沿 |
| `TIM_INPUTCHANNELPOLARITY_FALLING` | 单脉冲输入极性：下降沿 |
| `TIM_IT_UPDATE` | 更新中断源 |
| `TIM_IT_CC1` | 通道 1 捕获/比较中断源 |
| `TIM_IT_CC2` | 通道 2 捕获/比较中断源 |
| `TIM_IT_CC3` | 通道 3 捕获/比较中断源 |
| `TIM_IT_CC4` | 通道 4 捕获/比较中断源 |
| `TIM_IT_COM` | TIM1 换相中断源 |
| `TIM_IT_TRIGGER` | 触发中断源 |
| `TIM_IT_BREAK` | TIM1 刹车中断源 |
| `TIM_LOCKLEVEL_OFF` | TIM1 配置锁级别：不锁定 |
| `TIM_LOCKLEVEL_1` | TIM1 配置锁级别1；保护字段随等级递增，直到外设复位才解除 |
| `TIM_LOCKLEVEL_2` | TIM1 配置锁级别2；保护字段随等级递增，直到外设复位才解除 |
| `TIM_LOCKLEVEL_3` | TIM1 配置锁级别3；保护字段随等级递增，直到外设复位才解除 |
| `TIM_TRGO_RESET` | 用 EGR 的 UG 作为 TRGO 输出 |
| `TIM_TRGO_ENABLE` | 以计数器使能 CNT_EN 作为 TRGO |
| `TIM_TRGO_UPDATE` | 主触发输出：更新事件 |
| `TIM_TRGO_OC1` | 主触发输出：通道 1 比较脉冲/捕获事件 |
| `TIM_TRGO_OC1REF` | 主触发输出：OC1REF 参考信号 |
| `TIM_TRGO_OC2REF` | 主触发输出：OC2REF 参考信号 |
| `TIM_TRGO_OC3REF` | 主触发输出：OC3REF 参考信号 |
| `TIM_TRGO_OC4REF` | 主触发输出：OC4REF 参考信号 |
| `TIM_MASTERSLAVEMODE_ENABLE` | 主从同步 MSM：开启 |
| `TIM_MASTERSLAVEMODE_DISABLE` | 主从同步 MSM：关闭 |
| `TIM_OPMODE_SINGLE` | 单脉冲运行方式：下次更新事件停止计数 |
| `TIM_OPMODE_REPETITIVE` | 单脉冲运行方式：重复运行 |
| `TIM_OSSI_ENABLE` | 空闲时输出先被迫为无效电平，死区后进入预设空闲电平；仅 TIM1 |
| `TIM_OSSI_DISABLE` | TIM1 空闲关闭态：关闭 |
| `TIM_OSSR_ENABLE` | 运行中输出无效时，已使能的主/互补输出保持其无效电平；仅 TIM1 |
| `TIM_OSSR_DISABLE` | TIM1 运行关闭态：关闭 |
| `TIM_OCMODE_TIMING` | 输出比较模式：冻结 OCREF 仅用于比较定时 |
| `TIM_OCMODE_ACTIVE` | 输出比较模式：匹配置有效 |
| `TIM_OCMODE_INACTIVE` | 输出比较模式：匹配置无效 |
| `TIM_OCMODE_TOGGLE` | 输出比较模式：匹配翻转 |
| `TIM_OCMODE_PWM1` | 输出比较模式：PWM 模式 1 |
| `TIM_OCMODE_PWM2` | 输出比较模式：PWM 模式 2，逻辑相对 PWM1 反转 |
| `TIM_OCMODE_FORCED_ACTIVE` | 输出比较模式：强制有效 |
| `TIM_OCMODE_FORCED_INACTIVE` | 输出比较模式：强制无效 |
| `TIM_OCIDLESTATE_SET` | TIM1 主输出空闲电平：置高 |
| `TIM_OCIDLESTATE_RESET` | TIM1 主输出空闲电平低 |
| `TIM_OCNIDLESTATE_SET` | TIM1 互补输出空闲电平：置高 |
| `TIM_OCNIDLESTATE_RESET` | TIM1 互补输出空闲电平低 |
| `TIM_OCNPOLARITY_HIGH` | TIM1 互补有效极性：高有效/高电平 |
| `TIM_OCNPOLARITY_LOW` | TIM1 互补有效极性：低有效/低电平 |
| `TIM_OUTPUTNSTATE_DISABLE` | TIM1 互补输出使能：关闭 |
| `TIM_OUTPUTNSTATE_ENABLE` | TIM1 互补输出使能：开启 |
| `TIM_OCPOLARITY_HIGH` | 主输出有效极性：高有效/高电平 |
| `TIM_OCPOLARITY_LOW` | 主输出有效极性：低有效/低电平 |
| `TIM_OUTPUTSTATE_DISABLE` | 主输出使能：关闭 |
| `TIM_OUTPUTSTATE_ENABLE` | 主输出使能：开启 |
| `TIM_OCFAST_DISABLE` | PWM 快速响应：关闭 |
| `TIM_OCFAST_ENABLE` | PWM 快速响应：开启 |
| `TIM_SLAVEMODE_DISABLE` | 从模式：关闭 |
| `TIM_SLAVEMODE_RESET` | TRGI 上升沿重新初始化计数器 |
| `TIM_SLAVEMODE_GATED` | 从模式：TRGI 高时允许计数 |
| `TIM_SLAVEMODE_TRIGGER` | 从模式：TRGI 上升沿启动计数 |
| `TIM_SLAVEMODE_EXTERNAL1` | 从模式：从模式外部时钟 1 |
| `TIM_TI1SELECTION_CH1` | TI1 输入来源：CH1输入，不进行CH1–CH3异或 |
| `TIM_TI1SELECTION_XORCOMBINATION` | TI1 输入来源：CH1–CH3 异或 |
| `TIM_TRIGGERPOLARITY_INVERTED` | 触发输入极性：反相 |
| `TIM_TRIGGERPOLARITY_NONINVERTED` | 触发输入极性：不反相 |
| `TIM_TRIGGERPOLARITY_RISING` | 触发输入极性：上升沿 |
| `TIM_TRIGGERPOLARITY_FALLING` | 触发输入极性：下降沿 |
| `TIM_TRIGGERPOLARITY_BOTHEDGE` | 库极性编码；与TS选择TI1F_ED双边沿检测通路分别配置，不能以此符号代替触发源路由 |
| `TIM_TRIGGERPRESCALER_DIV1` | 触发输入预分频：除以 1 |
| `TIM_TRIGGERPRESCALER_DIV2` | 触发输入预分频：除以 2 |
| `TIM_TRIGGERPRESCALER_DIV4` | 触发输入预分频：除以 4 |
| `TIM_TRIGGERPRESCALER_DIV8` | 触发输入预分频：除以 8 |
| `TIM_TS_ITR0` | 触发输入选择：内部触发 0，核对互联表 |
| `TIM_TS_ITR1` | 触发输入选择：内部触发 1，核对互联表 |
| `TIM_TS_ITR2` | 触发输入选择：内部触发 2，核对互联表 |
| `TIM_TS_ITR3` | 触发输入选择：内部触发 3，核对互联表 |
| `TIM_TS_TI1F_ED` | 触发输入选择：TI1 双边沿检测 |
| `TIM_TS_TI1FP1` | 触发输入选择：滤波后的 TI1FP1 输入 |
| `TIM_TS_TI2FP2` | 触发输入选择：滤波后的 TI2FP2 输入 |
| `TIM_TS_ETRF` | 触发输入选择：滤波后的外部 ETR 输入 |
| `TIM_TS_NONE` | 无新内部触发源需求；不能据此推定旧TS配置会被清除 |


来源：[固定HAL TIM头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h)。

[返回定时器主题](../../知识库/06_定时器PWM与同步.md) · [图形关系与来源](图形关系与来源.md)
