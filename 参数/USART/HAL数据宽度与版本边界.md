# HAL UART/USART：数据宽度、波特率与版本边界

## 1 适用范围与证据

本文比较ST官方STM32F1 HAL驱动的固定v1.1.4提交 de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9 与v1.1.10提交 77fbb30b7a1d02533980400083e48c559aae5a4f，文件为 Src/stm32f1xx_hal_usart.c。§2–§7对应同步USART驱动；§8单独核对异步HAL_UART。两者的波特率宏、状态机等结论不可互相直接套用，也不推广到DMA搬运或其他系列。两份完整源码均已与官方Git blob核对；本轮仅进行源码审查，没有编译、执行原函数或实机验证。

## 2 v1.1.4：9位字长加校验时的内存访问不一致

当 WordLength=USART_WORDLENGTH_9B 且 Parity!=USART_PARITY_NONE 时，线上的有效数据为8位，旧版若干CPU搬运分支却使用 uint16_t 指针访问内存，同时每项仅移动1字节。

|路径|旧版源码位置|内存动作|
|---|---|---|
|HAL_USART_Transmit|L770–789|从uint16_t指针读入发送数据，校验开启时只前移1字节|
|HAL_USART_Receive|L870–879|把DR&0x00FF以uint16_t写入，随后前移1字节|
|HAL_USART_TransmitReceive|L974–1000|发送半字读、接收半字写；校验开启时各前移1字节|
|USART_Transmit_IT内部函数|L2461–2477|发送半字读，前移1字节|
|USART_Receive_IT内部函数|L2533–2544|接收半字写，前移1字节|
|USART_TransmitReceive_IT内部函数|L2616–2658|相同类型的逐字节前移与半字访问|

因此，若应用提供恰好 N 字节的连续缓冲，且该路径正常处理 N 个字符：最后一次半字访问从偏移 N−1 开始，覆盖偏移 N−1 和 N；偏移 N 已在该缓冲之外。接收赋值的高8位为0，在STM32小端内存布局下会额外写下一字节为0。前面的写入也会暂时影响下一位置。发送路径则会额外读取相邻字节。

这里 N 为 Size 指定的字符数（正整数），偏移单位为字节，从0开始。以上为源代码的指针类型、访问宽度和步长推导；实际故障表现受编译器、对齐、缓冲布局和异常设置影响，不能据此承诺某种确定的HardFault或可观察波形。按字节前移还会产生奇地址的半字访问，简单增加一个尾部字节不能作为完整修复证明。

