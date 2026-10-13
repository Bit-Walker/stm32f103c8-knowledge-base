# TIM HAL 扩展接口

STM32F103C8T6，固定来源整合参考。TIM1支持互补输出/刹车/COM，TIM2～4不支持这些高级功能。先看[HAL初始化边界](HAL初始化边界.md)、[时基与更新](计数时基与更新.md)。单通道Stop、软件READY或HAL_OK都须结合具体实现及实际状态解释。


本页保留35个HAL_TIMEx接口及两个TIMEx内部DMA回调。接口签名与固定de129f1实现逐项核对；HAL/LL枚举不可混传。以下描述需结合初始化及共享资源约束，原型匹配不表示全部语义复核完成。

### `HAL_TIMEx_HallSensor_Init`

```c
HAL_StatusTypeDef HAL_TIMEx_HallSensor_Init (TIM_HandleTypeDef * htim, TIM_HallSensor_InitTypeDef * sConfig);
```

初始化霍尔传感器接口。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `sConfig`：原型所示配置结构指针；字段和合法组合见本章结构说明。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- 中心对齐与边沿对齐切换前先按手册处理计数器状态及必要复位；HAL DeInit 是否真正停计数、执行外设复位取决于通道状态及 MSP 实现，不能仅凭调用名称保证。详见[初始化与复位约束](HAL初始化边界.md)。Init 不代替相应 Start。

固定实现约束：固定HAL实现先清MMS再选择OC2REF，TIM_OC2_SetConfig也清CC2S，不能套用本次发现的LL Hall两项字段残留问题。但本函数调用TIM_Base_SetConfig会发UG，应预先处理下游触发和正在运行的输出。

来源：[固定实现L130](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L130)。

### `HAL_TIMEx_HallSensor_DeInit`

```c
HAL_StatusTypeDef HAL_TIMEx_HallSensor_DeInit (TIM_HandleTypeDef * htim);
```

释放霍尔传感器接口。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

来源：[固定实现L222](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L222)。

### `HAL_TIMEx_HallSensor_MspInit`

```c
void HAL_TIMEx_HallSensor_MspInit (TIM_HandleTypeDef * htim);
```

用户实现底层初始化霍尔传感器接口。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定实现L258](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L258)。

### `HAL_TIMEx_HallSensor_MspDeInit`

```c
void HAL_TIMEx_HallSensor_MspDeInit (TIM_HandleTypeDef * htim);
```

用户实现底层释放霍尔传感器接口。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定实现L273](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L273)。

### `HAL_TIMEx_HallSensor_Start`

```c
HAL_StatusTypeDef HAL_TIMEx_HallSensor_Start (TIM_HandleTypeDef * htim);
```

启动霍尔传感器接口。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

来源：[固定实现L288](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L288)。

### `HAL_TIMEx_HallSensor_Stop`

```c
HAL_StatusTypeDef HAL_TIMEx_HallSensor_Stop (TIM_HandleTypeDef * htim);
```

停止霍尔传感器接口。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

来源：[固定实现L315](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L315)。

### `HAL_TIMEx_HallSensor_Start_IT`

```c
HAL_StatusTypeDef HAL_TIMEx_HallSensor_Start_IT (TIM_HandleTypeDef * htim);
```

以中断方式启动霍尔传感器接口。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

来源：[固定实现L336](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L336)。

### `HAL_TIMEx_HallSensor_Stop_IT`

```c
HAL_StatusTypeDef HAL_TIMEx_HallSensor_Stop_IT (TIM_HandleTypeDef * htim);
```

停止并关闭中断霍尔传感器接口。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

来源：[固定实现L366](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L366)。

### `HAL_TIMEx_HallSensor_Start_DMA`

```c
HAL_StatusTypeDef HAL_TIMEx_HallSensor_Start_DMA (TIM_HandleTypeDef * htim, uint32_t * pData, uint16_t Length);
```

