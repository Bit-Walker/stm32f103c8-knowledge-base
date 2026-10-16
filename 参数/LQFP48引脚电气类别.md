# LQFP48 引脚电气类别与固定映射

先按物理脚号核对电气类别，再选外设功能。以下只整理 DS5319 Rev20 Table5 的 LQFP48 列；已有的[GPIO模式、复用与重映射表](引脚复用与AFIO.md)继续作为配置入口，不在这里重复。

## 物理脚号与电气类别

Type 的 I/O 表示输入/输出，I 为输入、O 为输出、S 为供电。FT 是原表明确标出的5 V容忍类别；“—”和“空白”分别保留原表短横线和空格，均不能当作FT。FT也不是任意工作状态下的接线许可，输入电压、上下拉、注入电流及BOOT0例外须联用[硬件电气参数](01_硬件电气参数.md)。

### 电源、复位与晶振相关脚

| 物理脚号 | 引脚/复位主功能 | Type | I/O Level |
|---:|---|---|---|
| 1 | VBAT | S | — |
| 2 | PC13 | I/O | — |
| 3 | PC14 | I/O | — |
| 4 | PC15 | I/O | — |
| 5 | OSC_IN | I | — |
| 6 | OSC_OUT | O | — |
| 7 | NRST | I/O | — |
| 8 | VSSA | S | — |
| 9 | VDDA | S | — |
| 23 | VSS_1 | S | — |
| 24 | VDD_1 | S | — |
| 35 | VSS_2 | S | — |
| 36 | VDD_2 | S | — |
| 44 | BOOT0 | I | 空白 |
| 47 | VSS_3 | S | — |
| 48 | VDD_3 | S | — |

PC13/14/15的复位主功能列受Table5注6约束：PC13/14/15只描述首次备份域上电；后续取决于主复位不清除的备份寄存器。其3 mA供电开关、2 MHz、30 pF及不得作电流源的完整限制见[PC13至PC15的输出限制](GPIO模式与寄存器.md#pc13-至-pc15-的输出限制)，PC14/15的LSE占用与低功耗条件见[PC14与PC15](GPIO模式与寄存器.md#pc14-与-pc15)。

5、6脚复位后是OSC_IN/OSC_OUT；软件可通过PD01_REMAP作为PD0/PD1使用。HSE占用、只能选择50 MHz输出档位及不提供EXTI的限制见[封装和路由条件](GPIO模式与寄存器.md#封装和路由条件)。不得把Table5其他封装的独立PD0/PD1行所列FT和CAN重映射搬到这两个OSC脚。

### PA端口

| 物理脚号 | 引脚/复位主功能 | Type | I/O Level |
|---:|---|---|---|
| 10 | PA0 | I/O | — |
| 11 | PA1 | I/O | — |
| 12 | PA2 | I/O | — |
| 13 | PA3 | I/O | — |
| 14 | PA4 | I/O | — |
| 15 | PA5 | I/O | — |
| 16 | PA6 | I/O | — |
| 17 | PA7 | I/O | — |
| 29 | PA8 | I/O | FT |
| 30 | PA9 | I/O | FT |
| 31 | PA10 | I/O | FT |
| 32 | PA11 | I/O | FT |
| 33 | PA12 | I/O | FT |
| 34 | PA13 / JTMS-SWDIO | I/O | FT |
| 37 | PA14 / JTCK-SWCLK | I/O | FT |
| 38 | PA15 / JTDI | I/O | FT |

PA13/14/15复位主功能分别是JTMS/SWDIO、JTCK/SWCLK、JTDI，不能仅凭“PA”名称当成已释放的GPIO。调试占用及SWJ_CFG选择见[GPIO模式与寄存器](GPIO模式与寄存器.md)。

### PB端口

| 物理脚号 | 引脚/复位主功能 | Type | I/O Level |
|---:|---|---|---|
| 18 | PB0 | I/O | — |
| 19 | PB1 | I/O | — |
| 20 | PB2 / BOOT1 | I/O | FT |
| 21 | PB10 | I/O | FT |
| 22 | PB11 | I/O | FT |
| 25 | PB12 | I/O | FT |
| 26 | PB13 | I/O | FT |
| 27 | PB14 | I/O | FT |
| 28 | PB15 | I/O | FT |
| 39 | PB3 / JTDO | I/O | FT |
| 40 | PB4 / JNTRST | I/O | FT |
| 41 | PB5 | I/O | 空白 |
| 42 | PB6 | I/O | FT |
| 43 | PB7 | I/O | FT |
| 45 | PB8 | I/O | FT |
| 46 | PB9 | I/O | FT |

PB5未标FT，不能因为相邻PB脚标FT而一并认定。PB3、PB4复位主功能为调试信号；PB4原表拼作JNTRST，现有配置页沿用RM0008的NJTRST名称，均指同一物理脚。PB3的TRACESWO用途同样须与调试配置核对。

## 不依赖重映射的功能补充

下列是现有重映射表之外的固定功能，不重复其TIM、CAN、USART数据脚与SPI1表。表中的功能互为备选，不表示可同时启用。

| 功能 | 对应引脚（物理脚号） |
|---|---|
| I2C2 SCL / SDA | PB10（21）/ PB11（22） |
| I2C1 SMBA / I2C2 SMBA | PB5（41）/ PB12（25） |
| SPI2 NSS / SCK | PB12（25）/ PB13（26） |
| SPI2 MISO / MOSI | PB14（27）/ PB15（28） |
| USART1 CK / CTS / RTS | PA8（29）/ PA11（32）/ PA12（33） |
| USB DM / DP | PA11（32）/ PA12（33） |
| MCO / WKUP | PA8（29）/ PA0（10） |
| TAMPER-RTC / OSC32_IN / OSC32_OUT | PC13（2）/ PC14（3）/ PC15（4） |

SMBA是SMBus Alert信号；这只是引脚功能定位，不代替外设配置。ADC12_IN0～IN9的PA0～PA7、PB0/PB1对应关系已列在[ADC硬件模式与事件](ADC/硬件模式与事件.md)，这里不重列。

## 共脚选择与封装边界

- Table5注4要求：多个外设共用同一I/O时，为避免复用冲突，同一时刻只通过对应RCC外设时钟使能位启用其中一个外设。GPIO模式、外设使能和重映射选择仍须共同满足；不能把表中斜线理解成同时使用。
- 注3要求按实际器件的外设资源裁剪，依据Table2；注9的“可重映射”还取决于目标脚在所用封装确实存在。具体编码继续查[通信与定时器映射](引脚复用与AFIO.md#通信定时器映射)。
- 重映射目标须以本页物理引脚表核对；参考电压接线见[硬件电气参数](01_硬件电气参数.md)。

来源：[DS5319 Rev20 Table5 pp28–33](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf#page=28)，脚注1～9见[p33](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf#page=33)；注8仅涉及其他封装，不扩展到本表。这里补齐的是物理脚号、电气分类、固定映射与选择条件，不替代完整电气参数或已有重映射配置表。
