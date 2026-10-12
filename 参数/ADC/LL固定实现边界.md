# ADC LL 初始化与寄存器更新的固定实现边界

范围：STM32F103C8T6；固定提交 bd368aa335c529641d2e567574885e02deacc64a 的官方 LL ADC 头文件和 C 实现。两份文件已核对官方 Git blob 标识。以下为源码、字段编码与 RM0008 的交叉核查，不代表固件或实板测试。

## LL_ADC_REG_Init 的 CR1 写入值混入序列长度

固定 C 实现的 LL_ADC_REG_Init 在 ADC 禁用时，先通过 MODIFY_REG 修改 CR1.DISCEN/DISCNUM。但用于写入的表达式为 SequencerLength | SequencerDiscont；同一函数随后又正确调用 LL_ADC_REG_SetSequencerLength，将序列长度写入 SQR1。

头文件中的 LL_ADC_REG_SEQ_SCAN_ENABLE_nRANKS 使用 SQR1.L[23:20] 编码，即 `(n−1)<<20`。n 是规则序列 Rank 数，范围 1～16，无量纲；`<<20` 表示左移 20 位。RM0008 Rev21 p238 中 CR1 的相同位号却是：bit23 为 AWDEN、bit22 为 JAWDEN、bits21:20 为保留位。因此该固定实现向 CR1 构造的写入值可能额外包含看门狗使能位或保留位。

|规则序列长度|SQR1.L 编码|该编码误用于 CR1 时涉及的字段|
|---:|---:|---|
|2|0x00100000|保留 bit20|
|3|0x00200000|保留 bit21|
|4|0x00300000|保留 bits21:20|
|5|0x00400000|JAWDEN|
|9|0x00800000|AWDEN|
|16|0x00F00000|AWDEN、JAWDEN 与保留 bits21:20|

该函数的清除掩码只包含 DISCEN/DISCNUM，不能用它清除由此前调用带入的看门狗位。表中是寄存器写入值的静态推导；不对保留位在芯片上的存储/读回效果作断言，也不声称每种配置都会产生可见错误中断。实际后果还取决于看门狗阈值、中断使能及所用组。

该指定版本初始化规则组时存在上述寄存器副作用。工程若依赖该版本，应核对实际寄存器写入，使用经过验证的修正版或明确的寄存器配置流程。

