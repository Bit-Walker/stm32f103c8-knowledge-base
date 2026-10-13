# SPI 片选与 HAL 初始化边界

适用 STM32F103C8T6。依据 RM0008 Rev21 §25.3.1–25.3.3（pp703–707）、§25.5.1–25.5.2（pp743–744），并交叉检查固定 STM32F1 HAL 提交 `bd368aa335c529641d2e567574885e02deacc64a`。以下为文档与源码核查，未做板级时序验证。

## NSS 的三种管理配置

NSS（Slave Select，低有效片选）可参与内部选择判定或作为主机片选输出。SSM（Software Slave Management）和 SSI（Internal Slave Select）位于 SPI_CR1（Control Register 1）；SSOE（SS Output Enable）位于 SPI_CR2（Control Register 2）。

| 配置 | 官方定义及适用条件 | 开发时需要保留的边界 |
|---|---|---|
| SSM=1，软件管理 | 内部选择信息由 SSI 提供，外部 NSS 引脚可用于其他功能 | SSI 控制内部选择状态；不能把修改 SSI 当作外部 GPIO 片选电平操作 |
| SSM=0、SSOE=1，硬件输出 | 用于主机；NSS 在主机开始通信时拉低，保持低直到 SPI 禁用 | 不保证每个数据项、DMA TC 或 HAL 调用结束时产生高脉冲 |
| SSM=0、SSOE=0，硬件输入 | 从机 NSS 低选中、高取消；主机可用于多主机配置 | 主机配置流程要求 NSS 输入在传输期间保持高；从机须满足有效片选条件 |

来源：RM0008 p703、p706、p707。主机的软件管理配置为 SSM=1、SSI=1；从机为 SSM=1、SSI=0。SPE（SPI Enable）为 SPI_CR1 的外设使能位，清零前须按具体模式完成[正常停机顺序](SPI状态标志与停机边界.md)。

“外部 NSS 可用于其他功能”仍受引脚复用和器件勘误限制。ES096 的 SPI1/USART2、SPI2/USART3、I2C2/SPI2 内部复用冲突及规避条件见[GPIO 内部复用冲突](GPIO内部复用冲突.md)。不能单凭软件 NSS 模式断定其他复用输出一定正常。

## HAL 配置怎样对应片选位

固定头文件中，`SPI_MODE_MASTER` 同时包含 MSTR（Master Selection）和 SSI；`SPI_MODE_SLAVE` 为零。`SPI_NSS_SOFT` 对应 SSM；`SPI_NSS_HARD_INPUT` 为零；`SPI_NSS_HARD_OUTPUT` 把 SSOE 左移 16 位编码。

`HAL_SPI_Init` 将 Mode 中的 MSTR/SSI 和 NSS 中的 SSM 组合到 CR1 配置表达式中，再将 NSS 右移 16 位后的 SSOE 部分用于 CR2。因而软件 NSS 的主／从内部 SSI 值来自 Mode 选项；NSS 选项本身没有提供一个任意外部片选 GPIO。

来源：[模式与 NSS 宏 L205–257](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal_spi.h#L205-L257)、[初始化寄存器配置 L420–455](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L420-L455)。

## HAL 正常返回与外部片选的关系

以固定版本的阻塞 `HAL_SPI_Transmit` 为例：正常末尾通过 `SPI_EndRxTxTransaction` 等待 TXE=1、BSY=0，随后置句柄 READY 并返回。该正常收尾路径不主动禁用 SPI。因此，在主机硬件 NSS 输出配置下，不能把这次函数正常返回当作 NSS 已释放的证据。

这是由手册 NSS 保持条件与具体函数路径共同得到的结论，适用所列路径。主机单线接收和双线 RXONLY 的 `SPI_EndRxTransaction` 会调用禁用 SPI；不能把发送路径的结论泛化为所有接收模式。实际外部片选还取决于引脚配置、板级连接以及应用是否执行额外操作。

来源：[阻塞发送末尾 L926–949](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L926-L949)、[接收和收发收尾函数 L3641–3694](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L3641-L3694)。DMA 的启动、回调和错误条件见[HAL SPI 接收与 DMA](HAL_SPI接收与DMA启动边界.md)。

## 初始化入口的适用边界

- 只有句柄 `State=HAL_SPI_STATE_RESET` 分支执行 MspInit 或已注册的 MspInitCallback；再次调用 Init 不保证重复配置 GPIO、时钟和 NVIC。
- Init 的流程没有先等待已有传输正常结束。运行中重新初始化需要应用协调，不能作为受控收尾的替代步骤。
- 有效 Motorola 从机配置下，Init 会把句柄中的 BaudRatePrescaler 改为 DIV2；RM0008 p706 明确从机的 BR 位不决定接收到的串行时钟速率。
- 本器件不支持 TI 模式，TIMode 应为 `SPI_TIMODE_DISABLE`。源码中的其他条件分支不能用作支持 TI 模式的依据。

来源：[HAL_SPI_Init L330–455](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L330-L455)。源码 Git blob 为 `d1c741075bc63718c9032bab7fd9eb23cc4a880b`，头文件 Git blob 为 `309eb5bd2397b23ec7fb652c4a9ee29875d4f424`。

官方手册：[RM0008](https://www.st.com/resource/en/reference_manual/cd00171190-stm32f101xx-stm32f102xx-stm32f103xx-stm32f105xx-and-stm32f107xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf)。在线文件可能更新，本文以 Rev21 的所列页码为准。
