# DS5319：I²C与SPI电气时序来源

固定依据：DS5319 Rev20（2025-07），STM32F103x8/xB。[官方PDF](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf)。线上同名文件可能更新，下面校验值标识本次实际读取副本，不表示重新下载并与当前线上文件逐字节比对。

- PDF SHA-256：`1e54ce18e6c34c5b4a78986f26e245e143748c721009fc9af5953795c30686bc`
- 本次引用的PDF文件页与印刷页均对应：11、12、38、68、69、70、71、72、104。
- 固定副本共114个PDF页，正文页脚多为`/115`；本记录不据此认证全文件完整性。
- 两篇整理：[I²C电气时序、上拉与负载](../参数/I2C/电气时序与上拉负载.md)、[SPI电气时序与主从约束](../参数/SPI电气时序与主从约束.md)。

## SRC-DS5319-R20-I2C-ELECTRICAL

原位置：§5.3.16，Table41 p68及全部注1–4；Figure32 p69及全部注1–2；Table42 p69及全部注1–2。保留开漏PMOS结构限制，标准/快速模式数值、未列边界、时钟条件、数据保持条件和滤波脚注；表42单独列出固定供时、电压、Rp与频率容差。

### Table41原行到整理位置

表内Min/Max次序均保留；上升/下降的合并符号不遗漏任何一根线。

| 原行/符号 | 整理位置 | 核对内容 |
|---|---|---|
| tw(SCLL) | I²C §3.1 | 标准4.7/未列；快速1.3/未列，µs |
| tw(SCLH) | I²C §3.1 | 标准4.0/未列；快速0.6/原格空白，µs |
| tsu(SDA) | I²C §3.1 | 标准250/未列；快速100/未列，ns |
| th(SDA) | I²C §3.1 | 标准未列/3450；快速未列/900，ns；注3 |
| tr(SDA)、tr(SCL) | I²C §2 | 标准未列/1000；快速未列/300，ns |
| tf(SDA)、tf(SCL) | I²C §2 | 两模式均未列/300，ns |
| th(STA) | I²C §3.2 | 标准4.0/未列；快速0.6/未列，µs |
| tsu(STA) | I²C §3.2 | 标准4.7/未列；快速0.6/未列，µs |
| tsu(STO) | I²C §3.2 | 标准4.0/未列；快速0.6/未列，µs |
| tw(STO:STA) | I²C §3.2 | 标准4.7/未列；快速1.3/未列，µs |
| Cb | I²C §2 | 两模式均未列/400，pF |
| tSP | I²C §2 | 两模式均0/50，ns；注4 |
| 注1 | I²C §1 | 设计规定、未经生产测试 |
| 注2 | I²C §1、§4 | PCLK1至少2/4 MHz；400 kHz时为10 MHz整数倍 |
| 注3 | I²C §3.1 | 不延长SCL低电平时的最大保持时间条件 |
| 注4 | I²C §2 | 原意保留，未擅自推导必滤/不滤区间 |

Table41注4原句为“The minimum width of the spikes filtered by the analog filter is above tSP(max).” 本次没有改写其方向、删去该注或借用其他版本替换。

### Table42原行到整理位置

I²C §4按升序列出全部六行：20→0x0384、50→0x0168、100→0x00B4、200→0x803C、300→0x8028、400→0x801E；频率单位kHz。表头固定条件fPCLK1=36 MHz、VDD_I2C=3.3 V、Rp=4.7 kΩ完整保留。注1的Rp/fSCL定义与注2的约200 kHz±5%、其余范围±2%、外部元件精度条件均位于同节。表42未单列保证类型，不套用表41设计规定注。

## SRC-DS5319-R20-SPI-ELECTRICAL

原位置：§5.3.16，Table43 p70及前文与全部注1–3；Figures33–34 p71、Figure35 p72。SPI1/APB2与SPI2/APB1挂接依据Figure1 p11；时钟分配路径依据Figure2 p12。默认测试条件引用Table9 p38；重组页仅选录与C8T6相关的电源、总线频率、封装功耗和等级6温区，不宣称完整重刊Table9。

### Table43原行到整理位置

T为前文一般测试条件说明，C为注1特性评估、除另有规定外未经生产测试。若原表把符号合并为一行，下面仍逐个列明；若主从分行则分别保留。

