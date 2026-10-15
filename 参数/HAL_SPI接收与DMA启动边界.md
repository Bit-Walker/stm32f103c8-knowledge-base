# HAL SPI 接收与 DMA 启动边界

固定实现为 ST 官方 stm32f1xx-hal-driver 提交 `bd368aa335c529641d2e567574885e02deacc64a`。本文核查 SPI（Serial Peripheral Interface，串行外设接口）的接收入口、双 DMA 启动及停止分支；不代表完整 SPI 手册，不包含编译或实机验收。

硬件状态与正常收尾见[SPI 状态标志与停机边界](SPI状态标志与停机边界.md)，包含清标志副作用及 CRC 器件勘误。

## 主机双线接收会发送缓冲区内容

在 `SPI_MODE_MASTER` 且 `SPI_DIRECTION_2LINES` 时，HAL_SPI_Receive 将状态置为 BUSY_RX，并调用 HAL_SPI_TransmitReceive，同一个 pData 同时作为发送与接收缓冲区。中断版 Receive_IT 和 DMA 版 Receive_DMA 使用相同的转交方式。本文中的 BUSY_RX、READY 等是 HAL 软件状态，不是线路测量结果。

这条路径通过发送产生时钟，发送数据来源是传入的缓冲区，不是库自动填充的固定 0 或 0xFF。若从设备对占位字节有要求，应明确准备发送数据；需要独立控制收发内容时，可使用分离发送、接收缓冲区的收发接口，并按从设备协议设计事务。异步传输结束前须保持缓冲区有效，不能由 CPU 随意改写。

此结论仅针对上述主机双线分支；单线、双线只接收模式及从机行为不能直接套用。Size 的官方说明为 u8 或 u16 数据元素数量，应结合 DataSize 判断，不能无条件当作字节数。

来源：[轮询接收](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L952-L989)、[中断接收](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L1522-L1542)、[DMA 接收](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L1804-L1828)。

## Receive_DMA 在此分支需要两路 DMA

主机双线 Receive_DMA 会转交 TransmitReceive_DMA，使用 SPI 句柄关联的接收 DMA 句柄 hdmarx 和发送 DMA 句柄 hdmatx。不能因为 API 名称包含 Receive，就只配置接收 DMA。

TransmitReceive_DMA 保留入口的 BUSY_RX 状态，并由此为接收 DMA 选择接收完成路径；普通收发调用则选择收发完成路径。发送 DMA 的半完成、完成、错误及中止回调被设为 NULL；事务关闭安排在接收完成路径。应用应正确关联句柄、DMA 通道、IRQ 分发及缓冲区，避免把发送 DMA 完成当作全部事务完成。

这描述的是当前驱动如何设置回调，不代表已覆盖循环模式、CRC、线路忙状态或所有错误恢复情形。

来源：[双 DMA 初始化、回调及启动](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L1914-L2041)。

## 启动失败可能留下部分状态

该版本先启动接收 DMA，成功后置位 SPI 接收 DMA 请求使能位 RXDMAEN，再启动发送 DMA。

| 失败位置 | 该错误返回分支执行的动作 | 不能假定自动完成的动作 |
|---|---|---|
| 接收 DMA 启动失败 | 设置 SPI DMA 错误、解锁 SPI、返回 HAL_ERROR | 不在此分支恢复 SPI READY |
| 发送 DMA 启动失败 | 设置 SPI DMA 错误、解锁 SPI、返回 HAL_ERROR | 不在此分支中止已启动的接收 DMA、清 RXDMAEN 或恢复 SPI READY |

以上是外层返回分支的静态事实。实际已接收多少数据、是否已有 DMA 中断发生，取决于硬件和并发时序。错误返回后不能直接认为“什么都没启动”，也不能只改软件 State 再重试。

匹配版本 HAL_DMA_Start_IT 在 READY 路径将 DMA 状态转为 BUSY，配置并启用通道；其他状态路径返回 HAL_BUSY。其完整入口还受句柄锁约束。应用应先确认通道所有权及错误发生位置，保存错误信息，再按实际活动状态清理；不得为恢复此事务而盲目中止其他所有者的 DMA。

来源：[SPI 启动错误分支](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L1990-L2023)、[匹配 DMA 启动实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L361-L405)。

## DMAStop 的返回值与硬件状态分别核对

