# Smartcard 与 IrDA：CPU 数据宽度与初始化边界

范围限 STMicroelectronics/stm32f1xx-hal-driver 两个固定提交的阻塞与中断 CPU 收发。v1.1.4 为 de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9，v1.1.10 为 77fbb30b7a1d02533980400083e48c559aae5a4f。四份实现及四份配套头文件均已核对完整 Git blob；没有新增固件执行或实机验证，专用驱动生命周期的当前核查范围见配套DMA页。

## 已核对的版本差异

|模块及条件|固定 v1.1.4|固定 v1.1.10|
|---|---|---|
|HAL_SMARTCARD，阻塞/IT CPU 收发|uint16_t 指针访问，每项前移1字节|对应路径改为 uint8_t 访问，每项前移1字节|
|HAL_IRDA，WordLength=9B且有校验，阻塞/IT CPU 收发|uint16_t 指针访问，每项前移1字节|该访问宽度与步长组合仍存在|

头文件允许 IrDA 的9B字长及偶/奇校验组合；Smartcard 本身只允许9B加偶/奇校验，因此不能靠这些字长/校验断言自动排除所列路径。

对于按 N 项八位载荷分配的 N 字节缓冲，半字访问的最后一次从偏移 N−1 开始，名义跨度到偏移 N。接收可能覆盖末尾之外一字节，发送可能越界读取；多项访问还可能落在奇地址。实际总线访问、编译优化与故障结果须依目标环境判断。本结论不构成实机验证，也不把额外分配一个尾字节当作全部类型/对齐问题的通用修复。

## Smartcard 的赋值类型

旧版 Receive 和 SMARTCARD_Receive_IT 先将目标转为 uint16_t *，再执行形如 *tmp = (uint8_t)(DR & 0xFF) 的赋值并前移1字节。右侧 uint8_t 强转限制数值；左侧仍是 uint16_t 对象访问。在 STM32 小端表示下高字节为零，仍涉及相邻字节。旧版 TX/Transmit_IT同样半字读取后前移1字节；新版四条路径均为字节访问。

来源：[旧版阻塞 L756–860](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_smartcard.c#L756-L860)、[旧版IT L1997–2070](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_smartcard.c#L1997-L2070)、[新版阻塞 L751–850](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_smartcard.c#L751-L850)、[新版IT L1991–2065](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_smartcard.c#L1991-L2065)。

## IrDA 的分支条件

两版四条 CPU 收发路径先以 WordLength==IRDA_WORDLENGTH_9B 选择半字访问，再按 Parity 选择步长：无校验2字节，有校验1字节。UART/USART 在固定v1.1.10相应路径的修复不能外推到HAL_IRDA。新版接收注释还写M1-M0；C8的实际字段为单一CR1.M，不据通用注释增加不存在的字段。

来源：[旧版阻塞 L770–920](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_irda.c#L770-L920)、[旧版IT L2452–2563](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_irda.c#L2452-L2563)、[新版阻塞 L764–916](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_irda.c#L764-L916)、[新版IT L2461–2576](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_irda.c#L2461-L2576)、[新版IrDA参数检查 L618–623](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_irda.h#L618-L623)。

上述 CPU 访问宽度不决定 DMA 的 MSIZE、PSIZE、MINC，DMA路径须独立检查。


## 参数检查
- IrDA 允许8B/9B，无/奇/偶校验；其波特率断言为 BaudRate < 115201。
- Smartcard 只允许9B、奇/偶校验、0.5/1.5停止位；波特率断言为 BaudRate < 4500001。
- 两个上限断言都允许零，而 BRR 计算宏除以波特率；调用方必须排除零。断言范围不能替代实际 PCLK、BRR 可表示性及硬件模式条件检查。
- Init / SetConfig 没有对 Prescaler 做独立合法性断言。IrDA 成员为 uint8_t，Smartcard 成员为 uint32_t；成员类型不替代硬件合法值。硬件 PSC 语义见已发布寄存器页及 RM0008 Rev21 p826。
- IRDA_BRR 与 SMARTCARD_BRR 的分数进位项采用 DIVFRAQ & 0xF0，没有已查 HAL_USART 宏的额外移位；不得把 USART 宏问题直接推广到它们。
来源：[IrDA参数与BRR](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_irda.h#L618-L642)、[Smartcard参数与BRR](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_smartcard.h#L694-L715)。

## 初始化顺序
IrDA：gState BUSY → 关闭 UE → SetConfig → 清 LINEN/STOP/CLKEN、SCEN/HDSEL → 开 UE → PSC → IRLP → IREN → 两状态 READY。
Smartcard：gState BUSY → PSC/GT → SetConfig → 清 LINEN、IREN/HDSEL → PEIE/EIE → 开 UE → NACK → SCEN → 两状态 READY。入口没有对应 IrDA 的关闭 UE 步骤；SetConfig 内先清 TE/RE 再处理同步时钟字段。
两个 Init 均不能自动构成活动 DMA / 活动发送的安全重初始化：本体不调用 DMA Abort、不等待 TC、不完成既有缓冲所有权交回。外设配置写入和软件 READY 不能作为原传输资源已释放的证据。
来源：[IrDA Init](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_irda.c#L293-L359)、[Smartcard Init](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_smartcard.c#L296-L367)、[Smartcard SetConfig](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_smartcard.c#L2256-L2333)。


## 核查范围

两个 Init / SetConfig 的四对固定版本函数体去注释、空白后逐对相同。本文未闭合所有基础宏与编译配置；不据未闭合定义发布 IrDA BRR 二次初始化的数值故障结论。

参见[专用DMA启动、完成与错误边界](Smartcard与IrDA_DMA边界.md)、[UART/USART数据宽度](HAL数据宽度与版本边界.md)、[固定来源身份](../../来源/驱动实现.md#src-usart-dedicated-fixed-boundaries)。

## 接口声明与实际实现

两版专用头文件的HAL函数原型、定义位置、const变化及回调条件见[Smartcard与IrDA HAL接口索引](Smartcard与IrDA_HAL接口索引.md)。其中HAL_SMARTCARD_ReInit虽有头文件声明，对应两份固定模块C文件未见定义，不能当作本页已验证的重初始化入口。

初始化结构17个字段、两版一致的配置符号、PSC命名与实际时钟来源，以及控制宏的寄存器/软件状态边界，见[配置字段及宏](Smartcard与IrDA配置字段及宏.md)。
