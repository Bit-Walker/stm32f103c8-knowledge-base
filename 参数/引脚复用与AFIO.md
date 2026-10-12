# 引脚复用与AFIO

与[GPIO模式与寄存器](GPIO模式与寄存器.md)共同界定适用条件。

## 外设模式

|外设信号/用途|GPIO配置|
|---|---|
|TIM1、TIM2/3/4输入捕获、ETR；TIM1 BKIN|浮空输入|
|TIM1、TIM2/3/4输出比较/PWM；TIM1互补输出CHxN|复用推挽|
|USART TX（全双工或半双工）、CK、RTS|复用推挽；TX也允许复用开漏|
|USART RX（全双工）、CTS|浮空或上拉输入|
|USART半双工RX脚|不使用，可作GPIO|
|I2C SCL/SDA|复用开漏|
|CAN TX / RX|复用推挽 / 浮空或上拉输入|
|USB DM/DP|USB启用后自动连至内部收发器|
|ADC输入|模拟模式|
|PC13 TAMPER/RTC输出|配置BKP_CR/BKP_RTCCR后硬件强制对应引脚模式|
|MCO时钟输出|复用推挽|
|EXTI外部输入|浮空、上拉或下拉输入|

|SPI信号|配置/角色|GPIO模式|
|---|---|---|
|SCK|主机 / 从机|复用推挽 / 浮空输入|
|MOSI|全双工主机 / 全双工从机|复用推挽 / 浮空或上拉输入|
|MOSI|单线双向主机 / 单线双向从机|复用推挽 / 不使用可作GPIO|
|MISO|全双工主机|浮空或上拉输入|
|MISO|全双工从机点对点 / 多从机|复用推挽 / 复用开漏|
|MISO|单线双向主机|不使用可作GPIO|
|MISO|单线双向从机点对点 / 多从机|复用推挽 / 复用开漏|
|NSS|硬件输入主/从|浮空、上拉或下拉输入|
|NSS|主机硬件NSS输出使能|复用推挽|
|NSS|软件管理|不使用，可作GPIO|

C8无I2S、DAC、SDIO、FSMC、Ethernet、OTG，删除其引脚配置表；不能因SPI2在通用手册称SPI2/I2S而认为C8支持I2S。


原厂定位：RM0008 Rev21 §9.1.11，Table22/23 p166；Table24 pp166–167及note1；Table25 p167；Table27/28/29 p168及Table29 note1；ADC文字和Figure19 p169；Table33 p170。Table24原文使用“Half duplex synchronous mode”表述，此表沿用其半双工引脚结论，不借此定义USART协议模式。C8资源裁剪须联用DS5319 Rev20 Table2 p10。

## 通信/定时器映射

|字段|编码|信号对应|
|---|---|---|
|CAN_REMAP[1:0]|00|RX PA11；TX PA12|
|CAN_REMAP[1:0]|10|RX PB8；TX PB9|
|CAN_REMAP[1:0]|01|普通CAN功能未用；ES096 §2.3.1 p10另允许CAN不用时的USART1_RTS专门规避|
|CAN_REMAP[1:0]|11|PD0/PD1仅100/144脚支持，C8不可用|
|USART1_REMAP|0 / 1|TX PA9/RX PA10；或TX PB6/RX PB7|
|USART2_REMAP|0|CTS PA0、RTS PA1、TX PA2、RX PA3、CK PA4；重映射1至PD3～7在C8无引脚|
|USART3_REMAP|00|TX PB10、RX PB11、CK PB12、CTS PB13、RTS PB14；01/11的PC10～12或PD8～12在C8不可用；10未用|
|I2C1_REMAP|0 / 1|SCL PB6/SDA PB7；或SCL PB8/SDA PB9|
|SPI1_REMAP|0|NSS PA4、SCK PA5、MISO PA6、MOSI PA7|
|SPI1_REMAP|1|NSS PA15、SCK PB3、MISO PB4、MOSI PB5；需释放对应JTAG脚|

