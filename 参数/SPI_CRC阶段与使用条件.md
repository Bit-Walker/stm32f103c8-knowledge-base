# SPI CRC 阶段与使用条件

适用 STM32F103C8T6。依据 RM0008 Rev21 §25.3.6（pp715–716）、§25.3.9（p721）、§25.5.5–25.5.7（pp746–748），以及固定 HAL 提交 `bd368aa335c529641d2e567574885e02deacc64a`。本文覆盖硬件阶段、寄存器含义和驱动使用条件；尚未提供与指定外部协议逐比特对齐的 CRC 算法验证或实板测试。

## 计算器与数据宽度

CRC（Cyclic Redundancy Check，循环冗余校验）在发送、接收方向各有独立计算器；按 SPI_CRCPR 中的可编程多项式逐位计算，采样边沿由 CPOL/CPHA 决定。数据帧宽度 DFF 同时决定本 SPI 的 CRC 宽度：8 位数据使用 8 位 CRC，16 位数据使用 16 位 CRC。

| 寄存器 | 相对 SPI 基址偏移 | 复位值 | 功能与访问条件 |
|---|---|---|---|
| SPI_CRCPR：CRC Polynomial Register | 0x10 | 0x0007 | 多项式配置，可按需要更改；不能只凭复位值认定已匹配某外部协议的完整 CRC 参数 |
| SPI_RXCRCR：RX CRC Register | 0x14 | 0x0000 | 接收方向计算结果，只读；8 位帧只考虑低 8 位，16 位帧考虑全 16 位 |
| SPI_TXCRCR：TX CRC Register | 0x18 | 0x0000 | 发送方向计算结果，只读；宽度规则同上 |

RM0008 pp747–748 明确：BSY=1 时读取 RXCRCR 或 TXCRCR 可能得到错误值。p748 首段写 TxCRC[7:0]，随后明确 16 位帧使用全部 16 位；这里保留按帧宽度区分的完整条件。

## CPU 搬运与 DMA 搬运的 CRC 阶段

CRCEN（CRC Calculation Enable）位于 SPI_CR1（Control Register 1），使能 CRC 计算并重置收发 CRC 寄存器。RM0008 p742 要求在 SPE=0 时修改 CRCEN。CRCNEXT（CRC Transfer Next）用于指定随后的 CRC 阶段。

| 搬运与方向 | 手册要求 |
|---|---|
| CPU，全双工或仅发送 | 最后一项数据写入 SPI_DR 后立即设置 CRCNEXT，在末项结束前完成该操作；随后发送计算得到的 CRC |
| CPU，仅接收 | 收到倒数第二项数据后设置 CRCNEXT，为末项数据之后的 CRC 阶段作准备 |
| DMA | 数据尾部 CRC 的发送和接收自动完成，不使用 CRCNEXT；CRC 接收后仍须读 SPI_DR 清 RXNE |

SPI_DR（Data Register）是数据寄存器。CRC 传输阶段计算被冻结；全双工或仅接收时，接收的 CRC 与本地 SPI_RXCRCR 比较，不匹配置 SPI_SR（Status Register）的 CRCERR。置 ERRIE 可产生相应错误中断。这里的“自动完成”来自硬件章节，并不免除正确 DMA 配置、驱动限制和错误处理。

仅接收的倒数第二项要求按原文保留，不据此给出已验证的单项接收实现。高位速率时，RM0008 p716 要求 CRCNEXT 在末项结束前写入，并警告 CRC 发送关键序列中的软件函数调用可能导致末项或 CRC 错误；不能假设函数分层和任意中断延迟都满足时序。

## 从机时钟、片选与重新同步

- 从机应在 SCK 稳态时使能 CRC。RM0008 p716 指出 CRCEN=1 后 CRC 已对从机 SCK 输入敏感，与 SPE 的取值无关。
- 硬件 NSS 从机在数据阶段到 CRC 阶段之间必须持续保持选中（NSS 低）。
- 从机 NSS 高时 CRC 仍可能计算，多从机场景尤其需要注意。取消选择与重新选择之间，主从双方须协调重置 CRC；具体顺序及 ES096 的另外一项冻结限制见[SPI 状态与 CRC 勘误](SPI状态标志与停机边界.md#crc-的两项器件勘误)。

## 固定 HAL 的额外使用条件

固定驱动文件的使用说明明确指出：DMA 循环模式不管理 CRC 功能；主机双线 RXONLY 和主机单线接收不能使用 DMA 循环模式。不能因回调实现存在 CIRC 分支，就认为以上配置得到驱动支持。

同一使用说明要求 HAL_SPI_DMAPause / HAL_SPI_DMAStop 在 SPI 回调中使用；主机 RXONLY 或单线接收为避免发起新传输，另列 DeInit 后 Init 的流程。它们是该版本声明的使用条件，具体停机、片选与在途数据仍需结合[HAL DMA 路径](HAL_SPI接收与DMA启动边界.md)和[初始化边界](SPI片选与HAL初始化边界.md)判断。

来源：[固定 HAL 使用限制 L56–70](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L56-L70)。固定源文件 Git blob：`d1c741075bc63718c9032bab7fd9eb23cc4a880b`。

官方手册：[RM0008](https://www.st.com/resource/en/reference_manual/cd00171190-stm32f101xx-stm32f102xx-stm32f103xx-stm32f105xx-and-stm32f107xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf)。在线文件可能更新，本文使用 Rev21 的所列页码。
