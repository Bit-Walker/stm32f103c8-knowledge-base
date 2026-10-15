# SPI 片选与 HAL 初始化边界

依据 RM0008 Rev21 §25.3.1–25.3.3（pp703–707）、§25.5.1–25.5.2（pp742–744），并交叉检查固定 STM32F1 HAL 提交 `bd368aa335c529641d2e567574885e02deacc64a`。以下为文档与源码核查，未做板级时序验证。

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
- `TIMode` 应配置为 `SPI_TIMODE_DISABLE`。

来源：[HAL_SPI_Init L330–455](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L330-L455)。源码 Git blob 为 `d1c741075bc63718c9032bab7fd9eb23cc4a880b`，头文件 Git blob 为 `309eb5bd2397b23ec7fb652c4a9ee29875d4f424`。

## SPI_InitTypeDef 全部初始化字段

下表列出固定头文件的全部 11 个字段，均为 `uint32_t`。枚举宏是配置编码；不能把分频数或模式序号直接代替宏值。

| 字段 | 固定版本的取值 | 对应含义与条件 |
|---|---|---|
| Mode | SPI_MODE_MASTER / SPI_MODE_SLAVE | 主／从模式；主机宏包含 MSTR 和 SSI |
| Direction | SPI_DIRECTION_2LINES / SPI_DIRECTION_2LINES_RXONLY / SPI_DIRECTION_1LINE | 双线全双工／双线只接收／单线双向模式；单线具体发送或接收方向还需相应传输路径设置 |
| DataSize | SPI_DATASIZE_8BIT / SPI_DATASIZE_16BIT | 数据帧宽度；8／16 位配置与 CRC 宽度关联 |
| CLKPolarity | SPI_POLARITY_LOW / SPI_POLARITY_HIGH | SCK 空闲时低／高 |
| CLKPhase | SPI_PHASE_1EDGE / SPI_PHASE_2EDGE | 第一／第二个时钟跳变沿采样；对应边沿的上升或下降由极性共同决定 |
| NSS | SPI_NSS_SOFT / SPI_NSS_HARD_INPUT / SPI_NSS_HARD_OUTPUT | 软件选择／硬件输入／硬件输出，详见上文的主从适用条件 |
| BaudRatePrescaler | SPI_BAUDRATEPRESCALER_2、_4、_8、_16、_32、_64、_128、_256 | 主机串行时钟分频选择；从机不以此设置外部输入 SCK，且 Init 会改写该字段 |
| FirstBit | SPI_FIRSTBIT_MSB / SPI_FIRSTBIT_LSB | 最高有效位／最低有效位先传 |
| TIMode | SPI_TIMODE_DISABLE | 本器件只允许关闭 TI 模式 |
| CRCCalculation | SPI_CRCCALCULATION_DISABLE / SPI_CRCCALCULATION_ENABLE | CRC 关闭／开启；还受 USE_SPI_CRC 构建配置和循环 DMA 使用限制约束 |
| CRCPolynomial | 1～65535 的奇数 | CRC 多项式配置值；该范围不保证与任意外部 CRC 协议匹配 |

