# TIM LL 初始化的状态与返回值约束

适用STM32F103C8T6。本文核对ST驱动固定提交de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9的LL TIM实现及同提交头文件；结论不自动适用于其他版本。本文是固定来源整合参考，未编译、执行固件或进行板上测量。

## 1 初始化返回值的范围

|入口|实现中的动作与返回路径|使用边界|
|---|---|---|
|LL_TIM_Init|修改计数模式、CKD、ARR、PSC及适用实例的RCR，调用GenerateEvent_UPDATE，最终SUCCESS|函数不先停止CEN，不隔离TRGO；SUCCESS不证明输出安全、更新事件无副作用或所有写入均被硬件接受|
|LL_TIM_OC_Init|CH1～CH4分别分派到OC1Config～OC4Config；未匹配通道返回ERROR|有效通道助手最终SUCCESS；assert_param检查与硬件回读是不同机制|
|LL_TIM_IC_Init|CH1～CH4分别分派到IC1Config～IC4Config；未匹配通道返回ERROR|助手先禁用对应CCxE，配置后再次启用；不能把调用结束当作通道仍关闭|
|LL_TIM_ENCODER_Init|暂时关闭CC1E/CC2E，配置两个输入与SMS，最后启用CC1E/CC2E，SUCCESS|未先停止CEN；SetEncoderMode仅以SMS为修改掩码，没有清除ECE的调用|
|LL_TIM_HALLSENSOR_Init|配置TI1异或、TI1F_ED复位从模式、CH1捕获和CH2延时参考，启用CC1E/CC2E，SUCCESS|复用已有配置时有MMS与CC2S残留条件，见下一节|
|LL_TIM_BDTR_Init|以临时值构造BDTR，调用寄存器写入，最终SUCCESS|未回读验证LOCK限制下的字段是否接受写入；不能以SUCCESS证明保护配置已生效|
|LL_TIM_DeInit|支持实例调用相应APB的ForceReset/ReleaseReset；不匹配实例返回ERROR|属于外设复位路径；本节未单独展开LL bus宏全部依赖，不能与HAL的MSP依赖DeInit混为一谈|

CEN为计数使能，CKD为采样时钟分频字段，ARR为自动重装，PSC为预分频，RCR为重复计数；SMS为从模式选择，ECE为外部时钟模式2使能；CCxE为通道x使能，TRGO为触发输出，LOCK为保护字段锁定等级。