以 DMA 方式启动霍尔传感器接口。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `pData`：DMA 接收目标缓冲区地址，TIM 捕获数据写入内存；直到 DMA 停止前必须有效。
- `Length`：DMA 传输项数，非字节数；数据宽度由 DMA 配置决定。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

固定实现约束：在READY路径先把State置BUSY，且调用HAL_DMA_Start_IT前已启用CC1、改写关联DMA回调；DMA启动失败返回HAL_ERROR时，这些动作没有完整回滚。BUSY状态立即返回HAL_BUSY；其他State未统一拒绝。

来源：[固定实现L392](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L392)。

### `HAL_TIMEx_HallSensor_Stop_DMA`

```c
HAL_StatusTypeDef HAL_TIMEx_HallSensor_Stop_DMA (TIM_HandleTypeDef * htim);
```

停止 DMA 方式霍尔传感器接口。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

固定实现约束：先关闭CC1与CC1 DMA请求，再调用HAL_DMA_Abort_IT但忽略其返回值；随后条件式关闭CEN并返回HAL_OK。该函数体未直接将句柄State设回READY，不能用返回值证明DMA与软件状态全部恢复。

来源：[固定实现L452](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L452)。

### `HAL_TIMEx_OCN_Start`

```c
HAL_StatusTypeDef HAL_TIMEx_OCN_Start (TIM_HandleTypeDef * htim, uint32_t Channel);
```

启动TIM1 互补输出比较。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- 仅 TIM1 CH1、CH2、CH3 对应的 N 输出；没有 CH4N。

来源：[固定实现L508](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L508)。

### `HAL_TIMEx_OCN_Stop`

