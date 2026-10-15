# TIM状态标志、软件事件与DMA窗口

TIM1高级事件与TIM2～4共享事件分别列明；本文与[参数表](硬件参数表.md)、[时基更新](计数时基与更新.md)配合。

定时器事件作为ADC触发源、定时器向DMA提出搬运请求，以及ADC规则通道转换完成后向DMA提出ADC_DR结果搬运请求，分别由各自选择字段和物理映射决定。[ADC触发选择表](../ADC/寄存器与触发参数.md#117-完整触发选择)给出C8的完整八种规则/注入编码；[DMA1请求表](../DMA参数与HAL接口.md#dma1-完整请求映射)给出共享通道约束。TIM4_CC4可触发ADC规则组，同时TIM4_CH4没有独立DMA1请求连线；不能从其中一张映射表推定另一张。依据：RM0008 Rev21 Tables67–68（pp225–226）、Figure50/Table78（pp281–282）。

## 1 SR标志与清除条件

SR偏移0x10。以下有效状态位采用rc_w0，软件写0清除；仅输入捕获模式还具有读CCRx清CCxIF的副作用。

|位|字段|适用实例|事件与限制|
|---|---|---|---|
|0|UIF|TIM1～4|计数溢出/下溢更新，以及URS=0时UG/从模式更新；须满足UDIS及TIM1重复计数条件|
|1～4|CC1IF～CC4IF|TIM1～4|输出比较按匹配及CMS方向选择置位；输入捕获时置位，读对应CCR也清除|
|5|COMIF|TIM1|控制预装载发生COM更新；TIM2～4此位保留|
|6|TIF|TIM1～4|从控制器使用的有效TRGI边沿；门控模式包含打开和关闭两种边沿|
|7|BIF|TIM1|刹车事件标志；刹车仍有效时不能按普通历史标志清除。TIM2～4此位保留|
|9～12|CC1OF～CC4OF|TIM1～4|已有CCxIF未清时再次捕获的一般过捕获指示；ES096允许漏报及误报|

bit8及15:13保留。输出比较中CCR>ARR时，CCxIF仍会在向上/中心对齐溢出或向下下溢置位；不能仅从CCR不在计数范围推断没有比较标志。输入模式读CCR清标志，输出模式读CCR不据此清CCxIF。

标志为锁存状态，不累计发生次数；状态位、DIER请求使能、NVIC配置及回调执行分别核对。固定LL ClearFlag与HAL清标志宏将目标位的反码写入SR，避免把rc_w0字段随意改成普通读改写的清位操作。读CCR与新捕获竞争时，ES096 §§2.6.5–6规定新数据可已锁存而标志漏报，也可未丢数据却置CCxOF；读取顺序或单独检查CCxOF均不能构成完整无丢样证明。

来源：[RM0008 Rev21 TIM1 SR pp346–347](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=346)、[TIM2～4 SR pp410–411](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=410)、[ES096 Rev15 pp15–16](https://www.st.com/resource/en/errata_sheet/es096-stm32f101x8b-stm32f102x8b-and-stm32f103x8b-mediumdensity-device-limitations-stmicroelectronics.pdf#page=15)。

## 2 EGR软件事件的不同作用

EGR偏移0x14，事件位软件写1触发后由硬件自动清零。

|位|字段|适用实例|手册明确描述的作用|
|---|---|---|---|
|0|UG|TIM1～4|重新初始化CNT及预分频计数，按UDIS等条件更新缓冲寄存器；URS控制更新请求范围|
|1～4|CC1G～CC4G|TIM1～4|输出模式置对应CCxIF及允许的请求；输入模式还将当前CNT锁存到CCRx，原CCxIF已高时置CCxOF|
|5|COMG|TIM1|CCPC=1时更新具有互补输出通道的CCxE、CCxNE、OCxM控制预装载|
|6|TG|TIM1～4|置TIF，并可产生已允许的触发中断/DMA请求|
|7|BG|TIM1|软件刹车，清MOE、置BIF；按BIE允许中断|

TIM2～4的COMG/BG位置保留；各实例没有的位不应写入。C8没有独立刹车DMA使能BDE，尽管RM的BG/刹车通用文字提到DMA，也不能为它补造请求通道。

TG的字段定义只保证TIF及允许的请求，不据名称扩展为一次真实TRGI输入，也不承诺触发从模式计数启动、复位或产生某种PWM脉冲。CCxG在输出模式的描述同样不能直接替代真实CNT与CCR比较以及输出模式时序。需要确定波形时，应按计数器、模式和输出控制路径核验。

来源：[RM0008 Rev21 TIM1 EGR pp347–348](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=347)、[TIM2～4 EGR p412](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=412)。固定LL GenerateEvent系列分别写对应EGR位，见[接口参考](LL接口.md)。

## 3 DCR编码与DMAR重定向

DCR偏移0x48：DBA[4:0]为从CR1起的寄存器索引，DBL[12:8]为突发传输项数减1；DBL=00000～10001对应1～18项，其他编码不使用。DMAR偏移0x4C，为32位间接窗口。

`A_target = A_CR1 + 4 × (DBA + i)`

A_target为当前重定向寄存器地址，A_CR1为该定时器CR1地址，单位均为字节地址；常数4表示相邻寄存器地址步长4字节；DBA和i均为无量纲整数，i是硬件维护的突发项索引，范围0～DBL。字段DBL表示末项索引，传输项数为DBL+1。

例如访问CCR2、CCR3、CCR4：DBA=0xE，项数3，DBL字段应为2；DMA外设地址仍指向DMAR。连续两组数据需DMA传输项数6，不能把“3 transfers”的文字误写成DBL=3。DMA单项宽度与CPU访问规则分别解释：RM示例允许DMA半字搬运，而CPU访问32位DMAR的写操作按字进行。

TIM2～4在0x30与0x44分别没有TIM1的RCR/BDTR，突发窗口不能穿过这些不存在的功能寄存器再假定所有项有效。DMA地址步进、方向、实际DMA1请求映射及缓冲区有效期仍须独立配置。一次DMA搬运完成不证明最后的CCR预装载已反映为完整输出波形，停止与释放边界见[HAL生命周期](HAL生命周期与DMA.md)。

来源：[RM0008 Rev21 TIM1 DCR/DMAR pp361–362](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=361)、[TIM2～4寄存器段](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=404)。本文按手册示例的寄存器索引与项数编码换算，未进行在途DMA或波形板测。

[返回定时器主题](../../知识库/06_定时器PWM与同步.md) · [图形关系与来源](图形关系与来源.md)
