# USART LL 初始化与波特率读回边界

适用于 STM32F103C8 的 16 倍过采样分支，以 STM32F1 LL v1.1.4、提交 de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9 为逐项定位基准，并与 v1.1.10、提交 77fbb30b7a1d02533980400083e48c559aae5a4f 比较。以下是源代码静态核查与整数算术复核，未执行固件或板卡通信测试；两版的具体差别见§6，不直接推广到其他版本。

## 1 初始化入口的配置范围

LL_USART_Init 要求 USART 已禁用。UE=1 时返回 ERROR，函数体不进入配置寄存器的分支。UE=0 时依次修改 CR1 的字长、校验、收发方向，CR2 的停止位和 CR3 的硬件流控，再取得外设时钟、计算 BRR。

该入口不将整个外设复位，也不统一清除原来的同步时钟、LIN、Smartcard、IrDA、半双工、DMA 请求或中断配置。复用一个曾用于其他模式的 USART 时，应按目标模式分别检查这些保留字段。关闭 UE 和完整重置外设是不同操作。

BaudRate=0 或取得的外设时钟为零时，函数不进入 BRR 配置分支并返回 ERROR，但前面的 CR1/CR2/CR3 配置已经执行，不自动回滚。这里描述违反有效配置前提后的失败控制流，不建议用零波特率作为正常配置方法。

