# TIM HAL 导出宏参考

固定来源整合参考。保留33个宏入口，按固定v1.1.4头文件列出定位；v1.1.10差异另见初始化边界。原型/名称匹配不表示已完成所有宏依赖或并发时序验证。C8仅支持TIM1～TIM4。


宏不是带类型检查的普通函数。不要把带自增等副作用的表达式作为参数；部分参数会被重复求值，多次寄存器写入也不是一次原子操作。CCMR的输入/输出字段复用，调用OC预装载/快速模式宏前必须确认相应通道处于输出模式，不能在输入捕获配置中把相同位号当作输出功能。读写仍须满足状态、实例和通道限制。

### `__HAL_TIM_RESET_HANDLE_STATE`

调用形态：`__HAL_TIM_RESET_HANDLE_STATE(__HANDLE__)`。

固定v1.1.4将State置RESET，动态回调注册开启时还清14个MSP回调指针。v1.1.10增加通道及DMABurst状态复位。它不操作外设或DMA硬件，不重置锁和DMA关联；详见[版本与回调副作用](HAL初始化边界.md#4-reset_handle_state的版本与回调副作用)。

[固定头文件L987](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L987)

### `__HAL_TIM_ENABLE`

调用形态：`__HAL_TIM_ENABLE(__HANDLE__)`。

句柄参数；置 CEN，使能计数，无返回。

[固定头文件L1013](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1013)

### `__HAL_TIM_MOE_ENABLE`

调用形态：`__HAL_TIM_MOE_ENABLE(__HANDLE__)`。

句柄参数；置 TIM1 的 MOE，无返回。

[固定头文件L1020](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1020)

### `__HAL_TIM_DISABLE`

调用形态：`__HAL_TIM_DISABLE(__HANDLE__)`。

句柄参数；当有关通道均关闭时才清 CEN，避免破坏其他仍使用的通道。

[固定头文件L1027](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1027)

### `__HAL_TIM_MOE_DISABLE`

调用形态：`__HAL_TIM_MOE_DISABLE(__HANDLE__)`。

句柄参数；仅当所有 CCx/CCxN 输出通道都禁用时清 MOE，TIM1 专用。宏不清 AOE；AOE=1且刹车无效时，后续UEV仍可重新置MOE，但通道是否输出还取决于CCER等条件。

[固定头文件L1044](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1044)

### `__HAL_TIM_MOE_DISABLE_UNCONDITIONALLY`

调用形态：`__HAL_TIM_MOE_DISABLE_UNCONDITIONALLY(__HANDLE__)`。

句柄参数；无条件清TIM1的MOE。实际引脚可能被禁用或驱动到配置的空闲电平，由OSSI/OIS、极性、通道使能及GPIO共同决定（MOE=0时OSSR不参与）；不能据此统一声称两端为低、已经高阻或外部驱动器安全。此操作影响整颗TIM1的输出资源。宏保留AOE、CEN和CCER；AOE=1且刹车无效时，后续UEV可重新置MOE，所以“无条件清除”不表示持续锁定关断。

[固定头文件L1061](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1061)

### `__HAL_TIM_ENABLE_IT`

调用形态：`__HAL_TIM_ENABLE_IT(__HANDLE__, __INTERRUPT__)`。

句柄加 TIM_IT_* 掩码；开放相应中断，无返回。

[固定头文件L1077](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1077)

### `__HAL_TIM_DISABLE_IT`

调用形态：`__HAL_TIM_DISABLE_IT(__HANDLE__, __INTERRUPT__)`。

句柄加 TIM_IT_* 掩码；关闭相应中断，无返回。

[固定头文件L1093](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1093)

### `__HAL_TIM_ENABLE_DMA`

调用形态：`__HAL_TIM_ENABLE_DMA(__HANDLE__, __DMA__)`。

句柄加 TIM_DMA_* 掩码；开放对应 DMA 请求，不配置 DMA 控制器。

[固定头文件L1108](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1108)

### `__HAL_TIM_DISABLE_DMA`

调用形态：`__HAL_TIM_DISABLE_DMA(__HANDLE__, __DMA__)`。

句柄加 TIM_DMA_* 掩码；关闭对应 DMA 请求。

[固定头文件L1123](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1123)

### `__HAL_TIM_GET_FLAG`

调用形态：`__HAL_TIM_GET_FLAG(__HANDLE__, __FLAG__)`。

句柄加TIM_FLAG_*；表达式为(SR & mask)==mask。对合法组合掩码是全部位匹配，零掩码会得到真，不能用零掩码表示“没有事件”。查询状态位不等同于中断使能或完整事件计数。

[固定头文件L1143](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1143)

### `__HAL_TIM_CLEAR_FLAG`

调用形态：`__HAL_TIM_CLEAR_FLAG(__HANDLE__, __FLAG__)`。

句柄加TIM_FLAG_*掩码；直接向SR写~mask，以rc_w0语义清所选位，不是先读SR再逐位修改。清标志不撤回已传播的触发或DMA请求。

[固定头文件L1163](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1163)

### `__HAL_TIM_GET_IT_SOURCE`

调用形态：`__HAL_TIM_GET_IT_SOURCE(__HANDLE__, __INTERRUPT__)`。

句柄加TIM_IT_*；(DIER & mask)==mask时返回SET，否则RESET。组合掩码要求全部位开放，零掩码返回SET；它不读取SR的事件发生状态。

[固定头文件L1180](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1180)

### `__HAL_TIM_CLEAR_IT`

调用形态：`__HAL_TIM_CLEAR_IT(__HANDLE__, __INTERRUPT__)`。

句柄加中断对应掩码；清相应挂起状态，不等于禁用中断。

[固定头文件L1197](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1197)

### `__HAL_TIM_IS_TIM_COUNTING_DOWN`

调用形态：`__HAL_TIM_IS_TIM_COUNTING_DOWN(__HANDLE__)`。

句柄参数；返回计数方向是否向下。

[固定头文件L1206](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1206)

### `__HAL_TIM_SET_PRESCALER`

调用形态：`__HAL_TIM_SET_PRESCALER(__HANDLE__, __PRESC__)`。

句柄加0～65535的PSC值；下一更新事件生效。固定宏只写PSC，不同步Init.Prescaler，也不自动产生UG。

[固定头文件L1214](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1214)

### `__HAL_TIM_SET_COUNTER`

调用形态：`__HAL_TIM_SET_COUNTER(__HANDLE__, __COUNTER__)`。

句柄加 0–65535 的 CNT 值；改变当前计数值。

[固定头文件L1222](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1222)

### `__HAL_TIM_GET_COUNTER`

调用形态：`__HAL_TIM_GET_COUNTER(__HANDLE__)`。

句柄参数；返回当前 CNT。

[固定头文件L1229](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1229)

### `__HAL_TIM_SET_AUTORELOAD`

调用形态：`__HAL_TIM_SET_AUTORELOAD(__HANDLE__, __AUTORELOAD__)`。

句柄加ARR值，C8寄存器有效低16位，正常计数要求1～65535；宏同时写ARR与Init.Period，未作范围检查。硬件生效时间由预装载决定；两处赋值不是一次原子操作。

[固定头文件L1237](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1237)

### `__HAL_TIM_GET_AUTORELOAD`

调用形态：`__HAL_TIM_GET_AUTORELOAD(__HANDLE__)`。

句柄参数；直接读取ARR。ARPE=1时读到的是软件可见预装载值，不能单凭读回认定内部活动值已装入。

[固定头文件L1248](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1248)

### `__HAL_TIM_SET_CLOCKDIVISION`

调用形态：`__HAL_TIM_SET_CLOCKDIVISION(__HANDLE__, __CKD__)`。

句柄加 TIM_CLOCKDIVISION_DIV1/2/4；设置 CKD 并保持句柄对应配置一致。

[固定头文件L1260](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1260)

### `__HAL_TIM_GET_CLOCKDIVISION`

调用形态：`__HAL_TIM_GET_CLOCKDIVISION(__HANDLE__)`。

句柄参数；返回 CKD 配置编码。

[固定头文件L1275](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1275)

### `__HAL_TIM_SET_ICPRESCALER`

调用形态：`__HAL_TIM_SET_ICPRESCALER(__HANDLE__, __CHANNEL__, __ICPSC__)`。

句柄、通道、TIM_ICPSC_DIV1/2/4/8；设置输入捕获事件预分频。

[固定头文件L1294](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1294)

### `__HAL_TIM_GET_ICPRESCALER`

调用形态：`__HAL_TIM_GET_ICPRESCALER(__HANDLE__, __CHANNEL__)`。

句柄、通道；返回输入捕获预分频编码，不是整数除数。

[固定头文件L1315](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1315)

### `__HAL_TIM_SET_COMPARE`

调用形态：`__HAL_TIM_SET_COMPARE(__HANDLE__, __CHANNEL__, __COMPARE__)`。

句柄、通道、CCR值；设置选定通道比较值，预装载决定生效时机。固定宏对非CH1/CH2/CH3参数直接选择CCR4，调用者必须先保证通道合法；不能用TIM_CHANNEL_ALL写四个通道。

[固定头文件L1333](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1333)

### `__HAL_TIM_GET_COMPARE`

调用形态：`__HAL_TIM_GET_COMPARE(__HANDLE__, __CHANNEL__)`。

句柄、通道；读取对应CCR。输出预装载使能时不能将读值自动视为当前活动比较值；输入捕获模式读取还涉及清CCxIF及并发捕获边界。固定宏对非CH1/CH2/CH3参数直接选择CCR4，因此非法通道不会自动返回参数错误。

[固定头文件L1350](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1350)

### `__HAL_TIM_ENABLE_OCxPRELOAD`

调用形态：`__HAL_TIM_ENABLE_OCxPRELOAD(__HANDLE__, __CHANNEL__)`。

句柄、通道；开放相应 CCR 预装载。

[固定头文件L1367](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1367)

### `__HAL_TIM_DISABLE_OCxPRELOAD`

调用形态：`__HAL_TIM_DISABLE_OCxPRELOAD(__HANDLE__, __CHANNEL__)`。

句柄、通道；关闭相应 CCR 预装载。

[固定头文件L1384](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1384)

### `__HAL_TIM_ENABLE_OCxFAST`

调用形态：`__HAL_TIM_ENABLE_OCxFAST(__HANDLE__, __CHANNEL__)`。

句柄、通道；仅 PWM1/PWM2 有效。触发有效边沿可像比较匹配一样直接作用于 CCx 输出，忽略等待计数器比较的过程；原文给出触发采样至输出响应缩短为 3 个定时器时钟周期。

[固定头文件L1405](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1405)

### `__HAL_TIM_DISABLE_OCxFAST`

调用形态：`__HAL_TIM_DISABLE_OCxFAST(__HANDLE__, __CHANNEL__)`。

句柄、通道；关闭快速响应后按 CNT 与 CCRx 的正常比较关系输出；原文给出的触发有效边沿至输出激活最小延迟为 5 个定时器时钟周期。

[固定头文件L1426](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1426)

### `__HAL_TIM_URS_ENABLE`

调用形态：`__HAL_TIM_URS_ENABLE(__HANDLE__)`。

句柄参数；设置 URS，使更新中断/DMA 请求限于计数器溢出/下溢。

[固定头文件L1440](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1440)

### `__HAL_TIM_URS_DISABLE`

调用形态：`__HAL_TIM_URS_DISABLE(__HANDLE__)`。

句柄参数；清 URS，允许 UG 和从控制器更新等来源产生更新请求。

[固定头文件L1453](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1453)

### `__HAL_TIM_SET_CAPTUREPOLARITY`

调用形态：`__HAL_TIM_SET_CAPTUREPOLARITY(__HANDLE__, __CHANNEL__, __POLARITY__)`。

句柄、通道、输入极性；经两步清/设修改CCER极性字段。C8普通捕获按RISING/FALLING使用；头文件的BOTHEDGE常量不能证明硬件具备该捕获能力，也不会单独把TS切换到TI1F_ED双边沿检测路径。

[固定头文件L1470](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1470)

[返回定时器主题](../../知识库/06_定时器PWM与同步.md) · [图形关系与来源](图形关系与来源.md)
