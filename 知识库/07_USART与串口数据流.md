# USART与串口数据流

[返回总目录](../README.md)

通用同步/异步收发器（USART）的串口数据流需要同时看清硬件实例、收发寄存器和软件缓冲区。本章先列出 USART1、USART2、USART3 的资源与内部路径，再提供硬件参数、HAL/LL 接口和芯片勘误的入口；数据格式与传输收尾的共同条件集中在第 4 节。

- [1 实例、时钟与DMA资源](#1-实例时钟与dma资源)
- [2 硬件与参数](#2-硬件与参数)
- [3 固定HAL与LL接口](#3-固定hal与ll接口)
- [4 数据格式与传输边界](#4-数据格式与传输边界)
- [5 图形与交叉参考](#5-图形与交叉参考)

![USART收发数据路径](../assets/usart/usart_data_path.svg)

## 1 实例、时钟与DMA资源

|实例|基址|时钟来源|外部 IRQ 编号|DMA1 发送|DMA1 接收|
|---|---|---|---:|---:|---:|
|USART1|0x40013800|PCLK2，APB2|37|通道 4|通道 5|
|USART2|0x40004400|PCLK1，APB1|38|通道 7|通道 6|
|USART3|0x40004800|PCLK1，APB1|39|通道 2|通道 3|

IRQ 编号是 CMSIS 的外部中断编号，不是含 16 个内核异常后的向量表总索引。DMA 通道与其他外设共享映射；同时打开同一通道对应的多个请求源，不能获得独立缓冲服务。

依据：[固定CMSIS器件头文件，中断编号](https://github.com/STMicroelectronics/cmsis-device-f1/blob/c8e9a4a4f16b6d2cb2a2083cbe5161025280fb22/Include/stm32f103xb.h#L119-L121)、[基址](https://github.com/STMicroelectronics/cmsis-device-f1/blob/c8e9a4a4f16b6d2cb2a2083cbe5161025280fb22/Include/stm32f103xb.h#L575-L611)，DMA 映射见 RM0008 Rev21 §13.3.7 及知识库 DMA 参数页。

PCLK1、PCLK2 分别是 APB1、APB2 的外设时钟。正常工作条件下，PCLK2 最高 72 MHz，PCLK1 最高 36 MHz。USART 波特率时钟使用对应 PCLK，不采用定时器的 APB 预分频倍频规则。

16 倍采样下，USART1 的发生器最大位率为 4.5 Mbit/s，USART2、USART3 为 2.25 Mbit/s。实际通信还取决于 GPIO、电气、时钟误差和软件/DMA 服务能力。

### 内部模块与控制关系

图 279 中的模块按数据、时钟和事件分为以下关系。软件通过数据寄存器 DR 访问收发数据，通过状态寄存器 SR 读取相关事件；同一 DR 地址两侧的发送数据寄存器 TDR、接收数据寄存器 RDR，已在总览图中分开表示。

|模块|输入或控制|输出及交叉条件|
|---|---|---|
|发送数据路径|CPU/DMA 写 DR → TDR → 发送移位寄存器|TX 引脚；TXE 表示 TDR 空，TC 对应发送完成条件|
|接收数据路径|RX → 接收移位寄存器 → RDR|CPU/DMA 读 DR；RXNE 表示接收数据寄存器非空，与接收错误一起在 SR 中反映|
|公共波特率发生器|PCLK、波特率寄存器 BRR 的整数/分数字段|产生接收/发送时序；TE、RE 分别控制发送、接收方向|
|CK 控制|CLKEN、CPOL、CPHA、LBCL|普通同步模式按有效数据位输出时钟 CK；Smartcard 另用 GTPR.PSC（GTPR：保护时间与预分频寄存器）|
|帧与校验|M：字长；STOP：停止位；PCE：校验使能；PS：奇偶选择|字长、停止区、奇偶校验生成/检查|
|接收唤醒单元|WAKE、RWU、CR2.ADD（CR2：控制寄存器 2）|空闲或地址标记唤醒，影响普通接收事件|
|扩展模式|SCEN/NACK、HDSEL、IREN/IRLP、LINEN|智能卡（Smartcard）、单线、红外（IrDA）、LIN 条件；须遵守模式互斥|
|DMA 请求|DMAT、DMAR 与发送/接收状态|两个方向独立请求；请求使能不代表 DMA 通道已正确配置|
|硬件流控|CTSE、RTSE 及 CTS/RTS 引脚|约束发送起帧和通知接收硬件空间|
|中断控制|SR 状态与相应中断使能位（IE）|合入该 USART 的单一 IRQ，完整布尔条件见[中断事件与使能条件](../参数/USART/工作模式流控与中断.md#8-中断事件与使能条件)|
|保护时间|GTPR.GT|Smartcard 发送完成后延迟 TC 置位|

图 279 中的简写（例如 HD、LINE、CKEN）应以寄存器定义的 HDSEL、LINEN、CLKEN 等正式字段名检索。图内 SW_RX 标注没有在本表推导成额外外部引脚；可用引脚及重映射须查芯片封装和 GPIO 主题。

来源：[RM0008 图279](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=789)及[寄存器定义，pp817–827](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=817)。

## 2 硬件与参数

- [帧结构、采样、波特率与错误](../参数/USART/帧格式波特率与接收错误.md)：字长与校验、TXE/TC、起始与停止采样、错误标志、分数分频和误差预算
- [工作模式、流控与中断](../参数/USART/工作模式流控与中断.md)：静默地址、LIN、同步主机、单线半双工、Smartcard、IrDA、RTS/CTS 及单 IRQ 合并
- [寄存器与访问副作用](../参数/USART/寄存器与访问副作用.md)：SR、DR、BRR、CR1/2/3、GTPR 的偏移、位域、复位及读写条件
- [硅勘误](../参数/USART/硅勘误.md)：PE、IDLE、地址唤醒、CTS/Break、RTS 违规及 GPIO/DMA 交叉约束

## 3 固定HAL与LL接口

HAL 的 UART 模块用于异步通信，USART 模块用于同步通信；这里的驱动模块名与 USART1～USART3 硬件实例编号是两层概念。固定版本原型按这两个模块及 Smartcard/IrDA 专用模块分别保存，专用模块另有 CPU 访问、初始化和 DMA 边界专题。

USART 硬件支持某模式时，仍须核对封装引脚组合和驱动调用顺序。无论依据是硬件支持，还是头文件中存在某个 STOP 编码，都不能据此认定仅改初始化字段即可切换为该模式。

### UART 与同步 USART 的 HAL

- [HAL配置、句柄与状态编码](../参数/USART/HAL配置句柄与状态.md)：完整字段、两套状态枚举、错误码及回调 ID
- [HAL接口索引](../参数/USART/HAL接口索引.md)：UART 与同步 USART 分别按两版保存参数类型、顺序及回调条件
- [HAL数据宽度与版本边界](../参数/USART/HAL数据宽度与版本边界.md)：旧版 CPU 访问宽度风险、分频进位、参数断言、状态与超时副作用
- [UART ReceiveToIdle](../参数/USART/ReceiveToIdle与事件位置.md)：v1.1.10 新增接口、回调位置/类型、普通与循环 DMA 的结束条件
- [DMA生命周期](../参数/USART/DMA生命周期.md)：启动返回、暂停、中止、伴随发送、错误资源和回调重入

### Smartcard 与 IrDA 专用驱动

- [Smartcard与IrDA配置、句柄及宏](../参数/USART/Smartcard与IrDA配置字段及宏.md)：Init/句柄字段、状态与回调 ID、配置编码、PSC 时钟来源、标志读取/清除和中断使能宏边界
- [Smartcard与IrDA HAL接口索引](../参数/USART/Smartcard与IrDA_HAL接口索引.md)：60 个不同接口名称、两版 120 条声明的原型/定义位置和回调条件；单列 ReInit 声明与实现差异
- [数据宽度与初始化](../参数/USART/Smartcard与IrDA数据宽度及初始化.md)：两版 CPU 访问差异、参数校验与重初始化边界
- [DMA启动、完成与错误边界](../参数/USART/Smartcard与IrDA_DMA边界.md)：RX 错误方向的句柄访问、启动返回值、循环模式差异及回调资源条件

### LL 接口与初始化

- [LL接口及结构索引](../参数/USART/LL接口与配置符号.md)：字段与符号、寄存器对应关系
- [LL初始化和模式边界](../参数/USART/LL初始化与模式边界.md)：UE 前提、部分写入、BRR 截断、模式清置掩码及保留字段

<a id="4-需要一起保存的事实"></a>

## 4 数据格式与传输边界

- **有效数据位与字长配置。** 有效数据位数由字长位 M 与校验使能位 PCE 共同决定。常见 8E1/8O1 表示 8 个有效数据位、偶/奇校验和 1 个停止位，在 F1 上对应 9 位字长加校验。因此，代码中的 `WordLength` 不能直接当作有效载荷位数。
- **发送完成。** DMA 完成、TDR 空、线路发送结束、HAL 句柄 READY 分别回答不同问题，不能把其中一项替代全部事务收尾。
- **标志清除与数据读取。** 按 SR→DR 的顺序清标志会读取接收数据；全双工发送中的 SR 读取/DR 写入还涉及奇偶校验错误（PE）勘误。因此，错误采集与数据读取需要共同设计。
- **IDLE 与缓冲消费位置。** IDLE（空闲检测）既不是永久可靠的协议分隔符，也不是锁存 DMA 计数的事件。协议边界及缓冲消费位置须分别建立。

## 5 图形与交叉参考

本主题按固定手册与驱动提交定位。每项结论分别标出硬件修订、驱动提交和原始位置；固定版本中的某一缺陷修正不保证其他缺陷已解决。图形整合范围、源文差异及验证限制见图形关系页。

- [图形关系与来源](../参数/USART/图形关系与来源.md)
- [DMA参数与请求映射](../参数/DMA参数与HAL接口.md)
- [引脚复用与AFIO](../参数/引脚复用与AFIO.md)
- [GPIO内部复用冲突](../参数/GPIO内部复用冲突.md)
- [范围与已知限制](../已知限制.md)
- [RM0008来源](../来源/RM0008.md#src-rm0008-r21-usart-hardware)
- [固定驱动来源](../来源/驱动实现.md#src-usart-fixed-safety-boundaries)

接口名称、原型和固定函数体核查只证明相应静态内容，不表示全部函数语义及状态交错均已完成审查。本文没有新增固件执行或板端测试；所记载的历史模型结果仅限原来注明的范围，未穷尽中断抢占、编译选项、用户 MSP 与实际电气条件。