HAL_SPI_DMAStop 对每个非空 Tx/Rx DMA 句柄调用阻塞 HAL_DMA_Abort。任一路失败会记录 SPI DMA 错误并令返回值为 HAL_ERROR；之后仍清除 SPI 的发送／接收 DMA 请求使能位 TXDMAEN／RXDMAEN，并设置 SPI READY。

匹配 HAL_DMA_Abort 仅在 DMA BUSY 路径关闭中断和通道、清标志并恢复 READY；非 BUSY 路径设置 NO_XFER、解锁并返回 HAL_ERROR。该阻塞函数不调用传输完成或中止回调。SPI DMAStop 开头有关 DMA Abort 生成完成回调的注释，不能替代这份实际实现。HAL_DMA_Abort_IT 是另一个接口，在其 BUSY 路径会调用非空中止回调。

DMAStop 本身不关闭 SPI、不清传输计数、不清接收溢出标志 OVR（Overrun），也不等待忙状态标志 BSY（Busy）。因此返回 ERROR 不等于完全未清理，SPI READY 也不等于线路已结束。外设剩余数据、片选和从设备协议状态须另外核对，不能把这个函数当作无条件恢复整笔事务的保证。

来源：[SPI DMAStop](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L2401-L2435)、[阻塞与中断 DMA Abort](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L415-L491)。

## Pause / Resume 操作与在途数据

固定版本的 HAL_SPI_DMAPause 在锁宏之后清除控制寄存器 2（CR2，Control Register 2）中的 TXDMAEN、RXDMAEN，随后解锁。函数体不等待 TXE/BSY、不禁用 SPI、不调用 HAL_DMA_Abort，也不清传输计数或修改 SPI 句柄 State。暂停 DMA 请求不能据此解释成在途数据、移位过程或外部时钟均已停止。

HAL_SPI_DMAResume 在锁宏之后同时设置 TXDMAEN、RXDMAEN。它没有保存暂停前的请求使能掩码，也未按 Direction、State 或关联 DMA 句柄是否存在选择单一方向；因而不能假定它只恢复暂停前开启的那一路请求。

这两个函数都不显式重新配置 DMA 地址、长度或通道状态。Resume 不能代替重新建立已 Abort 的 DMA 事务；还需核对通道、缓冲区、SPI 模式和从设备协议。基础锁宏未在此展开，不能把正常尾部的 HAL_OK 推广成任意入口条件都返回成功。

以上是固定源码控制流核查，不是板级暂停时序保证。驱动使用说明要求 Pause/Stop 在 SPI 回调内调用，相关循环模式限制继续适用。

来源：[Pause / Resume L2355–2393](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L2355-L2393)、[使用条件 L56–70](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L56-L70)。

## 完成回调、循环模式与传输错误

以下继续限定于上述固定版本的双 DMA 接收／收发路径。

先满足该版本[使用说明 L56–70](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L56-L70)的限制：主机双线 RXONLY 和主机单线接收不能使用 DMA 循环模式；DMA 循环模式不管理 CRC 功能。该说明还要求 HAL_SPI_DMAPause / HAL_SPI_DMAStop 在 SPI 回调内调用，并对主机 RXONLY／单线接收列出 DeInit 后 Init 以避免新传输的流程。下面的实现分析不放宽这些使用条件；CRC 硬件阶段见[SPI CRC 阶段与使用条件](SPI_CRC阶段与使用条件.md)。

| 接收 DMA 配置 | 完成回调路径的动作 | 使用边界 |
|---|---|---|
| 普通模式，接收入口 | 关闭 SPI ERR 中断、处理所启用的 CRC、撤销相应 DMA 请求、检查终结条件、清 Rx 计数、置 READY；有错误时转错误回调 | 主机双线会撤销两路 DMA 请求；该接收完成路径只清 RxXferCount，不能单凭 TxXferCount 残值判定仍在传输 |
| 普通模式，收发入口 | 关闭 ERR 中断、处理所启用的 CRC、检查终结条件、撤销两路请求、清 Tx/Rx 计数、置 READY；有错误时转错误回调 | 回调结果仍需结合错误状态与从设备协议 |
| 循环模式 | 跳过上述普通模式清理块，调用相应完成回调 | 一次回调不表示停机、请求关闭或软件状态 READY；缓冲区会继续参与传输 |

这里以接收 DMA 通道 CCR 的 CIRC 位选择分支。它不证明任意 Tx/Rx 模式组合都有效；配对配置与应用缓冲区所有权仍须一致。