```c
HAL_StatusTypeDef HAL_TIMEx_OCN_Stop (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止TIM1 互补输出比较。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- 仅 TIM1 CH1、CH2、CH3 对应的 N 输出；没有 CH4N。

来源：[固定实现L543](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L543)。

### `HAL_TIMEx_OCN_Start_IT`

```c
HAL_StatusTypeDef HAL_TIMEx_OCN_Start_IT (TIM_HandleTypeDef * htim, uint32_t Channel);
```

以中断方式启动TIM1 互补输出比较。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- 仅 TIM1 CH1、CH2、CH3 对应的 N 输出；没有 CH4N。

来源：[固定实现L572](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L572)。

### `HAL_TIMEx_OCN_Stop_IT`

```c
HAL_StatusTypeDef HAL_TIMEx_OCN_Stop_IT (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止并关闭中断TIM1 互补输出比较。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- 仅 TIM1 CH1、CH2、CH3 对应的 N 输出；没有 CH4N。

固定实现约束：固定实现先关闭所选CCxIE，再关闭所选N输出。当全部CC1NE/CC2NE/CC3NE为0时关闭BIE，判断中不包含主输出CCxE；主输出仍工作时也可能失去刹车中断通知。此处是DIER中断门，不等同于关闭BDTR.BKE硬件刹车保护。所选CCxIE同样是主/N共享资源。

来源：[固定实现L638](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L638)。

### `HAL_TIMEx_OCN_Start_DMA`

```c
HAL_StatusTypeDef HAL_TIMEx_OCN_Start_DMA (TIM_HandleTypeDef * htim, uint32_t Channel, uint32_t * pData, uint16_t Length);
```

以 DMA 方式启动TIM1 互补输出比较。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`。
- `pData`：DMA 内存源缓冲区地址，比较/PWM 数据从内存写入 TIM；直到 DMA 停止前必须有效。
- `Length`：DMA 传输项数，非字节数；数据宽度由 DMA 配置决定。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。
- 仅 TIM1 CH1、CH2、CH3 对应的 N 输出；没有 CH4N。

来源：[固定实现L704](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L704)。

### `HAL_TIMEx_OCN_Stop_DMA`

```c
HAL_StatusTypeDef HAL_TIMEx_OCN_Stop_DMA (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止 DMA 方式TIM1 互补输出比较。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。
- 仅 TIM1 CH1、CH2、CH3 对应的 N 输出；没有 CH4N。

来源：[固定实现L822](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L822)。

### `HAL_TIMEx_PWMN_Start`

```c
HAL_StatusTypeDef HAL_TIMEx_PWMN_Start (TIM_HandleTypeDef * htim, uint32_t Channel);
```

启动TIM1 互补 PWM。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- 仅 TIM1 CH1、CH2、CH3 对应的 N 输出；没有 CH4N。

来源：[固定实现L917](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L917)。

### `HAL_TIMEx_PWMN_Stop`

```c
HAL_StatusTypeDef HAL_TIMEx_PWMN_Stop (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止TIM1 互补 PWM。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- 仅 TIM1 CH1、CH2、CH3 对应的 N 输出；没有 CH4N。

来源：[固定实现L951](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L951)。

### `HAL_TIMEx_PWMN_Start_IT`

```c
HAL_StatusTypeDef HAL_TIMEx_PWMN_Start_IT (TIM_HandleTypeDef * htim, uint32_t Channel);
```

以中断方式启动TIM1 互补 PWM。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- 仅 TIM1 CH1、CH2、CH3 对应的 N 输出；没有 CH4N。

来源：[固定实现L980](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L980)。

### `HAL_TIMEx_PWMN_Stop_IT`

```c
HAL_StatusTypeDef HAL_TIMEx_PWMN_Stop_IT (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止并关闭中断TIM1 互补 PWM。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- 仅 TIM1 CH1、CH2、CH3 对应的 N 输出；没有 CH4N。

固定实现约束：固定实现先关闭所选CCxIE，再关闭所选N输出。当全部CC1NE/CC2NE/CC3NE为0时关闭BIE，判断中不包含主输出CCxE；主输出仍工作时也可能失去刹车中断通知。此处是DIER中断门，不等同于关闭BDTR.BKE硬件刹车保护。所选CCxIE同样是主/N共享资源。

来源：[固定实现L1045](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1045)。

### `HAL_TIMEx_PWMN_Start_DMA`

```c
HAL_StatusTypeDef HAL_TIMEx_PWMN_Start_DMA (TIM_HandleTypeDef * htim, uint32_t Channel, uint32_t * pData, uint16_t Length);
```

以 DMA 方式启动TIM1 互补 PWM。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`。
- `pData`：DMA 内存源缓冲区地址，比较/PWM 数据从内存写入 TIM；直到 DMA 停止前必须有效。
- `Length`：DMA 传输项数，非字节数；数据宽度由 DMA 配置决定。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。
- 仅 TIM1 CH1、CH2、CH3 对应的 N 输出；没有 CH4N。

来源：[固定实现L1112](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1112)。

### `HAL_TIMEx_PWMN_Stop_DMA`

```c
HAL_StatusTypeDef HAL_TIMEx_PWMN_Stop_DMA (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止 DMA 方式TIM1 互补 PWM。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。
- 仅 TIM1 CH1、CH2、CH3 对应的 N 输出；没有 CH4N。

来源：[固定实现L1229](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1229)。

### `HAL_TIMEx_OnePulseN_Start`

```c
HAL_StatusTypeDef HAL_TIMEx_OnePulseN_Start (TIM_HandleTypeDef * htim, uint32_t OutputChannel);
```

启动TIM1 互补单脉冲。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `OutputChannel`：单脉冲输出通道，CH1 或 CH2；互补输出使用对应 N 路。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- 仅 TIM1 具有互补输出的单脉冲通道，按 CH1/CH2 单脉冲输入输出配对使用。

来源：[固定实现L1312](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1312)。

### `HAL_TIMEx_OnePulseN_Stop`

```c
HAL_StatusTypeDef HAL_TIMEx_OnePulseN_Stop (TIM_HandleTypeDef * htim, uint32_t OutputChannel);
```

停止TIM1 互补单脉冲。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `OutputChannel`：单脉冲输出通道，CH1 或 CH2；互补输出使用对应 N 路。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- 仅 TIM1 具有互补输出的单脉冲通道，按 CH1/CH2 单脉冲输入输出配对使用。

来源：[固定实现L1337](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1337)。

### `HAL_TIMEx_OnePulseN_Start_IT`

```c
HAL_StatusTypeDef HAL_TIMEx_OnePulseN_Start_IT (TIM_HandleTypeDef * htim, uint32_t OutputChannel);
```

以中断方式启动TIM1 互补单脉冲。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `OutputChannel`：单脉冲输出通道，CH1 或 CH2；互补输出使用对应 N 路。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- 仅 TIM1 具有互补输出的单脉冲通道，按 CH1/CH2 单脉冲输入输出配对使用。

固定实现约束：固定实现开启CC1IE和CC2IE，再启用所选N通道与MOE；函数体不设置BIE或CEN。不能把OCN/PWMN的Start_IT副作用直接推广到这个入口。

来源：[固定实现L1366](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1366)。

### `HAL_TIMEx_OnePulseN_Stop_IT`

```c
HAL_StatusTypeDef HAL_TIMEx_OnePulseN_Stop_IT (TIM_HandleTypeDef * htim, uint32_t OutputChannel);
```

停止并关闭中断TIM1 互补单脉冲。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `OutputChannel`：单脉冲输出通道，CH1 或 CH2；互补输出使用对应 N 路。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

- 仅 TIM1 具有互补输出的单脉冲通道，按 CH1/CH2 单脉冲输入输出配对使用。

固定实现约束：固定实现同时关闭CC1IE与CC2IE，再关闭所选N通道，并使用条件式MOE/CEN关闭宏。两路比较中断的其他使用方可能受到影响。

来源：[固定实现L1397](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1397)。

### `HAL_TIMEx_ConfigCommutEvent`

```c
HAL_StatusTypeDef HAL_TIMEx_ConfigCommutEvent (TIM_HandleTypeDef * htim, uint32_t InputTrigger, uint32_t CommutationSource);
```

配置 TIM1 换相更新来源，使 CCxE、CCxNE、OCxM 的预装载在 COM 事件时生效。

以下三个 ConfigCommutEvent 接口的 NONE/SOFTWARE 细节，除 UM1850 第544～545页外，还对照了 [ST 官方 HAL v1.1.4 实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1467-L1619) 与[同版本常量](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L650-L657)。该标签日期为2020-01-29，作为与文档年代相近的固定版本补证，不声称PDF指定了这个唯一软件版本。TIM_TS_NONE=0xFFFF是API哨兵值，不能直接当成SMCR.TS字段写入；此实现遇到NONE时保持原TS。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `InputTrigger`：TRGI 来源；ITR 实际连线取决于定时器实例，TIM_TS_NONE 表示本次不选择新的内部触发源，不能据此假定会清掉原 TS 字段。
  - 可用编码：`TIM_TS_ITR0`、`TIM_TS_ITR1`、`TIM_TS_ITR2`、`TIM_TS_ITR3`、`TIM_TS_NONE`。
- `CommutationSource`：换相来源；SOFTWARE 配置 CCUS=0，软件须另写 TIM_EGR.COMG 才产生软件换相事件；TRGI 配置 CCUS=1，除软件 COMG 外也允许所选 TRGI 上升沿产生换相。三个配置函数本身都不写 COMG，不因传入 SOFTWARE 而立即产生事件；仅 TIM1。
  - 可用编码：`TIM_COMMUTATION_TRGI`、`TIM_COMMUTATION_SOFTWARE`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

来源：[固定实现L1467](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1467)。

### `HAL_TIMEx_ConfigCommutEvent_IT`

```c
HAL_StatusTypeDef HAL_TIMEx_ConfigCommutEvent_IT (TIM_HandleTypeDef * htim, uint32_t InputTrigger, uint32_t CommutationSource);
```

配置 TIM1 换相更新来源并开放 COM 中断。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `InputTrigger`：TRGI 来源；ITR 实际连线取决于定时器实例，TIM_TS_NONE 表示本次不选择新的内部触发源，不能据此假定会清掉原 TS 字段。
  - 可用编码：`TIM_TS_ITR0`、`TIM_TS_ITR1`、`TIM_TS_ITR2`、`TIM_TS_ITR3`、`TIM_TS_NONE`。
- `CommutationSource`：换相来源；SOFTWARE 配置 CCUS=0，软件须另写 TIM_EGR.COMG 才产生软件换相事件；TRGI 配置 CCUS=1，除软件 COMG 外也允许所选 TRGI 上升沿产生换相。三个配置函数本身都不写 COMG，不因传入 SOFTWARE 而立即产生事件；仅 TIM1。
  - 可用编码：`TIM_COMMUTATION_TRGI`、`TIM_COMMUTATION_SOFTWARE`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

来源：[固定实现L1523](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1523)。

### `HAL_TIMEx_ConfigCommutEvent_DMA`

```c
HAL_StatusTypeDef HAL_TIMEx_ConfigCommutEvent_DMA (TIM_HandleTypeDef * htim, uint32_t InputTrigger, uint32_t CommutationSource);
```

配置 TIM1 换相 DMA 请求；该接口配置换相来源并使能 COMDE；原文“only COMDE”针对 DMA 部分，DMA 通道和传输本身仍须由应用配置。补证的v1.1.4实现还会通过 htim->hdma[TIM_DMA_ID_COMMUTATION] 安装完成、半完成和错误回调，所以调用前须先创建并关联有效DMA句柄；该接口不代替启动带源/目标地址与长度的DMA传输。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `InputTrigger`：TRGI 来源；ITR 实际连线取决于定时器实例，TIM_TS_NONE 表示本次不选择新的内部触发源，不能据此假定会清掉原 TS 字段。
  - 可用编码：`TIM_TS_ITR0`、`TIM_TS_ITR1`、`TIM_TS_ITR2`、`TIM_TS_ITR3`、`TIM_TS_NONE`。
- `CommutationSource`：换相来源；SOFTWARE 配置 CCUS=0，软件须另写 TIM_EGR.COMG 才产生软件换相事件；TRGI 配置 CCUS=1，除软件 COMG 外也允许所选 TRGI 上升沿产生换相。三个配置函数本身都不写 COMG，不因传入 SOFTWARE 而立即产生事件；仅 TIM1。
  - 可用编码：`TIM_COMMUTATION_TRGI`、`TIM_COMMUTATION_SOFTWARE`。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

固定实现约束：本函数会改写关联换相DMA句柄的完成、半完成、错误回调并开启COMDE，但不调用HAL_DMA_Start_IT。须先建立有效DMA句柄、Parent、传输配置及传输状态，不能仅凭配置函数HAL_OK判断DMA已开始。

来源：[固定实现L1580](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1580)。

### `HAL_TIMEx_MasterConfigSynchronization`

```c
HAL_StatusTypeDef HAL_TIMEx_MasterConfigSynchronization (TIM_HandleTypeDef * htim, TIM_MasterConfigTypeDef * sMasterConfig);
```

配置 TRGO 主触发输出和主从同步模式；核对 RM0008 中各定时器 ITR 实际连线。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `sMasterConfig`：原型所示配置结构指针；字段和合法组合见[TIM_MasterConfigTypeDef](HAL配置字段.md#tim_masterconfigtypedef)。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。

来源：[固定实现L1629](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1629)。

### `HAL_TIMEx_ConfigBreakDeadTime`

```c
HAL_StatusTypeDef HAL_TIMEx_ConfigBreakDeadTime (TIM_HandleTypeDef * htim, TIM_BreakDeadTimeConfigTypeDef * sBreakDeadTimeConfig);
```

配置 TIM1 的刹车、死区、锁定、OSSI/OSSR 和自动输出恢复；锁定前必须一次配好受保护字段。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。
- `sBreakDeadTimeConfig`：原型所示配置结构指针；字段和合法组合见[TIM_BreakDeadTimeConfigTypeDef](HAL配置字段.md#tim_breakdeadtimeconfigtypedef)。

返回：`HAL_StatusTypeDef` 状态码；HAL_OK 表示本接口报告成功，启动/停止是否已达到所需硬件状态还须符合对应实现契约，非 HAL_OK 应按具体失败路径处理。


- 刹车中断需另外用 `__HAL_TIM_ENABLE_IT(htim, TIM_IT_BREAK)` 并配置 NVIC；配置 BDTR 不等于已开放中断。源文所述 break2/system break 并非 C8 的第二路可配置硬件刹车功能。

来源：[固定实现L1687](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1687)。

### `HAL_TIMEx_CommutCallback`

```c
void HAL_TIMEx_CommutCallback (TIM_HandleTypeDef * htim);
```

TIM1 换相完成回调。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

来源：[固定实现L1765](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1765)。

### `HAL_TIMEx_CommutHalfCpltCallback`

```c
void HAL_TIMEx_CommutHalfCpltCallback (TIM_HandleTypeDef * htim);
```

TIM1 换相 DMA 半传输回调。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

来源：[固定实现L1779](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1779)。

### `HAL_TIMEx_BreakCallback`

```c
void HAL_TIMEx_BreakCallback (TIM_HandleTypeDef * htim);
```

TIM1 刹车事件回调；进入回调时硬件可能已经清除 MOE 并关闭输出。

- `htim`：TIM 句柄指针，本器件的 Instance 必须为 TIM1。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

来源：[固定实现L1794](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1794)。

### `HAL_TIMEx_HallSensor_GetState`

```c
HAL_TIM_StateTypeDef HAL_TIMEx_HallSensor_GetState (TIM_HandleTypeDef * htim);
```

返回句柄状态：霍尔传感器接口。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_TIM_StateTypeDef`（RESET/READY/BUSY/TIMEOUT/ERROR），是句柄软件状态。

来源：[固定实现L1827](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1827)。

### `TIMEx_DMACommutationCplt`

```c
void TIMEx_DMACommutationCplt (DMA_HandleTypeDef * hdma);
```

驱动内部换相 DMA 全传输回调。

- `hdma`：关联 DMA 句柄指针，其 Parent 应指向所属 TIM 句柄。

返回：无返回值。

固定实现约束：该固定实现先把所属TIM句柄State设为READY，再调用用户换相完成回调；没有在此停止输出或统一禁用DMA请求。

来源：[固定实现L1850](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1850)。

### `TIMEx_DMACommutationHalfCplt`

```c
void TIMEx_DMACommutationHalfCplt (DMA_HandleTypeDef * hdma);
```

驱动内部换相 DMA 半传输回调。

- `hdma`：关联 DMA 句柄指针，其 Parent 应指向所属 TIM 句柄。

返回：无返回值。

固定实现约束：该固定实现也把所属TIM句柄State设为READY，再调用用户半完成回调。半传输完成不代表剩余DMA已停止；READY不能用作释放缓冲区或重配置共享实例的唯一依据。

来源：[固定实现L1869](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim_ex.c#L1869)。

## 明确排除的原文接口

`HAL_TIMEx_RemapConfig(TIM_HandleTypeDef *htim, uint32_t Remap)` 在原章中有列出，处理特定器件的 TIM2 内部触发/PTP 重映射能力；STM32F103C8T6 不具备该互联型功能，故不列为可调用接口。C8 的 TIM 引脚重映射应使用 AFIO 对应接口，不能用同名“Remap”推定二者相同。


[返回定时器主题](../../知识库/06_定时器PWM与同步.md) · [图形关系与来源](图形关系与来源.md)
