# ROM 串口引导的连接与识别

调试接口暂时不可用时，可通过芯片内置的 ROM 引导程序建立串口连接。本页先完成连接和身份查询，便于将接线、启动选择与后续烧写问题分开排查。

## 接线与启动

- 主机串口 TX 接 PA10（USART1_RX），RX 接 PA9（USART1_TX），两端共地。
- 复位进入系统存储器时，设置 BOOT0=1、BOOT1=0。引脚采样时刻见[启动源与采样时刻](../../知识库/01_器件边界与硬件设计.md#41-启动源与采样时刻)。
- 主机串口采用 8 位数据、偶校验、1 位停止位，即 8E1；串口电平须满足板上 I/O 电气条件。
- 引导程序使用内部 HSI 经 PLL 得到 24 MHz 时钟，运行不依赖外部晶体。

依据：[AN2606 Rev70，Table 2、§21.1、Table 45](https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf#page=116)。TX/RX 交叉接线与共地是按收发方向得到的接线要求。

## 先握手，再查询能力

1. 发送单字节 `0x7F`，用于串口速率识别。
2. 收到 `0x79` 表示 ACK，可以开始命令交互；`0x1F` 表示 NACK。
3. 发送 Get 命令 `0x00 0xFF`，按返回帧读取版本与支持的命令列表。
4. 身份查询使用 Get ID 命令。后续命令以设备返回的能力列表为准。

普通命令由命令字节及其按位取反字节组成，两者异或为 `0xFF`。数据块的 XOR 校验规则另行定义，不能把这两个规则混用。

依据：[AN3155 Rev22，§1、§3、§3.1](https://www.st.com/resource/en/application_note/an3155-how-to-use-usart-protocol-in-bootloader-on-stm32-mcus-stmicroelectronics.pdf#page=5)。本页没有执行任何板端命令；也未提供擦除、写入或修改保护状态的操作流程。

## RAM 地址要避开引导程序占用

引导程序占用从 `0x20000000` 开始的 512 字节 RAM。AN2606 记录 V2.2 会拒绝 Read Memory、Write Memory 和 Go 对这一区域的访问；设备参数表列出的可用 RAM 范围为 `0x20000200～0x20004FFF`。

准备 RAM 下载程序时，应同时核对装载地址、程序占用和栈空间，不能沿用从 SRAM 起点开始的普通链接布局。

依据：[AN2606 Rev70，§21.1、Table 46](https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf#page=116)、[设备相关参数表](https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf#page=518)。

## 连接失败时的排查顺序

先检查 BOOT 电平与复位，再检查 PA9/PA10 接线、共地和 8E1 配置，随后观察发送 `0x7F` 后是否收到 ACK。能收到 ACK 后，再分析命令帧和设备返回的能力列表。

以上为基于官方协议的排查顺序，尚未在具体板卡验证。版本和来源范围见[ROM 串口引导资料](../../来源/ROM串口引导资料.md)。