出处：
- [固定 C 实现，LL_ADC_REG_Init L645–730](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_adc.c#L645-L730)
- [固定头文件，序列长度编码 L592–607](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L592-L607)
- [RM0008 Rev21，CR1 位定义 p238](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=238)

相关历史记录：ST 社区有针对 F2 提交的同类报告，ST 员工确认了 F4 的问题并报告 F4 固件包修复。这个记录仅作背景，不能当作 F1 已获官方确认或修复的证据；本节 F1 结论来自上列固定源码和寄存器定义。[ST 社区记录](https://community.st.com/stm32-mcus-embedded-software-32/bug-in-stm32f2-adc-low-level-driver-ll-adc-reg-init-regarding-sequencerlength-76566)

## LL_ADC_DeInit 返回值的保证范围

该固定实现将局部 status 初始化为 SUCCESS。若 ADC 已使能，先把两组触发源设为软件源并调用 LL_ADC_Disable；只有随后读 ADON 为零时才执行寄存器清理。函数没有在 ADON 仍非零的分支将 status 改为 ERROR，最终仍返回原 status。

UM1850 Rev3 p651 将返回值列为 SUCCESS 和 ERROR，并分别关联寄存器是否已反初始化。该固定实现没有落实失败分支的 ERROR 返回，故文档契约与实现应分开记录。SUCCESS 不能单独证明全部寄存器已清理、触发已隔离或 DMA 缓冲区可复用。它也没有 HAL 句柄状态、HAL 回调和资源回收机制。

在确实进入寄存器清理分支时，C8 所选分支会清 CR1.DUALMOD，并把 HTR 的 12 位阈值设为 0xFFF。这与本章已核 HAL_ADC_DeInit 主体不清 DUALMOD、把 HTR 清零的行为不同，不能跨层套用。

[固定实现 LL_ADC_DeInit](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_adc.c#L389-L537)

## LL_ADC_CommonDeInit 实际请求的复位范围

该固定函数仅调用以 LL_APB2_GRP1_PERIPH_ADC1 为参数的 ForceReset/ReleaseReset，然后返回 SUCCESS。已进一步核对同一固定提交的 LL bus 头文件：ADC1 常量映射 RCC_APB2ENR_ADC1EN，即位9（0x200）；ForceReset/ReleaseReset 分别对 RCC_APB2RSTR 按该掩码置位和清位。RM0008 Rev21 p107 定义 bit9 为 ADC1RST、bit10 为 ADC2RST。该调用没有同时操作 ADC2RST。

UM1850 Rev3 p650 的 CommonDeInit 描述明确覆盖同一公共组中的全部 ADC；p651 也推荐用它对全部实例作硬复位。这与所核固定实现的复位掩码不一致。知识库需要同时保留该文档表述和版本限定：此指定实现请求 ADC1 复位，不能替代对 ADC2 的独立寄存器清理。公共双模式控制发生变化本身仍可能影响另一 ADC 的工作，应先按两实例的资源所有权停机。这里确认的是软件复位请求路径，没有执行 ADC2 实板保留值测试。

- [固定 CommonDeInit 实现 L279–291](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_adc.c#L279-L291)
- [固定 LL bus 常量](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_bus.h#L174-L177)；[ForceReset](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_bus.h#L928-L931)；[ReleaseReset](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_bus.h#L983-L986)
- [RM0008 Rev21，ADC1RST/ADC2RST，p107](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=107)

## 结构默认值与生效条件

|结构默认函数|写入的默认值|边界|
|---|---|---|
|LL_ADC_CommonStructInit|Multimode=INDEPENDENT|仅填结构；公共初始化要求两 ADC 均禁用|
|LL_ADC_StructInit|右对齐，扫描使能|仅填结构；不配置 RCC/GPIO 或各 Rank|
|LL_ADC_REG_StructInit|软件触发、1 Rank、间断关闭、单次、DMA 请求关闭|序列长度字段使用枚举编码，不能把任意整数当编码|
|LL_ADC_INJ_StructInit|软件触发、1 Rank、间断关闭、独立注入|仅填结构；组长度改变后仍须建立完整 Rank 布局|

Init、REG_Init、INJ_Init 在所选 ADC 已使能时返回 ERROR；CommonInit 在组内任一实例使能时返回 ERROR。INJ_Init 的字段更新使用明确清除掩码，不能把 HAL 注入配置中 DISABLE 不清旧位的结论套到这里。

这些完整 LL 初始化函数由 USE_FULL_LL_DRIVER 配置控制，并需要相应 C 实现；内联操作和结构默认值的存在不能证明应用已经链接、调用这些初始化函数。

UM 文档依据：[UM1850 Rev3 p650–651](https://www.st.com/resource/en/user_manual/um1850-description-of-stm32f1-hal-and-lowlayer-drivers-stmicroelectronics.pdf#page=650)。页码按该保留版本，不以未来在线版本相同页号为保证。

## LL_ADC_Enable 的重复调用会涉及启动语义

固定头文件 L3244–3247 直接执行 `SET_BIT(ADCx->CR2, ADC_CR2_ADON)`，未先检查使能状态。RM0008 Rev21 pp218、243 规定：ADON 已为 1，再写 1，且 CR2 其它位未同时改变时，会启动转换。在上电并校准后再次无条件使能 ADC，可能引入未计划的转换。操作顺序应根据状态区分：保留上电状态的校准流程完成后，直接准备接收并开放所需触发；只有确实关闭过 ADC 时才重新上电并等待稳定。

这是调用顺序说明的修正，不将 LL 的直接寄存器接口称为驱动错误；没有执行固件或实板测试。

## 从 ADC 状态查询的地址偏移与接口说明不一致

固定头文件的 `LL_ADC_IsActiveFlag_SLV_EOS`、`LL_ADC_IsActiveFlag_SLV_JEOS`、`LL_ADC_IsActiveFlag_SLV_AWD1` 均通过 `__ADC_PTR_REG_OFFSET(ADCxy_COMMON->SR, 1U)` 取得读地址。该内部宏把第二个参数左移 2 位后加到基地址，单位是 32 位寄存器，不是 ADC 实例。

C8 的公共入口 ADC12_COMMON 指向 ADC1_BASE，公共 SR 位于偏移 0。按这个固定实现，传入合法公共入口后，读地址为 `0x40012400 + (1 << 2) = 0x40012404`，即 ADC1_CR1。ADC2_SR 的实际地址为 `0x40012800`，两 ADC 实例相距 0x400 字节。这里的地址和位号来自固定 CMSIS 定义以及 RM0008 Rev21 pp51、237–240。

|接口|按名字/文档预期查询|固定实现实际读取|
|---|---|---|
|LL_ADC_IsActiveFlag_SLV_EOS|ADC2_SR.EOC，bit1|ADC1_CR1.AWDCH 的 bit1|
|LL_ADC_IsActiveFlag_SLV_JEOS|ADC2_SR.JEOC，bit2|ADC1_CR1.AWDCH 的 bit2|
|LL_ADC_IsActiveFlag_SLV_AWD1|ADC2_SR.AWD，bit0|ADC1_CR1.AWDCH 的 bit0|

因此这些特定版本的 SLV 包装函数返回 0/1，不能作为 ADC2 完成或越界事件的证据。源码中直接以 ADCx 访问 SR 的单实例查询函数没有这一实例地址偏移；在评估读取方式时必须核对具体函数和传入实例，不能仅检查返回类型。这里仅完成静态地址推导，没有执行硬件读数验证，也没有推定其他版本的修复状态。

出处：
- [固定偏移宏，L227–228](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L227-L228)
- [固定 SLV_EOS，L3663–3673](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3663-L3673)；[SLV_JEOS，L3699–3706](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3699-L3706)；[SLV_AWD1，L3730–3735](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3730-L3735)
- [固定 CMSIS 公共结构](https://github.com/STMicroelectronics/cmsis-device-f1/blob/c8e9a4a4f16b6d2cb2a2083cbe5161025280fb22/Include/stm32f103xb.h#L167-L174)；[ADC1/ADC2 基地址](https://github.com/STMicroelectronics/cmsis-device-f1/blob/c8e9a4a4f16b6d2cb2a2083cbe5161025280fb22/Include/stm32f103xb.h#L607-L608)；[公共入口](https://github.com/STMicroelectronics/cmsis-device-f1/blob/c8e9a4a4f16b6d2cb2a2083cbe5161025280fb22/Include/stm32f103xb.h#L671)
- [RM0008 Rev21，地址映射 p51](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=51)，SR/CR1 定义 pp237–240。

## 内部通道看门狗编码中的软件标记

固定头文件用 bit31（0x80000000）标记温度传感器、VREFINT 这类内部通道。`ADC_CHANNEL_ID_MASK` 包含这个软件标记，`LL_ADC_AWD_CH_TEMPSENSOR_*`、`LL_ADC_AWD_CH_VREFINT_*` 和 `__LL_ADC_ANALOGWD_CHANNEL_GROUP` 生成的内部通道监视编码会保留它。随后 `LL_ADC_SetAnalogWDMonitChannels` 将该编码整体作为 CR1 修改操作的置位参数，未在该函数中去掉软件标记。

这确认了传给寄存器写操作的值包含 bit31；RM0008 Rev21 p238 将 CR1[31:24] 列为必须保持复位值的保留位。不能把软件内部通道标记解释成芯片寄存器功能位，也不能据此推定保留位实际可写、读回或造成何种芯片行为。最终写操作还须结合工程所用 CMSIS 宏定义核对；此处没有实板验证结果。

出处：[软件通道标记与掩码 L115–122](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L115-L122)、[内部通道监视编码 L817–822](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L817-L822)、[寄存器修改实参 L3016–3021](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_ll_adc.h#L3016-L3021)。
