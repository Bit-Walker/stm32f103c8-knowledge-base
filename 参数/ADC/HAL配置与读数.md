# ADC 配置更新与结果读取的实现边界

范围：STM32F103C8T6，固定 HAL v1.1.4 与 v1.1.10。以下通过已有官方源码副本及寄存器说明核对；没有执行固件或实板测试。配置字段的取值另见参数表。

## 1 注入配置中的 DISABLE 不保证清除已设置位

两个固定版本的 HAL_ADCEx_InjectedConfigChannel 在 AutoInjectedConv=ENABLE 且选择软件注入源时设置 CR1.JAUTO；在 InjectedDiscontinuousConvMode=ENABLE 且 AutoInjectedConv=DISABLE 时设置 CR1.JDISCEN。相应分支没有在字段为 DISABLE 时清除旧 JAUTO/JDISCEN 的 else 操作。

因此，重复调用并把字段改为 DISABLE，不能独立证明硬件位已经关闭。尤其不能先启用 JAUTO，再仅把结构字段改为 AutoInjectedConv=DISABLE、InjectedDiscontinuousConvMode=ENABLE 就认定获得合法的纯间断模式；旧 JAUTO 可能仍在。RM0008 §11.3.9–10 明确禁止自动注入与间断模式同时使用。

更改模式前应按固定驱动和应用所有权执行受控停止、明确清理旧配置并读回核对。这里不提供未经实板验证的通用热切换补丁，也不假定反复调用配置函数具有完整覆盖赋值语义。

## 2 内部温度通道启动等待的条件

常规 HAL_ADC_ConfigChannel 仅在“通道为温度、ADC1 的 TSVREFE 此前为零”时，置 TSVREFE 后进入温度启动等待。若先配置 VREFINT，它会打开共同内部通路但不走温度专用等待；随后配置温度时，TSVREFE 已为一，等待分支会被跳过。

HAL_ADCEx_InjectedConfigChannel 的两个固定版本还存在重复使能代码：配置内部通道时前面先无条件设置 TSVREFE，后面才以 TSVREFE 是否为零决定是否进入温度等待。在正常寄存器写入有效、无并发改写的情况下，后面的零值条件不成立。不能根据函数后半段出现等待循环，就承诺调用已经等待传感器稳定。

这属于等待控制流的缺口；实际从使能到采样可能已经过去足够时间，不能由源码直接断言每次测量必错。应用应明确满足从内部通路使能到有效采样的启动时间，并另外满足采样窗口要求。DS5319 Rev20 p78 Table51 的 tSTART 为 4～10 µs；该启动时间与 RM 推荐的温度采样窗口 17.1 µs 是不同参数。

## 3 配置失败与部分写入

规则通道配置先改写序列和 SMPR，再检查温度/VREFINT 是否被误配到 ADC2；误配时返回 HAL_ERROR 并置 ERROR_CONFIG，已经完成的寄存器写入不会自动回滚。

注入配置在检测部分组合错误后仍继续处理采样时间、偏移及内部通路，返回错误也不能视为“原配置完全没变”。此外：

- 修改 JEXTSEL 的分支只在 ADC 禁用时执行；ADC 已使能时可能跳过此字段而继续其他配置，不因此必然返回错误。
- 注入 Rank 应满足 1≤Rank≤InjectedNbrOfConversion≤4，扫描关闭时仅配置 Rank 1。改变组长度会改变 JSQR 实际布局，应按新长度重新建立完整序列。
- 同一注入组的长度、自动模式、间断模式和触发源是公共设置；逐 Rank 调用时应保持一致。
- 同一物理通道的采样时间由规则/注入组共享；更改一组可能影响另一组。

HAL_ADC_AnalogWDGConfig 分别检查高低阈值的 12 位范围，但没有检查 LowThreshold≤HighThreshold 的关系；调用方必须建立有效窗口。WatchdogNumber 在该实现中未使用。Channel 虽仅在单通道监控时对硬件比较有效，函数仍将它写入 CR1，应使用合法通道编码或明确初始化为零，避免未初始化字段的额外位进入寄存器。

