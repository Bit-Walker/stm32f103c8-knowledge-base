# ADC 轮询接口的完成判据与版本边界

适用对象：STM32F103C8T6；实现证据固定到 STM32F1 HAL v1.1.4 与 v1.1.10。以下是源码阅读与寄存器位运算核对，不代表实板时序测试，也不代表原厂已发布勘误。

## 1 规则组与注入组的分支条件

|接口|等待硬件标志的条件|其余配置采用的路径|成功返回后的标志处理|
|---|---|---|---|
|HAL_ADC_PollForConversion|CR1.SCAN=0 且 SQR1.L=0；此前还要求 CR2.DMA=0|软件估算循环，不检查本次外部触发是否发生，也不以 EOC 确认整个序列完成|清 STRT、EOC，置软件状态 REG_EOC|
|HAL_ADCEx_InjectedPollForConversion|JSQR.JL=0，即注入序列长度为 1|JL 非零时为软件估算循环，不以 JEOC 确认整个注入序列完成|清 JSTRT、JEOC、EOC，置软件状态 INJ_EOC|

规则组 SCAN=1、仅一 Rank 仍进入估算路径；注入组的分支只检查 JL，不应照抄规则组的 SCAN 条件。两个接口均不能通过函数名称或返回 HAL_OK 单独证明任意扫描序列已经产生全部新结果。

规则组 CR2.DMA=1 时接口直接置 ERROR_CONFIG 并返回 HAL_ERROR。这包含为读取双 ADC 配对结果而设置 ADC1.CR2.DMA 的配置，即使没有启用 DMA1 通道，也会被该检查拒绝。

注入组接口成功路径还清除 EOC；它与使用 EOC 的规则组软件消费流程存在共享标志影响，不能把两个轮询流程视作彼此独立。清标志发生在接口返回前；已通过正常启动流程清除旧标志、触发配置有效、数据寄存器对应正确 Rank 等条件仍需满足。

固定源码：
- [v1.1.4 规则轮询，L1203–1329](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1203-L1329)
- [v1.1.10 规则轮询，L1193–1325](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_adc.c#L1193-L1325)
- [v1.1.4 注入轮询，L384–494](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L384-L494)
- [v1.1.10 注入轮询，L381–497](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_adc_ex.c#L381-L497)

## 2 Timeout 的真实行为

两种路径都包含 Timeout 检查，尽管源码注释称序列估算路径不能设置超时。有限 Timeout 基于 HAL_GetTick，单位 ms；HAL_MAX_DELAY 禁用超时退出。超时路径设置 HAL_ADC_STATE_TIMEOUT、解锁并返回 HAL_TIMEOUT，不自动关闭 ADC，不等同于取消后续触发或终止硬件采集。

单次标志等待在进入循环前已经有完成标志时，Timeout=0 仍可成功；在标志尚未置位时按超时检查返回。v1.1.10 在判定超时后重新检查标志，减少被抢占期间完成而误报超时的情况。估算路径新增的复查仍针对循环计数，没有增加 EOC/JEOC 完成验证。

轮询时间基准必须可推进；例如中断优先级配置使 HAL tick 无法运行时，有限 Timeout 不再保证按墙钟时间退出。对估算路径，循环变量增加一次不等于恰好一个 CPU 时钟周期，不能从计数直接给出实测持续时间。

## 3 转换周期估算宏的掩码缺口

估算循环计数按以下实现计算：

`K = (SystemCoreClock / fADC) × ADC_CONVCYCLES_MAX_RANGE(hadc)`

K 是循环迭代次数上限，无量纲；SystemCoreClock 是驱动记录的内核时钟频率，单位 Hz；fADC 是 HAL_RCCEx_GetPeriphCLKFreq 返回的 ADC 时钟频率，单位 Hz；除法使用整数运算；hadc 是 ADC 句柄；宏返回以 ADC 时钟周期数表示的数值。该式没有乘以序列 Rank 数。

该宏不能保证对全部合法采样配置给出保守最大转换周期。两个固定头文件的 ADC_CONVCYCLES_MAX_RANGE 均存在以下实际表达式：对 SMPR2 的最低采样编码位检查使用 ADC_SAMPLETIME_ALLCHANNELS_SMPR1BIT0。SMPR1 掩码只覆盖位 0、3、6、9、12、15、18、21；SMPR2 的通道 8、9 最低编码位分别位于 24、27，未包含在该掩码中。

可逐位复核的配置如下。其余通道采样编码均为 000，只有指定通道设为 111，即采样 239.5 周期：

|指定通道|SMPR2|SMPR1|宏实际返回|该通道采样加转换周期|
|---|---|---|---|---|
|通道 8，C8T6 的 PB0|0x07000000|0|84|239.5+12.5=252|
|通道 9，C8T6 的 PB1|0x38000000|0|84|239.5+12.5=252|

推导：两者的采样编码 bit2、bit1 检查均非零，进入高档位分支；错误使用的 SMPR1 bit0 掩码与 SMPR2 相与为零，SMPR1 本身也为零，故三目表达式选择 71.5+12.5=84，而非 239.5+12.5=252。两通道是 C8T6 实际引出的模拟输入，不能作为仅其他封装适用的情形排除。

这证明宏数值并非所有合法配置的保守上界。它本身不能证明实板循环一定早于转换结束，因为编译结果、访存、中断及每次迭代开销会影响实际延时。应以硬件完成标志或适当的数据搬运完成契约组织结果消费，不能以此估算循环的 HAL_OK 充当完整采集凭据。

固定源码：
- [v1.1.4 掩码定义，L438–460](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L438-L460)
- [v1.1.4 周期宏，L769–782](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L769-L782)
- [v1.1.10 周期宏，L768–781](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_adc.h#L768-L781)
- RM0008 Rev21 §11.12.4–5，pp244–245：SMPR1/SMPR2 字段和采样周期编码。

## 4 注入停止的可用条件

HAL_ADCEx_InjectedStop 在软件状态 REG_BUSY 为零且硬件 JAUTO 为零时，才调用公共 ADC 停止/禁用路径；成功后清 REG_BUSY 和 INJ_BUSY、置 READY。否则置 ERROR_CONFIG 并返回 HAL_ERROR。其判断包含软件状态，不能将 REG_BUSY=0 自动等价为硬件规则组完全空闲。

因此，该接口不能承诺在规则组仍运行时单独关闭注入组。自动注入应从合适的规则组停止流程整体停机，并核对 DMA、触发生产者及缓冲区所有权。

- [v1.1.4 InjectedStop，L331–376](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L331-L376)
- [v1.1.10 InjectedStop，L328–373](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_adc_ex.c#L328-L373)