| 原符号/条件行 | 整理位置 | Min / Max；单位；类型 |
|---|---|---|
| fSCK=1/tc(SCK)，Master | SPI §2 | 未列/18；MHz；T |
| fSCK=1/tc(SCK)，Slave | SPI §2 | 未列/18；MHz；T |
| tr(SCK)、tf(SCK)，C=30 pF | SPI §2 | 未列/8；ns；T |
| DuCy(SCK)，Slave | SPI §2 | 30/70；%；T |
| tsu(NSS)，Slave | SPI §4.2 | 4 tPCLK/未列；时间；C |
| th(NSS)，Slave | SPI §4.2 | 2 tPCLK/未列；时间；C |
| tw(SCKH)、tw(SCKL)，Master，fPCLK=36 MHz、presc=4 | SPI §2 | 50/60；ns；C |
| tsu(MI)，Master | SPI §3 | 5/未列；ns；C |
| tsu(SI)，Slave | SPI §4.1 | 5/未列；ns；C |
| th(MI)，Master | SPI §3 | 5/未列；ns；C |
| th(SI)，Slave | SPI §4.1 | 4/未列；ns；C |
| ta(SO)，Slave，fPCLK=20 MHz | SPI §4.2 | 0 ns/3 tPCLK；C及注2 |
| tdis(SO)，Slave | SPI §4.2 | 2/10；ns；C及注3 |
| tv(SO)，Slave，after enable edge | SPI §4.1 | 未列/25；ns；C |
| tv(MO)，Master，after enable edge | SPI §3 | 未列/5；ns；C |
| th(SO)，Slave，after enable edge | SPI §4.1 | 15/未列；ns；C |
| th(MO)，Master，after enable edge | SPI §3 | 2/未列；ns；C |
| 注1及表前说明 | SPI §1与逐行类型 | 保留保证差别，不声称全部逐片生产测试 |
| 注2 | SPI §4.2 | 最早开始驱动与最迟数据有效是不同判据 |
| 注3 | SPI §4.2 | 最早数据失效与最迟进入Hi-Z是不同判据 |

原Table43中NSS与ta(SO)行位于合并的ns单位栏内，但数值含tPCLK；整理明确保留时间表达式，不将周期倍数误作固定纳秒。20 MHz下150 ns只作为3 tPCLK换算示例。

## 原图位置与标签

| 原图 | 位置与标识 | 用途和保留要求 |
|---|---|---|
| Figure32 | p69；ai14133g | I²C测量电路和AC边沿；两条图注含0.3/0.7 VDD、Rp/Rs/VDD_I2C定义；STOP→START图标tsu与表标tw差异保留 |
| Figure33 | p71；MSv41658V2 | SPI从机CPHA=0，含CPOL=0/1；完整NSS、SCK、MISO、MOSI及首尾位关系 |
| Figure34 | p71；MSv41659V2 | SPI从机CPHA=1，含CPOL=0/1；不可套用CPHA=0首位关系 |
| Figure35 | p72；MSv72626V1 | SPI主机，完整CPHA/CPOL组合；NSS input High标签不改为应用片选输出 |

图32～35已由同一固定副本原样裁切，嵌入两篇电气时序页。完整标题、所有信号与测量箭头、图32两条图注均保留；图33～35所在整页未见附属编号图注。裁切坐标、像素尺寸和校验值见[原图裁切记录](../assets/manual/ds5319-r20/I2C_SPI原图来源.md)。不改绘图标签，也不从示意间距推出新的时序数值。

## 待澄清与整理边界

1. Table41注2的400 kHz时钟倍数要求与Table42的36 MHz、400 kHz示例不一致，未取得ST进一步澄清；不声称发现了已确认官方勘误。
2. Table41注4保留其原意，不自行补充滤波区间保证。
3. Table41快速模式tw(SCLH)最大值原格空白；Figure32的tsu(STO:STA)与表41的tw(STO:STA)标法不同，均保留来源事实。
4. 本批完整整理的是Table41、42、43，另选录关联条件和图示定位；不宣称覆盖完整I²C/SPI寄存器、协议流程、勘误或全部GPIO电气表，亦未作板端验证。
