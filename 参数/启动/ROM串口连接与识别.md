# ROM 串口引导的连接与识别

调试接口暂时不可用时，可通过芯片内置的 ROM 引导程序建立串口连接。本页先完成连接和身份查询，便于将接线、启动选择与后续烧写问题分开排查。

## 接线与启动

- 主机串口 TX 接 PA10（USART1_RX），RX 接 PA9（USART1_TX），两端共地。
- 复位进入系统存储器时，设置 BOOT0=1、BOOT1=0。引脚采样时刻见[启动源与采样时刻](../../知识库/01_器件边界与硬件设计.md#41-启动源与采样时刻)。
- 主机串口采用 8 位数据、偶校验、1 位停止位，即 8E1；串口电平须满足板上 I/O 电气条件。
- 引导程序使用内部 HSI 经 PLL 得到 24 MHz 时钟，运行不依赖外部晶体。

依据：[AN2606 Rev70，Table 2、§21.1、Table 45](https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf#page=116)。TX/RX 交叉接线与共地是按收发方向得到的接线要求。

## 先握手，再查询能力

以下字节均按十六进制表示，应以二进制字节发送；例如 `0x7F` 是一个字节，不是字符 `0`、`x`、`7`、`F`。

### 1. 同步串口速率

1. 复位进入系统存储器后，主机按 8E1 发送单字节 `0x7F`。
2. ROM 用该帧识别串口速率，成功后返回 `0x79`，即确认字节 ACK。
3. 收到同步 ACK 后再发命令。后续命令交互中的 `0x1F` 是拒绝字节 NACK，应与“没有收到任何字节”分开判断。

`0x7F` 是初始同步帧，不是每条命令的前缀。同步流程见 [AN3155 Rev22 §1、Figure 1，p5](https://www.st.com/resource/en/application_note/an3155-how-to-use-usart-protocol-in-bootloader-on-stm32-mcus-stmicroelectronics.pdf#page=5)。

### 2. Get：读取版本和命令列表

发送 `0x00 0xFF`。成功响应按以下顺序接收：

1. 起始 ACK：`0x79`。
2. 长度字节 `N`。
3. 接收 `N+1` 个内容字节：第一个是版本字节，其余 `N` 个是支持的命令码。
4. 最后再接收一个 ACK：`0x79`，本次响应才完整。

`N` 不包含长度字节本身，也不包含首尾 ACK；不要把它当成整帧长度。版本字节例如 `0x22` 表示 2.2；对 STM32F1，该版本指内置引导程序版本，见 [AN2606 Rev70 §21.3 注释，p118](https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf#page=118)。应记录设备实际返回值，不用 AN3155 的文档修订号代替。

命令集合按实际返回列表保存，不把应用笔记的跨器件示例硬编码成每块板都相同的列表。

依据：[AN3155 Rev22 §3.1、Figures 2–3，pp9–11](https://www.st.com/resource/en/application_note/an3155-how-to-use-usart-protocol-in-bootloader-on-stm32-mcus-stmicroelectronics.pdf#page=9)。

### 3. Get ID：核对产品组

确认列表包含 Get ID 命令码 `0x02` 后，发送 `0x02 0xFD`。响应仍以 ACK 开始和结束，中间的长度字节 `N` 表示随后产品 ID（PID）的字节数减 1。

对 AN3155 描述的两字节 PID 格式，`N=0x01`，先收到高字节，再收到低字节。AN2606 的设备参数表把 STM32F10xxx 中容量组的 PID 列为 `0x410`，按两字节表示为 `0x0410`，因此成功响应可写成：

`0x79 0x01 0x04 0x10 0x79`

依次是起始 ACK、长度、PID 高字节、PID 低字节、结束 ACK。`0x0410` 用于核对产品组，不能单凭它确定完整订货号、封装或 Flash 容量，也不是单颗芯片的唯一标识。

版本条件须同时保留：AN2606 Table 46 记录 V2.1 才将 Get ID 改成两字节返回，V2.2 又增加下节的 RAM 访问限制。主机应按实际 `N` 和版本解析；若遇到旧格式，不能直接套用上述五字节示例。

依据：[AN3155 Rev22 §3.3、Figure 6，p14](https://www.st.com/resource/en/application_note/an3155-how-to-use-usart-protocol-in-bootloader-on-stm32-mcus-stmicroelectronics.pdf#page=14)、[AN2606 Rev70 Table 46，p117](https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf#page=117)、[Table 226，中容量组 PID，p518](https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf#page=518)。

### 命令校验与接收边界

普通命令由命令字节及其按位取反字节组成，两者异或为 `0xFF`。数据块的 XOR 校验规则另行定义，不能把这两个规则混用。

接收程序应区分同步 ACK、命令起始 ACK、按长度读取的内容和结束 ACK。内容阶段按长度消费字节，不应仅靠“遇到 `0x79` 就结束”判断边界。收到 NACK 表示命令被拒绝或执行出错；主机接收超时则表示没有在预期时间收齐响应，不能把超时伪装成设备返回的 NACK。

依据：[AN3155 Rev22 §3，Table 2 注 1 与通信校验规则，pp7–8](https://www.st.com/resource/en/application_note/an3155-how-to-use-usart-protocol-in-bootloader-on-stm32-mcus-stmicroelectronics.pdf#page=7)。按长度接收及区分主机超时是据上述帧格式得到的主机实现要求；本页不规定未经器件验证的统一超时数值，也没有执行任何板端命令。

## RAM 地址要避开引导程序占用

引导程序占用从 `0x20000000` 开始的 512 字节 RAM，即 `0x20000000～0x200001FF`。AN2606 记录 V2.2 会以 NACK 拒绝 Read Memory、Write Memory 和 Go 对这一区域的访问；设备参数表列出的可用 RAM 范围为 `0x20000200～0x20004FFF`，两端地址均包含。

准备 RAM 下载程序时，应同时核对装载地址、程序占用和栈空间，不能沿用从 SRAM 起点开始的普通链接布局。

依据：[AN2606 Rev70 §21.1、Table 45，p116](https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf#page=116)、[§21.3、Table 46，p117](https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf#page=117)、[Table 226，p518](https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf#page=518)。

## 连接失败时的排查顺序

1. **同步前无响应：** 先检查 BOOT 电平与复位，再检查 PA9/PA10 接线、共地和 8E1 配置，随后观察发送 `0x7F` 后是否收到 ACK。
2. **同步成功后收到 NACK：** 检查命令字与取反字节是否配对，以及命令是否出现在 Get 返回列表中。
3. **响应中途超时或字节错位：** 检查长度字节是否按“后续内容数减 1”解释、是否漏收结束 ACK，以及串口读取是否把多次到达的数据正确拼接。状态不确定时重新复位进入 ROM，再从同步开始，避免把 `0x7F` 插入未完成的命令帧。

以上为基于官方协议的排查顺序，尚未在具体板卡验证。版本和来源范围见[ROM 串口引导资料](../../来源/ROM串口引导资料.md)。
