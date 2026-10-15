# ADC 初始化、反初始化及软件状态边界

依据固定 HAL v1.1.4 / v1.1.10 源码阅读；没有执行实板验证。

## Init 的资源与回调条件

HAL_ADC_Init 对空 hadc 返回 HAL_ERROR。正常配置路径先停止并禁用 ADC，再设置公共扫描、规则组连续/间断模式、触发选择、数据对齐和规则序列长度；它不替代逐 Rank 通道配置、注入组配置、看门狗、双模式设置或校准。

只有入口 State 恰为 RESET 时才执行 MSP 初始化。USE_HAL_ADC_REGISTER_CALLBACKS==1 时，这条路径把五个转换/看门狗/错误回调重设为默认弱函数；MspInitCallback 非空时保留并调用，空时才回退默认弱函数。MspDeInitCallback 的空指针回退发生于反初始化路径。普通回调应在成功初始化后注册，提前设置普通回调不能保证经过 RESET 初始化后仍保留。

Init 修改的是明确列出的字段，不提供清除所有历史错误状态的承诺。例如已存在的 State.ERROR_DMA 不在本函数的状态清除掩码内。ErrorCode 清零与 State 位图清除是不同操作。

## 连续/间断冲突不能只检查返回值

在所核两版实现中，如果 ContinuousConvMode 和 DiscontinuousConvMode 同时为 ENABLE，函数设置 State.ERROR_CONFIG 和 ErrorCode.INTERNAL，但这条分支没有立即返回，也没有将局部返回值改为 HAL_ERROR。若随后的寄存器回读检查通过，ErrorCode 会再清零，State 置 READY，同时保留 ERROR_CONFIG，返回值仍可能为 HAL_OK。

这条源码路径要求知识库把“规则连续与间断互斥”写为调用前必须满足的配置约束，不能承诺驱动必以失败返回值阻止所有非法组合。这里的“可能”以使能/禁用成功、寄存器回读相符等前提为限；不把它扩写为任何错误配置都返回成功。

参数断言也取决于工程 assert_param 配置；关闭断言后，不能将范围检查宏存在当作运行时输入已被拒绝。

## DeInit 的确切范围

HAL_ADC_DeInit 先调用 ADC 公共停止/禁用路径，成功后才清理它列出的寄存器字段、调用 MSP 反初始化、清 ErrorCode 并使句柄 State=RESET。停止/禁用失败时不能宣称这些后续清理已完成。

需要纠正旧接口摘要“恢复 ADC 寄存器和句柄的初始状态”的无条件表述：

- 函数对 CR1 的清除掩码不包含 DUALMOD，单靠该函数主体不能保证把双模式选择清成独立模式。
- 函数将 HTR 清零；RM0008 Rev21 §11.12.7 p246 的 HTR 复位值为 0x00000FFF，所核操作不等同于该复位值。RM p252 总表另有 HTR 零值冲突，两处来源的冲突仍需保留，复位值不能据此视为已无歧义。
- DMA 控制器、GPIO、NVIC、RCC 等资源是否回收取决于 MSP 实现和应用所有权；函数存在与句柄 RESET 本身不足以证明整套资源已复位。
- 若工程自定义 MSP 执行了外设硬件复位，最终硬件状态会受该实现影响。上述两项指所核通用函数主体，不能越过用户 MSP 推断最终寄存器值。

恢复采集应先隔离触发并确认本事务硬件停止，再按工程固定驱动和 MSP 的实际步骤恢复配置、校准及缓冲区所有权。单独手改 State 或 ErrorCode 会丢失诊断，且不证明硬件恢复。

## Start、Stop 和 GetState 的解释

Start 成功会设置规则忙状态并根据软件/外部触发及主从身份启动或武装转换；外部触发路径可以在尚无样本时返回成功。自动注入模式还会设置相应注入忙状态。Stop 成功通过公共禁用路径清规则/注入忙状态，不能将其描述为保留注入运行的“只停规则组”。

GetState 和 GetError 分别返回软件字段，不执行寄存器核对或硬件自检。READY 可以与未清除的错误位并存；相关软件完成位也不在所有路径中等价于数据新鲜。

## 固定来源

- [v1.1.4 Init，L421–627](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L421-L627)
- [v1.1.4 DeInit，L639–775](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L639-L775)
- [v1.1.10 对应实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_adc.c#L421-L771)
- [v1.1.4 Start/Stop](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1046-L1181)
- [RM0008 Rev21 §11.12.8](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=246)

相关停止和恢复条件见[DMA生命周期与恢复](DMA生命周期与恢复.md)。

## 校准入口的两版顺序与返回值传递

HAL_ADCEx_Calibration_Start的显式等待位置及错误传播须分别核对：

|条件|v1.1.4|v1.1.10|
|---|---|---|
|两ADC时钟的显式估算等待|在禁用成功后、ADC_Enable之前|在ADC_Enable返回OK后、RSTCAL之前|
|禁用helper返回值|先检查成功，才进入校准分支|立即被后续ADC_Enable返回值覆盖，没有先检查禁用结果|
|使能helper返回值|调用ADC_Enable但不接收其返回值，继续RSTCAL路径|接收返回值，仅OK时进入RSTCAL路径|
|RSTCAL/CAL超时|置内部错误State并返回HAL_ERROR|超时判定后复查对应位，仍置位才报错|

RM0008 p223要求校准前已上电至少两个ADC时钟；新版本已将显式等待移到使能之后。等待仍是由SystemCoreClock和ADC频率计算的软件循环，放置位置的修正不等于经过板端精确时序测量。

这两版也不能仅用“使能顺序已修复”概括全部错误处理。旧版忽略使能失败返回，新版覆盖禁用失败返回，均属于可直接从函数体确认的控制流事实。不能由此推定实际芯片必然出现这些失败，也不能在未满足后续校准完成条件时声称一定返回OK。调用结果、ErrorCode、State及实际ADC状态须联合解释；提前在函数外置ADON也不能保证绕过函数内部重新禁用的步骤。

来源：[v1.1.4校准入口L126起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L126)、[v1.1.10禁用/使能与等待L131–159](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_adc_ex.c#L131-L159)、[RM0008 Rev21 p223](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=223)。本段为固定源码顺序审查，未执行失败注入或硬件校准测试。
