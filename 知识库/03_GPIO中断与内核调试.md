# GPIO中断与内核调试

[返回总目录](../README.md)

从引脚电平到中断处理函数，依次涉及 GPIO 配置、AFIO 复用、EXTI 路由和 NVIC 中断控制。本章先说明这条路径，再介绍 SysTick、异常现场和调试观察。

依据为 RM0008 Rev21、PM0056 Rev7、DS5319 Rev20、ES096 Rev15 及 UM1850 Rev3；原图收录情况见[图表关系与覆盖范围](../参数/图表关系与覆盖范围.md)。

## 1 GPIO配置必须同时看模式和数据通路

GPIO（通用输入/输出）的模式与速度由 MODE、CNF 字段控制。下文无前缀的成组 0/1 编码按二进制读，0x 前缀表示十六进制；同名字段应连同寄存器前缀检索。

完整模式、寄存器访问属性及备份域条件见[GPIO模式与寄存器](../参数/GPIO模式与寄存器.md)。

### 1.1 模式与读回

| 用途 | 配置及读写解释 |
|---|---|
| 上拉/下拉输入 | MODE=00、CNF=10；ODR=1选上拉，ODR=0选下拉 |
| 通用推挽/开漏 | ODR控制锁存；开漏写1只是高阻，需外部上拉 |
| 复用推挽/开漏 | 外设控制输出，ODR不能控制该脚；未启动外设时输出不保证 |
| 模拟输入 | 数字输入缓冲、输出及上下拉关闭，IDR读0 |
| 实际电平回读 | 数字路径用IDR；ODR只反映最后锁存值，不证明脚已到目标电平 |

