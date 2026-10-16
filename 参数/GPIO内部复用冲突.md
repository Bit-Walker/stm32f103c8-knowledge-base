# GPIO内部复用冲突

排查复用输出异常时，除引脚映射外，还要核对共享外设的时钟和工作模式。以下按引脚列出 [ES096 Rev15 §2.3.1～§2.3.10](../来源/ES096.md#src-es096-r15-gpio-conflicts) 的十条限制，印刷页与 PDF 文件页均为 pp10～13。

“有时钟”是条款中的外设时钟条件，不代表相关信号一定被使用。例如 SMBA（SMBus 告警信号）未使用、USART 仅接收，仍可能占用内部输出；PA12 的 CAN 冲突甚至发生在 CAN 无时钟时。各条的条件必须一起判断，不能把这些具体冲突概括成所有外设通用的优先级表。

| 原条款/页 | 涉及资源 |
|---|---|
| [§2.3.1 p10](#231-pa12) | PA12：USART1_RTS 与 CAN_TX |
| [§2.3.2 pp10–11](#232-pa4) | PA4：SPI1 从机与 USART2_CK |
| [§2.3.3 p11](#233-pa4) | PA4：SPI1 主机与 USART2_CK |
| [§2.3.4 p11](#234-pb12) | PB12：SPI2 从机与 USART3_CK |
| [§2.3.5 p11](#235-pb12) | PB12：SPI2 主机与 USART3_CK |
| [§2.3.6 pp11–12](#236-pb12) | PB12：I2C2_SMBA 与 SPI2_NSS、USART3_CK |
| [§2.3.7 p12](#237-pb5) | PB5：I2C1_SMBA 与重映射 SPI1_MOSI |
| [§2.3.8 p12](#238-pb5) | PB5：I2C1_SMBA 与重映射 TIM3_CH2 |
| [§2.3.9 pp12–13](#239-usartx_tx) | USARTx_TX 与其他复用输出 |
| [§2.3.10 p13](#2310-pa9) | PA9：USART1 Tx 与 TIM1_CH2 |

## 2.3.1 PA12

涉及 USART1_RTS（USART1 硬件流控输出）和 CAN_TX（CAN 发送输出）。

- **同时成立的条件：** USART1有时钟；CAN无时钟；PA12为复用输出
- **后果：** 即使不用CAN_TX，内部CAN_TX默认1，USART1_RTS不可用
- **原厂规避及边界：** 使用USART1_RTS时：若也用CAN，CAN移到另一I/O配置；若不用CAN，CAN_REMAP=01未用配置。01仅是该条明确规避，不是CAN正常映射

## 2.3.2 PA4

USART2_CK 是 USART2 同步模式的时钟输出。

- **同时成立的条件：** SPI1与USART2均有时钟；PA4为复用输出；SPI1从机
- **后果：** USART2同步CK不能使用
- **原厂规避及边界：** 无规避

## 2.3.3 PA4

NSS 是 SPI 的片选信号；SSOE 是 SPI_CR2 中的 NSS 输出使能位；SSM 是 SPI_CR1 中的软件从机管理位。

- **同时成立的条件：** SPI1与USART2均有时钟；PA4为复用输出；SPI1主机且NSS软件管理
- **后果：** USART2_CK不输出，不能用于同步模式
- **原厂规避及边界：** 要输出USART2_CK，置SPI1_CR2.SSOE，使SPI1 NSS配置为输出；原条款只明确要求SSOE置位，不额外推定SSM配置步骤

## 2.3.4 PB12

USART3_CK 是 USART3 同步模式的时钟输出。

- **同时成立的条件：** SPI2与USART3均有时钟；PB12为复用输出；SPI2从机
- **后果：** USART3同步CK不能使用
- **原厂规避及边界：** 无规避

## 2.3.5 PB12

这里的 NSS 为 SPI2 片选信号，SSOE 为 SPI2_CR2 中的 NSS 输出使能位。

- **同时成立的条件：** SPI2与USART3均有时钟；PB12为复用输出；SPI2主机且NSS软件管理
- **后果：** USART3_CK不输出，不能用于同步模式
- **原厂规避及边界：** 要输出USART3_CK，置SPI2_CR2.SSOE，使SPI2 NSS配置为输出

## 2.3.6 PB12

I2C2_SMBA 是 SMBus Alert（SMBus 告警）信号；SPI2_NSS 为片选信号，USART3_CK 为同步时钟输出。

- **同时成立的条件：** I2C2与SPI2同时有时钟，或I2C2与USART3同时有时钟；PB12为复用输出
- **后果：** 即使未用SMBA，I2C2_SMBA仍与SPI2_NSS输出或USART3_CK冲突；该AF输出且I2C2有时钟时PB12默认1
- **原厂规避及边界：** I2C2_SMBA作为输出：SPI2必须主机且NSS软件管理；I2C2_SMBA作为输入：SPI2可主/从机，但NSS须软件管理。I2C2使用中，SPI2不得用其他配置；USART3不得用同步模式

## 2.3.7 PB5

重映射后的 SPI1_MOSI（主机发送、从机接收的数据线）与 I2C1_SMBA（SMBus 告警）共用 PB5。

- **同时成立的条件：** I2C1与SPI1均有时钟；SPI1已重映射；PB5为复用输出；条款限定重映射SPI1主机
- **后果：** SPI1_MOSI与I2C1_SMBA内部冲突，即使SMBA未用
- **原厂规避及边界：** 不并用I2C1和重映射SPI1主机；原workaround进一步写明使用重映射SPI1时关闭I2C1时钟。不得只靠GPIO重配消除

## 2.3.8 PB5

TIM3_CH2 是定时器 3 的通道 2；此条涉及重映射至 PB5 后，与 I2C1_SMBA（SMBus 告警）的冲突。

- **同时成立的条件：** I2C1与TIM3均有时钟；PB5为复用输出（对应重映射TIM3_CH2）
- **后果：** I2C1_SMBA即使未使用仍冲突，PB5默认1；TIM3_CH2输出不可用
- **原厂规避及边界：** TIM3_CH2仅可使用输入模式

## 2.3.9 USARTx_TX

TX 表示发送输出；TE 是 USARTx_CR1 的发送器使能位，TE=0 表示关闭发送器；AF 表示复用功能。

- **同时成立的条件：** USART仅接收，USARTx_CR1.TE=0；该USARTx_TX脚共享另一复用输出
- **后果：** 即使未使用TX，内部TX输出为1，不能输出其他AF
- **原厂规避及边界：** 不把该USARTx_TX对应引脚配置为AF输出；原workaround称仅可用输入模式，并保持TE=0。不能缩略成“TX未用所以可任意复用”

## 2.3.10 PA9

TIM1_CH2 是定时器 1 的通道 2，PWM 指脉宽调制输出模式。

- **同时成立的条件：** USART1及TIM1均有时钟；PA9为复用输出；正文写TIM1_CH2 PWM enabled without output
- **后果：** USART1 Tx(PA9)发送异常字符
- **原厂规避及边界：** 原workaround要求用TIM1_REMAP把TIM1_CH2移到其他I/O；但C8的部分映射仍PA9，全映射PE11不引出，不能提供可用C8重映射方案。标题with output与正文without output不一致，保留原差异，不自改触发条件

## 修订与封装适用性

修订适用性：[ES096 Table3](../来源/ES096.md#src-es096-r15-gpio-conflicts) pp2–3逐行列§2.3.1–9，列顺序A/B/Z/1/Y/2/3/X。§2.3.2和§2.3.4各列N，其余七条各列A；A表示限制存在且有规避，N表示限制存在且无规避，不是“已修复”。§2.3.10未列于Table3，不能补成任何修订状态。此处只摘GPIO九行，不替代其余ES096矩阵。

C8裁剪依据：[RM0008 Rev21 §9.3.7 Table46](../来源/RM0008.md#src-rm0008-r21-gpio-remap) p179（TIM1_CH2默认和部分映射PA9、全映射PE11）；[DS5319 Rev20 §3 Table5](../来源/DS5319.md#src-ds5319-r20-gpio-pin) pp28–33（LQFP48不引出PE11）。CAN映射的特殊01规避保留ES096优先，普通CAN映射表仍将01标未用。

落实重映射规避时，字段位置与 AFIO_MAPR 读改写边界见[引脚复用与 AFIO](引脚复用与AFIO.md)：SWJ_CFG（调试端口配置）为只写、读值未定义，修改重映射字段时也要明确保留期望的调试配置。