### 定时器

|TIM2_REMAP|CH1/ETR|CH2|CH3|CH4|
|---|---|---|---|---|
|00|PA0|PA1|PA2|PA3|
|01|PA15|PB3|PA2|PA3|
|10|PA0|PA1|PB10|PB11|
|11|PA15|PB3|PB10|PB11|

CH1和ETR共脚，不能同时使用。PA15/PB3需释放JTAG。

|TIM3_REMAP|CH1|CH2|CH3|CH4|
|---|---|---|---|---|
|00|PA6|PA7|PB0|PB1|
|10|PB4|PB5|PB0|PB1|

TIM3的01未用；11全重映射到PC6～9，C8无这些引脚，不能用。PB4需释放NJTRST。TIM4只能用未重映射PB6/7/8/9；TIM4重映射到PD12～15在C8不可用。TIM3/TIM4的ETR不随通道重映射。按 [DS5319引脚来源](../来源/DS5319.md#src-ds5319-r20-gpio-pin) 引脚定义表，TIM3_ETR在PD2、TIM4_ETR在PE0，C8 LQFP48均未引出；RM0008 §9.4.2 把TIM3_ETR也写成PE0，与该器件数据手册不一致，不能沿用。

|TIM1信号|TIM1_REMAP=00|TIM1_REMAP=01|
|---|---|---|
|ETR|PA12|PA12|
|CH1/CH2/CH3/CH4|PA8/PA9/PA10/PA11|同左|
|BKIN|PB12|PA6|
|CH1N|PB13|PA7|
|CH2N|PB14|PB0|
|CH3N|PB15|PB1|

TIM1的10未用、11全重映射到GPIOE在C8不可用。TIM5内部LSI、TIM8 ADC触发和TIM9～14重映射均无对应C8硬件，相关位保留；ADC1/2外部常规触发EXTI11、注入触发EXTI15按ADC章节选择，不能改接TIM8。


原厂定位：CAN Table34 p176及note3；TIM4 Table43 p178及封装脚注；TIM3 Table44 p178；TIM2 Table45 p179（note2明确CH1/ETR不能同时使用）；TIM1 Table46 p179；USART Tables52–54 pp180–181；I2C1 Table55 p181；SPI1 Table56 p181；映射字段§9.4.2 pp184–186。DS5319 Rev20 Table5 pp28–33决定C8 LQFP48实际脚。ADC remap适用性见Tables38–41 pp177–178；TIM5 Table42 p178。

## AFIO字段

基址0x40010000。读写前先开RCC_APB2ENR.AFIOEN，仅32位访问。复位均0，保留位保持0。

### AFIO_EVCR，0x00

bit7 EVOE（rw）=1将内核EVENTOUT接到所选脚；bits6:4 PORT（rw）为000 PA、001 PB、010 PC、011 PD，100 PE在C8无端口，其他编码不可用；bits3:0 PIN（rw）选0～15。必须选择封装实际存在且允许该功能的脚。bits31:8保留。EVENTOUT能力本来就不扩展到PF/PG。

### AFIO_MAPR，0x04

|位|字段|访问/说明|
|---|---|---|
|26:24|SWJ_CFG|只写，读值未定义；编码见调试表|
|15|PD01_REMAP|rw，1将PD0/PD1映射到OSC_IN/OUT；0不映射|
|14:13|CAN_REMAP|rw，编码见通信表|
|12|TIM4_REMAP|rw；C8保持0，1无可用封装目标|
|11:10|TIM3_REMAP|rw；C8用00或10|
|9:8|TIM2_REMAP|rw；四种均有C8引脚|
|7:6|TIM1_REMAP|rw；C8用00或01|
|5:4|USART3_REMAP|rw；C8保持00|
|3|USART2_REMAP|rw；C8保持0|
|2|USART1_REMAP|rw|
|1|I2C1_REMAP|rw|
|0|SPI1_REMAP|rw|

C8中31:27、23:16没有适用功能，保持复位值。**SWJ_CFG读未定义，不能依赖对整个MAPR的普通读改写保留调试选择。**维护软件影子或每次明确写入期望SWJ_CFG，其余字段照所需保留。

### AFIO_EXTICR1～4

|寄存器|偏移|bits3:0|bits7:4|bits11:8|bits15:12|
|---|---|---|---|---|---|
|AFIO_EXTICR1|0x08|EXTI0|EXTI1|EXTI2|EXTI3|
|AFIO_EXTICR2|0x0C|EXTI4|EXTI5|EXTI6|EXTI7|
|AFIO_EXTICR3|0x10|EXTI8|EXTI9|EXTI10|EXTI11|
|AFIO_EXTICR4|0x14|EXTI12|EXTI13|EXTI14|EXTI15|

每字段rw，0000=PA、0001=PB、0010=PC、0011=PD；原全系列还有PE/PF/PG编码，C8不使用。bits31:16保留。仅能选择实际引脚；PC仅13～15，C8的PD0/1没有此EXTI功能。每条EXTIn只选一个端口的同号脚，PA0与PB0不能同时独立触发EXTI0。AFIO_MAPR2属于带额外定时器的其他型号，C8不实现适用字段，本章不提供可写配置。


原厂定位：§9.4 p183（时钟及访问宽度）；§9.4.1 p183（EVCR）；§9.4.2 pp184–186（非互联型MAPR）；§9.4.3–6 pp191–192（EXTICR）；§9.4.7 pp193–194（MAPR2属于额外资源）。不把互联型pp187–190位图抄入C8。


[RM0008 §9.1；§9.1.1；§9.1.7–§9.1.10；§9.2.1–§9.2.3，p159,160,161,163,164,165,166,171,172,194](../来源/RM0008.md#src-rm0008-r21-gpio-mode)；[RM0008 §9.1.2；§9.2；§9.2.4–§9.2.6，p161,162,171,173,174](../来源/RM0008.md#src-rm0008-r21-gpio-atomic)；[RM0008 §9.1.6；§9.2.7，p162,174,175](../来源/RM0008.md#src-rm0008-r21-gpio-lock)；[RM0008 §9.1.3–§9.1.5；§9.1.9；§9.1.11，p162,164,165,166,167,168,169,170](../来源/RM0008.md#src-rm0008-r21-gpio-af-input)；[RM0008 §9.3.1–§9.3.3；§9.4.2，p175,176,185](../来源/RM0008.md#src-rm0008-r21-gpio-pd01)；[RM0008 §9.3.5；§9.4.2，p176,177,184](../来源/RM0008.md#src-rm0008-r21-gpio-swj)；[RM0008 §9.3.6–§9.3.10；§9.4.2，p177,178,179,180,181,184,185,186](../来源/RM0008.md#src-rm0008-r21-gpio-remap)；[RM0008 §9.4；§9.4.1–§9.4.6，p183,184,185,186,191,192](../来源/RM0008.md#src-rm0008-r21-gpio-afio)；[DS5319 §3 Pinouts and pin description，p28,29,30,31,32,33](../来源/DS5319.md#src-ds5319-r20-gpio-pin)；[ES096 §2.3.1–§2.3.10，p10,11,12,13](../来源/ES096.md#src-es096-r15-gpio-conflicts)；[RM0008 §10.2；§10.2.2–§10.2.5；§9.3.2；§9.4.3–§9.4.6，p175,191,192,207,208,209,210](../来源/RM0008.md#src-rm0008-r21-exti-route)；[RM0008 §10.3–§10.3.7，p211,212,213,214](../来源/RM0008.md#src-rm0008-r21-exti-reg)；[RM0008 §10.1，p204,205,206](../来源/RM0008.md#src-rm0008-r21-exti-vector)
