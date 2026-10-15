# TIM LL 符号与适用限制

符号来自固定 de129f1 头文件，按用途分组。传参使用符号编码，具体实例、通道和运行条件见[LL 接口](LL接口.md)。

- [时基与计数](#时基与计数)
- [通道与控制更新](#通道与控制更新)
- [输入映射与编码器](#输入映射与编码器)
- [输入捕获滤波](#输入捕获滤波)
- [ETR 滤波](#etr-滤波)
- [ETR 极性与预分频](#etr-极性与预分频)
- [输出比较与 PWM](#输出比较与-pwm)
- [输出保护与锁定](#输出保护与锁定)
- [主从同步与触发](#主从同步与触发)
- [DMA burst 起始寄存器](#dma-burst-起始寄存器)
- [DMA burst 长度](#dma-burst-长度)
- [捕获比较 DMA 请求](#捕获比较-dma-请求)
- [状态与中断使能](#状态与中断使能)

## 时基与计数

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_TIM_CLOCKDIVISION_DIV1` | CKD 滤波/死区时钟分频：除以 1 |
| `LL_TIM_CLOCKDIVISION_DIV2` | CKD 滤波/死区时钟分频：除以 2 |
| `LL_TIM_CLOCKDIVISION_DIV4` | CKD 滤波/死区时钟分频：除以 4 |
| `LL_TIM_CLOCKSOURCE_INTERNAL` | 计数时钟源：内部时钟 |
| `LL_TIM_CLOCKSOURCE_EXT_MODE1` | 计数时钟源：外部时钟模式 1 |
| `LL_TIM_CLOCKSOURCE_EXT_MODE2` | 计数时钟源：外部时钟模式 2 |
| `LL_TIM_COUNTERDIRECTION_UP` | 当前计数方向：向上 |
| `LL_TIM_COUNTERDIRECTION_DOWN` | 当前计数方向：向下 |
| `LL_TIM_COUNTERMODE_UP` | 计数模式：向上 |
| `LL_TIM_COUNTERMODE_DOWN` | 计数模式：向下 |
| `LL_TIM_COUNTERMODE_CENTER_UP` | CMS=01（TIM_CR1_CMS_0）；中心对齐，输出比较标志按下数方向条件产生；名称UP不代表标志在上数置位 |
| `LL_TIM_COUNTERMODE_CENTER_DOWN` | CMS=10（TIM_CR1_CMS_1）；中心对齐，输出比较标志按上数方向条件产生；名称DOWN不代表标志在下数置位 |
| `LL_TIM_COUNTERMODE_CENTER_UP_DOWN` | 中心对齐；输出比较标志在向上及向下计数时均产生 |
| `LL_TIM_ONEPULSEMODE_SINGLE` | 单脉冲运行方式：下次更新事件停止计数 |
| `LL_TIM_ONEPULSEMODE_REPETITIVE` | 单脉冲运行方式：重复运行 |
| `LL_TIM_UPDATESOURCE_REGULAR` | 计数边界、UG 或从控制器均可产生更新请求 |
| `LL_TIM_UPDATESOURCE_COUNTER` | 只有计数边界产生更新请求 |

## 通道与控制更新

各接口接受的通道及组合方式见对应参数说明。

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_TIM_CCUPDATESOURCE_COMG_ONLY` | TIM1 控制位 COM 更新来源：仅软件 COMG |
| `LL_TIM_CCUPDATESOURCE_COMG_AND_TRGI` | TIM1 控制位 COM 更新来源：软件 COMG 或 TRGI |
| `LL_TIM_CHANNEL_CH1` | 选择 CH1 |
| `LL_TIM_CHANNEL_CH1N` | 选择 CH1N（TIM1） |
| `LL_TIM_CHANNEL_CH2` | 选择 CH2 |
| `LL_TIM_CHANNEL_CH2N` | 选择 CH2N（TIM1） |
| `LL_TIM_CHANNEL_CH3` | 选择 CH3 |
| `LL_TIM_CHANNEL_CH3N` | 选择 CH3N（TIM1） |
| `LL_TIM_CHANNEL_CH4` | 选择 CH4 |

## 输入映射与编码器

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_TIM_ACTIVEINPUT_DIRECTTI` | 捕获映射：IC1←TI1、IC2←TI2、IC3←TI3、IC4←TI4 |
| `LL_TIM_ACTIVEINPUT_INDIRECTTI` | 捕获映射：IC1←TI2、IC2←TI1、IC3←TI4、IC4←TI3 |
| `LL_TIM_ACTIVEINPUT_TRC` | 捕获映射：内部触发控制信号 |
| `LL_TIM_ENCODERMODE_X2_TI1` | 官方头文件编码SMS=001；按RM0008在TI2边沿计数，方向由TI1电平决定，见版本冲突说明 |
| `LL_TIM_ENCODERMODE_X2_TI2` | 官方头文件编码SMS=010；按RM0008在TI1边沿计数，方向由TI2电平决定，见版本冲突说明 |
| `LL_TIM_ENCODERMODE_X4_TI12` | x4 模式，两路边沿均计数，方向由另一输入电平决定 |
| `LL_TIM_ICPSC_DIV1` | 捕获事件预分频：除以 1 |
| `LL_TIM_ICPSC_DIV2` | 捕获事件预分频：除以 2 |
| `LL_TIM_ICPSC_DIV4` | 捕获事件预分频：除以 4 |
| `LL_TIM_ICPSC_DIV8` | 捕获事件预分频：除以 8 |
| `LL_TIM_IC_POLARITY_RISING` | 捕获有效边沿：上升沿 |
| `LL_TIM_IC_POLARITY_FALLING` | 捕获有效边沿：下降沿 |

## 输入捕获滤波

$`f_{\mathrm{CK\_INT}}`$ 为定时器内核时钟频率， $`f_{\mathrm{DTS}}`$ 为 CKD 分频后的滤波／死区时钟频率，单位均为 Hz。FDIV1_N2/N4/N8 使用前者，其余分频滤波档使用后者。定义见[固定头文件 L653–668](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L653-L668)。

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_TIM_IC_FILTER_FDIV1` | 无数字滤波；以 $`f_{\mathrm{DTS}}`$ 采样 |
| `LL_TIM_IC_FILTER_FDIV1_N2` | 采样频率 $`f_{\mathrm{CK\_INT}}`$ ，连续 2 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV1_N4` | 采样频率 $`f_{\mathrm{CK\_INT}}`$ ，连续 4 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV1_N8` | 采样频率 $`f_{\mathrm{CK\_INT}}`$ ，连续 8 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV2_N6` | 采样频率 $`f_{\mathrm{DTS}}/2`$ ，连续 6 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV2_N8` | 采样频率 $`f_{\mathrm{DTS}}/2`$ ，连续 8 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV4_N6` | 采样频率 $`f_{\mathrm{DTS}}/4`$ ，连续 6 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV4_N8` | 采样频率 $`f_{\mathrm{DTS}}/4`$ ，连续 8 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV8_N6` | 采样频率 $`f_{\mathrm{DTS}}/8`$ ，连续 6 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV8_N8` | 采样频率 $`f_{\mathrm{DTS}}/8`$ ，连续 8 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV16_N5` | 采样频率 $`f_{\mathrm{DTS}}/16`$ ，连续 5 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV16_N6` | 采样频率 $`f_{\mathrm{DTS}}/16`$ ，连续 6 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV16_N8` | 采样频率 $`f_{\mathrm{DTS}}/16`$ ，连续 8 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV32_N5` | 采样频率 $`f_{\mathrm{DTS}}/32`$ ，连续 5 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV32_N6` | 采样频率 $`f_{\mathrm{DTS}}/32`$ ，连续 6 个一致样本 |
| `LL_TIM_IC_FILTER_FDIV32_N8` | 采样频率 $`f_{\mathrm{DTS}}/32`$ ，连续 8 个一致样本 |

## ETR 滤波

时钟符号与上表相同；基准选择见[固定头文件 L767–774](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L767-L774)。

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_TIM_ETR_FILTER_FDIV1` | 无数字滤波；以 $`f_{\mathrm{DTS}}`$ 采样 |
| `LL_TIM_ETR_FILTER_FDIV1_N2` | 采样频率 $`f_{\mathrm{CK\_INT}}`$ ，连续 2 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV1_N4` | 采样频率 $`f_{\mathrm{CK\_INT}}`$ ，连续 4 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV1_N8` | 采样频率 $`f_{\mathrm{CK\_INT}}`$ ，连续 8 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV2_N6` | 采样频率 $`f_{\mathrm{DTS}}/2`$ ，连续 6 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV2_N8` | 采样频率 $`f_{\mathrm{DTS}}/2`$ ，连续 8 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV4_N6` | 采样频率 $`f_{\mathrm{DTS}}/4`$ ，连续 6 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV4_N8` | 采样频率 $`f_{\mathrm{DTS}}/4`$ ，连续 8 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV8_N6` | 采样频率 $`f_{\mathrm{DTS}}/8`$ ，连续 6 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV8_N8` | 采样频率 $`f_{\mathrm{DTS}}/8`$ ，连续 8 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV16_N5` | 采样频率 $`f_{\mathrm{DTS}}/16`$ ，连续 5 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV16_N6` | 采样频率 $`f_{\mathrm{DTS}}/16`$ ，连续 6 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV16_N8` | 采样频率 $`f_{\mathrm{DTS}}/16`$ ，连续 8 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV32_N5` | 采样频率 $`f_{\mathrm{DTS}}/32`$ ，连续 5 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV32_N6` | 采样频率 $`f_{\mathrm{DTS}}/32`$ ，连续 6 个一致样本 |
| `LL_TIM_ETR_FILTER_FDIV32_N8` | 采样频率 $`f_{\mathrm{DTS}}/32`$ ，连续 8 个一致样本 |

## ETR 极性与预分频

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_TIM_ETR_POLARITY_NONINVERTED` | ETR 极性：不反相 |
| `LL_TIM_ETR_POLARITY_INVERTED` | ETR 极性：反相 |
| `LL_TIM_ETR_PRESCALER_DIV1` | ETR 预分频：除以 1 |
| `LL_TIM_ETR_PRESCALER_DIV2` | ETR 预分频：除以 2 |
| `LL_TIM_ETR_PRESCALER_DIV4` | ETR 预分频：除以 4 |
| `LL_TIM_ETR_PRESCALER_DIV8` | ETR 预分频：除以 8 |

## 输出比较与 PWM

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_TIM_OCIDLESTATE_LOW` | TIM1 主输出空闲电平：低电平 |
| `LL_TIM_OCIDLESTATE_HIGH` | TIM1 主输出空闲电平：高电平 |
| `LL_TIM_OCMODE_FROZEN` | 输出比较模式：冻结 OCREF |
| `LL_TIM_OCMODE_ACTIVE` | 输出比较模式：匹配置有效 |
| `LL_TIM_OCMODE_INACTIVE` | 输出比较模式：匹配置无效 |
| `LL_TIM_OCMODE_TOGGLE` | 输出比较模式：匹配翻转 |
| `LL_TIM_OCMODE_FORCED_INACTIVE` | 输出比较模式：强制无效 |
| `LL_TIM_OCMODE_FORCED_ACTIVE` | 输出比较模式：强制有效 |
| `LL_TIM_OCMODE_PWM1` | 输出比较模式：PWM 模式 1 |
| `LL_TIM_OCMODE_PWM2` | 输出比较模式：PWM 模式 2，逻辑相对 PWM1 反转 |
| `LL_TIM_OCPOLARITY_HIGH` | 主输出有效极性：高电平有效 |
| `LL_TIM_OCPOLARITY_LOW` | 主输出有效极性：低电平有效 |
| `LL_TIM_OCSTATE_DISABLE` | 输出通道使能：关闭 |
| `LL_TIM_OCSTATE_ENABLE` | 输出通道使能：开启 |

## 输出保护与锁定

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_TIM_AUTOMATICOUTPUT_DISABLE` | TIM1 自动恢复 MOE：关闭 |
| `LL_TIM_AUTOMATICOUTPUT_ENABLE` | TIM1 自动恢复 MOE：开启 |
| `LL_TIM_BREAK_DISABLE` | TIM1 刹车：关闭 |
| `LL_TIM_BREAK_ENABLE` | TIM1 刹车：开启 |
| `LL_TIM_BREAK_POLARITY_LOW` | BKIN 有效极性：低电平有效 |
| `LL_TIM_BREAK_POLARITY_HIGH` | BKIN 有效极性：高电平有效 |
| `LL_TIM_LOCKLEVEL_OFF` | TIM1 配置锁级别：不锁定 |
| `LL_TIM_LOCKLEVEL_1` | TIM1 配置锁级别1；保护范围逐级增加，复位前不可解除 |
| `LL_TIM_LOCKLEVEL_2` | TIM1 配置锁级别2；保护范围逐级增加，复位前不可解除 |
| `LL_TIM_LOCKLEVEL_3` | TIM1 配置锁级别3；保护范围逐级增加，复位前不可解除 |
| `LL_TIM_OSSI_DISABLE` | TIM1 空闲关闭态：关闭 |
| `LL_TIM_OSSI_ENABLE` | 空闲时输出先被迫为无效电平，死区后进入预设空闲电平；仅 TIM1 |
| `LL_TIM_OSSR_DISABLE` | TIM1 运行关闭态：关闭 |
| `LL_TIM_OSSR_ENABLE` | 运行中输出无效时，已使能的主/互补输出保持其无效电平；仅 TIM1 |

## 主从同步与触发

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_TIM_SLAVEMODE_DISABLED` | 从模式：关闭 |
| `LL_TIM_SLAVEMODE_RESET` | TRGI 上升沿重新初始化计数器 |
| `LL_TIM_SLAVEMODE_GATED` | 从模式：TRGI 高时允许计数 |
| `LL_TIM_SLAVEMODE_TRIGGER` | 从模式：TRGI 上升沿启动计数 |
| `LL_TIM_TRGO_RESET` | 用 EGR 的 UG 作为 TRGO 输出 |
| `LL_TIM_TRGO_ENABLE` | 以计数器使能 CNT_EN 作为 TRGO |
| `LL_TIM_TRGO_UPDATE` | 主触发输出：更新事件 |
| `LL_TIM_TRGO_CC1IF` | 主触发输出：通道 1 比较脉冲/捕获事件 |
| `LL_TIM_TRGO_OC1REF` | 主触发输出：OC1REF 参考信号 |
| `LL_TIM_TRGO_OC2REF` | 主触发输出：OC2REF 参考信号 |
| `LL_TIM_TRGO_OC3REF` | 主触发输出：OC3REF 参考信号 |
| `LL_TIM_TRGO_OC4REF` | 主触发输出：OC4REF 参考信号 |
| `LL_TIM_TS_ITR0` | 触发输入选择：内部触发 0，核对互联表 |
| `LL_TIM_TS_ITR1` | 触发输入选择：内部触发 1，核对互联表 |
| `LL_TIM_TS_ITR2` | 触发输入选择：内部触发 2，核对互联表 |
| `LL_TIM_TS_ITR3` | 触发输入选择：内部触发 3，核对互联表 |
| `LL_TIM_TS_TI1F_ED` | 触发输入选择：TI1 双边沿检测 |
| `LL_TIM_TS_TI1FP1` | 触发输入选择：滤波后的 TI1FP1 输入 |
| `LL_TIM_TS_TI2FP2` | 触发输入选择：滤波后的 TI2FP2 输入 |
| `LL_TIM_TS_ETRF` | 触发输入选择：滤波后的外部 ETR 输入 |

## DMA burst 起始寄存器

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_TIM_DMABURST_BASEADDR_CR1` | DMA 突发起始寄存器 CR1 |
| `LL_TIM_DMABURST_BASEADDR_CR2` | DMA 突发起始寄存器 CR2 |
| `LL_TIM_DMABURST_BASEADDR_SMCR` | DMA 突发起始寄存器 SMCR |
| `LL_TIM_DMABURST_BASEADDR_DIER` | DMA 突发起始寄存器 DIER |
| `LL_TIM_DMABURST_BASEADDR_SR` | DMA 突发起始寄存器 SR |
| `LL_TIM_DMABURST_BASEADDR_EGR` | DMA 突发起始寄存器 EGR |
| `LL_TIM_DMABURST_BASEADDR_CCMR1` | DMA 突发起始寄存器 CCMR1 |
| `LL_TIM_DMABURST_BASEADDR_CCMR2` | DMA 突发起始寄存器 CCMR2 |
| `LL_TIM_DMABURST_BASEADDR_CCER` | DMA 突发起始寄存器 CCER |
| `LL_TIM_DMABURST_BASEADDR_CNT` | DMA 突发起始寄存器 CNT |
| `LL_TIM_DMABURST_BASEADDR_PSC` | DMA 突发起始寄存器 PSC |
| `LL_TIM_DMABURST_BASEADDR_ARR` | DMA 突发起始寄存器 ARR |
| `LL_TIM_DMABURST_BASEADDR_RCR` | DMA 突发起始寄存器 RCR（TIM1） |
| `LL_TIM_DMABURST_BASEADDR_CCR1` | DMA 突发起始寄存器 CCR1 |
| `LL_TIM_DMABURST_BASEADDR_CCR2` | DMA 突发起始寄存器 CCR2 |
| `LL_TIM_DMABURST_BASEADDR_CCR3` | DMA 突发起始寄存器 CCR3 |
| `LL_TIM_DMABURST_BASEADDR_CCR4` | DMA 突发起始寄存器 CCR4 |
| `LL_TIM_DMABURST_BASEADDR_BDTR` | DMA 突发起始寄存器 BDTR（TIM1） |

## DMA burst 长度

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_TIM_DMABURST_LENGTH_1TRANSFER` | 一次 DMA 突发 1 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_2TRANSFERS` | 一次 DMA 突发 2 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_3TRANSFERS` | 一次 DMA 突发 3 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_4TRANSFERS` | 一次 DMA 突发 4 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_5TRANSFERS` | 一次 DMA 突发 5 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_6TRANSFERS` | 一次 DMA 突发 6 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_7TRANSFERS` | 一次 DMA 突发 7 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_8TRANSFERS` | 一次 DMA 突发 8 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_9TRANSFERS` | 一次 DMA 突发 9 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_10TRANSFERS` | 一次 DMA 突发 10 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_11TRANSFERS` | 一次 DMA 突发 11 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_12TRANSFERS` | 一次 DMA 突发 12 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_13TRANSFERS` | 一次 DMA 突发 13 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_14TRANSFERS` | 一次 DMA 突发 14 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_15TRANSFERS` | 一次 DMA 突发 15 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_16TRANSFERS` | 一次 DMA 突发 16 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_17TRANSFERS` | 一次 DMA 突发 17 项传输的编码 |
| `LL_TIM_DMABURST_LENGTH_18TRANSFERS` | 一次 DMA 突发 18 项传输的编码 |

## 捕获比较 DMA 请求

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_TIM_CCDMAREQUEST_CC` | CC DMA 请求来源：对应捕获/比较事件 |
| `LL_TIM_CCDMAREQUEST_UPDATE` | CC DMA 请求来源：更新事件 |

## 状态与中断使能

| 符号 | 中文含义与适用条件 |
|---|---|
| `LL_TIM_SR_UIF` | 更新状态标志 |
| `LL_TIM_SR_CC1IF` | 通道 1 捕获/比较状态标志 |
| `LL_TIM_SR_CC2IF` | 通道 2 捕获/比较状态标志 |
| `LL_TIM_SR_CC3IF` | 通道 3 捕获/比较状态标志 |
| `LL_TIM_SR_CC4IF` | 通道 4 捕获/比较状态标志 |
| `LL_TIM_SR_COMIF` | TIM1 换相状态标志 |
| `LL_TIM_SR_TIF` | 触发状态标志 |
| `LL_TIM_SR_BIF` | TIM1 刹车状态标志 |
| `LL_TIM_SR_CC1OF` | 通道 1 过捕获状态标志 |
| `LL_TIM_SR_CC2OF` | 通道 2 过捕获状态标志 |
| `LL_TIM_SR_CC3OF` | 通道 3 过捕获状态标志 |
| `LL_TIM_SR_CC4OF` | 通道 4 过捕获状态标志 |
| `LL_TIM_DIER_UIE` | 更新中断使能位 |
| `LL_TIM_DIER_CC1IE` | 通道 1 捕获/比较中断使能位 |
| `LL_TIM_DIER_CC2IE` | 通道 2 捕获/比较中断使能位 |
| `LL_TIM_DIER_CC3IE` | 通道 3 捕获/比较中断使能位 |
| `LL_TIM_DIER_CC4IE` | 通道 4 捕获/比较中断使能位 |
| `LL_TIM_DIER_COMIE` | TIM1 换相中断使能位 |
| `LL_TIM_DIER_TIE` | 触发中断使能位 |
| `LL_TIM_DIER_BIE` | TIM1 刹车中断使能位 |

来源：[固定LL TIM头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h)。

[返回定时器主题](../../知识库/06_定时器PWM与同步.md) · [图形关系与来源](图形关系与来源.md)
