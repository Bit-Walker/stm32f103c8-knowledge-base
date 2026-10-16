# SPI 电气时序与主从约束

先确定谁驱动SCK与数据，再按本机主/从角色核对输入建立保持、输出有效时间和NSS窗口。这里重组 DS5319 Rev20 Table43 的所有参数与脚注；HAL配置和状态标志另见文末的软件页面。

## 1 适用范围、供时与保证类型

适用于SPI1/2；引脚与复用限制见[引脚复用与AFIO](引脚复用与AFIO.md)。

| 检查项 | 适用条件 |
|---|---|
| VDD主电源 | 2～3.6 V |
| SPI1对应APB2 | fPCLK2=0～72 MHz |
| SPI2对应APB1 | fPCLK1=0～36 MHz |

以上摘自[Table9 p38](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf#page=38)，SPI1/APB2与SPI2/APB1总线挂接见[原厂方框图Figure1 p11](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf#page=11)，时钟分配路径见[原厂时钟树Figure2 p12](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf#page=12)。表9的0 MHz是一般范围下界，不表示0 MHz下可以通信。通用供电、温度与功耗条件及其余电气边界见[硬件电气参数](01_硬件电气参数.md)。

[Table43 p70](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf#page=70)前文说明：除另有规定，参数来自Table9所列环境温度、fPCLKx和VDD条件下的测试。以下用两类标记保留保证差别：

- **T**：适用上述一般说明；原表未加注1，不另外声称逐片生产测试。
- **C**：原表注1“由特性评估获得，除另有规定外未经生产测试”。不能改写为设计保证或逐片测试。

“未列”对应原表短横线，不表示0或无限。tPCLK是所用SPI外设对应PCLK的周期，fPCLK是该时钟频率，presc是SPI分频系数。原表虽把部分PCLK倍数放在合并的ns单位栏内，4 tPCLK、2 tPCLK、3 tPCLK本身都是时间表达式，不能读成固定4、2、3 ns。

## 2 两端先对齐时钟与负载

| 符号与检查对象 | 条件 | Min | Max | 单位 | 类型 |
|---|---|---:|---:|---|---|
| fSCK=1/tc(SCK)：SPI时钟频率；tc(SCK)为周期 | 主机 | 未列 | 18 | MHz | T |
| fSCK=1/tc(SCK)：SPI时钟频率 | 从机 | 未列 | 18 | MHz | T |
| tr(SCK)、tf(SCK)：SCK上升与下降时间 | 电容负载C=30 pF | 未列 | 8 | ns | T |
| DuCy(SCK)：从机输入时钟占空比 | 从机 | 30 | 70 | % | T |
| tw(SCKH)、tw(SCKL)：SCK高、低电平时间 | 主机，fPCLK=36 MHz，presc=4 | 50 | 60 | ns | C |

高低电平50～60 ns只属于所列36 MHz、/4条件，不能搬到所有频率。表43未把所有数据时序都标为30 pF条件；30 pF明确列在SCK边沿一行，不擅自扩展。GPIO输出模式及实际电压/负载仍须检查[硬件电气参数](01_硬件电气参数.md)。

## 3 本机作主机：检查MISO输入和MOSI输出

MI是Master Input（主机输入，MISO），MO是Master Output（主机输出，MOSI）。tsu表示建立时间，th表示保持时间，tv表示输出有效时间。

| 符号与含义 | 条件/测量关系 | Min | Max | 单位 | 类型 |
|---|---|---:|---:|---|---|
| tsu(MI)：数据输入建立时间 | 主机 | 5 | 未列 | ns | C |
| th(MI)：数据输入保持时间 | 主机 | 5 | 未列 | ns | C |
| tv(MO)：数据输出有效时间 | 主机，输出使能边沿之后 | 未列 | 5 | ns | C |
| th(MO)：数据输出保持时间 | 主机，输出使能边沿之后 | 2 | 未列 | ns | C |

边沿位置必须按CPOL/CPHA对照[Figure35 p72，原图MSv72626V1](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf#page=72)。CPOL是时钟极性，CPHA是时钟相位；这里的“使能边沿”是原表after enable edge所指的数据输出更新边沿，不是GPIO或外设时钟使能操作。原图中的NSS input保持High，不应改画成应用GPIO片选输出。

工程使用：主机的输入窗口要与从设备输出延迟及板级传播延迟一起检查；上表只给本器件一侧的边界，不能单凭18 MHz上限认定整条链路可运行。

## 4 本机作从机：检查MOSI输入、MISO输出与NSS

SI是Slave Input（从机输入，MOSI），SO是Slave Output（从机输出，MISO）。NSS是从机选择信号。

### 4.1 数据输入输出

| 符号与含义 | 条件/测量关系 | Min | Max | 单位 | 类型 |
|---|---|---:|---:|---|---|
| tsu(SI)：数据输入建立时间 | 从机 | 5 | 未列 | ns | C |
| th(SI)：数据输入保持时间 | 从机 | 4 | 未列 | ns | C |
| tv(SO)：数据输出有效时间 | 从机，输出使能边沿之后 | 未列 | 25 | ns | C |
| th(SO)：数据输出保持时间 | 从机，输出使能边沿之后 | 15 | 未列 | ns | C |

### 4.2 选中、释放与三态切换

| 符号与含义 | 条件 | Min | Max | 单位/时间表达式 | 类型 |
|---|---|---|---|---|---|
| tsu(NSS)：NSS建立时间 | 从机 | 4 tPCLK | 未列 | 对应PCLK周期的4倍 | C |
| th(NSS)：NSS保持时间 | 从机 | 2 tPCLK | 未列 | 对应PCLK周期的2倍 | C |
| ta(SO)：数据输出访问时间 | 从机，fPCLK=20 MHz | 0 | 3 tPCLK | 时间；Min为0 ns，Max为3个PCLK周期 | C，注2 |
| tdis(SO)：数据输出禁用时间 | 从机 | 2 | 10 | ns | C，注3 |

- 注2：ta(SO)的最小值指输出开始驱动的最短时间，最大值指数据变为有效的最长时间，两端并非同一种判据。按表列20 MHz条件，3 tPCLK换算为150 ns（换算值，不是原表新增额定）。该行不能无依据外推到其他PCLK。
- 注3：tdis(SO)的最小值指输出数据失效的最短时间，最大值指输出进入Hi-Z的最长时间。Hi-Z为高阻态；不能把2 ns当作保证已进入高阻的时间。

从机的NSS与SCK边沿请分别对照[Figure33，CPHA=0](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf#page=71)（MSv41658V2）和[Figure34，CPHA=1](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf#page=71)（MSv41659V2）。原图均保留CPOL=0/1两种情况；这里不重画或改变标签，也不把一种CPHA的首位访问关系套到另一种。

## 5 与软件边界配合使用

- [SPI片选与HAL初始化边界](SPI片选与HAL初始化边界.md)：NSS软硬件管理与引脚配置；其配置规则不能代替上表的建立保持时间。
- [SPI状态标志与停机边界](SPI状态标志与停机边界.md)：判断发送结束与停机顺序。
- [HAL SPI接收与DMA启动边界](HAL_SPI接收与DMA启动边界.md)：调用路径与DMA启动限制。
- [I²C电气时序](I2C/电气时序与上拉负载.md)；[固定来源与覆盖边界](../来源/DS5319_I2C_SPI电气时序.md)。

本页为固定文档静态整理，未作板级波形验证；与对端器件、走线、负载组合后的裕量需另行核算和测量。