普通收发终结助手先等待 TXE 置位，再等待 BSY 复位。接收终结助手在主机单线或双线 RXONLY 时关闭 SPI；主机 RXONLY 等待 RXNE 复位，其余分支等待 BSY 复位。此版本等待助手除 HAL_GetTick 检查外，还设有软件递减计数兜底；Timeout 不等于 HAL_MAX_DELAY 时，计数归零会令后续检查退出超时。因此不能把默认 HAL_Delay 的时基停滞行为直接套到这个助手，也不能把软件循环次数当作精确毫秒计时保证。

来源：[接收完成](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L2788-L2877)、[收发完成](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L2887-L2972)、[终结条件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L3571-L3695)。

### Tx 与 Rx 的 DMA 错误上报不对称

该收发启动路径给 Rx DMA 安装 SPI_DMAError，却把 Tx DMA 的 XferErrorCallback 置为 NULL。匹配 HAL_DMA_IRQHandler 在实际进入 TE 分支时，先关闭故障通道的 DMA 中断、清标志、记录 DMA 错误并置 DMA READY、解锁，再调用非空的错误回调。

因此单独处理 Tx DMA TE，不会通过这一空回调链调用 SPI_DMAError 或用户 SPI 错误回调。这里不能扩大为“所有发送错误都不会通知”：其他 SPI 中断和应用监测仍可能发现异常。DMA IRQ 的 HT、TC、TE 使用 if/else-if 顺序，也不能假设多个标志同时存在时 TE 总在第一次进入 IRQ 时优先处理。

Rx TE 经 SPI_DMAError 则会清两路 SPI DMA 请求，记录 SPI DMA 错误、置 SPI READY 并调用错误回调；这个外层函数本身不显式中止对端 Tx DMA，也不清 SPI 传输计数。

RM0008 Rev21 §13.3.5 p280 说明 DMA 传输错误由硬件清除故障通道 EN 并置 TEIF；仅在 TEIE 使能时产生该错误中断。还须叠加 ES096 Rev15 §2.4.1 的例外：活动通道的全局 GIF 清除若与传输错误在同一时钟周期发生，自动禁用可能失败且 TEIF 不置位；活动期间应使用各事件的专用清除位。详见[DMA 标志与勘误约束](DMA参数与HAL接口.md)。硬件的一般错误处理动作不等于同时清理两路 DMA、SPI 请求和从设备事务。故障取证需区分 SPI 状态、两个 DMA 状态、请求位及实际线路，不宜只用是否收到 SPI ErrorCallback 判断健康。

来源：[回调赋值](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L1970-L2012)、[DMA IRQ](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L602-L680)、[SPI DMA 错误回调](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L3031-L3047)。DMA1 固定映射及共享请求条件复用[DMA 参数与 HAL 接口](DMA参数与HAL接口.md)；RM0008 Rev21 §13.3.7 Table78 p282 中 SPI1 Rx/Tx 分别为 Ch2/Ch3，SPI2 Rx/Tx 分别为 Ch4/Ch5，不能把同通道的多个请求视为独立队列。

## SPI IRQ 错误链与 DMA 错误链

以下限定同一固定 HAL 版本。SPI 外设的 OVR/MODF 错误与 DMA 控制器自身的 TE 错误从不同入口处理，回调行为须分别核查。

`HAL_SPI_IRQHandler` 先读取 CR2/SR 快照。没有 OVR 且 RXNE 和对应中断使能成立时，调用 RxISR 并返回；随后检查 TXE 和对应中断使能，成立则调用 TxISR 并返回；再检查 MODF/OVR 与 ERR 中断使能。这个顺序是单次调用的控制流，不是 NVIC 优先级，也不表示同时存在的标志会一次处理完。

在 OVR 分支中，State=BUSY_TX 时仅清 OVR 后返回，不记录 OVR 错误；同一快照若有 MODF，也不会在这个返回之后继续处理。不能据此断言后续中断永远不会处理 MODF。

进入错误处理且 ErrorCode 非零后，函数关闭 RXNE/TXE/ERR 中断，先将 SPI State 设为 READY。若入口 CR2 快照含任一 DMA 请求使能，则清两个请求位，依次为非空 Rx、Tx DMA 句柄设置 SPI_DMAAbortOnError，再分别调用 HAL_DMA_Abort_IT；失败时追加 SPI ABORT 错误。

