# TIM LL 辅助宏与编码器符号冲突

固定de129f1头文件，固定来源整合。保留8个原宏入口及既有算术边界核查。


宏不是带类型检查的普通函数。不要把带自增等副作用的表达式作为参数；读写寄存器仍须满足本章状态和实例限制。

### `__LL_TIM_CALC_DEADTIME`

调用形态：`__LL_TIM_CALC_DEADTIME(__TIMCLK__, __CKD__, __DT__)`。

输入 TIM 时钟 Hz、CKD 枚举、目标死区 ns；返回 DTG 编码，仅用于 TIM1。硬件可表示的延迟为 0–127、128–254（步长 2）、256–504（步长 8）、512–1008 个 $`t_{\mathrm{DTS}}`$ ；不是连续的 0–1023 个 $`t_{\mathrm{DTS}}`$ 。必须把返回编码按本章分段公式反算为实际死区，尤其功率开关的最小安全死区不得仅凭请求值判断。

下述计算细节核对 [ST HAL v1.1.4 固定头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L917-L968)，属于该版本宏实现边界，UM1850 只给单位和接口用途。宏先用整数皮秒近似计算 $`t_{\mathrm{DTS}}`$ ，再相对这个近似值按所在分段向下量化；请求达到内部 $`1024t_{\mathrm{DTS}}`$ 边界及以上时返回 0，而不是饱和到最大死区。返回 0 因而既可能表示零/过小请求，也可能表示超范围，不能当成成功状态。`TIMCLK` 必须非零，CKD 必须为 DIV1/2/4。部分分支在转换成 uint64_t 之前先做 `DT×1000U`；普通 32 位无符号输入超过 4294967 ns 就存在中间溢出风险，不能用超大请求测试其限幅。

整数皮秒的截断也须保留：按固定头文件[内部 TIM_CALC_DTS 定义](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L150-L162)，72 MHz、CKD=DIV1时使用13888 ps，而理想时钟周期是13888.888… ps。请求1736 ns时宏返回DTG=125，按理想72 MHz硬件时基反算为1736.111… ns，略高于请求。因此这里的“向下量化”不构成实际死区始终≤请求的保证；同样也不能保证满足最小死区。该数值是依据固定宏和硬件分段式的有理数复算，未包含实际时钟误差、引脚延迟或板端测量。

### `__LL_TIM_CALC_PSC`

调用形态：`__LL_TIM_CALC_PSC(__TIMCLK__, __CNTCLK__)`。

输入 TIM 时钟 Hz、目标计数时钟 Hz。上述固定版本在 $`\mathrm{TIMCLK}\geq\mathrm{CNTCLK}`$ 时返回 $`\left\lfloor\frac{\mathrm{TIMCLK}}{\mathrm{CNTCLK}}\right\rfloor-1`$ ，否则返回 0；调用者须确认结果处于 0–65535，不能把说明中的合法范围当作对任意输入都自动限幅的保证。实际频率为 $`\frac{\mathrm{TIMCLK}}{\mathrm{PSC}+1}`$ ，因整数除法截断，它可能高于目标。例如 72 MHz 请求 5 MHz，PSC=13，实际约 5.143 MHz。需要“不超过目标”时应另行按向上取整的除数选 PSC。两个频率均应为正，尤其 `CNTCLK=0` 会除零。

### `__LL_TIM_CALC_ARR`

调用形态：`__LL_TIM_CALC_ARR(__TIMCLK__, __PSC__, __FREQ__)`。

输入 TIM 时钟 Hz、PSC、目标输出频率 Hz。上述固定版本在 $`\left\lfloor\frac{\mathrm{TIMCLK}}{\mathrm{PSC}+1}\right\rfloor\geq\mathrm{FREQ}`$ 时返回 $`\left\lfloor\frac{\mathrm{TIMCLK}}{\mathrm{FREQ}(\mathrm{PSC}+1)}\right\rfloor-1`$ ，否则返回 0。`FREQ` 必须为正，PSC 必须在 0–65535；合法 C8 时钟和通过该条件的输入下，分母不超过 `TIMCLK`。输出还须检查 ARR≤65535 且正常计数时 ARR≠0，返回 0 并不保证产生请求频率。该式按边沿对齐、无重复计数影响的周期解释；中心对齐不能直接套用。实际频率通常因截断而不低于目标。

### `__LL_TIM_CALC_DELAY`

调用形态：`__LL_TIM_CALC_DELAY(__TIMCLK__, __PSC__, __DELAY__)`。

