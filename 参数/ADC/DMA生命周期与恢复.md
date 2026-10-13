# ADC DMA 启停、状态与恢复边界

固定HAL v1.1.4与v1.1.10，面向C8。独立ADC与双ADC接口分别分析；本页恢复原参考中已存在的生命周期条件，不把公共API原型齐全当作行为信息齐全。

## 1 启动成功与DMA接受请求

HAL_ADC_Start_DMA和HAL_ADCEx_MultiModeStart_DMA会覆盖关联DMA句柄的完成、半完成及错误回调，但所核两版均不传播HAL_DMA_Start_IT的返回值。底层因忙或锁定拒绝新地址/长度时，外层仍可能开放ADC请求并返回HAL_OK；旧DMA地址/长度不因此更新，回调却可能已经改变。

调用前须建立DMA资源独占或串行化、正确Parent、通道、方向、宽度、地址和长度。合法长度为1～65535项；关闭assert不自动得到完整参数拒绝。缓冲区所有权不能由外层HAL_OK单独移交。ADC普通DMA完成回调主要修改软件状态和通知用户，不保证清ADON、CONT或停止后续转换。

双模式还要求ADC2规则触发选择为ADC_SOFTWARE_START；否则主句柄增加ERROR_CONFIG并返回错误。函数通过临时从句柄操作ADC2，不同步应用自己的ADC2句柄状态。新版本从使能失败时主可能已使能且未回滚，DMA尚未启动；外层错误也不等于所有硬件仍保持调用前状态。

## 2 独立ADC的Stop_DMA版本差异

|入口及分支|v1.1.4|v1.1.10|
|---|---|---|
|ADC禁用失败|不进入DMA请求清除和Abort分支|相同分支边界|
|ADC禁用成功、DMA为BUSY|清ADC DMA请求，调用Abort；成功才清ADC忙态，失败置ERROR_DMA|同类处理|
|ADC禁用成功、DMA已非BUSY|仍调用Abort；可得到NO_XFER和HAL_ERROR，进而新置ADC.State.ERROR_DMA|跳过Abort并可返回HAL_OK；忙态归一化也位于被跳过的分支内|

普通非循环DMA传满后，DMA IRQ的软件状态可已置READY。旧版随后Stop制造的NO_XFER/ERROR_DMA不等于发生真实传输TE。新版避免这一NO_XFER路径，但外部触发或连续采样留下的REG_BUSY可在ADC已禁用、请求已关且函数返回OK后仍存在；软件触发单次完成不能无条件套用这一例子。

两版真实TE后的Stop→Start也可能保留ADC.State.ERROR_DMA。Start清ErrorCode不等于清State错误位；半完成仍可正常通知，全完成却因旧State错误转发到错误回调。当前DMA.ErrorCode=NONE不能独立排除此软件路径。

## 3 双ADC停止须独立判断

两版MultiModeStop_DMA正常顺序为：禁用ADC1→借临时句柄禁用ADC2→清主CR2.DMA→清主CR1.DUALMOD→Abort DMA→清主REG_BUSY/INJ_BUSY并置READY。清DUALMOD在两份固定实现中均存在，不能按UM“保留模式”的说明直接重启而不重配。

普通DMA完成且已非BUSY时，Abort仍可返回NO_XFER/HAL_ERROR；随后主忙态仍归一化，且不会因这次Abort失败新置主ERROR_DMA。已有错误State的保留须另看，不能照搬独立ADC新版本的归一化遗漏。

部分失败须保留顺序：主禁用失败时尚未处理从；主成功而从禁用失败时，DMA请求、DUALMOD和DMA Abort均尚未清理。新版本可出现主State.ERROR_INTERNAL而ErrorCode为NONE；重试Stop成功仍不保证清该State，Init仍可能拒绝。旧版临时从句柄仅赋Instance，未整体初始化；失败helper对其State作读改写，因此不对该未初始化失败路径承诺确定结果。新版本临时从句柄已零初始化。

正常停止实际会禁用ADC2，但应用自有hadc2未随之同步；残留软件忙态不单独证明ADC2仍在转换。C8的ADC2没有独立DMA请求，不能用独立HAL_ADC_Stop_DMA代替主从协调。

## 4 数据格式和恢复条件

组合字高半字ADC2、低半字ADC1，半字内部仍按各自ALIGN解释。两路右对齐时各取低12位；左对齐时先在各自16位半字内右移4位。采用外设/存储器word宽度时，一个DMA项为4字节；以MINC=1写入连续数组、保留整段结果时，容量至少4×Length字节，Length为无量纲项数。MINC=0会重复覆盖同一个内存字，不能保存Length项历史结果。地址递增和容量条件见[DMA缓冲区契约](../../知识库/04_DMA与缓冲区协作.md#1-dma1资源通道和数据项)。组合字不能直接传入单ADC电压宏。

HAL_ADC_Init并不清State.ERROR_DMA；真实TE后单靠Stop→Init→重配模式→Start仍可保留错误回调分支。成功DeInit重置传入ADC句柄，但DMA、另一ADC及GPIO/NVIC回收取决于MSP和应用所有权。

恢复须先隔离触发、保存诊断，分别确认本事务ADC1、必要时ADC2、DMA已停止，再按实际驱动和MSP重建资源、序列、校准与双模式。只改State或清ErrorCode不证明硬件停止，禁用失败时不能释放缓冲区。

## 5 固定来源与验证边界

- [独立Stop v1.1.4 L1692起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1692)、[v1.1.10 L1694起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_adc.c#L1694)
- [双模式Start/Stop v1.1.4 L670–861](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L670-L861)、[v1.1.10 L675起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_adc_ex.c#L675)
- [DMA Abort v1.1.4 L416起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_dma.c#L416)、[v1.1.10 L415起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_dma.c#L415)

留存的定向主机用例支持上述分支：独立ADC每版本8场景，双模式旧版6、新版9场景；禁用失败由显式受控条件注入，旧版临时句柄不确定路径未作确定状态断言。这些用例不模拟采样、硬件清EN、真实总线或中断时序，不说明实际故障概率；这些主机用例不构成板卡验证。固定bd368aa快照的ADC/DMA文件与所列v1.1.10文件字节一致，该一致性不扩展到未核对的其它文件。