来源：[LL TIM实现L168–727](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_tim.c#L168-L727)、[SetEncoderMode L2529–2532](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2529-L2532)。更新及TRGO条件见[计数时基与更新](计数时基与更新.md)。

## 2 Hall初始化的两项历史状态依赖

### 2.1 MMS通过按位或合入，旧选择可能保留

该版本先读取CR2，然后执行tmpcr2按位或LL_TIM_TRGO_OC2REF，随后将tmpcr2作为CR2写入参数。中间没有清除MMS字段。头文件的OC2REF编码为MMS=101；因此形成的字段参数为旧MMS按位或101。

|调用前MMS|构造出的MMS参数|RM0008对应的TRGO选择|
|---|---|---|
|000、001、100、101|101|OC2REF|
|010、011、110、111|111|OC4REF|

这里MMS是CR2[6:4]的三位字段，表内数字为二进制；OC2REF/OC4REF分别为第2/4通道内部输出参考。表格来自固定源码的位运算及手册编码核对，未进行板上复现。复位值000满足该实现的OC2REF预期；例如原先使用更新事件TRGO、MMS=010时，构造参数会成为111。函数没有对此返回ERROR。

### 2.2 CH2的输入/输出选择未被清除

同一函数读取CCMR1后，用OC2M、OC2FE、OC2PE、OC2CE掩码清理CH2控制字段，再合入PWM2编码；掩码不含CC2S[1:0]。因此调用前CC2S非零时，该选择仍保留在CCMR1写入参数中。RM0008规定CC2S=00为输出，01/10/11为输入；不能据此函数注释直接认定任何旧配置都会变为CH2 PWM2输出。

MMS和CC2S是独立条件。只修正TRGO选择仍不足以覆盖先前CH2为输入的场景。配置流程应在触发和输出已隔离的条件下，明确建立CC2S=00及MMS=101，并检查实际寄存器；还需按实例处理CCPC、LOCK和其他可保留状态。这里没有宣称仅这两项就是完整安全初始化。

来源：[Hall实现L595–664](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_tim.c#L595-L664)、[TRGO编码L704–712](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L704-L712)、[RM0008 Rev21 MMS p340](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=340)、[CC2S p349](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=349)。

版本复核：提交77fbb30b7a1d02533980400083e48c559aae5a4f中，[Hall函数L603–673](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_ll_tim.c#L603-L673)仍保留上述按位或及省略CC2S的清除掩码。两份函数体忽略注释与空白后相同；这只验证函数体，不代表两个版本所有头文件、宏和编译配置都已对照完毕。

HAL接口边界：同一de129f1提交的[HAL_TIMEx_HallSensor_Init L130–214](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L130-L214)在设置OC2REF前明确清除MMS；其调用的[TIM_OC2_SetConfig L5933起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim.c#L5933-L5960)也清除CC2S。因此上面两项具体的残留条件不能泛化到该HAL初始化实现。HAL仍须独立检查UG、运行状态和输出保护等其他约束。

## 3 StructInit的默认值与芯片适用范围

StructInit仅填写配置结构，没有对外设进行初始化。下列为固定实现的赋值内容。

|结构入口|默认字段|
|---|---|
|LL_TIM_StructInit|Prescaler=0，CounterMode=UP，Autoreload=0xFFFFFFFF，ClockDivision=DIV1，RepetitionCounter=0|
|LL_TIM_OC_StructInit|OCMode=FROZEN，OCState/OCNState=DISABLE，CompareValue=0，OCPolarity/OCNPolarity=HIGH，OCIdleState/OCNIdleState=LOW|
|LL_TIM_IC_StructInit|ICPolarity=RISING，ICActiveInput=DIRECTTI，ICPrescaler=DIV1，ICFilter=FDIV1|
|LL_TIM_ENCODER_StructInit|EncoderMode=X2_TI1；IC1/IC2各自为RISING、DIRECTTI、DIV1、FDIV1|
|LL_TIM_HALLSENSOR_StructInit|IC1Polarity=RISING，IC1Prescaler=DIV1，IC1Filter=FDIV1，CommutationDelay=0|
|LL_TIM_BDTR_StructInit|OSSR/OSSI=DISABLE，LockLevel=OFF，DeadTime=0，BreakState=DISABLE，BreakPolarity=LOW，AutomaticOutput=DISABLE|

Autoreload的通用默认值0xFFFFFFFF不代表C8拥有32位ARR。C8的TIM1～TIM4自动重装字段为16位；应填写适合本芯片和目标周期的值，不把该默认值写成C8参数上限。TIM1的RCR为8位，TIM2～TIM4没有该功能。没有启用输出和保护的默认结构也不能直接代表具体功率级的安全配置。

来源：[默认结构与初始化实现L306–727](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_tim.c#L306-L727)、RM0008 Rev21 §14.4.12–13、§15.4的ARR字段。

## 4 尚需区分的证据层次

LL_TIM_BDTR_Init在AOE修改之后，还以TIM_BDTR_MOE为清除掩码、AutomaticOutput为设置参数调用MODIFY_REG。该版本头文件把AutomaticOutput的ENABLE定义为TIM_BDTR_AOE。这里只确认源码操作数；尚未独立闭合所用基础MODIFY_REG宏的全部依赖，不将它扩展为已验证的引脚电平或硬件测试结论。配置BDTR后的MOE、AOE与锁定字段应分别核对。

来源：[BDTR实现L698–727](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_ll_tim.c#L698-L727)、[AutomaticOutput常量L469–470](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L469-L470)。

提交77fbb30b7a1d02533980400083e48c559aae5a4f的[BDTR函数L708–737](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_ll_tim.c#L708-L737)已没有该MOE掩码调用。本节将其记录为固定版本间的源码差异，不据此声称已经测得输出行为差异。

[返回定时器主题](../../知识库/06_定时器PWM与同步.md) · [图形关系与来源](图形关系与来源.md)