来源：[阻塞发送/接收，v1.1.4 L744–910](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_usart.c#L744-L910)、[阻塞双向 L938–1028](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_usart.c#L938-L1028)、[中断搬运 L2455–2670](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_usart.c#L2455-L2670)。

## 3 v1.1.10：该组合改走字节访问

新版将半字访问条件收窄为“9位字长且无校验”；9位字长加校验改走uint8_t访问，使用0xFF掩码提取有效8位。所核对的阻塞发送、接收、双向收发及对应中断内部函数均采用这一条件。

|帧配置|新版CPU缓冲元素|接收有效数据掩码|
|---|---|---|
|9位、无校验|uint16_t，每项2字节|0x01FF|
|9位、有校验|uint8_t，每项1字节|0xFF|
|8位、无校验|uint8_t，每项1字节|0xFF|
|8位、有校验|uint8_t，每项1字节|0x7F|

阻塞HAL_USART_TransmitReceive另在9位无校验时检查发送、接收指针的2字节对齐，不满足则在加锁/开始传输前返回HAL_ERROR。此检查只按实际出现的函数说明，不能推广为所有API都替调用方检查对齐。DMA仍须按其独立的PSIZE、MSIZE、MINC配置核对缓冲范围。

来源：[v1.1.10 阻塞接口 L740–1055](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L740-L1055)、[中断接口 L2490–2725](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L2490-L2725)。

这是固定版本实现差异，不推断首次修复版本，也不表示v1.1.10所有停止、错误、回调或同步通信路径均已无缺陷。

## 4 分数进位缺陷在两份固定版本中均存在

两版头文件的 USART_BRR 都把分数舍入溢出项写成 `(USART_DIVFRAQ(...) & 0xF0U) << 1U`。若舍入后分数为16，该项加到BRR的是0x20，而按16倍采样的寄存器编码，整数部分进1应只增加0x10。两版 USART_SetConfig 均实际调用此宏写BRR。

以PCLK=36,000,000 Hz、目标波特率=1,130,000 bit/s为例，按宏的无符号整数步骤：

|中间量|结果|
|---|---:|
|DIV = floor(PCLK×25/(4×BaudRate))|199|
|DIVMANT = floor(DIV/100)|1|
|DIVFRAQ = floor(((DIV−DIVMANT×100)×16+50)/100)|16|
|两版HAL USART宏的BRR|0x30，即48|
|相应发生器波特率 PCLK/BRR|750,000 bit/s|
|按最近有效分频选择的BRR|0x20，即32|
|BRR=32对应的发生器波特率|1,125,000 bit/s|

PCLK是所选USART外设时钟频率（Hz），BaudRate是目标波特率（bit/s）；DIV、DIVMANT、DIVFRAQ是宏的无量纲整数中间量，BRR为原始寄存器编码，floor表示向下取整。此例在32位无符号中间量范围内，无须引入乘法溢出来解释差异。

该结果仅为固定源表达式的整数算术核对，未测量引脚输出。不能以“升级到v1.1.10”同时推定本页内存访问问题和这一分频问题都解决。LL_USART_SetBaudRate属于另一套实现，本例中其计算为0x20；驱动名称、版本和最终BRR应分别记录。

来源：[v1.1.4 宏 L606–617](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_usart.h#L606-L617)、[v1.1.10 宏 L610–621](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L610-L621)、[v1.1.10调用点 L2787–2798](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L2787-L2798)。

## 5 回调注册与剩余计数也有版本差异

- v1.1.4 的 HAL_USART_RegisterCallback / UnRegisterCallback 在状态分支前调用 __HAL_LOCK，结束前调用 __HAL_UNLOCK；v1.1.10删除这两处软件锁操作。两版仍按READY/RESET等状态限制允许的回调类型。这个软件锁差异不构成任一版本支持并发注册的保证，应用仍应协调回调指针和传输生命周期。
- v1.1.4 的阻塞 Transmit / Receive / TransmitReceive 在等待当前项TXE/RXNE之前先递减相应XferCount；若等待超时，该计数可能已包括一项尚未实际搬运的数据。v1.1.10把递减放在对应访问之后，但写入TDR仍不等于线路发送完成。不能跨版本将 Size−XferCount 直接解释为对端已收到的字符数。

来源：[v1.1.4 回调注册 L440–646](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_usart.c#L440-L646)、[v1.1.10 回调注册 L444–641](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L444-L641)；阻塞接口范围见§2、§3。

## 6 Init/DeInit并不替代事务收尾

两份固定HAL_USART_Init都只在句柄State为RESET时调用底层MspInit，随后设BUSY并进入USART_SetConfig。该配置函数先清TE/RE，修改CR2的时钟/停止位字段，再按字长/校验/Mode修改CR1，并清CR3的RTSE/CTSE。它基于读回值修改所选位，不能把整寄存器WRITE_REG调用误读成“所有其他位都已复位”。

具体边界：

- Init没有先等待TC或停止已有DMA事务的步骤，也没有以当前BUSY状态拒绝重新初始化。
- CR1中的其他字段（包括不在写掩码中的UE/中断位）以及CR3中的DMAT/DMAR等请求位可能保留；Init随后还会清LINEN、SCEN、HDSEL、IREN，置UE，并将句柄写READY、ErrorCode清零。
- 同步USART初始化主动置CLKEN并清硬件流控RTSE/CTSE。不能将其当成异步UART初始化的同义入口。
- DeInit清UE并调用MspDeInit，最后把软件状态设RESET、ErrorCode清零并解锁。主体未逐路Abort DMA；用户提供的MspDeInit可能做额外清理，因此是否回收DMA须查实际工程回调，不能仅从函数名保证。

来源：[v1.1.4 Init/DeInit L295–395](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_usart.c#L295-L395)、[v1.1.10配置实现 L2733–2798](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L2733-L2798)。

## 7 阻塞超时的检查位置

USART_WaitOnFlagUntilTimeout只在所等标志尚未达到目标时检查Timeout。若目标标志在进入helper时已满足，Timeout=0也可能直接返回HAL_OK；HAL_MAX_DELAY跳过有限超时判断。超时按调用方传入的起始tick累计，阻塞收发没有逐字符自动重新计时。

超时分支实际清的是TXEIE、RXNEIE、PEIE和EIE，写State=READY并解锁；源码中把第一项注释称为“Transmit Complete Interrupt”，但实际位是TXEIE，不能据注释宣称TCIE一定被清。该helper没有停止USART发送器、清DMAT/DMAR或中止DMA的步骤，也不把这次超时转成一个新增的USART ErrorCode位。

来源：[v1.1.10 helper L2315–2350](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_usart.c#L2315-L2350)。

## 8 异步HAL_UART也有同类旧版宽度问题

另行核对固定v1.1.4的 Src/stm32f1xx_hal_uart.c，发现9位字长且开启校验时，阻塞发送、阻塞接收及内部UART_Transmit_IT、UART_Receive_IT也使用半字访问、每项仅前移1字节。旧版接收L1147–1156与L3001–3010的半字写入，同样可能越过恰好Size字节的缓冲末尾；发送则存在相邻字节读取。此处是对该文件的独立证据核查，并非依据同步USART名称推断。

固定v1.1.10的对应四条路径将半字访问限定为9位无校验，9位加校验走字节路径。线上的“8个有效数据位＋奇/偶校验”在F1配置中对应M=1、PCE=1，所以这个风险可能涉及通常称为8E1/8O1的应用，不能只按口头的“9位协议”筛选。

来源：[v1.1.4阻塞收发 L1022–1180](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_uart.c#L1022-L1180)、[旧版IT搬运 L2920–3023](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_uart.c#L2920-L3023)、[v1.1.10阻塞收发 L1135–1288](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L1135-L1288)、[新版IT搬运 L3529–3626](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L3529-L3626)。

本条不改变§4的范围：分数进位额外左移问题是所核对的HAL_USART宏，不能据这里共同的内存问题声称HAL_UART波特率宏也有相同缺陷。

## 9 参数断言不构成分频有效性检查

两份固定版本的 IS_UART_BAUDRATE 和 IS_USART_BAUDRATE 都仅检查 BaudRate≤4,500,000，没有排除0，也没有根据所选PCLK检查最小有效USARTDIV。

- BaudRate=0会进入含除以BaudRate的宏表达式。调用方必须先拒绝0；不能期待这些固定实现稳定返回HAL_ERROR。这里不推断具体编译产物的除零异常表现。
- 以USART2、PCLK1=36 MHz、BaudRate=4.5 Mbit/s为例，统一上限断言可通过，但宏计算BRR=8，对应USARTDIV=0.5，低于16倍采样模式要求的最小分频1。4.5 Mbit/s不能因通过这个统一断言就作为USART2/3在36 MHz下的有效设置。
- assert_param还可能按工程配置被关闭；即使开启，也只检查其实际表达式，不是完整的外设配置验证器。

式中BaudRate为目标位率（bit/s），PCLK1为APB1外设时钟频率（Hz），BRR为寄存器编码；USARTDIV=BRR/16为无量纲分频数。上述例子是固定整数宏与硬件分频条件的联合核对，未运行固件或测试线路。

来源：[v1.1.4 UART宏 L804–814](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_uart.h#L804-L814)、[v1.1.10 UART宏 L863–875](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_uart.h#L863-L875)、[v1.1.10 USART宏 L608–621](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_usart.h#L608-L621)；硬件分频见[RM0008 Rev21 pp798–799](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=798)。

## 专用模式驱动的独立版本边界

HAL_UART / HAL_USART的修复结论不自动推广到HAL_IRDA或HAL_SMARTCARD；参见[Smartcard与IrDA数据宽度及初始化](Smartcard与IrDA数据宽度及初始化.md)。