来源：[结构字段 L45–84](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal_spi.h#L45-L84)、[取值宏 L202–296](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal_spi.h#L202-L296)。波形含义结合 RM0008 pp703–705；该表不替代电气时序和驱动吞吐限制。

### CRC 参数校验的边界

`CRCPolynomial` 字段注释与 `IS_SPI_CRC_POLYNOMIAL` 的实际表达式均要求 1～65535 且为奇数；该检查宏上方的参数注释却写下界 0，并未列奇数条件。这里保留差异，使用与字段说明及表达式一致的范围。

`HAL_SPI_Init` 在 `USE_SPI_CRC != 0` 且 CRC 开启时通过 `assert_param` 检查多项式；当 `USE_SPI_CRC=0` 时，函数把句柄中的 CRCCalculation 改为 DISABLE。不能将上述断言契约解释成任何构建下非法值都会返回 HAL_ERROR。

来源：[检查宏及其注释 L619–626](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal_spi.h#L619-L626)、[CRC 构建分支 L377–385](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L377-L385)。本节未测试非法参数在特定工程构建下的实际后果。

## 配置字段的硬件写入条件

RM0008 对以下字段规定了不同的修改条件。配置结构中的字段赋值本身不会改写外设；实际寄存器写入仍须满足对应条件。

| SPI_CR1 字段 | 含义 | 原厂写入条件 |
|---|---|---|
| DFF（Data Frame Format） | 8／16 位数据帧格式 | 仅在 SPE=0、SPI 禁用时写入 |
| CRCEN（Hardware CRC Calculation Enable） | 硬件 CRC 计算使能 | 仅在 SPE=0、SPI 禁用时写入 |
| LSBFIRST（Frame Format） | 数据位先后顺序 | 通信进行中不得改变 |
| BR[2:0]（Baud Rate Control） | 主机串行时钟分频 | 通信进行中不得改变 |
| MSTR（Master Selection） | 主／从模式选择 | 通信进行中不得改变 |
| CPOL（Clock Polarity）、CPHA（Clock Phase） | 时钟极性和采样相位 | 通信进行中不得改变 |

来源：RM0008 Rev21 §25.5.1 pp742–744。“SPI 禁用”和“通信未进行”按原文分别保留；正常停止通信的时点见[状态标志与停机边界](SPI状态标志与停机边界.md)。

固定版本 `HAL_SPI_Init` 先调用 `__HAL_SPI_DISABLE`，然后整体写 CR1 和 CR2。CR2 的写入值仅保留所选 SSOE，因此该次写入也清除 SPI 的 Tx/Rx DMA 请求使能以及 TXE/RXNE/ERR 中断使能。函数本身没有调用 DMA Abort，也没有等待 TXE/BSY 完成正常收尾。其末尾清 ErrorCode 并把 SPI 句柄置为 READY；这些软件状态不能证明之前的数据传输已经正常结束或相连 DMA 通道已经完成清理。

来源：[HAL_SPI_Init L330–455](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L330-L455)、RM0008 Rev21 §25.5.2 p744。此处说明函数自身的固定实现；应用自定义 MspInit 回调可能另有操作，未据此断言所有工程的完整初始化流程相同。

## DeInit 与回调生命周期

以下结论限定于上述固定 HAL 提交，不包含应用自行扩展的资源管理。

### DeInit 的硬件动作与 MSP 职责

`HAL_SPI_DeInit` 将句柄设为 BUSY，调用 `__HAL_SPI_DISABLE`，执行 MspDeInit，随后清 ErrorCode、把 State 设为 RESET 并解锁。`__HAL_SPI_DISABLE` 仅清 SPI_CR1.SPE；函数内的“Disable the SPI Peripheral Clock”注释不能据以认定 RCC 的 SPI 时钟已关闭。

默认弱 `HAL_SPI_MspDeInit` 函数仅处理未使用参数，没有实际清理 GPIO、RCC、NVIC 或 DMA。实际资源释放取决于应用覆盖的 MSP 函数或注册的 MspDeInitCallback。DeInit 主体也未等待 TXE/BSY、未调用 DMA Abort；不能仅凭 HAL_OK 或 State=RESET 判断先前传输已正常收尾、所有硬件资源已经复位。

来源：[HAL_SPI_DeInit L458–499](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L458-L499)、[默认 MspDeInit L523–531](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L523-L531)、[使能／禁用宏 L434–446](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal_spi.h#L434-L446)。

### 运行时注册回调的状态条件

`USE_HAL_SPI_REGISTER_CALLBACKS=1` 时，RegisterCallback 和 UnRegisterCallback 的状态分支如下。此表描述到达状态检查后的允许范围，不穷举锁处理等其他返回路径。

| SPI 句柄 State | 允许的 CallbackID 类型 |
|---|---|
| READY | Tx/Rx/TxRx 完成，Tx/Rx/TxRx 半完成，Error、Abort，以及 MspInit、MspDeInit，共十类 |
| RESET | 仅 MspInit、MspDeInit |
| 其他状态 | 状态分支报 HAL_ERROR 并置 HAL_SPI_ERROR_INVALID_CALLBACK |

不支持的 CallbackID 也置 INVALID_CALLBACK 并报 HAL_ERROR。RegisterCallback 的 pCallback=NULL 检查直接报错；UnRegisterCallback 成功时把所选指针恢复为对应默认弱函数，不是置 NULL。

来源：[RegisterCallback L537–651](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L537-L651)、[UnRegisterCallback L652–749](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L652-L749)。

### DeInit 后重新 Init 的回调恢复条件

Init 的 RESET 分支将 TxCplt、RxCplt、TxRxCplt、TxHalfCplt、RxHalfCplt、TxRxHalfCplt、Error、AbortCplt 八个回调指针重新设为对应默认弱函数。因此，应用通过 RegisterCallback 安装的这八类回调，在正常 DeInit→Init 后需要按应用需求重新注册，并检查返回结果。

这与链接时覆盖默认弱函数的方式不同：覆盖后的同名函数仍是该工程中的默认实现。已有非空 MspInitCallback 在 Init 中保留；DeInit 仅在 MspDeInitCallback 为 NULL 时补入默认函数。不要把八个数据／错误回调的重置规律套用到两个 MSP 指针上。

来源：[Init RESET 分支 L389–418](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L389-L418)、[DeInit MSP 分支 L479–490](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_spi.c#L479-L490)。这是对固定源码分支的归纳，未作板级验证。

## GPIO 配置与引脚映射入口

SPI 的 GPIO 模式取决于主／从、单双线、点对点或多从机以及 NSS 管理方式。按[引脚复用与 AFIO 的 SPI 信号表](引脚复用与AFIO.md#外设模式)选择模式；同页的[通信映射表](引脚复用与AFIO.md#通信定时器映射)列出 SPI1 默认与重映射引脚及 JTAG 引脚释放条件。原厂依据为 RM0008 Rev21 Table25 p167、Table56 p181，避免将所有 SPI 引脚统一配置成复用推挽。

官方手册：[RM0008](https://www.st.com/resource/en/reference_manual/cd00171190-stm32f101xx-stm32f102xx-stm32f103xx-stm32f105xx-and-stm32f107xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf)。在线文件可能更新，本文以 Rev21 的所列页码为准。