MODE输出编码01/10/11分别是10/2/50 MHz，不能按二进制文字猜速度。速度档位表示驱动能力条件，不生成对应频率；PC13/14/15等特殊脚仍受电气限制。依据：[RM0008 §9.1；§9.1.1；§9.1.7–§9.1.10；§9.2.1–§9.2.3](../来源/RM0008.md#src-rm0008-r21-gpio-mode)。

### 1.2 配置顺序

工程配置可按“核查封装和占用→开GPIO/AFIO及所需外设时钟→建立目标锁存或外设配置→设置路由和GPIO模式→使能功能→检查IDR/外部波形”组织；这由数据通路关系导出，不保证未经板级验证的切换无毛刺。GPIO来源的EXTI须配置为输入模式（浮空、上拉或下拉；RM0008 Rev 21 §9.1.3 p162及§9.1.11 Table 33 p170），I²C用复用开漏，ADC用模拟；SPI则须按主从、单双线、NSS方案分别选模式，不能一律复用推挽。逐项依据见[RM0008 §9.1.3–§9.1.5；§9.1.9；§9.1.11](../来源/RM0008.md#src-rm0008-r21-gpio-af-input)。

### 1.3 原子置位与配置锁

GPIO、AFIO寄存器仅允许32位访问。用BSRR一次写同时置/清选中ODR位，避免主循环与ISR对ODR读改写丢失更新；BSRR低16位置位、高16位复位，同一脚两者都写1时置位优先。不要读改写BSRR，也不要把“位操作原子”扩大成多寄存器初始化整体原子。CRL/CRH的配置共享、MAPR影子及锁序列仍需协调所有者。

LCKR锁定的是选中引脚的CRL/CRH配置，不锁ODR。固定低16位掩码执行LCKK写1→0→1→读0→可选读1确认，完成后直至复位不能改选择集合。它适用于防误改配置，不能代替任务间同步。依据：[RM0008 §9.1.2；§9.2；§9.2.4–§9.2.6](../来源/RM0008.md#src-rm0008-r21-gpio-atomic)；[RM0008 §9.1.6；§9.2.7](../来源/RM0008.md#src-rm0008-r21-gpio-lock)。

HAL 接入细节见[GPIO 与 EXTI 调用边界](../参数/HAL_GPIO与EXTI调用边界.md)。固定版本 HAL_GPIO_Init 不清 EXTI 挂起、不配置 NVIC；共享 IRQ 的 HAL 处理函数也不会自动把复合掩码逐位分发。

## 2 AFIO重映射与内部复用冲突要分开检查

全部外设角色、重映射与AFIO字段见[引脚复用与AFIO](../参数/引脚复用与AFIO.md)；十条内部复用冲突完整条件见[GPIO内部复用冲突](../参数/GPIO内部复用冲突.md)。

先确认目标脚在LQFP48引出，再确认调试/晶体释放，最后核查ES096的内部冲突。C8的PD0/PD1可在HSE关闭后借用OSC_IN/OUT，但没有对应EXTI能力；用作输出时，DS5319引脚表脚注限定只能选择50 MHz输出模式（MODE=11），不能套用普通GPIO的2/10 MHz档位，这也不保证实际负载下能产生50 MHz波形；TIM3全映射、TIM4映射和TIM1全映射等指向缺失端口的方案不可用。

SPI1映射至PA15/PB3/PB4/PB5还需释放相关JTAG脚。依据：[RM0008 §9.3.1–§9.3.3；§9.4.2](../来源/RM0008.md#src-rm0008-r21-gpio-pd01)；[RM0008 §9.3.6–§9.3.10；§9.4.2](../来源/RM0008.md#src-rm0008-r21-gpio-remap)；[DS5319 §3 Pinouts and pin description](../来源/DS5319.md#src-ds5319-r20-gpio-pin)。

### 2.1 调试引脚的释放

AFIO_MAPR的SWJ_CFG只写且读值未定义。普通整字读改写可能破坏已有调试选择；应由一个配置所有者维护软件影子，或每次明确写期望SWJ_CFG并保留其他所需位。SWJ_CFG=001保留完整JTAG/SWD但禁用NJTRST，只释放PB4；PA13、PA14、PA15及PB3仍由调试口占用。

010关闭JTAG而保留PA13/14的SWD，释放PA15及PB4；PB3仅在不用异步SWO时释放。100关闭全部SWJ。编码及释放条件见RM0008 Rev 21 §9.3.5 Table 37及note 1，p177；字段只写语义见§9.4.2 p184。依据：[RM0008 §9.3.5；§9.4.2](../来源/RM0008.md#src-rm0008-r21-gpio-swj)；[RM0008 §9.4；§9.4.1–§9.4.6](../来源/RM0008.md#src-rm0008-r21-gpio-afio)。

### 2.2 内部复用冲突

| 已核查并用风险 | 工程后果 |
|---|---|
| I²C1与重映射SPI1主机同时有时钟 | PB5受SMBA内部输出干扰，即使没有使用告警；不能只改GPIO消除 |
| I²C1与重映射TIM3_CH2并用 | PB5不能作该PWM输出；勘误只允许相应输入组合 |
| 只接收USART，TE=0 | 内部TX仍可能保持高，不能因此把TX复用脚交给另一输出 |
| USART1与TIM1_CH2涉及PA9 | TIM1部分重映射仍在PA9；全映射到PE11在C8不可用，不能照搬规避 |

这些是选定风险，全部条件见[ES096 §2.3.1–§2.3.10](../来源/ES096.md#src-es096-r15-gpio-conflicts)。USART1_RTS/CAN冲突的专门规避中，ES096允许在CAN不用时用CAN_REMAP=01这一未用配置；它不是一般CAN功能映射的合法选项，也不授权其他“保留编码试一试”。PA9条款还存在标题/正文表述差异，且原修订矩阵漏列，不能自补“所有版本已修复/未修复”的结论，见[ES096 §2.3.1–§2.3.10](../来源/ES096.md#src-es096-r15-gpio-conflicts)。

## 3 EXTI的路由 屏蔽和挂起不是同一层

[EXTI寄存器与路由](../参数/EXTI寄存器与路由.md)保留六寄存器、边沿写入窗口与19条线边界；[C8完整外部向量表](../参数/C8外部向量表.md)保留IRQ0～42。

C8有EXTI0～18：0～15各从同号GPIO选一个来源，16/17/18固定为PVD/RTC Alarm/USB Wakeup。因此PA0和PB0不能各自独占一条EXTI0，PC仅有13～15可选，PD0/1不可用。EXTI5～9和10～15分别共享NVIC入口，ISR必须区分所有可能来源。依据：[RM0008 §10.2；§10.2.2–§10.2.5；§9.3.2；§9.4.3–§9.4.6](../来源/RM0008.md#src-rm0008-r21-exti-route)、[RM0008 §10.1](../来源/RM0008.md#src-rm0008-r21-exti-vector)。

![RM0008 Rev21 Figure20，p207：EXTI中断和事件路径原图](../assets/manual/rm0008-r21/p207-gpio-exti.png)

来源：ST RM0008 Rev21 Figure20，p207；原图裁切，未改动连线或补画寄存器接口。

上支路先经Interrupt mask再到Pending request register；下支路经Event mask产生事件脉冲。IMR与EMR独立：纯事件需EMR=1且IMR=0；两者都开可同时产生事件和中断，不能沿用“无需清pending”的简化说法。

### 3.1 初始化顺序

初始化顺序为：配置输入及AFIO路由→选择RTSR/FTSR边沿→清遗留PR→放行IMR或EMR→按中断需要设置并使能NVIC。EXTI_PR在细节定义与汇总表中有复位值矛盾，保守地显式清目标位。RTSR写入期间到达的上升沿、FTSR写入期间到达的下降沿可能丢失，不宜靠动态反复改边沿进行无损计数。

### 3.2 挂起标志的清除

EXTI_PR为写1清，直接写要清的掩码；PR读改写会把读到的其他1一起清掉，尤其容易损坏共享IRQ处理。IMR屏蔽新边沿所在的中断锁存路径，不能假定被屏蔽期间所有边沿都排队；已有PR也不会仅因改掩码自动清除。只在NVIC禁止IRQ则仍可保留请求挂起，是另一种行为。EXTI软件请求重复前也要清PR使SWIER回0。依据：[RM0008 §10.3–§10.3.7](../来源/RM0008.md#src-rm0008-r21-exti-reg)。

低功耗还必须叠加ES096：PVD和USB Wakeup不能走WFE事件唤醒，WFE前中断也有事件寄存器竞态。实际入口与清理顺序见[时钟复位与低功耗](https://github.com/Bit-Walker/stm32f103c8-knowledge-base/blob/main/知识库/02_时钟复位与低功耗.md#4-低功耗选择由状态保持和唤醒源决定)，不能仅凭通用EXTI图决定可用唤醒方案。

## 4 NVIC优先级必须贯通到临界区

相关字段布局与参数见[内核寄存器参数](../参数/内核寄存器参数.md)及[异常与屏蔽参数](../参数/异常与屏蔽参数.md)。

C8有43个外部IRQ，编号0～42；异常号为IRQ编号加16，向量表首项则是初始MSP。STIR写外部IRQ编号，不加16；系统异常不能套用外部IRQ接口。单个pending位不会累计次数，清NVIC pending不清active，也不替代撤销外设中断源。只读外设数据是否自动清标志，要按外设章节，不能对所有ISR套用统一模板。依据：[RM0008 §10.1](../来源/RM0008.md#src-rm0008-r21-exti-vector)、[PM0056 §4.3.2–4.3.6；§4.3.8–4.3.10](../来源/PM0056.md#src-pm0056-r7-nvic-state)。

### 4.1 优先级分组

优先级逻辑范围0～15，数值小更紧急。直接寄存器优先级在字节高4位，CMSIS SetPriority参数却是未左移的逻辑值；重复左移会配错。先定PRIGROUP，再编码各IRQ，再使能。抢占级决定能否打断，子优先级只排序同组等待；HAL的GROUP命名不要当PRIGROUP原始数值。

依据：[PM0056 §2.3.5–2.3.6；§4.3.7；§4.4.5](../来源/PM0056.md#src-pm0056-r7-priority)；[core_cm3_cmsis590.h 对应来源副本行号](../来源/驱动实现.md#src-cmsis590-cm3)；[stm32f103xb.h 对应来源副本行号](../来源/驱动实现.md#src-stm32f103xb-core)、[PM0056 §2.3.5–2.3.6；§4.3.7；§4.4.5](../来源/PM0056.md#src-pm0056-r7-priority)；[stm32f1xx_hal_cortex.h 对应来源副本行号](../来源/驱动实现.md#src-hal-cortex-group-snapshot)。

补充分组对照（C8的4个实现位；HAL名字不是AIRCR原始编码）：

| HAL分组名 | PRIGROUP原始值 | 抢占位数/级数 | 子优先级位数/级数 |
|---|---|---|---|
| GROUP_0 | 7 | 0/1 | 4/16 |
| GROUP_1 | 6 | 1/2 | 3/8 |
| GROUP_2 | 5 | 2/4 | 2/4 |
| GROUP_3 | 4 | 3/8 | 1/2 |
| GROUP_4 | 3 | 4/16 | 0/1 |

表中0位写“1种编码”仅表示没有可区分的该类优先级，不代表存在一位。依据PM0056 Rev7 Table45、UM1850 Rev3 §10.1.4和[HAL分组宏快照](../来源/驱动实现.md#src-hal-cortex-group-snapshot)。

### 4.2 屏蔽与临界区

| 屏蔽机制 | 能力和边界 |
|---|---|
| NVIC单路禁止 | 阻止该IRQ激活，不自动清挂起 |
| PRIMASK | 阻止可配置异常激活，不屏蔽NMI/HardFault |
| BASEPRI | 非零按组优先级阈值屏蔽；0表示无此屏蔽，不能按同组子优先级细分 |
| FAULTMASK | 除NMI外均可屏蔽，具有额外上下文约束，不作为普通临界区工具 |

临界区保存并恢复原屏蔽状态，不能退出时无条件开中断。进入嵌套临界区时也不能把已有BASEPRI改成更弱屏蔽；需要只增强门槛时，可依据BASEPRI_MAX语义设计入口，再恢复保存值。这是工程建议，须结合RTOS和特权上下文核验。

BASEPRI写值要按寄存器编码，阈值子优先级部分宜为0。volatile既不让多次访问原子，也不代替内存屏障：DMB处理顺序，DSB等待先前操作完成，ISB刷新后续执行上下文，三者不能互换。依据：[PM0056 §2.1.3 Core registers；§3.9.2；§3.9.6–3.9.7](../来源/PM0056.md#src-pm0056-r7-mask)；[ARM DDI0403E.b §B1.5.4 Exception priorities and preemption，pB1-583,B1-584,B1-585](../来源/Arm_DDI0403Eb.md#src-armv7m-eb-mask)、[PM0056 §2.2.4；§3.9.3–3.9.5](../来源/PM0056.md#src-pm0056-r7-barriers)。

### 4.3 向量表迁移

向量迁移前先完整准备MSP、NMI、故障和所有已启用入口，地址必须落在实际Flash/SRAM。沿用本库PM0056的0x200字节保守对齐约定，并处理DSB/ISB；这不是声称所有Cortex-M3架构均只能512字节对齐。

异常入口最低位要为1以指示Thumb。AIRCR写分组/复位还必须带0x05FA钥匙，不能将读回的0xFA05用普通读改写送回。依据：[PM0056 §2.3.4；§4.3.10；§4.4.4](../来源/PM0056.md#src-pm0056-r7-vtor)；[PM0056 §2.2.4；§3.9.3–3.9.5](../来源/PM0056.md#src-pm0056-r7-barriers)；[ARM DDI0403E.b §B1.5.3 The vector table，pB1-581,B1-582](../来源/Arm_DDI0403Eb.md#src-armv7m-eb-vector)、[PM0056 §2.3.5–2.3.6；§4.3.7；§4.4.5](../来源/PM0056.md#src-pm0056-r7-priority)；[stm32f1xx_hal_cortex.h 对应来源副本行号](../来源/驱动实现.md#src-hal-cortex-group-snapshot)。

## 5 SysTick既是时基也是有副作用的寄存器

[SysTick接口参数](../参数/SysTick接口参数.md)保留UM1850参数文字与固定CMSIS实现差异。

SysTick 周期与重装值的关系为：

$$
T=\frac{R+1}{f_{\mathrm{ST}}},\qquad R=f_{\mathrm{ST}}T-1
$$

$T$ 为重复周期，单位 s；$R$ 为 LOAD 寄存器中的无量纲整数；$f_{\mathrm{ST}}$ 为 SysTick 时钟频率，单位 Hz，可来自 HCLK 或 HCLK/8，下标 ST 表示 SysTick。

持续周期计数要求 $R$ 为 1～0xFFFFFF。LOAD=0 没有正常的 1→0 转换。生成 1 ms 周期时：

- 使用 72 MHz HCLK：$R=71999$。
- 使用 HCLK/8：$R=8999$。

依据：[PM0056 §4.5–4.5.6、§4.4.3](../来源/PM0056.md#src-pm0056-r7-systick)。

初始化或重配置前先协调时基所有者；为避免中途计数跨越新旧配置，可先停止SysTick，再按“写LOAD→写VAL清当前计数→必要时清旧挂起→配置优先级→写CTRL”处理。HAL_SYSTICK_Config传的是周期时钟数R+1，并会选HCLK、设最低优先级等，不能把LOAD值直接传入；HAL/RTOS已占用时不可另行随意重配。

依据：[UM1850 §10.1.1；§10.1.4；§10.2.1](../来源/UM1850.md#src-um1850-r3-cortex)；[core_cm3_cmsis590.h 对应来源副本行号](../来源/驱动实现.md#src-cmsis590-cm3)；[stm32f103xb.h 对应来源副本行号](../来源/驱动实现.md#src-stm32f103xb-core)；[stm32f1xx_hal_cortex.c 对应来源副本行号](../来源/驱动实现.md#src-hal-cortex-snapshot)。

### 5.1 读取和写入的副作用

读CTRL会清COUNTFLAG，写VAL任意值也会清当前值及COUNTFLAG；这些动作都不等于清已挂起SysTick异常。调试器实时查看CTRL可能改变软件之后观察到的结果。CALIB的9000来自最大HCLK/8=9 MHz时约1 ms尺度，不自动跟随当前时钟，也不能凭TENMS名字当10 ms；SKEW、复位字值在源文有冲突，按已知时钟计算周期并核验实际标志。

依据：[PM0056 §4.5–4.5.6；§4.4.3](../来源/PM0056.md#src-pm0056-r7-systick)、[PM0056 §4.5.4；§4.5.6](../来源/PM0056.md#src-pm0056-r7-calib-conflict)；[RM0008 §10.1.1 SysTick calibration value register](../来源/RM0008.md#src-rm0008-r21-systick-calib)。

SysTick与故障观察的访问副作用不能混用：

| 对象 | 对齐/访问宽度 | 读操作 | 写操作及边界 |
|---|---|---|---|
| SysTick CTRL | 对齐32位 | 读取会清COUNTFLAG | 只设置控制字段；不能靠此清异常pending |
| SysTick VAL | 对齐32位 | 读取当前计数 | 任意值清当前计数及COUNTFLAG，不清异常pending |
| ICSR.PENDSTCLR | ICSR对齐32位 | 该位只写，读值未知 | 写1清SysTick pending；应直接写目标动作位掩码 |
| CFSR | 字节、对齐16/32位 | 正常读取，不清故障位 | 故障状态W1C；保留位写0 |
| HFSR | 对齐32位 | 正常读取，不清故障位 | 目标故障状态W1C；DEBUG_VT及保留位保持0 |
| MMFAR/BFAR | 对齐32位 | 取地址后再核相应VALID位 | 不是清故障状态的接口 |

依据：[PM0056 §4.5–4.5.6；§4.4.3](../来源/PM0056.md#src-pm0056-r7-systick)、[PM0056 §2.4；§4.4.9–4.4.14](../来源/PM0056.md#src-pm0056-r7-fault-evidence)、[Arm Cortex-M3 TRM DDI0337E §8.2.2 NVIC register descriptions / Configurable Fault Status Registers](../来源/Arm_DDI0337E.md#src-arm-cm3-r1p1-fault-w1c)。CFSR的三个子字段可分别在0xE000ED28读字节MMFSR、0xE000ED29读字节BFSR、0xE000ED2A读半字UFSR。

实现边界：与官方commit 77fbb30b7a1d02533980400083e48c559aae5a4f逐字节相同的HAL Cortex C文件中，HAL_SYSTICK_CLKSourceConfig读改写CTRL；结合上表可推得调用会消耗COUNTFLAG。这是[固定HAL Cortex C实现](../来源/驱动实现.md#src-hal-cortex-snapshot)与寄存器语义的推导，不是所有HAL版本已逐版证明。修改时钟源后也要重新核对LOAD与期望周期。

## 6 故障现场先取证 再决定是否清除

异常硬件帧保存R0～R3、R12、LR、PC、xPSR共8字，R4～R11不在其中。Handler使用MSP，但被中断线程的帧可能在PSP；用入口LR的EXC_RETURN判断：0xFFFFFFF1返回Handler/MSP，0xFFFFFFF9返回Thread/MSP，0xFFFFFFFD返回Thread/PSP。还要考虑对齐填充与入栈故障，不能一律拿当前C函数SP当原始帧。依据：[PM0056 §2.1.1–2.1.3；§2.3.7](../来源/PM0056.md#src-pm0056-r7-exception-frame)。

### 6.1 故障状态判读

| 证据 | 解释边界 |
|---|---|
| HFSR.FORCED | 可配置故障升级，继续查CFSR根因 |
| HFSR.VECTTBL | 取向量失败，压栈PC是被打断处，不是损坏向量地址 |
| PRECISERR / IMPRECISERR | 前者可用压栈PC定位；后者异步，PC不必指向出错写操作 |
| BFARVALID / MMARVALID | 地址有效前提；未置位不能采用寄存器旧值 |
| STKERR / UNSTKERR等 | 入栈/出栈失败，不能无条件信任完整帧 |

按PM0056 §4.4.14，先保存MMFAR/BFAR，再读对应有效位；有效位为1才采用地址。该顺序是原厂针对抢占风险给出的取证要求，并不保证CFSR、HFSR、地址和栈帧构成不可分割的同一时刻快照；仍须协调会改写状态的更高优先级故障处理程序。

记录CFSR、HFSR、SHCSR、栈选择和可验证帧后再清状态。CFSR/HFSR相关故障位正常读取、写1清，不能当读清，也不能普通写0清零；写HFSR只针对目标故障位，DEBUG_VT及保留位保持0。C8无可编程MPU、无硬件浮点协处理器，但仍有固定执行/特权限制；NOCP或MemManage字段不证明相应硬件存在。依据：[PM0056 §2.4；§4.4.9–4.4.14](../来源/PM0056.md#src-pm0056-r7-fault-evidence)；[Arm Cortex-M3 TRM DDI0337E §8.2.2 NVIC register descriptions / Configurable Fault Status Registers](../来源/Arm_DDI0337E.md#src-arm-cm3-r1p1-fault-w1c)；[stm32f103xb.h 对应来源副本行号](../来源/驱动实现.md#src-stm32f103xb-core)、[PM0056 §2.4；§4.4.9–4.4.14](../来源/PM0056.md#src-pm0056-r7-fault-evidence)。


## 7 调试应保留恢复入口 并承认观察会改变系统

调试引脚、ID、传输、跟踪及冻结字段见[调试寄存器与协议](../参数/调试寄存器与协议.md)。

复位后五个SWJ脚立即交给调试逻辑，应用释放前外部电路应容忍其偏置/三态。固件很快关闭SWD或进入低功耗时，用连接NRST的复位下连接流程，在释放复位前设置复位捕获；这不是绕过读保护的方法。调试组件也并非所有字段只受上电复位，DHCSR.C_HALT及部分DEMCR位还有系统复位规则。

依据：[RM0008 §31.3–§31.4.4](../来源/RM0008.md#src-rm0008-r21-debug-pins)、[RM0008 §31.10–§31.11](../来源/RM0008.md#src-rm0008-r21-debug-reset)；[DDI0337E §10.1 Table10-1；§10.2.1；§10.2.4](../来源/Arm_DDI0337E.md#src-ddi0337e-debug-state)。

C8可用6个指令比较器、2个literal比较器及4个DWT比较器；断点/补丁会争同一FPB资源。PB3异步SWO需SWD模式，不能把ITM/DWT跟踪当ETM完整指令轨迹，也没有PE2～6同步Trace口。

ITM输出满或调试器不在时要避免无限等待。依据：[RM0008 §31.12–§31.14.4](../来源/RM0008.md#src-rm0008-r21-debug-fpb-dwt-itm)；[DDI0337E §11.6.1 ITM Stimulus Ports 0–31及TPR](../来源/Arm_DDI0337E.md#src-ddi0337e-itm-fifo)；[RM0008 §31.1；§31.4；§31.15；§31.17.2；§31.17.7–§31.17.9](../来源/RM0008.md#src-rm0008-r21-debug-trace)；[DS5319 §3 Table5](../来源/DS5319.md#src-ds5319-r20-debug-package)；[DDI0337E §11.5.1；§13.2.2](../来源/Arm_DDI0337E.md#src-ddi0337e-trace-boundary)。

停核不等于全部外设停止。按需求设置定时器、看门狗、CAN接收更新等冻结位；TIM1冻结时输出有安全关断行为，会改变PWM实验。DHCSR的S_RESET_ST、S_RETIRE_ST是读清粘滞位，反复观察也会消耗证据；持续处于复位时，S_RESET_ST连续读取仍可为1。

DBGMCU_IDCODE/CR的脱机CPU访问受C8勘误限制，读0不能诊断成芯片型号0。依据：[RM0008 §31.16.2–§31.16.3；§31.18](../来源/RM0008.md#src-rm0008-r21-debug-freeze)；[ES096 §2.2.2–§2.2.4；§1 Table3](../来源/ES096.md#src-es096-r15-debug-access)、[RM0008 §31.10–§31.11](../来源/RM0008.md#src-rm0008-r21-debug-reset)；[DDI0337E §10.1 Table10-1；§10.2.1；§10.2.4](../来源/Arm_DDI0337E.md#src-ddi0337e-debug-state)、[RM0008 §31.6.1–§31.6.4](../来源/RM0008.md#src-rm0008-r21-debug-id)；[ES096 §2.2.2–§2.2.4；§1 Table3](../来源/ES096.md#src-es096-r15-debug-access)；[ES096 首页Applicability及Tables1–2；§1 Tables3–4](../来源/ES096.md#src-es096-r15-revision-matrix)。

### 7.1 调试探针的协议约束

若开发的是调试探针，还需遵守SWD的posted AP读、RDBUFF取末次结果、WAIT/FAULT条件性数据阶段、至少两个写后空闲时钟及上电ACK确认；总线事务OK不等于电源域已经就绪。Park位在原RM与后续ADIv5规范有差异，直接沿用已核查[RM0008 §31.8.1–§31.8.5](../来源/RM0008.md#src-rm0008-r21-swd-protocol)；[IHI0031A §5.2–§5.4.5](../来源/IHI0031A.md#src-ihi0031a-swd-protocol)；[IHI0031D §B4.2，pB4-110](../来源/IHI0031D.md#src-ihi0031d-swd-park)；[IHI0031A §3.4.1–§3.4.2](../来源/IHI0031A.md#src-ihi0031a-power-ack)的版本辨析，不能自行拼接不同规范的时序。

## 8 按故障层次缩小定位范围

[硅修订矩阵](../参数/硅修订矩阵.md)保留ES096 Tables1–4对应状态与缺项。

引脚无输出先看电源/实际脚和IDR，再看模式、SWJ/晶体占用、MAPR写入及ES096内部冲突；不要一开始只改ODR。ISR不来按“外设源→EXTI路由/掩码→PR→NVIC使能/挂起→优先级/屏蔽→向量入口”逐层取证；反复重入先确认源是否真正撤销。只在调试器下失败或成功，则核对读清副作用、冻结/低功耗调试位和复位窗口。涉及硅规避时回查[ES096 首页Applicability及Tables1–2；§1 Tables3–4](../来源/ES096.md#src-es096-r15-revision-matrix)，保留版本条件，避免把摘要当作无条件保证。
