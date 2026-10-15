# SPI 状态标志与停机边界

依据 RM0008 Rev21 §25.3.7–25.3.11（pp717–722）、§25.5.1–25.5.4（pp742–746）及 ES096 Rev15。本文聚焦状态、正常收尾与错误副作用；不是完整 SPI 协议、CRC 算法或全部寄存器表。

## 三个常用状态的含义

| 标志 | 能说明什么 | 不能据此推断什么 |
|---|---|---|
| TXE：Transmit buffer empty | 发送缓冲空，可装入下一项；写 DR 清该标志 | 末位已在线路发送完 |
| RXNE：Receive buffer not empty | 接收缓冲有有效数据；读 DR 清该标志 | 软件已处理或保存该数据 |
| BSY：Busy | 通信层活动状态，由硬件更新 | 任意模式都能用它逐项计数或判断接收结束 |

RM0008 p717 明确：主机双向接收（MSTR=1、BIDIMODE=1、BIDIOE=0）期间 BSY 保持低。连续通信时主机可持续 BSY=1，从机则在数据项之间有一个 SPI 时钟周期的低电平。逐项搬运应按 TXE/RXNE；使用 BSY 必须同时检查工作模式。

DR（Data Register）为数据寄存器；实际完整名称为 SPI_DR。SPI_SR（Status Register）为状态寄存器，SPI_CR1/CR2（Control Register 1/2）为控制寄存器。这里的“发送缓冲”与移位过程是不同阶段。

## 正常收尾按模式选择

RM0008 §25.3.8 p718 给出以下顺序。它们描述正常结束后的停机，不能当作中途故障恢复的无条件处方。

| 模式及条件 | 原厂正常停机顺序 |
|---|---|
| 主／从全双工，BIDIMODE=0、RXONLY=0 | 确认末项 RXNE，等待 TXE=1，再等待 BSY=0，清 SPE |
| 单向只发送，或 BIDIMODE=1、BIDIOE=1 的双向发送 | 末项写入 DR 后等待 TXE=1，再等待 BSY=0，清 SPE |
| 主机 RXONLY，或双向接收 | 第 n−1 次 RXNE 后等待一个 SPI 时钟周期，再清 SPE；随后等待最后一次 RXNE，再考虑停止外设时钟／进入停止状态 |
| 从机 RXONLY，或双向接收 | 清 SPE 后当前传输完成才有效停止；停止时钟之前还须等待 BSY=0 |

n 为本次计划接收的数据项数量。上述 n−1 描述不应擅自扩展为已经验证的 n=1 软件实现；具体单项接收方案还需核对初始化时序、HAL 路径和总线时钟。每次读取接收数据及清 RXNE 的安排也必须与应用或 DMA 配合。

原文差异：p718 最后一种从机模式写了“disable”同时标注 SPE=1。该页开头及 §25.5.1 p743 定义 SPE=0 禁用、SPE=1 使能；本页据字段定义采用清 SPE，并保留矛盾位置。该差异已对原 PDF 页面视觉核对，非文本抽取错误。

## DMA 完成与线路完成

§25.3.9 p719 要求发送 DMA 完成后仍先等待 TXE=1，再等待 BSY=0。DMA 的 TCIF 表示数据搬运完成；末项可能仍在移位发送。对于不连续通信，写 DR 到 BSY 置位存在两个 APB 时钟周期的延迟，不能只在写后立即读到 BSY=0 就关闭外设。

Figures247/248 p720 的三数据项示例分别展示发送末次写 DR 与接收末次读 DR；发送 DMA TC 出现后，线路发送仍可继续。两图已核对，但本页尚未逐波形重绘，不能视为完整原图替代。

HAL 接收分支、DMA 部分启动、普通／循环完成和错误回调条件见[HAL SPI 接收与 DMA 启动边界](HAL_SPI接收与DMA启动边界.md)。硬件章节“只接收可只开 Rx DMA”的一般说明，不能替代主机双线 HAL Receive_DMA 实际需要两路 DMA 的调用条件。

## 错误标志和读写副作用

| 错误 | 影响与清理条件 |
|---|---|
| MODF：Mode fault，模式故障 | 主机选择条件异常可导致 SPE 和 MSTR 被硬件清除；清错误后仍须恢复期望模式和使能状态 |
| OVR：Overrun，接收溢出 | 新数据未能更新已占用接收缓冲；读 DR 后读 SR 清除，丢失的数据不会因清标志恢复 |
| CRCERR：CRC error | SR 中该位写 0 清；不能套用 EXTI/DMA 的写 1 清模板 |

固定 HAL 提交 bd368aa335c529641d2e567574885e02deacc64a 的清 MODF 宏先读 SR，再清 CR1.SPE；不会自动恢复主机模式或重新使能。OVR 宏实际读 DR 后读 SR，因此调试观察或清理调用可能消费接收数据。CRCERR 宏向 SR 写该位为 0 的掩码。

RM0008 p721 的 MODF 清除文字允许 read or write SR；本页保留官方 HAL 采用的读 SR 路径，不建议任意写 SR。p745 OVR/MODF 字段引用到了 I2S 错误章节 §25.4.7，SPI 实际清除序列应对照 §25.3.10 p721。

来源：[固定 HAL 清标志宏 L406–432](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal_spi.h#L406-L432)，Git blob `309eb5bd2397b23ec7fb652c4a9ee29875d4f424`。

## CRC 的两项器件勘误

ES096 Rev15 §2.10.1（p22）：从机启用 CRC 时，即使 NSS 高、器件已取消选择，CRC 仍受通信时钟影响。规避是在取消选择与下次选择之间，主从双方协调重置 CRC：SPE=0，CRCEN=0，CRCEN=1，再 SPE=1。不能只清 CRCERR 就认为 CRC 累积状态已重同步。

§2.10.2（pp22–23）：SPI 主／从、全双工或单向模式启用 CRC，且通过轮询／中断搬运时，同 DMA 通道所连的另一外设进行 DMA 传输，可能在最后或倒数第二项附近使 CRC 冻结。原厂建议在应用允许时改用 SPI DMA；这不是给任意 DMA 配置的可靠性保证。

该修订 p4 矩阵中，两条在 Rev A/B/Z/1/Y/2/3/X 八列均为 A（有该限制），已视觉核查。不推断未列出的芯片修订。引脚内部复用冲突另见[GPIO 内部复用冲突](GPIO内部复用冲突.md)。

官方来源：[RM0008](https://www.st.com/resource/en/reference_manual/cd00171190-stm32f101xx-stm32f102xx-stm32f103xx-stm32f105xx-and-stm32f107xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf)、[ES096](https://www.st.com/resource/en/errata_sheet/es096-stm32f101x8b-stm32f102x8b-and-stm32f103x8b-mediumdensity-device-limitations-stmicroelectronics.pdf)。在线文件可能更新，以上结论以指定修订及页码为准。