输入 TIM 时钟 Hz、PSC、目标延迟 µs；上述固定版本返回 $`\left\lfloor\frac{\mathrm{TIMCLK}\times\mathrm{DELAY}}{1000000(\mathrm{PSC}+1)}\right\rfloor`$ ，乘法/除法中间量使用 uint64_t，最后转换为 uint32_t。这是向下取整的计数值，不保证“至少延迟请求时长”；还须检查结果为 C8 的 16 位 CCR 可表示范围，并满足所用计数模式和 ARR 关系。PSC 取 0–65535；不要先在宏外用 32 位计算 `TIMCLK×DELAY`。范围检查必须针对尚未窄化的 uint64_t 商，不能仅检查宏已经转换成 uint32_t 的返回值：72 MHz、PSC=0、DELAY=59652324 µs 时真实商为 4294967328，宏回绕返回 32，虽看似落入 16 位范围，却完全不代表所需延迟。

### `__LL_TIM_CALC_PULSE`

调用形态：`__LL_TIM_CALC_PULSE(__TIMCLK__, __PSC__, __DELAY__, __PULSE__)`。

输入 TIM 时钟 Hz、PSC、延迟 µs、脉宽 µs；上述固定版本实际返回 `CALC_DELAY(TIMCLK,PSC,PULSE)+CALC_DELAY(TIMCLK,PSC,DELAY)`，两项分别截断后相加，不是先相加时间再统一取整，也没有减 1。它被原文称为 ARR 辅助值，但不能据此忽略向上 PWM2 单脉冲的实际有效宽度 $`\frac{\mathrm{ARR}-\mathrm{CCR}+1}{f_{\mathrm{CNT}}}`$ ：例如 $`f_{\mathrm{CNT}}=1\,\mathrm{MHz}`$ 、DELAY=10 µs、PULSE=20 µs，宏给 CCR=10、ARR=30，对应有效高电平为 21 个计数周期（未计外部触发同步延迟）。精确脉宽须按所用极性/模式反算 ARR；不要擅自把宏本身描述成“总计数减 1”。检查每项在 CALC_DELAY 内转换前的 64 位商、随后两项和的 32 位溢出及 C8 最终 1≤ARR≤65535（ARR=0 阻塞计数），且应满足单脉冲模式对 CCR/ARR 的条件。

### `__LL_TIM_GET_ICPSC_RATIO`

调用形态：`__LL_TIM_GET_ICPSC_RATIO(__ICPSC__)`。

输入 LL_TIM_ICPSC_DIV1/2/4/8 编码，返回整数 1/2/4/8。

### `LL_TIM_WriteReg`

调用形态：`LL_TIM_WriteReg(__INSTANCE__, __REG__, __VALUE__)`。

参数为 TIM 实例、寄存器成员名、写入值；直接写寄存器，无返回，受 LOCK 和硬件只读位约束。

### `LL_TIM_ReadReg`

调用形态：`LL_TIM_ReadReg(__INSTANCE__, __REG__)`。

参数为 TIM 实例、寄存器成员名；返回寄存器值。

### 编码器 x2 模式的文档/符号冲突

UM1850 的 HAL/LL 常量说明把 TI1 命名项解释为在 TI1 边沿计数，TI2 项解释为在 TI2 边沿计数；RM0008 的编码器接口正文明确规定 **SMS=001 在 TI2 边沿计数，SMS=010 在 TI1 边沿计数，SMS=011 在两路边沿计数**，方向由另一路电平决定。RM 的 SMS 位表还把部分 TI1FP1/TI2FP2 后缀写反，须结合编码器正文与框图理解。

补充核对 ST 官方 HAL v1.1.4 的 [HAL 头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L631-L633) 和 [LL 头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L695-L697)（标签日期2020-01-29，固定commit为 de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9）：HAL 的 TIM_ENCODERMODE_TI1、LL 的 LL_TIM_ENCODERMODE_X2_TI1 实际均为 SMS_0，即001；对应TI2命名项为SMS_1，即010。同一历史版本的注释已存在上述UM/RM冲突。这里以实际SMS编码和RM硬件定义说明行为，不能只按符号后缀决定接线。这一固定版本与UM1850 Rev 3年代相近，但原PDF没有指定它为唯一对应的软件版本；项目仍须按实际所用库核对本地宏值和实现。


[返回定时器主题](../../知识库/06_定时器PWM与同步.md) · [图形关系与来源](图形关系与来源.md)