## 4 TIM1_CC3 的硬件支持与断言列表

RM0008 Rev21 Table67 p225 中，规则 EXTSEL=010 对应 TIM1_CC3。两个固定 ADCEx 头文件均定义 ADC_EXTERNALTRIGCONV_T1_CC3。但适用于 STM32F103xB 的 IS_ADC_EXTTRIG 列表漏列这一项；不能从其他高容量型号分支包含该常量，推定 C8 分支也已包含。

HAL_ADC_Init 调用 assert_param(IS_ADC_EXTTRIG(...))。启用相应完整断言时，TIM1_CC3 会进入断言失败处理路径，具体停机、记录或返回行为取决于工程的 assert_failed 实现；关闭断言时，该检查不构成运行时拒绝。该列表遗漏不改变 C8 硬件触发表的有效编码。知识库须同时保留硬件支持和指定 HAL 版本的断言差异，不删掉真实触发源，也不建议为掩盖问题而整体关闭断言。

## 5 结果读取没有隐含等待

|接口|实际读取|返回数据解释及副作用|
|---|---|---|
|HAL_ADC_GetValue|对应 ADC 的 DR|返回原始 uint32_t；读取 DR 的硬件行为会清 EOC；不等待本次转换，不自动转成电压|
|HAL_ADCEx_InjectedGetValue|按 Rank 读取 JDR1～JDR4|返回原始 uint32_t；按 ALIGN 和偏移后的有符号位布局解释，不保证是本轮新值；读取 JDR 本身不代替 JEOC 完成处理|
|HAL_ADCEx_MultiModeGetValue|先读 ADC1_DR；若 ADC1.CR2.DMA=0，再读 ADC2_DR 左移16位并 OR 合成|ADC1 位于低半字、ADC2 位于高半字；DMA=0 的回退是两次寄存器读取，不能视为原子锁存的一对结果|

硬件单次读 ADC1_DR 获取双 ADC 高低半字的有效组合，要求 ADC1.CR2.DMA=1；这与 DMA1 通道是否使能不同。上述 HAL 回退路径说明，不能把硬件单次读取条件扩写为该 API 在所有版本下的强制先决条件。此处两个固定版本已核实具有回退路径，不以其他未核快照作等同承诺。

## 6 IRQ 的版本差异

v1.1.4 按 EOC、JEOC、AWD 顺序逐次读取当前中断使能位和状态位；v1.1.10 在入口读取 SR 和 CR1 到局部快照，后面的三类判断使用这些快照。用户回调改变硬件寄存器后，本次调用的后续判断可能因此在两版间不同，不能无条件按“回调刚关闭某中断，后面的分支就不会再运行”设计流程。

两个版本都先处理 EOC 分支，未用 JEOC 排除注入完成对 EOC 的置位；规则/注入共用时仍须核对数据来源。各分支调用用户回调后才执行该分支的软件清标志操作，回调内重新启动等重入流程需要单独评审。

## 固定出处

- [v1.1.4 规则通道与看门狗配置](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1992-L2177)
- [v1.1.10 规则通道与看门狗配置](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_adc.c#L2000-L2185)
- [v1.1.4 注入配置](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L996-L1237)
- [v1.1.10 注入配置](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_adc_ex.c#L1000-L1241)
- [v1.1.4 中等容量规则触发断言列表](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L521-L529)
- [v1.1.10 同一条件分支](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_adc_ex.h#L520-L528)
- [v1.1.4 注入与双模式读数](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L885-L945)
- [v1.1.10 注入与双模式读数](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_adc_ex.c#L889-L949)
- [v1.1.4 IRQ](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1774-L1896)
- [v1.1.10 IRQ](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_adc.c#L1780-L1905)

相关配置定义见[HAL配置字段](HAL配置字段.md)，停止和恢复条件见[DMA生命周期与恢复](DMA生命周期与恢复.md)。