来源：[LL_USART_Init，L200–322](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_usart.c#L200-L322)。宏调用中的写入掩码和分支按该文件核对；完整 RCC 频率计算链及用户改写的底层宏不在本项核查范围。

## 2 SUCCESS 不单独证明目标波特率可表示

固定实现先将状态赋为 SUCCESS，再调用 LL_USART_SetBaudRate，随后以 assert_param 检查 BRR 的上下限。断言不是另一个返回 ERROR 的分支，其实际中断或返回行为还取决于工程配置及断言处理函数。

更重要的是，LL_USART_SetBaudRate 将计算结果转换为 uint16_t 后写入 BRR。超过 16 位范围的原始结果可能先被截断，随后针对已写入 BRR 的上下限检查不一定能发现原始溢出。应在调用前检查目标分频的可表示范围，并在初始化后以真实外设时钟和最终 BRR 核对结果。

例如 USART1 的 PCLK2=72 MHz、目标为 100 bit/s 时，按这份固定 LL 宏计算得到原始 BRR=720000。转成 uint16_t 后为 64640，即 0xFC80；它满足 BRR≥16 且 BRR≤65535，但按理想时钟计算的实际位率约为 1113.861 bit/s。固定 Init 的这条路径仍能返回 SUCCESS。该例用于说明超出可表示范围时的截断，不将 100 bit/s 列为这一时钟配置下的合法工作点。

记 B_actual=f_P/BRR：B_actual 为依据最终寄存器计算的位率，单位 bit/s；f_P 为 USART 外设时钟频率，单位 Hz；BRR 为寄存器的无量纲整数值。本例未计实际振荡器误差、线路影响和接收端容差，不是实测位率。

来源：[分频整数宏，L378–385](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L378-L385)、[SetBaudRate，L1088–1091](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1088-L1091)、[Init 的配置和断言，L294–316](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_usart.c#L294-L316)。

## 3 GetBaudRate 的非零结果不是合法性证明

固定 C8 分支只检查 BRR 低 16 位是否非零；非零时返回 PeriphClk/BRR 的整数商，零时返回零。它没有完整检查 BRR≥16，也不核对传入的 PeriphClk 与当前 RCC 时钟是否相符。

因此，“未初始化或无效 BRR 返回零”的通用描述应限定到实际检查条件。以 BRR=1、传入 PeriphClk=72 MHz 为例，函数会计算出 72000000，而该 BRR 不满足 C8 的有效最小分频要求。这个数是软件整数计算结果，不能视为器件可实现的 72 Mbit/s 波特率。GetBaudRate 也不是对线路信号的测量；正常配置下的非整数位率会向下取整到整数 bit/s。

来源：[GetBaudRate，L1102–1114](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1102-L1114)。

## 4 StructInit 的条件字段

LL_USART_StructInit 将波特率设为 9600，字长为 8 位、停止位为 1 位、无校验、同时允许收发、关闭硬件流控。OverSampling 字段只在定义 USART_CR1_OVER8 时赋值；C8 的固定器件定义没有该位，因此其配置路径不使用该字段，StructInit 也不为它写默认值。不能因为结构体中保留字段，就推断 C8 支持 8 倍过采样或 StructInit 清零了整个结构体。

来源：[StructInit，L331–343](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_usart.c#L331-L343)；器件适用性按知识库固定 STM32F103xB 头文件确定。

## 5 ClockInit 关闭输出时保留其他时钟字段

LL_USART_ClockInit 同样要求 UE=0。ClockOutput 为禁止时只清 CLKEN，不按结构体覆盖 CPOL、CPHA 和 LBCL；允许时才联合配置这些字段。LL_USART_ClockStructInit 填写默认结构体，不直接修改外设。应用不应把“时钟输出已关”解释成所有时钟相位、极性和末位脉冲字段都已恢复默认。

来源：[ClockInit，L357–407](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_usart.c#L357-L407)、[ClockStructInit，L416起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_usart.c#L416)。


## 6 与固定 v1.1.10 的比较

v1.1.10 保留上文所述的配置顺序、UE 门控、BRR 前的部分写入、16 位截断、GetBaudRate 非零判断，以及 StructInit/ClockInit 条件行为。其 Init 删除了 BRR 上限断言，保留下限断言；本页 100 bit/s 算例在两份分频宏中的整数结果相同。新版部分形参增加 const 限定，不能把旧版原型逐字当作新版声明。

该比较仅覆盖本页列出的函数与分频宏，不等于 UART、同步 USART、IrDA、Smartcard 的所有 HAL/LL 路径已经一致。

来源：[v1.1.10 Init，L196–315](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_ll_usart.c#L196-L315)、[StructInit/ClockInit，L324–401](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_ll_usart.c#L324-L401)、[分频宏，L378–386](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_ll_usart.h#L378-L386)、[Set/GetBaudRate，L1089–1115](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_ll_usart.h#L1089-L1115)。


## 7 Disable 与事务收尾

两份固定 LL_USART_Disable 函数都仅调用清UE位的操作，没有轮询TC、超时、DMA停止、缓冲区归还或HAL句柄状态维护。安全发送收尾仍应按RM0008要求先确认本次TC；需要保留接收数据时还须另行协调接收源及DMA。

接口注释描述禁用后当前操作被丢弃；RM0008 p821对UE停止时点的英文存在不完整表述。本页不据此承诺精确停机周期、已发送字符完整性，或所有活动事务已经安全结束，也不把函数返回当作完成确认。

来源：[v1.1.4 Disable，L416–428](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L416-L428)、[v1.1.10 Disable，L417–429](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_ll_usart.h#L417-L429)、[RM0008发送收尾，p793](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=793)、[UE定义，p821](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=821)。

## 8 模式辅助函数的精确改写范围

以下七个函数在固定 v1.1.4 与 v1.1.10 中的可执行语句相同。它们返回 void，直接修改寄存器，没有等待 TC、检查 UE、停止 DMA 或恢复 HAL 句柄状态的步骤。切换时仍须按目标模式及各字段的硬件写入条件安排顺序。

表中“清零”包括所列字段的全部位，“置位”表示置 1；未列出的字段保留。STOP=00 为 1 个停止位，STOP=11 为 1.5 个停止位。

|函数后缀（统一前缀 LL_USART_Config）|CR2 清零|CR2 置位|CR3 清零|CR3 置位|
|---|---|---|---|---|
|AsyncMode|LINEN、CLKEN|无|SCEN、IREN、HDSEL|无|
|SyncMode|LINEN|CLKEN|SCEN、IREN、HDSEL|无|
|LINMode|CLKEN、STOP|LINEN|IREN、SCEN、HDSEL|无|
|HalfDuplexMode|LINEN、CLKEN|无|SCEN、IREN|HDSEL|
|SmartcardMode|LINEN|STOP[1:0]=11、CLKEN|IREN、HDSEL|SCEN|
|IrdaMode|LINEN、CLKEN、STOP|无|SCEN、HDSEL|IREN|
|MultiProcessMode|LINEN、CLKEN|无|SCEN、HDSEL、IREN|无|

这些调用还需与独立配置配合：

- 所有七个函数均不写 CR1、BRR 或 GTPR；字长、校验、收发使能、波特率等保留旧值。
- SyncMode 不配置 CPOL、CPHA、LBCL。CLKEN=1 本身不证明时钟相位和数据帧已正确配置。
- LINMode 和 IrdaMode 会将 STOP 清为 00。将它们概括为“只处理互斥模式位”会遗漏停止位变化。
- SmartcardMode 同时打开 CK 输出并把 STOP 设为 11；M、PCE、PS、PSC、GT、NACK 和 GPIO 等仍须独立核对。尤其不能把调用成功等同于已获得有效的卡时钟。
- HalfDuplexMode 保留 STOP、TE、RE 等状态；方向切换和总线电气条件需要另行处理。
- MultiProcessMode 的这组寄存器改写与 AsyncMode 相同；它不配置 WAKE、ADD 或 RWU，也不自动进入静默接收状态。
- 从 SmartcardMode 再调用 AsyncMode 时，CLKEN 和 SCEN 被清除，但 STOP=11 会保留。目标普通 UART 的停止位必须显式重新配置。这是依据上述写掩码推导的调用序列结果，并非实机测量。

来源：[v1.1.4 头文件 L1526–1770](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_usart.h#L1526-L1770)、[v1.1.10 头文件 L1527–1771](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_ll_usart.h#L1527-L1771)。模式约束需结合 [RM0008 Rev21 pp801–812](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=801) 与各寄存器字段条件解释。
