# TIM HAL 时基初始化与反初始化边界

固定来源整合参考。以下是两个固定版本的源代码阅读结论，不是固件执行或板端测试。C8只使用TIM1～TIM4；MSP回调、编译宏及用户改动另行决定实际工程行为。

- v1.1.4：de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9。
- v1.1.10：77fbb30b7a1d02533980400083e48c559aae5a4f。

## 1 Init会更新哪些硬件与软件状态

HAL_TIM_Base_Init检查空句柄并执行参数断言；State为RESET时才初始化锁并调用MSP。随后设BUSY、调用TIM_Base_SetConfig，最后设READY并返回HAL_OK。函数本体没有先清CEN、关闭全部通道、停止DMA或隔离TRGO接收端；不能把Init当作活动采集/输出的停止接口。

TIM_Base_SetConfig读取并更新CR1中的DIR/CMS、CKD及ARPE，写ARR、PSC；具备重复计数器的实例还写RCR，最后写EGR.UG。CR1其余状态及SMCR/CR2等既有配置不能假定因此回到复位值。UG的预装载、触发和标志后果仍受现有UDIS、URS、MMS及从模式配置影响。

v1.1.10还将DMABurstState、全部主通道与互补通道软件状态置READY；v1.1.4使用较早的共享状态表示。这些赋值不证明相关DMA或通道已在硬件上静止。需要重配时应先在资源所有权和系统输出保护要求下建立静止边界。

固定源码：[v1.1.4 Init L265起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim.c#L265)、[v1.1.10 Init L266起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_tim.c#L266)、[v1.1.4配置helper L5810–5850](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim.c#L5810-L5850)、[v1.1.10配置helper L6776–6823](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_tim.c#L6776-L6823)。

## 2 Period、RepetitionCounter与断言的版本条件

|字段或操作|v1.1.4|v1.1.10|C8硬件条件|
|---|---|---|---|
|Base_Init的Period检查|本函数未列IS_TIM_PERIOD断言|增加IS_TIM_PERIOD断言，要求>0且≤0xFFFF|ARR为16位，ARR=0阻塞计数|
|RepetitionCounter写入|支持实例直接写结构字段到RCR|同样直接写入|TIM1只允许有效低8位，0～255；TIM2～4没有RCR|
|写UG后的UIF处理|该helper没有随后清UIF语句|若立即读到UIF已置位，调用CLEAR_BIT清该位|清状态位不撤回已发生的UEV或TRGO|

断言是否启用、失败后如何处理，由工程的assert_param配置决定；断言不是统一返回HAL_ERROR的运行期参数检查。不能因结构字段类型为uint32_t或函数返回OK，就扩大硬件字段范围。

两版RepetitionCounter头文件注释均包含“高级定时器最大0xFFFF”的泛化文字，不能据此把F103C8的RCR扩为16位。本文使用RM0008 p357的REP[7:0]和本器件资源定义；寄存器保留位不应写入越界值。

v1.1.10的UIF条件清除只说明该次读到置位后的分支；没有等待所有潜在同步事件结束，也不撤回接收端已消费的触发。本页不据此保证任意时钟比、并发事件或运行时Init均无额外中断。

来源：[v1.1.10 Period断言定义L1656](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_tim.h#L1656)、[v1.1.4结构注释L62–69](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L62-L69)、[RM0008 Rev21 RCR，p357](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=357)。

## 3 DeInit、停计数、关时钟和外设复位分别核查

两版HAL_TIM_Base_DeInit本体均设置BUSY，调用__HAL_TIM_DISABLE，调用MSP释放回调，再将软件状态设RESET、解锁并返回HAL_OK。v1.1.10另复位DMABurstState和各通道软件状态。函数本体没有显式RCC时钟门控或RCC外设复位写入；默认弱MSP函数不执行资源释放动作，用户覆盖的MSP可能另有操作。

__HAL_TIM_DISABLE只在所有CCxE及CCxNE都为0时才清CR1.CEN，既不无条件停计数，也不关闭RCC门控。函数旁的“Disable the TIM Peripheral Clock”注释不能当作实际RCC操作的证据。若仍有通道使能，CEN可能保持；软件State=RESET不能代替真实计数、输出和DMA状态确认。

HAL注释建议中心/边沿模式切换前先复位，并举DeInit→Init为例。使用该建议时须检查MSP是否实际完成所需复位及资源收尾，不能把两次API调用自动等同于RCC硬件复位。复位或禁用共享定时器还会影响其它通道，必须先确认资源所有权和功率级安全态。

固定源码：[v1.1.4 DeInit L317起及弱MSP L368起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim.c#L317-L375)、[v1.1.10 DeInit L326起及弱MSP L384起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_tim.c#L326-L391)、[v1.1.4条件禁用宏L1027起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1027)、[v1.1.10条件禁用宏L1086起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_tim.h#L1086)。

## 4 RESET_HANDLE_STATE的版本与回调副作用

__HAL_TIM_RESET_HANDLE_STATE不是外设复位命令。固定头文件的赋值范围如下：

|条件|v1.1.4|v1.1.10|
|---|---|---|
|所有编译配置|State置HAL_TIM_STATE_RESET|State置RESET；ChannelState[0…3]及ChannelNState[0…3]置相应RESET；DMABurstState置RESET|
|USE_HAL_TIM_REGISTER_CALLBACKS=1|额外将14个MSP回调指针置NULL|同样额外清这14个MSP回调指针|
|USE_HAL_TIM_REGISTER_CALLBACKS≠1|没有上述条件回调字段操作|没有上述条件回调字段操作|

14个指针是Base、IC、OC、PWM、OnePulse、Encoder、HallSensor七类各自的MspInitCallback和MspDeInitCallback。先注册MSP回调后再使用此宏，会清除这些注册项；随后的Init可能转而采用默认弱MSP函数。事件完成/错误回调不在此宏的14项清空列表内，不能把它描述成清空所有回调；后续Init又有自己的回调恢复逻辑。

宏本体没有操作CEN、MOE、RCC、DMA硬件，也没有释放缓冲区或重置Lock、hdma[]关联。v1.1.10的软件ChannelNState数组有四个槽位不代表C8有CH4N引脚。应用必须先确认真实硬件及所有权状态，不以此宏强行修补活动传输的状态机。

来源：[v1.1.4宏定义L987起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L987)、[v1.1.10宏定义L1026起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_tim.h#L1026)。

[返回定时器主题](../../知识库/06_定时器PWM与同步.md) · [图形关系与来源](图形关系与来源.md)