匹配的 HAL_DMA_Abort_IT 在 BUSY 分支内同步调用中止回调。SPI_DMAAbortOnError 清两个 SPI 软件计数，然后直接调用用户 ErrorCallback，没有等待另一方向完成，也没有跨通道合并通知。

由此得到有条件的静态结论：若确实进入上述 DMA 错误分支，两个句柄非空且在各自 Abort_IT 调用时均为 BUSY，用户回调不改动相关状态或指针，则同一次 SPI IRQ 可同步调用两次 ErrorCallback。第一次发生在 Rx Abort 内，早于 IRQ 随后调用 Tx Abort；第一次回调不能作为 Tx DMA 通道已经禁用的证据。

只有一路有效、某路 DMA 已不处于 BUSY、回调修改状态或数据分支提前返回等条件会改变路径。应用不能无条件假定一次错误恰好通知一次，也不能仅凭 SPI READY 判断旧清理调用栈已经返回。用户主动 Abort_IT 使用另一个双通道回调协调逻辑，不能与这里的错误链混用。未穷举回调重入与中断交错，未做板级验证。

来源（固定提交 bd368aa335c529641d2e567574885e02deacc64a）：[SPI IRQ L2443–2543](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L2443-L2543)、[SPI_DMAAbortOnError L3054–3066](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L3054-L3066)、[DMA Abort_IT L456–491](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L456-L491)。

## Abort / Abort_IT 的完成时点与清理条件

以下只核查固定版本的所列分支；未穷尽用户回调重入、重新启动和所有中断交错，不作为可直接套用的完整故障恢复流程。

### 阻塞 Abort 的 DMA 分支

HAL_SPI_Abort 同时检查相应 SPI DMA 请求位和对应 DMA 句柄是否非空。请求位清除操作放在非空句柄的分支内；请求位与句柄配置不一致时，最后的 SPI READY 或传输计数归零不能证明该请求位已经清除。

| 分支条件 | 对应 DMA 清理与外设动作 |
|---|---|
| TXDMAEN 已置位且 hdmatx 非空 | 清 DMA 中止回调指针，调用阻塞 HAL_DMA_Abort，清 TXDMAEN，再等待 TXE；这个分支本身没有等待 BSY 或禁用 SPE |
| RXDMAEN 已置位且 hdmarx 非空 | 清 DMA 中止回调指针，调用阻塞 HAL_DMA_Abort，禁用 SPI，再清 RXDMAEN |

随后函数清两方向软件计数、处理错误码、清 OVR、将 SPI 句柄置 READY。两方向动作不同，软件状态不能统一代表已按正常收尾顺序结束物理事务。这里给出条件路径，不表示正确配置的工程必然出现句柄不一致。

来源：[HAL_SPI_Abort L2057–2185](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L2057-L2185)。

### Abort_IT 回调可以先于函数返回

HAL_SPI_Abort_IT 先配置非空 DMA 句柄的中止回调，再按请求位调用 HAL_DMA_Abort_IT。匹配版本的 HAL_DMA_Abort_IT 在 DMA BUSY 分支中关闭中断和通道、清标志、置 DMA READY、解锁，然后在返回之前直接调用非空 XferAbortCallback。

SPI 的 Tx/Rx DMA 中止回调先清本方向请求和回调指针；若另一方向存在且其中止回调指针仍非空，本次回调返回；否则清软件计数、清 OVR、置 SPI READY 并调用用户 AbortCpltCallback。因此，用户的 SPI 中止完成回调可以发生在 HAL_SPI_Abort_IT 尚未返回的同一调用栈中。入口函数在 abortcplt=1 的收尾分支也直接调用用户回调。

Tx 子回调等待 TXE；Rx 子回调禁用 SPI 后调用 EndRxTxTransaction 检查 TXE/BSY。该差异及可能发生的等待说明，不能仅凭 _IT 后缀推定入口立即返回、回调一定在之后的中断中执行，或回调到达就代表所有物理条件已经无误。

来源：[SPI Abort_IT L2203–2353](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L2203-L2353)、[匹配 DMA Abort_IT L456–491](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_dma.c#L456-L491)、[SPI DMA 中止回调 L3075–3185](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L3075-L3185)。

<a id="术语与来源身份"></a>

## 来源身份

Git blob：SPI C 文件 `d1c741075bc63718c9032bab7fd9eb23cc4a880b`；DMA C 文件 `80b65a4f0eb72ab673bf03b47ec2d45b0856a120`。所有源码链接固定到同一提交，避免将不同版本的启动与清理行为拼接。
