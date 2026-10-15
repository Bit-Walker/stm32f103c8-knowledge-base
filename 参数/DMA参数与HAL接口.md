# DMA参数与HAL接口

[生命周期与缓冲区正文](../知识库/04_DMA与缓冲区协作.md) · [图关系与来源](DMA图关系与来源.md)


本页用于查询 DMA 请求映射、数据宽度、寄存器访问及 HAL 调用条件。

- [请求映射](#dma1-完整请求映射)
- [宽度组合与地址步长](#全部数据宽度组合对齐和端序)
- [中断标志](#中断)
- [寄存器](#全部-dma1-寄存器)
- [HAL 接口](#hal接口与实际返回)
- [完成与错误检查顺序](#完成标志与错误分支的检查顺序)

数值及实现结论均保留对应原厂版本和位置。

## DMA1 完整请求映射

依据：[RM0008 Rev 21，§13.3.7 DMA request mapping](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=281)。


每通道的外设请求在进入 DMA 前简单逻辑或合并，不携带“是哪一个外设请求”的身份。一个通道任意时刻只能使能一个实际请求源；DMA 地址设置并不会筛选请求源。同一行内多个源不能同时依靠同一个通道独立搬运。

|DMA1 通道|所有 C8 可用硬件请求|
|---|---|
|1|ADC1；TIM2_CH3；TIM4_CH1|
|2|SPI1_RX；USART3_TX；TIM1_CH1；TIM2_UP；TIM3_CH3|
|3|SPI1_TX；USART3_RX；TIM1_CH2；TIM3_CH4；TIM3_UP|
|4|SPI2_RX；USART1_TX；I2C2_TX；TIM1_CH4；TIM1_TRIG；TIM1_COM；TIM4_CH2|
|5|SPI2_TX；USART1_RX；I2C2_RX；TIM1_UP；TIM2_CH1；TIM4_CH3|
|6|USART2_RX；I2C1_TX；TIM1_CH3；TIM3_CH1；TIM3_TRIG|
|7|USART2_TX；I2C1_RX；TIM2_CH2；TIM2_CH4；TIM4_UP|

RX表示接收，TX表示发送，CH表示捕获比较通道，UP表示更新事件，TRIG表示触发事件，COM表示换相事件。

原表 78 的 TIM1/Channel3 单元显示短横线，但同章图 50 明确列出 TIM1_CH2；此处保留该有效请求并明确原表与图的不一致。设计时同时核对外设 DMA 使能、请求时机和通道固定连接。所有通道还可由 MEM2MEM 软件启动。


## 全部数据宽度组合、对齐和端序

依据：[RM0008 Rev 21，§13.3.3 DMA channels; §13.3.4 Programmable data width, data alignment and endians](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=277)。


下表依据RM0008 Rev21 Table76的源/目的内容列、PSIZE/MSIZE字段及p277递增规则，对九种组合进行一致性整理；不是原表操作栏的逐字等价复制。设每次源数据低字节为 B0，后续地址顺序为 B1、B2……，PINC=MINC=1，NDT=4；每笔都只读一个源数据项，再写一个目的数据项，不做打包拼接。

|源位宽→目的位宽|源地址依次|目的地址依次|四个目的数据项|
|---|---|---|---|
|8→8|0、1、2、3|0、1、2、3|B0、B1、B2、B3|
|8→16|0、1、2、3|0、2、4、6|00B0、00B1、00B2、00B3|
|8→32|0、1、2、3|0、4、8、C|000000B0、000000B1、000000B2、000000B3|
|16→8|0、2、4、6|0、1、2、3|B0、B2、B4、B6|
|16→16|0、2、4、6|0、2、4、6|B1B0、B3B2、B5B4、B7B6|
|16→32|0、2、4、6|0、4、8、C|0000B1B0、0000B3B2、0000B5B4、0000B7B6|
|32→8|0、4、8、C|0、1、2、3|B0、B4、B8、BC|
|32→16|0、4、8、C|0、2、4、6|B1B0、B5B4、B9B8、BDBC|
|32→32|0、4、8、C|0、4、8、C|B3B2B1B0、B7B6B5B4、BBBAB9B8、BFBEBDBC|

表中地址均为相对各自基址的十六进制字节偏移；B 后面的数也是十六进制索引。窄源写宽目的时高位补零；宽源写窄目的时截去高位。小端顺序指最低地址保存最低有效字节，DMA 不进行大端/小端自动交换。原表p279操作栏存在以下可观察的不一致，整理时按源/目的内容列、字段宽度及p277递增规则取一致结果：

1. 8→16第3/4项READ写成B3/B4，而源列在地址2/3分别为B2/B3，目的列也分别为00B2/00B3。
2. 8→32第3/4项READ同样写成B3/B4，但源列和目的列对应B2/B3。
3. 32→16操作栏将B1B0等标为[7:0]，写目的偏移列为0/1/2/3；目的内容列却为0/2/4/6，且16位目的按p277规则每次加2字节。整理表据此保留低16位、目的步长2字节。

这是本次一致性判断及整理推导，不表示ST已经发布对应正式勘误；原厂图表的不一致没有被静默删除。

半字地址忽略 bit0，字地址忽略 bit1:0，硬件按相应自然边界对齐；不要借此把错误地址当成合法跨边界访问。

### AHB/APB 窄写复制陷阱

AHB 的字节/半字写会把数据复制到未使用的数据总线字节通道：写 0xABCD 半字时 HWDATA=0xABCDABCD，写 0xAB 字节时 HWDATA=0xABABABAB。如果目标 AHB 从设备不理会 HSIZE，又不报告错误，就会接收整个 32 位复制值。

AHB/APB 桥将上述操作转换成 32 位 APB 写：向字内任意字节地址写 B0 会成为向字边界写 B0B0B0B0；向偏移 0 或 2 写半字 B1B0 会成为 B1B0B1B0。因此外设寄存器宽度与数据宽度不能随意混用。例如备份寄存器是按 32 位地址边界排列的 16 位寄存器，宜配置 MSIZE=16 位、PSIZE=32 位，源每次增 2、目的每次增 4，避免写错寄存器间距。


## 中断

依据：[RM0008 Rev 21，§13.3.1 DMA transactions; §13.3.3 DMA channels; §13.3.5 Error management; §13.4 DMA registers](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=276)；[ES096 Rev 15，§2.4.1 DMA disable failure and error flag omission upon simultaneous transfer error and global flag clear](https://www.st.com/resource/en/errata_sheet/es096-stm32f101x8b-stm32f102x8b-and-stm32f103x8b-mediumdensity-device-limitations-stmicroelectronics.pdf#page=3)。


|事件|状态|使能|清除|
|---|---|---|---|
|半传输|HTIFx|HTIE|IFCR.CHTIFx 写 1|
|传输完成|TCIFx|TCIE|IFCR.CTCIFx 写 1|
|传输错误|TEIFx|TEIE|IFCR.CTEIFx 写 1|

GIFx 是该通道上述事件的综合标志；IFCR.CGIFx 写 1 同时清 GIF、HTIF、TCIF、TEIF。**按 ES096 §2.4.1，活动通道禁止使用 CGIFx 全清：它若与传输错误同周期发生，会丢失 TEIFx 并阻止通道自动禁用。活动期间分别使用 CHTIFx、CTCIFx、CTEIFx，CGIFx 只用于通道已停用后的清理。**DMA1 的 7 个通道各有独立 IRQ。清 DMA 标志采用写 1 清，与 ADC/TIM 的写 0 清不同；不能混用清标志模板。


## 全部 DMA1 寄存器

依据：[RM0008 Rev 21，§13.3.1 DMA transactions; §13.3.3 DMA channels; §13.3.5 Error management; §13.4 DMA registers](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=276)；[ES096 Rev 15，§2.4.2 Byte and half-word accesses not supported](https://www.st.com/resource/en/errata_sheet/es096-stm32f101x8b-stm32f102x8b-and-stm32f103x8b-mediumdensity-device-limitations-stmicroelectronics.pdf#page=13)；[ES096 Rev 15，§2.4.1 DMA disable failure and error flag omission upon simultaneous transfer error and global flag clear](https://www.st.com/resource/en/errata_sheet/es096-stm32f101x8b-stm32f102x8b-and-stm32f103x8b-mediumdensity-device-limitations-stmicroelectronics.pdf#page=3)。


DMA1 基址 0x40020000。**DMA 控制寄存器必须使用对齐的 32 位 word 访问。** RM0008 本节宣称可作 8/16 位访问的文字已由 ES096 §2.4.2 更正，byte/halfword 写会产生异常行为；这不影响 DMA 搬运的数据项仍支持 8、16、32 位。各字段有效范围如下，保留位保持复位值。所有寄存器复位值均为 0x00000000。rw=软件读写，r=只读，w=只写。

### 13.4.1 ISR，偏移 0x00

bit31:28 保留；通道 x=1～7 的四个只读状态位从 b=4(x−1) 开始：GIFx=b，TCIFx=b+1，HTIFx=b+2，TEIFx=b+3。0 表示该事件未发生，1 表示已发生；由硬件置位，通过 IFCR 对应位写 1 清除。

|通道|GIF|TCIF|HTIF|TEIF|
|---|---:|---:|---:|---:|
|1|0|1|2|3|
|2|4|5|6|7|
|3|8|9|10|11|
|4|12|13|14|15|
|5|16|17|18|19|
|6|20|21|22|23|
|7|24|25|26|27|

### 13.4.2 IFCR，偏移 0x04

bit31:28 保留。位布局与 ISR 相同，对应名称依次为 CGIFx、CTCIFx、CHTIFx、CTEIFx；全部 w。写 0 无作用，写 1 清对应标志；CGIFx 清该通道全部四类标志，但按 ES096 §2.4.1 只能在通道已停用时使用。直接写目标清除掩码，避免对只写寄存器做读改写。

### 13.4.3 CCRx，偏移 0x08+0x14(x−1)

有效字段全部 rw，bit31:15 保留。

|位|字段|全部编码与约束|
|---|---|---|
|14|MEM2MEM|0 外设请求模式；1 存储器到存储器，EN 后立即搬运；不可配合 CIRC|
|13:12|PL|00 低；01 中；10 高；11 很高|
|11:10|MSIZE|00 字节；01 半字；10 字；11 保留|
|9:8|PSIZE|00 字节；01 半字；10 字；11 保留|
|7|MINC|0 存储器端地址固定；1 每项按 MSIZE 递增|
|6|PINC|0 外设端地址固定；1 每项按 PSIZE 递增|
|5|CIRC|0 非循环；1 末项后重装数量和内部地址|
|4|DIR|0 从 CPAR 外设端读、向 CMAR 写；1 从 CMAR 读、向 CPAR 外设端写|
|3|TEIE|0 禁止、1 允许传输错误中断|
|2|HTIE|0 禁止、1 允许半传输中断|
|1|TCIE|0 禁止、1 允许完成中断|
|0|EN|0 禁用通道；1 使能；传输错误时硬件清零|

修改搬运配置应先禁用通道，不以 EN 清零代替寄存器复位。

### 13.4.4 CNDTRx，偏移 0x0C+0x14(x−1)

bit15:0 NDT，bit31:16 保留。NDT 范围 0～65535；仅 EN=0 时可写，EN=1 时只读，表示剩余数据项，每次 DMA 事务减 1。到零后非循环停在零，循环模式重装初始值。零计数不服务任何事务，无论 EN 是否为 1。

### 13.4.5 CPARx，偏移 0x10+0x14(x−1)

bit31:0 PA 为 rw 外设端基址，EN=1 时禁止写。PSIZE=01 时忽略 PA[0]，PSIZE=10 时忽略 PA[1:0]，分别按半字、字边界访问。此寄存器不随搬运递增，内部当前地址才递增。

### 13.4.6 CMARx，偏移 0x14+0x14(x−1)

bit31:0 MA 为 rw 存储器端基址，EN=1 时禁止写。MSIZE=01 时忽略 MA[0]，MSIZE=10 时忽略 MA[1:0]。此寄存器同样保留初始基址。

### 13.4.7 完整寄存器偏移地图

|通道|CCRx|CNDTRx|CPARx|CMARx|后续保留槽|
|---|---|---|---|---|---|
|1|0x08|0x0C|0x10|0x14|0x18|
|2|0x1C|0x20|0x24|0x28|0x2C|
|3|0x30|0x34|0x38|0x3C|0x40|
|4|0x44|0x48|0x4C|0x50|0x54|
|5|0x58|0x5C|0x60|0x64|0x68|
|6|0x6C|0x70|0x74|0x78|0x7C|
|7|0x80|0x84|0x88|0x8C|0x90|

另有 ISR=0x00、IFCR=0x04。原偏移公式中的 0d20 是十进制 20，即 0x14，不能误写成 0x20 的通道步长。

## DMA_InitTypeDef

以下七个成员的类型均为`uint32_t`（UM1850 Rev3 §14.1.1，印刷页148）。

依据：[UM1850 Rev 3，§3.9 HAL common resources；§14 HAL DMA Generic Driver（§14.1–14.3）](https://www.st.com/resource/en/user_manual/um1850-description-of-stm32f1-hal-and-lowlayer-drivers-stmicroelectronics.pdf#page=148)。

|成员|可选值与意义|
|---|---|
|Direction|`DMA_PERIPH_TO_MEMORY`、`DMA_MEMORY_TO_PERIPH`、`DMA_MEMORY_TO_MEMORY`|
|PeriphInc|`DMA_PINC_ENABLE`、`DMA_PINC_DISABLE`：外设侧地址增量|
|MemInc|`DMA_MINC_ENABLE`、`DMA_MINC_DISABLE`：存储器侧地址增量|
|PeriphDataAlignment|`DMA_PDATAALIGN_BYTE`、`DMA_PDATAALIGN_HALFWORD`、`DMA_PDATAALIGN_WORD`：8/16/32 位|
|MemDataAlignment|`DMA_MDATAALIGN_BYTE`、`DMA_MDATAALIGN_HALFWORD`、`DMA_MDATAALIGN_WORD`：8/16/32 位|
|Mode|`DMA_NORMAL` 或 `DMA_CIRCULAR`；存储器到存储器禁止循环模式|
|Priority|`DMA_PRIORITY_LOW`、`DMA_PRIORITY_MEDIUM`、`DMA_PRIORITY_HIGH`、`DMA_PRIORITY_VERY_HIGH`：通道仲裁的软件优先级，与 NVIC 优先级无关|

## DMA_HandleTypeDef（结构体标签__DMA_HandleTypeDef）

依据：[UM1850 Rev 3，§3.9 HAL common resources；§14 HAL DMA Generic Driver（§14.1–14.3）](https://www.st.com/resource/en/user_manual/um1850-description-of-stm32f1-hal-and-lowlayer-drivers-stmicroelectronics.pdf#page=148)。

|成员|类型与意义|
|---|---|
|Instance|`DMA_Channel_TypeDef *`，通道寄存器基址|
|Init|`DMA_InitTypeDef`，初始化参数|
|Lock|`HAL_LockTypeDef`，句柄锁|
|State|`HAL_DMA_StateTypeDef`，过程状态|
|Parent|`void *`，父外设句柄；`__HAL_LINKDMA` 同时将父句柄的DMA字段指向DMA句柄，并将DMA.Parent指回父句柄（UM1850 §3.9 p25）|
|XferCpltCallback|`void (*)(DMA_HandleTypeDef *)`，完整传输结束|
|XferHalfCpltCallback|同上，半传输结束|
|XferErrorCallback|同上，传输错误|
|XferAbortCallback|同上，终止通知|
|ErrorCode|`__IO uint32_t`，错误位图|
|DmaBaseAddress|`DMA_TypeDef *`，控制器基址，内部使用|
|ChannelIndex|`uint32_t`，通道标志位偏移／索引，内部使用|

## DMA宏

下表h均为`DMA_HandleTypeDef *`（UM1850 Rev3 §14.3，印刷页155–156，结合§14.1.2句柄定义）。

依据：[UM1850 Rev 3，§3.9 HAL common resources；§14 HAL DMA Generic Driver（§14.1–14.3）](https://www.st.com/resource/en/user_manual/um1850-description-of-stm32f1-hal-and-lowlayer-drivers-stmicroelectronics.pdf#page=148)；[stm32f1xx_hal_dma.c @ bd368aa335c529641d2e567574885e02deacc64a](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c)。

|宏|语义与返回|
|---|---|
|`__HAL_DMA_RESET_HANDLE_STATE(h)`|软件状态置 RESET；无返回|
|`__HAL_DMA_ENABLE(h)` / `__HAL_DMA_DISABLE(h)`|置位／清除通道使能；无返回，不自动维护完整父外设状态|
|`__HAL_DMA_ENABLE_IT(h,it)` / `__HAL_DMA_DISABLE_IT(h,it)`|it 可组合 `DMA_IT_TC`、`DMA_IT_HT`、`DMA_IT_TE`；无返回|
|`__HAL_DMA_GET_IT_SOURCE(h,it)`|检查指定源是否使能，返回 SET/RESET 语义|
|`__HAL_DMA_GET_COUNTER(h)`|返回 CNDTR 剩余数据项数；乘 MSIZE 对应的 1、2 或 4 字节得到剩余项对应的内存端搬运量。连续数组容量还须满足 MINC=1；MINC=0 重复访问同一内存项，不能据该乘积推断独立地址覆盖范围|

## DMA1各通道完整标志

依据：[UM1850 Rev 3，§3.9 HAL common resources；§14 HAL DMA Generic Driver（§14.1–14.3）](https://www.st.com/resource/en/user_manual/um1850-description-of-stm32f1-hal-and-lowlayer-drivers-stmicroelectronics.pdf#page=148)。

|通道|全局|全完成|半完成|传输错误|
|---|---|---|---|---|
|1|`DMA_FLAG_GL1`|`DMA_FLAG_TC1`|`DMA_FLAG_HT1`|`DMA_FLAG_TE1`|
|2|`DMA_FLAG_GL2`|`DMA_FLAG_TC2`|`DMA_FLAG_HT2`|`DMA_FLAG_TE2`|
|3|`DMA_FLAG_GL3`|`DMA_FLAG_TC3`|`DMA_FLAG_HT3`|`DMA_FLAG_TE3`|
|4|`DMA_FLAG_GL4`|`DMA_FLAG_TC4`|`DMA_FLAG_HT4`|`DMA_FLAG_TE4`|
|5|`DMA_FLAG_GL5`|`DMA_FLAG_TC5`|`DMA_FLAG_HT5`|`DMA_FLAG_TE5`|
|6|`DMA_FLAG_GL6`|`DMA_FLAG_TC6`|`DMA_FLAG_HT6`|`DMA_FLAG_TE6`|
|7|`DMA_FLAG_GL7`|`DMA_FLAG_TC7`|`DMA_FLAG_HT7`|`DMA_FLAG_TE7`|

## DMA1 能力

依据：[DS5319 Rev 20，§2.1 Device overview](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf#page=10)；[RM0008 Rev 21，§13.3.3 DMA channels; §13.3.4 Programmable data width, data alignment and endians](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=277)；[RM0008 Rev 21，§13.3.1 DMA transactions; §13.3.3 DMA channels; §13.3.5 Error management; §13.4 DMA registers](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=276)。

| 项目 | STM32F103C8T6 的使用边界 |
|---|---|
| 控制器 | DMA1，7 个通道 |
| 请求分配 | 外设请求到通道采用固定映射 |
| 传输方向 | 外设到存储器、存储器到外设、存储器到存储器；具体地址必须允许相应读写 |
| 数据宽度 | 源、目的端分别选择 8、16、32 位 |
| 地址模式 | 两端分别选择固定地址或递增地址 |
| 计数 | 每次配置最多 65 535 个数据项，不是固定 65 535 字节 |
| 连续数据 | 支持循环模式及半传输、传输完成、传输错误事件 |
| 软件优先级 | 4 级；相同软件优先级时，通道编号较小者优先 |

## APB外设分布

依据：[DS5319 Rev 20，§2.1 Device overview](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf#page=10)；[RM0008 Rev 21，§13.3.1 DMA transactions; §13.3.3 DMA channels; §13.3.5 Error management; §13.4 DMA registers](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=276)。

| 总线 | 与本笔记相关的常用外设 | 设计含义 |
|---|---|---|
| APB1 | USART2、USART3、SPI2、I2C1、I2C2、TIM2、TIM3、TIM4 | 同总线访问会竞争；不能只分别计算各外设速率 |
| APB2 | USART1、SPI1、ADC1、TIM1、GPIO | ADC1 在本器件中走 APB2，不应照搬其他系列的 AHB ADC 例子 |

## 原文理想时序下限

依据：[AN2548 Rev 9，§5.1 DMA transfer timing; §5.1.1 AHB peripheral and system volatile memory; §5.1.2 APB peripheral and system volatile memory; §5.2 Total service time and parallelism; §5.4 Impact of APB; §7 DMA overview](https://www.st.com/resource/en/application_note/an2548-introduction-to-dma-controller-for-stm32-mcus-stmicroelectronics.pdf#page=7)。

| 阶段 | 原文给出的理想下限或影响因素 |
|---|---|
| 仲裁与地址计算 | 没有更高优先级挂起请求、从设备已准备好时，至少 2 个 AHB 周期 |
| AHB 外设读取 | 至少 2 个 AHB 周期；总线共享或等待状态会增加时间 |
| SRAM 写入 | 一次独立读写访问为 1 个 AHB 周期；原文明确列出的 STM32F1 SRAM read-after-write（先写、后读）情形为 2 个 AHB 周期 |

## 资源不足表现

依据：[AN2548 Rev 9，§6 Insufficient resources threats](https://www.st.com/resource/en/application_note/an2548-introduction-to-dma-controller-for-stm32-mcus-stmicroelectronics.pdf#page=10)。

| 表现 | 原因与后果 | 应检查什么 |
|---|---|---|
| 接收溢出 Overrun | 下一数据到达前，旧数据尚未读走；可能丢失数据 | 外设溢出标志、总线负载、DMA 通道优先级 |
| 无标志的数据丢失 | 某些 GPIO 并行采样不会提供串口式溢出提示 | 采样时刻、外部时序和输入数据是否被覆盖 |
| 发送出现间隙 | 发送寄存器未及时补充数据 | 高频 SPI 等接口的 DMA 服务延迟 |
| 采样时序或数据序列异常 | 数据取走不及时或搬运与处理节奏不匹配 | ADC 触发、DMA 循环、处理端是否追上生产端 |

## 时延模型的保留条件

AN2548 Rev 9 §5.1–5.4，印刷页7–9，表2 p11：仲裁/地址计算理想至少2个AHB周期；AHB外设读取理想至少2个AHB周期；独立SRAM访问1个AHB周期，F1的read-after-write指先写后读情形2周期，不能说全部SRAM写都固定2周期。APB通用基本访问为2个APB周期，APB慢于AHB还需1个AHB同步周期；F1在跨系列表2的AHB/APB桥时钟项为3。以上不应未经阶段重叠分析机械相加。

握手 $`t_{\mathrm{Ack}}`$ 为 1 个 AHB 周期；原文说明不同通道的仲裁开销可被前一通道服务末段遮蔽；§5.2正文称AHB访问末尾两周期，图3首次重叠的网格画成最后一个AHB访问周期与随后Ack周期的重叠；后一次上行仲裁则位于下行访问末两格。这里只分别保留原图文表达，不据此推定F103精确硬件时序；这不是ST正式勘误。

CPU同APB访问的额外4周期也是简化模型，非任意分频下C8最坏常数。

以下是单位换算和工程整理公式。AN2548 的服务时间分解另见[吞吐量与最坏服务延迟](../知识库/04_DMA与缓冲区协作.md#4-吞吐量与最坏服务延迟)。

- $`t=n/f`$ ： $`n`$ 为相应总线的周期数，无量纲； $`f`$ 为该总线频率，单位 Hz； $`t`$ 为时间，单位 s。AHB与APB周期分别按各自频率换算，并区分串行阶段与可重叠阶段。
- $`B_{\mathrm{ideal}}=4f_{\mathrm{bus}}`$ ： $`f_{\mathrm{bus}}`$ 为相应总线频率，单位Hz；4表示32位等于4字节； $`B_{\mathrm{ideal}}`$ 为理想单方向字节率，单位B/s。假设每周期完成一次32位访问，不含一次DMA项所需的源读取、目的写入、握手、桥接、仲裁及等待。
- $`R_{\mathrm{item}}=R_{\mathrm{baud}}/n_{\mathrm{frame}}`$ ： $`R_{\mathrm{baud}}`$ 为波特率，单位baud，即符号/s； $`n_{\mathrm{frame}}`$ 为完整帧的符号数，在常见二进制USART中等于帧位数； $`R_{\mathrm{item}}`$ 单位项/s。2 Mbaud、8N1每帧1起始位+8数据位+1停止位，共10符号，故为200000项/s；原文250000为忽略帧开销的示意，不是8N1结果。
- $`B_{\mathrm{capacity}}\geq1.5B_{\mathrm{load}}`$ ： $`B_{\mathrm{capacity}}`$ 为可用服务能力， $`B_{\mathrm{load}}`$ 为预计负载，必须同口径、同单位，例如事务/s或已计入开销的等效带宽；1.5无量纲，来自原文额外50%余量建议。不得把外设有效字节/s直接与理想总线B/s比较。一次DMA项须分别预算源读取与目的写入路径；8位有效载荷也占用32位总线传输机会。该式仅表示平均余量，不证明实时截止。

## HAL接口与实际返回

UM1850 Rev 3 §14.2.5 pp151–154列出的12个API及参数保留如下；实际状态行为以固定提交bd368aa335c529641d2e567574885e02deacc64a为边界。DataLength的1～65535是硬件/调用契约；固定.c仅调用assert_param检查范围，不能声称关闭assert时仍会自动返回参数错误。__HAL_LOCK展开和完整状态枚举因缺固定主头文件而未核，不包括在下表已核返回分支中。

共用参数类型（UM1850 Rev3 §14.2.5，印刷页151–154）：hdma为`DMA_HandleTypeDef *`；SrcAddress、DstAddress、DataLength、CompleteLevel、Timeout均为`uint32_t`；CallbackID为`HAL_DMA_CallbackIDTypeDef`；pCallback为`void (*)(DMA_HandleTypeDef *)`。各接口返回类型见表；句柄和回调指向的对象须在调用及相应异步过程期间有效。

### HAL_DMA_Init

调用：`HAL_DMA_Init(hdma)`。

HAL_StatusTypeDef；空句柄ERROR，配置/软件状态初始化到READY；不是安全Abort。

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L142-L211)

### HAL_DMA_DeInit

调用：`HAL_DMA_DeInit(hdma)`。

HAL_StatusTypeDef；空句柄ERROR，正常RESET；清回调。

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L219-L284)

### HAL_DMA_Start

调用：`HAL_DMA_Start(hdma, SrcAddress, DstAddress, DataLength)`。

地址uint32_t；长度1～65535项；READY进入BUSY；成功OK；已通过锁宏进入函数主体后，非READY显式返回BUSY；锁宏展开尚未核验。

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L318-L350)

### HAL_DMA_Start_IT

调用：`HAL_DMA_Start_IT(hdma, SrcAddress, DstAddress, DataLength)`。

参数、状态与返回条件同 HAL_DMA_Start；TC/TE使能，HT仅在半完成回调非空时使能。

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L361-L407)

### HAL_DMA_Abort

调用：`HAL_DMA_Abort(hdma)`。

BUSY才禁用与清理，成功READY/OK；非BUSY返回ERROR+NO_XFER且未禁用。

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L415-L448)

### HAL_DMA_Abort_IT

调用：`HAL_DMA_Abort_IT(hdma)`。

BUSY路径在本调用同步执行非空Abort回调，回调可以早于返回；不保证另一次IRQ。

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L456-L491)

### HAL_DMA_PollForTransfer

调用：`HAL_DMA_PollForTransfer(hdma, CompleteLevel, Timeout)`。

CompleteLevel为HAL_DMA_FULL_TRANSFER或HAL_DMA_HALF_TRANSFER；Timeout为ms、0立即检查、HAL_MAX_DELAY无限等；执行到TE/超时分支时均ERROR而非HAL_TIMEOUT；目标完成标志已置位时跳过等待循环内的TE/超时检查；超时READY不清EN。

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L501-L594)

### HAL_DMA_IRQHandler

调用：`HAL_DMA_IRQHandler(hdma)`。

void；HT、TC、TE分支及对应中断使能门控；循环HT/TC保持BUSY；执行到TE分支才置READY/错误。

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L602-L680)

### HAL_DMA_RegisterCallback

调用：`HAL_DMA_RegisterCallback(hdma, CallbackID, pCallback)`。

READY、有效ID方可修改；NULL未被专门拒绝，意味着不调用；返回HAL_StatusTypeDef。

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L692-L733)

### HAL_DMA_UnRegisterCallback

调用：`HAL_DMA_UnRegisterCallback(hdma, CallbackID)`。

支持单个或ALL；READY、合法ID成功OK，非READY或非法ID显式返回ERROR；锁宏展开尚未核验。

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L743-L791)

### HAL_DMA_GetState

调用：`HAL_DMA_GetState(hdma)`。

HAL_DMA_StateTypeDef，仅软件状态。

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L819-L823)

### HAL_DMA_GetError

调用：`HAL_DMA_GetError(hdma)`。

uint32_t错误位图。

[固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L831-L834)

固定dma.c实际使用的状态标识为HAL_DMA_STATE_RESET、HAL_DMA_STATE_READY、HAL_DMA_STATE_BUSY；完整HAL_DMA_StateTypeDef枚举定义尚未按对应固定头文件核验，不能据此断言其他枚举不存在。Poll超时实际写入READY。错误位名：HAL_DMA_ERROR_NONE、TE、NO_XFER、TIMEOUT、NOT_SUPPORTED。回调ID完整名：HAL_DMA_XFER_CPLT_CB_ID、HAL_DMA_XFER_HALFCPLT_CB_ID、HAL_DMA_XFER_ERROR_CB_ID、HAL_DMA_XFER_ABORT_CB_ID、HAL_DMA_XFER_ALL_CB_ID（最后者用于解除全部）。TIM句柄索引为TIM_DMA_ID_UPDATE/CC1/CC2/CC3/CC4/COMMUTATION/TRIGGER，不是DMA硬件通道号。

普通模式HT成功轮询仍BUSY，完整完成轮询READY；循环模式Poll返回ERROR+NOT_SUPPORTED。主函数返回、句柄状态、硬件EN和CNDTR必须分别解释。固定IRQ实现按HT、else-if TC、else-if TE分派；同时挂起不是一次调用全部分发。这里是源码事实，不能据此承诺丢失的多轮HT/TC事件可恢复。

## 完成标志与错误分支的检查顺序

固定bd368aa实现的PollForTransfer仅在目标HT/TC标志尚未置位的while循环内检查TE和超时。若检查循环条件时目标完成标志已经置位，该调用跳过循环内的错误/超时判断，清选定完成标志并走HAL_OK路径；这不能额外证明所有错误位均为0。Timeout=0表示不继续等待，目标已经完成时仍可返回OK。有限超时还依赖HAL_GetTick正常推进；函数内的毫秒比较不构成包含中断抢占及调度延迟的硬实时返回上限。此处说明源码分支顺序，不据此认定任意HT/TC/TE组合必然可在硅片同一周期出现。

IRQ入口分别读取一次ISR与CCR快照，随后按已允许的HT、TC、TE依次作if/else-if选择。若进入时HT与TE均挂起且对应中断均已使能，会先处理HT及其非空半完成回调，本次不会继续进入TE分支。半完成回调因此不构成“错误已经优先处理”或“DMA仍在活动”的保证；新发生的事件也不能靠这次旧快照全部分发。原参数表的HT→TC→TE次序继续适用。

故障记录还须在再次操作句柄前保存：本版本Abort和Abort_IT在非BUSY分支直接把ErrorCode赋为HAL_DMA_ERROR_NO_XFER，覆盖原错误位图；它们没有在这一分支实际禁用通道。若Poll先因超时置READY、留下EN，再调用Abort，原TIMEOUT诊断可能被NO_XFER替换。不要以此手改State解锁，应保留原始错误、请求及通道状态，再走本事务明确拥有的停止路径。

来源：[固定PollForTransfer L501–594](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L501-L594)、[IRQ L602–680](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L602-L680)、[Abort/Abort_IT L415–491](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L415-L491)。以上是固定源码静态核查，未执行固件、故障注入或完整并发验证。

## 原厂证据边界

规则扫描/注入抢占依据[RM0008 Rev21 §§11.3.8–11.3.9 p221](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=221)；TIM burst依据[RM0008 Rev21 §§14.4.19–14.4.20 pp361–362](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=361)。相关结论直接使用这些原厂章节；它们不构成对AN3116或AN4776整份文档的核验，也不代表ADC与定时器主题已完整覆盖。
