# ROM 串口引导资料

## AN2606

[官方 PDF](https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf)，Rev70。

本次使用 Table 2 的启动条件、§21 的 USART1 引导配置和版本变化，以及设备相关参数表中的 RAM 范围。仅提取目标器件对应内容。

## AN3155

[官方 PDF](https://www.st.com/resource/en/application_note/an3155-how-to-use-usart-protocol-in-bootloader-on-stm32-mcus-stmicroelectronics.pdf)，Rev22。

本次使用 §1 的串口握手、§3 的 ACK/NACK 与命令校验规则，以及 §3.1 的能力查询。完整烧写协议及保护操作尚未整理。

## 正文入口

[ROM 串口引导的连接与识别](../参数/启动/ROM串口连接与识别.md)。

文档修订号与芯片实际引导程序版本分别记录；协议能力以设备查询结果为准。本次为资料核对，未执行串口命令或板端烧写。
