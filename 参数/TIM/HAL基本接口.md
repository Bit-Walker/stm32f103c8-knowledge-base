# TIM HAL 基本接口

参数结构见[HAL结构](HAL配置字段.md)，初始化与状态边界见[HAL初始化](HAL初始化边界.md)，启动/停止及DMA约束见[生命周期](HAL生命周期与DMA.md)。原型核验和字段说明不代替板上验证，返回HAL_OK仅代表对应实现报告成功。


以下保留既有资料的100个HAL函数入口，原型已逐项匹配固定de129f1头文件。HAL/LL枚举不可混传；尚未逐一复核全部运行状态组合。动态回调注册等补充入口见生命周期说明，不把100项误称为驱动全部导出符号。

## 本页导航

- [基本计数](#基本计数)
- [输出比较](#输出比较)
- [PWM](#pwm)
- [输入捕获](#输入捕获)
- [单脉冲](#单脉冲)
- [编码器](#编码器)
- [中断分发](#中断分发)
- [通道与时钟配置](#通道与时钟配置)
- [DMA burst](#dma-burst)
- [软件事件与捕获读数](#软件事件与捕获读数)
- [用户回调](#用户回调)
- [句柄状态查询](#句柄状态查询)
- [驱动内部辅助函数](#驱动内部辅助函数)

## 共同约定

- `HAL_StatusTypeDef` 表示本次接口调用的状态；HAL_OK 表示接口报告成功。启动、停止是否已达到所需硬件状态，按该接口的固定实现和硬件条件判断；其他返回值按实际失败路径处理。
- 中心对齐与边沿对齐切换前，先处理计数器状态及必要复位。DeInit 的实际停机和外设复位效果取决于通道状态及 MSP 实现；Init 后按用途调用对应 Start。详见[初始化与复位](HAL初始化边界.md)。

- `HAL_TIM_StateTypeDef` 的 RESET、READY、BUSY、TIMEOUT、ERROR 描述句柄软件状态；它们不直接测量引脚输出或 DMA 硬件是否静止。


## 基本计数

### `HAL_TIM_Base_Init`

```c
HAL_StatusTypeDef HAL_TIM_Base_Init (TIM_HandleTypeDef * htim);
```

初始化基本时基与句柄。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。


来源：[固定头文件L1768](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1768)。

补充核对：具体动作包括TIM_Base_SetConfig发UG；函数没有先关闭已有CEN/输出或隔离TRGO。RESET路径才执行相应MSP初始化。见[初始化约束](HAL初始化边界.md)。

### `HAL_TIM_Base_DeInit`

```c
HAL_StatusTypeDef HAL_TIM_Base_DeInit (TIM_HandleTypeDef * htim);
```

释放基本时基配置并调用相应 MSP 释放函数。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1769](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1769)。

补充核对：固定实现经条件式__HAL_TIM_DISABLE尝试清CEN，然后调用MSP释放并置软件RESET。默认弱MSP不实施RCC复位；其他通道仍使能时CEN可被保留，不能从名称推断寄存器已经恢复复位值。

### `HAL_TIM_Base_MspInit`

```c
void HAL_TIM_Base_MspInit (TIM_HandleTypeDef * htim);
```

用户提供的基本时基底层资源初始化回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定头文件L1770](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1770)。

### `HAL_TIM_Base_MspDeInit`

```c
void HAL_TIM_Base_MspDeInit (TIM_HandleTypeDef * htim);
```

用户提供的基本时基底层资源释放回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定头文件L1771](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1771)。

### `HAL_TIM_Base_Start`

```c
HAL_StatusTypeDef HAL_TIM_Base_Start (TIM_HandleTypeDef * htim);
```

启动基本时基。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1773](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1773)。

### `HAL_TIM_Base_Stop`

```c
HAL_StatusTypeDef HAL_TIM_Base_Stop (TIM_HandleTypeDef * htim);
```

停止基本时基。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1774](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1774)。

### `HAL_TIM_Base_Start_IT`

```c
HAL_StatusTypeDef HAL_TIM_Base_Start_IT (TIM_HandleTypeDef * htim);
```

启动基本时基并开放相关中断。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1776](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1776)。

### `HAL_TIM_Base_Stop_IT`

```c
HAL_StatusTypeDef HAL_TIM_Base_Stop_IT (TIM_HandleTypeDef * htim);
```

停止基本时基并关闭相关中断。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1777](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1777)。

### `HAL_TIM_Base_Start_DMA`

```c
HAL_StatusTypeDef HAL_TIM_Base_Start_DMA (TIM_HandleTypeDef * htim, uint32_t * pData, uint16_t Length);
```

启动基本时基的 DMA 传输。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `pData`：DMA 内存源缓冲区地址，数据从内存写入 TIM；直到 DMA 停止前必须有效。
- `Length`：DMA 传输项数，非字节数；数据宽度由 DMA 配置决定。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1779](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1779)。

### `HAL_TIM_Base_Stop_DMA`

```c
HAL_StatusTypeDef HAL_TIM_Base_Stop_DMA (TIM_HandleTypeDef * htim);
```

停止基本时基的 DMA 传输。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1780](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1780)。

## 输出比较

### `HAL_TIM_OC_Init`

```c
HAL_StatusTypeDef HAL_TIM_OC_Init (TIM_HandleTypeDef * htim);
```

初始化输出比较与句柄。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。


来源：[固定头文件L1790](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1790)。

### `HAL_TIM_OC_DeInit`

```c
HAL_StatusTypeDef HAL_TIM_OC_DeInit (TIM_HandleTypeDef * htim);
```

释放输出比较配置并调用相应 MSP 释放函数。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1791](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1791)。

### `HAL_TIM_OC_MspInit`

```c
void HAL_TIM_OC_MspInit (TIM_HandleTypeDef * htim);
```

用户提供的输出比较底层资源初始化回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定头文件L1792](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1792)。

### `HAL_TIM_OC_MspDeInit`

```c
void HAL_TIM_OC_MspDeInit (TIM_HandleTypeDef * htim);
```

用户提供的输出比较底层资源释放回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定头文件L1793](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1793)。

### `HAL_TIM_OC_Start`

```c
HAL_StatusTypeDef HAL_TIM_OC_Start (TIM_HandleTypeDef * htim, uint32_t Channel);
```

启动输出比较。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1795](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1795)。

### `HAL_TIM_OC_Stop`

```c
HAL_StatusTypeDef HAL_TIM_OC_Stop (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止输出比较。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1796](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1796)。

### `HAL_TIM_OC_Start_IT`

```c
HAL_StatusTypeDef HAL_TIM_OC_Start_IT (TIM_HandleTypeDef * htim, uint32_t Channel);
```

启动输出比较并开放相关中断。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1798](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1798)。

### `HAL_TIM_OC_Stop_IT`

```c
HAL_StatusTypeDef HAL_TIM_OC_Stop_IT (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止输出比较并关闭相关中断。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1799](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1799)。

### `HAL_TIM_OC_Start_DMA`

```c
HAL_StatusTypeDef HAL_TIM_OC_Start_DMA (TIM_HandleTypeDef * htim, uint32_t Channel, uint32_t * pData, uint16_t Length);
```

启动输出比较的 DMA 传输。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。
- `pData`：DMA 内存源缓冲区地址，数据从内存写入 TIM；直到 DMA 停止前必须有效。
- `Length`：DMA 传输项数，非字节数；数据宽度由 DMA 配置决定。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1801](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1801)。

### `HAL_TIM_OC_Stop_DMA`

```c
HAL_StatusTypeDef HAL_TIM_OC_Stop_DMA (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止输出比较的 DMA 传输。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1802](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1802)。

## PWM

### `HAL_TIM_PWM_Init`

```c
HAL_StatusTypeDef HAL_TIM_PWM_Init (TIM_HandleTypeDef * htim);
```

初始化PWM 输出与句柄。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。


来源：[固定头文件L1812](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1812)。

### `HAL_TIM_PWM_DeInit`

```c
HAL_StatusTypeDef HAL_TIM_PWM_DeInit (TIM_HandleTypeDef * htim);
```

释放PWM 输出配置并调用相应 MSP 释放函数。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1813](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1813)。

### `HAL_TIM_PWM_MspInit`

```c
void HAL_TIM_PWM_MspInit (TIM_HandleTypeDef * htim);
```

用户提供的PWM 输出底层资源初始化回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定头文件L1814](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1814)。

### `HAL_TIM_PWM_MspDeInit`

```c
void HAL_TIM_PWM_MspDeInit (TIM_HandleTypeDef * htim);
```

用户提供的PWM 输出底层资源释放回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定头文件L1815](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1815)。

### `HAL_TIM_PWM_Start`

```c
HAL_StatusTypeDef HAL_TIM_PWM_Start (TIM_HandleTypeDef * htim, uint32_t Channel);
```

启动PWM 输出。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1817](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1817)。

### `HAL_TIM_PWM_Stop`

```c
HAL_StatusTypeDef HAL_TIM_PWM_Stop (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止PWM 输出。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1818](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1818)。

### `HAL_TIM_PWM_Start_IT`

```c
HAL_StatusTypeDef HAL_TIM_PWM_Start_IT (TIM_HandleTypeDef * htim, uint32_t Channel);
```

启动PWM 输出并开放相关中断。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1820](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1820)。

### `HAL_TIM_PWM_Stop_IT`

```c
HAL_StatusTypeDef HAL_TIM_PWM_Stop_IT (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止PWM 输出并关闭相关中断。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1821](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1821)。

### `HAL_TIM_PWM_Start_DMA`

```c
HAL_StatusTypeDef HAL_TIM_PWM_Start_DMA (TIM_HandleTypeDef * htim, uint32_t Channel, uint32_t * pData, uint16_t Length);
```

启动PWM 输出的 DMA 传输。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。
- `pData`：DMA 内存源缓冲区地址，数据从内存写入 TIM；直到 DMA 停止前必须有效。
- `Length`：DMA 传输项数，非字节数；数据宽度由 DMA 配置决定。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1823](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1823)。

### `HAL_TIM_PWM_Stop_DMA`

```c
HAL_StatusTypeDef HAL_TIM_PWM_Stop_DMA (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止PWM 输出的 DMA 传输。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1824](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1824)。

## 输入捕获

### `HAL_TIM_IC_Init`

```c
HAL_StatusTypeDef HAL_TIM_IC_Init (TIM_HandleTypeDef * htim);
```

初始化输入捕获与句柄。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。


来源：[固定头文件L1834](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1834)。

### `HAL_TIM_IC_DeInit`

```c
HAL_StatusTypeDef HAL_TIM_IC_DeInit (TIM_HandleTypeDef * htim);
```

释放输入捕获配置并调用相应 MSP 释放函数。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1835](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1835)。

### `HAL_TIM_IC_MspInit`

```c
void HAL_TIM_IC_MspInit (TIM_HandleTypeDef * htim);
```

用户提供的输入捕获底层资源初始化回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定头文件L1836](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1836)。

### `HAL_TIM_IC_MspDeInit`

```c
void HAL_TIM_IC_MspDeInit (TIM_HandleTypeDef * htim);
```

用户提供的输入捕获底层资源释放回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定头文件L1837](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1837)。

### `HAL_TIM_IC_Start`

```c
HAL_StatusTypeDef HAL_TIM_IC_Start (TIM_HandleTypeDef * htim, uint32_t Channel);
```

启动输入捕获。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1839](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1839)。

### `HAL_TIM_IC_Stop`

```c
HAL_StatusTypeDef HAL_TIM_IC_Stop (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止输入捕获。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1840](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1840)。

### `HAL_TIM_IC_Start_IT`

```c
HAL_StatusTypeDef HAL_TIM_IC_Start_IT (TIM_HandleTypeDef * htim, uint32_t Channel);
```

启动输入捕获并开放相关中断。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1842](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1842)。

### `HAL_TIM_IC_Stop_IT`

```c
HAL_StatusTypeDef HAL_TIM_IC_Stop_IT (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止输入捕获并关闭相关中断。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1843](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1843)。

### `HAL_TIM_IC_Start_DMA`

```c
HAL_StatusTypeDef HAL_TIM_IC_Start_DMA (TIM_HandleTypeDef * htim, uint32_t Channel, uint32_t * pData, uint16_t Length);
```

启动输入捕获的 DMA 传输。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。
- `pData`：DMA 内存接收缓冲区地址，捕获值从 TIM 写入内存；直到 DMA 停止前必须有效。
- `Length`：DMA 传输项数，非字节数；数据宽度由 DMA 配置决定。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1845](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1845)。

### `HAL_TIM_IC_Stop_DMA`

```c
HAL_StatusTypeDef HAL_TIM_IC_Stop_DMA (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止输入捕获的 DMA 传输。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1846](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1846)。

## 单脉冲

### `HAL_TIM_OnePulse_Init`

```c
HAL_StatusTypeDef HAL_TIM_OnePulse_Init (TIM_HandleTypeDef * htim, uint32_t OnePulseMode);
```

初始化单脉冲与句柄。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `OnePulseMode`：单脉冲单次或重复方式。
  - 可用编码：`TIM_OPMODE_SINGLE`、`TIM_OPMODE_REPETITIVE`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。


来源：[固定头文件L1856](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1856)。

### `HAL_TIM_OnePulse_DeInit`

```c
HAL_StatusTypeDef HAL_TIM_OnePulse_DeInit (TIM_HandleTypeDef * htim);
```

释放单脉冲配置并调用相应 MSP 释放函数。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1857](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1857)。

### `HAL_TIM_OnePulse_MspInit`

```c
void HAL_TIM_OnePulse_MspInit (TIM_HandleTypeDef * htim);
```

用户提供的单脉冲底层资源初始化回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定头文件L1858](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1858)。

### `HAL_TIM_OnePulse_MspDeInit`

```c
void HAL_TIM_OnePulse_MspDeInit (TIM_HandleTypeDef * htim);
```

用户提供的单脉冲底层资源释放回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定头文件L1859](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1859)。

### `HAL_TIM_OnePulse_Start`

```c
HAL_StatusTypeDef HAL_TIM_OnePulse_Start (TIM_HandleTypeDef * htim, uint32_t OutputChannel);
```

开放已配置的单脉冲通道，等待输入触发；本接口不主动置 CEN，不能把返回成功当成脉冲已经发出。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `OutputChannel`：原文列 CH1 或 CH2；但所核对的 v1.1.4 与固定新快照在本接口中忽略此参数，CH1/CH2 同时启停。真正的输入/输出分工由 OnePulse_ConfigChannel 配置，不是在这里改选；互补输出另用 OnePulseN 接口。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1861](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1861)。

### `HAL_TIM_OnePulse_Stop`

```c
HAL_StatusTypeDef HAL_TIM_OnePulse_Stop (TIM_HandleTypeDef * htim, uint32_t OutputChannel);
```

停止单脉冲。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `OutputChannel`：原文列 CH1 或 CH2；但所核对的 v1.1.4 与固定新快照在本接口中忽略此参数，CH1/CH2 同时启停。真正的输入/输出分工由 OnePulse_ConfigChannel 配置，不是在这里改选；互补输出另用 OnePulseN 接口。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1862](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1862)。

### `HAL_TIM_OnePulse_Start_IT`

```c
HAL_StatusTypeDef HAL_TIM_OnePulse_Start_IT (TIM_HandleTypeDef * htim, uint32_t OutputChannel);
```

开放已配置的单脉冲通道及 CC1/CC2 中断，等待输入触发；本接口不主动置 CEN，不能把返回成功当成脉冲已经发出。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `OutputChannel`：原文列 CH1 或 CH2；但所核对的 v1.1.4 与固定新快照在本接口中忽略此参数，CH1/CH2 同时启停。真正的输入/输出分工由 OnePulse_ConfigChannel 配置，不是在这里改选；互补输出另用 OnePulseN 接口。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1864](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1864)。

### `HAL_TIM_OnePulse_Stop_IT`

```c
HAL_StatusTypeDef HAL_TIM_OnePulse_Stop_IT (TIM_HandleTypeDef * htim, uint32_t OutputChannel);
```

停止单脉冲并关闭相关中断。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `OutputChannel`：原文列 CH1 或 CH2；但所核对的 v1.1.4 与固定新快照在本接口中忽略此参数，CH1/CH2 同时启停。真正的输入/输出分工由 OnePulse_ConfigChannel 配置，不是在这里改选；互补输出另用 OnePulseN 接口。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1865](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1865)。

## 编码器

### `HAL_TIM_Encoder_Init`

```c
HAL_StatusTypeDef HAL_TIM_Encoder_Init (TIM_HandleTypeDef * htim, TIM_Encoder_InitTypeDef * sConfig);
```

初始化编码器接口与句柄。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `sConfig`：原型所示配置结构指针；字段和合法组合见本章结构说明。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。


来源：[固定头文件L1875](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1875)。

### `HAL_TIM_Encoder_DeInit`

```c
HAL_StatusTypeDef HAL_TIM_Encoder_DeInit (TIM_HandleTypeDef * htim);
```

释放编码器接口配置并调用相应 MSP 释放函数。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1876](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1876)。

### `HAL_TIM_Encoder_MspInit`

```c
void HAL_TIM_Encoder_MspInit (TIM_HandleTypeDef * htim);
```

用户提供的编码器接口底层资源初始化回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定头文件L1877](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1877)。

### `HAL_TIM_Encoder_MspDeInit`

```c
void HAL_TIM_Encoder_MspDeInit (TIM_HandleTypeDef * htim);
```

用户提供的编码器接口底层资源释放回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定头文件L1878](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1878)。

### `HAL_TIM_Encoder_Start`

```c
HAL_StatusTypeDef HAL_TIM_Encoder_Start (TIM_HandleTypeDef * htim, uint32_t Channel);
```

启动编码器接口。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_ALL`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1880](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1880)。

### `HAL_TIM_Encoder_Stop`

```c
HAL_StatusTypeDef HAL_TIM_Encoder_Stop (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止编码器接口。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_ALL`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1881](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1881)。

### `HAL_TIM_Encoder_Start_IT`

```c
HAL_StatusTypeDef HAL_TIM_Encoder_Start_IT (TIM_HandleTypeDef * htim, uint32_t Channel);
```

启动编码器接口并开放相关中断。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_ALL`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1883](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1883)。

### `HAL_TIM_Encoder_Stop_IT`

```c
HAL_StatusTypeDef HAL_TIM_Encoder_Stop_IT (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止编码器接口并关闭相关中断。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_ALL`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1884](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1884)。

### `HAL_TIM_Encoder_Start_DMA`

```c
HAL_StatusTypeDef HAL_TIM_Encoder_Start_DMA (TIM_HandleTypeDef * htim, uint32_t Channel, uint32_t * pData1, uint32_t * pData2, uint16_t Length);
```

启动编码器接口的 DMA 传输。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_ALL`。
- `pData1`：编码器通道 1 捕获 DMA 缓冲区。
- `pData2`：编码器通道 2 捕获 DMA 缓冲区。
- `Length`：DMA 传输项数，非字节数；数据宽度由 DMA 配置决定。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1886](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1886)。

C8请求连线约束：TIM3_CH2没有独立DMA1映射，不能把标准CC1/CC2双请求DMA流程原样套到TIM3；软件启动返回值不能补足缺失的物理请求。TIM1_CH2连线又存在图50与表78差异，详见[硬件映射](硬件参数表.md#tim1-dma1请求连线)。

### `HAL_TIM_Encoder_Stop_DMA`

```c
HAL_StatusTypeDef HAL_TIM_Encoder_Stop_DMA (TIM_HandleTypeDef * htim, uint32_t Channel);
```

停止编码器接口的 DMA 传输。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_ALL`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1888](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1888)。

## 中断分发

### `HAL_TIM_IRQHandler`

```c
void HAL_TIM_IRQHandler (TIM_HandleTypeDef * htim);
```

处理 TIM 的更新、捕获比较、触发、换相和刹车中断；按标志和使能位分发回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

来源：[固定头文件L1898](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1898)。

## 通道与时钟配置

### `HAL_TIM_OC_ConfigChannel`

```c
HAL_StatusTypeDef HAL_TIM_OC_ConfigChannel (TIM_HandleTypeDef * htim, TIM_OC_InitTypeDef * sConfig, uint32_t Channel);
```

按 TIM_OC_InitTypeDef 配置指定输出比较通道。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `sConfig`：原型所示配置结构指针；字段和合法组合见本章结构说明。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1908](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1908)。

### `HAL_TIM_PWM_ConfigChannel`

```c
HAL_StatusTypeDef HAL_TIM_PWM_ConfigChannel (TIM_HandleTypeDef * htim, TIM_OC_InitTypeDef * sConfig, uint32_t Channel);
```

按 TIM_OC_InitTypeDef 配置指定 PWM 通道及比较值。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `sConfig`：原型所示配置结构指针；字段和合法组合见本章结构说明。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1909](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1909)。

### `HAL_TIM_IC_ConfigChannel`

```c
HAL_StatusTypeDef HAL_TIM_IC_ConfigChannel (TIM_HandleTypeDef * htim, TIM_IC_InitTypeDef * sConfig, uint32_t Channel);
```

按 TIM_IC_InitTypeDef 配置指定输入捕获通道。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `sConfig`：原型所示配置结构指针；字段和合法组合见本章结构说明。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1910](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1910)。

### `HAL_TIM_OnePulse_ConfigChannel`

```c
HAL_StatusTypeDef HAL_TIM_OnePulse_ConfigChannel (TIM_HandleTypeDef * htim, TIM_OnePulse_InitTypeDef * sConfig, uint32_t OutputChannel, uint32_t InputChannel);
```

配置单脉冲的输出通道和触发输入通道；二者使用 CH1/CH2 的配对路径。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `sConfig`：原型所示配置结构指针；字段和合法组合见本章结构说明。
- `OutputChannel`：单脉冲输出所对应的基本通道，只传 TIM_CHANNEL_1 或 TIM_CHANNEL_2；另一通道作为输入。即使用 TIM1 的互补输出，此配置接口仍传 CH1/CH2 编码，随后由 HAL_TIMEx_OnePulseN_Start 等扩展接口开放对应 N 输出，不存在这里可传入的 CH1N/CH2N 选择枚举。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`。
- `InputChannel`：单脉冲触发输入通道，与输出通道配对选 CH1/CH2。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。


- 需要最短触发响应时，可用 `__HAL_TIM_ENABLE_OCxFAST`，在 PWM1/PWM2 模式下让触发边沿直接作用于输出，见后文快速模式的3/5周期约束。

来源：[固定头文件L1911](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1911)。

### `HAL_TIM_ConfigOCrefClear`

```c
HAL_StatusTypeDef HAL_TIM_ConfigOCrefClear (TIM_HandleTypeDef * htim, TIM_ClearInputConfigTypeDef * sClearInputConfig, uint32_t Channel);
```

配置外部信号清除指定通道 OCREF 的功能，适用于输出比较或 PWM。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `sClearInputConfig`：原型所示配置结构指针；字段和合法组合见本章结构说明。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1913](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1913)。

### `HAL_TIM_ConfigClockSource`

```c
HAL_StatusTypeDef HAL_TIM_ConfigClockSource (TIM_HandleTypeDef * htim, TIM_ClockConfigTypeDef * sClockSourceConfig);
```

配置计数器内部或外部时钟，必须在 Start 之前完成。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `sClockSourceConfig`：原型所示配置结构指针；字段和合法组合见本章结构说明。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1915](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1915)。

### `HAL_TIM_ConfigTI1Input`

```c
HAL_StatusTypeDef HAL_TIM_ConfigTI1Input (TIM_HandleTypeDef * htim, uint32_t TI1_Selection);
```

选择 TI1 来自 CH1 本身，或来自 CH1、CH2、CH3 的异或组合。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `TI1_Selection`：TI1 直接来自 CH1 或由 CH1–CH3 异或。
  - 可用编码：`TIM_TI1SELECTION_CH1`、`TIM_TI1SELECTION_XORCOMBINATION`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1916](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1916)。

### `HAL_TIM_SlaveConfigSynchro`

```c
HAL_StatusTypeDef HAL_TIM_SlaveConfigSynchro (TIM_HandleTypeDef * htim, TIM_SlaveConfigTypeDef * sSlaveConfig);
```

配置从模式、触发输入及其极性、预分频和滤波。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `sSlaveConfig`：原型所示配置结构指针；字段和合法组合见本章结构说明。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1917](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1917)。

### `HAL_TIM_SlaveConfigSynchro_IT`

```c
HAL_StatusTypeDef HAL_TIM_SlaveConfigSynchro_IT (TIM_HandleTypeDef * htim, TIM_SlaveConfigTypeDef * sSlaveConfig);
```

配置从模式同步，同时开放触发中断。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `sSlaveConfig`：原型所示配置结构指针；字段和合法组合见本章结构说明。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1918](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1918)。

## DMA burst

### `HAL_TIM_DMABurst_WriteStart`

```c
HAL_StatusTypeDef HAL_TIM_DMABurst_WriteStart (TIM_HandleTypeDef * htim, uint32_t BurstBaseAddress, uint32_t BurstRequestSrc, uint32_t * BurstBuffer, uint32_t BurstLength);
```

配置从内存经 DMAR 向连续 TIM 寄存器传输的 DMA 突发；BurstLength 解码得到的突发传输项数须与本次 DMA 数据项数一致；不能把 BurstLength 的位域编码数值直接与 CNDTR 或数组长度比较。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `BurstBaseAddress`：DMA 突发起始寄存器编码，非绝对内存地址。
  - 可用编码：`TIM_DMABASE_CR1`、`TIM_DMABASE_CR2`、`TIM_DMABASE_SMCR`、`TIM_DMABASE_DIER`、`TIM_DMABASE_SR`、`TIM_DMABASE_EGR`、`TIM_DMABASE_CCMR1`、`TIM_DMABASE_CCMR2`、`TIM_DMABASE_CCER`、`TIM_DMABASE_CNT`、`TIM_DMABASE_PSC`、`TIM_DMABASE_ARR`、`TIM_DMABASE_RCR`、`TIM_DMABASE_CCR1`、`TIM_DMABASE_CCR2`、`TIM_DMABASE_CCR3`、`TIM_DMABASE_CCR4`、`TIM_DMABASE_BDTR`。
- `BurstRequestSrc`：单个更新、CC、COM或触发请求源；本接口不接受将多个TIM_DMA_*按位或，COM仅TIM1。
  - 可用编码：`TIM_DMA_UPDATE`、`TIM_DMA_CC1`、`TIM_DMA_CC2`、`TIM_DMA_CC3`、`TIM_DMA_CC4`、`TIM_DMA_COM`、`TIM_DMA_TRIGGER`。
- `BurstBuffer`：内存源缓冲区，由 DMA 读取后经 DMAR 写入连续定时器寄存器；直到 DMA 停止前须保持内容及地址有效。
- `BurstLength`：DMA 突发长度编码，TIM_DMABURSTLENGTH_1TRANSFER 至 TIM_DMABURSTLENGTH_18TRANSFERS；1–18次寄存器传输，不得当作未经编码的任意整数。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1919](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1919)。


配套Start的单项长度编码0不代表零项，不能依赖TIM层NULL检查确保缓冲合法。组合请求以及Stop的错误传播在不同快照间有差异，见[DMA burst实现边界](HAL生命周期与DMA.md#dma-burst-请求选择空指针检查与停止差异)。
### `HAL_TIM_DMABurst_WriteStop`

```c
HAL_StatusTypeDef HAL_TIM_DMABurst_WriteStop (TIM_HandleTypeDef * htim, uint32_t BurstRequestSrc);
```

停止所选请求源的 TIM DMA 突发写入。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `BurstRequestSrc`：单个更新、CC、COM或触发请求源；本接口不接受将多个TIM_DMA_*按位或，COM仅TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1921](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1921)。


配套Start的单项长度编码0不代表零项，不能依赖TIM层NULL检查确保缓冲合法。组合请求以及Stop的错误传播在不同快照间有差异，见[DMA burst实现边界](HAL生命周期与DMA.md#dma-burst-请求选择空指针检查与停止差异)。
### `HAL_TIM_DMABurst_ReadStart`

```c
HAL_StatusTypeDef HAL_TIM_DMABurst_ReadStart (TIM_HandleTypeDef * htim, uint32_t BurstBaseAddress, uint32_t BurstRequestSrc, uint32_t * BurstBuffer, uint32_t BurstLength);
```

配置从连续 TIM 寄存器经 DMAR 读入内存的 DMA 突发；BurstLength 解码得到的突发传输项数须与本次 DMA 数据项数一致；不能把 BurstLength 的位域编码数值直接与 CNDTR 或数组长度比较。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `BurstBaseAddress`：DMA 突发起始寄存器编码，非绝对内存地址。
  - 可用编码：`TIM_DMABASE_CR1`、`TIM_DMABASE_CR2`、`TIM_DMABASE_SMCR`、`TIM_DMABASE_DIER`、`TIM_DMABASE_SR`、`TIM_DMABASE_EGR`、`TIM_DMABASE_CCMR1`、`TIM_DMABASE_CCMR2`、`TIM_DMABASE_CCER`、`TIM_DMABASE_CNT`、`TIM_DMABASE_PSC`、`TIM_DMABASE_ARR`、`TIM_DMABASE_RCR`、`TIM_DMABASE_CCR1`、`TIM_DMABASE_CCR2`、`TIM_DMABASE_CCR3`、`TIM_DMABASE_CCR4`、`TIM_DMABASE_BDTR`。
- `BurstRequestSrc`：单个更新、CC、COM或触发请求源；本接口不接受将多个TIM_DMA_*按位或，COM仅TIM1。
  - 可用编码：`TIM_DMA_UPDATE`、`TIM_DMA_CC1`、`TIM_DMA_CC2`、`TIM_DMA_CC3`、`TIM_DMA_CC4`、`TIM_DMA_COM`、`TIM_DMA_TRIGGER`。
- `BurstBuffer`：内存目标缓冲区，由 DMA 将连续定时器寄存器数据经 DMAR 写入；直到 DMA 停止前须保持地址和容量有效。
- `BurstLength`：DMA 突发长度编码，TIM_DMABURSTLENGTH_1TRANSFER 至 TIM_DMABURSTLENGTH_18TRANSFERS；1–18次寄存器传输，不得当作未经编码的任意整数。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1922](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1922)。


配套Start的单项长度编码0不代表零项，不能依赖TIM层NULL检查确保缓冲合法。组合请求以及Stop的错误传播在不同快照间有差异，见[DMA burst实现边界](HAL生命周期与DMA.md#dma-burst-请求选择空指针检查与停止差异)。
### `HAL_TIM_DMABurst_ReadStop`

```c
HAL_StatusTypeDef HAL_TIM_DMABurst_ReadStop (TIM_HandleTypeDef * htim, uint32_t BurstRequestSrc);
```

停止所选请求源的 TIM DMA 突发读取。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `BurstRequestSrc`：单个更新、CC、COM或触发请求源；本接口不接受将多个TIM_DMA_*按位或，COM仅TIM1。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

- DMA 缓冲区与关联句柄必须持续有效；单次/循环由 DMA 初始化决定，停机顺序应避免 DMA 仍访问已释放内存。

来源：[固定头文件L1924](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1924)。


配套Start的单项长度编码0不代表零项，不能依赖TIM层NULL检查确保缓冲合法。组合请求以及Stop的错误传播在不同快照间有差异，见[DMA burst实现边界](HAL生命周期与DMA.md#dma-burst-请求选择空指针检查与停止差异)。
## 软件事件与捕获读数

### `HAL_TIM_GenerateEvent`

```c
HAL_StatusTypeDef HAL_TIM_GenerateEvent (TIM_HandleTypeDef * htim, uint32_t EventSource);
```

通过 EGR 产生指定软件事件；COM、BREAK 在 C8 仅适用于 TIM1。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `EventSource`：EGR 软件事件位组合；COM/BREAK 仅 TIM1。
  - 可用编码：`TIM_EVENTSOURCE_UPDATE`、`TIM_EVENTSOURCE_CC1`、`TIM_EVENTSOURCE_CC2`、`TIM_EVENTSOURCE_CC3`、`TIM_EVENTSOURCE_CC4`、`TIM_EVENTSOURCE_COM`、`TIM_EVENTSOURCE_TRIGGER`、`TIM_EVENTSOURCE_BREAK`。

返回：`HAL_StatusTypeDef`，含义见[共同约定](#共同约定)。

来源：[固定头文件L1925](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1925)。

### `HAL_TIM_ReadCapturedValue`

```c
uint32_t HAL_TIM_ReadCapturedValue (TIM_HandleTypeDef * htim, uint32_t Channel);
```

读取指定通道 CCR 中的捕获值；计数器分辨率由 TIM 时钟和 PSC 决定。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。

返回：`uint32_t`，具体数值/位域含义见上方功能说明；Get 类不表示操作成功状态。

来源：[固定头文件L1926](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1926)。

## 用户回调

### `HAL_TIM_PeriodElapsedCallback`

```c
void HAL_TIM_PeriodElapsedCallback (TIM_HandleTypeDef * htim);
```

更新事件或时基 DMA 完成回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

来源：[固定头文件L1936](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1936)。

### `HAL_TIM_PeriodElapsedHalfCpltCallback`

```c
void HAL_TIM_PeriodElapsedHalfCpltCallback (TIM_HandleTypeDef * htim);
```

时基 DMA 半传输回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

来源：[固定头文件L1937](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1937)。

### `HAL_TIM_OC_DelayElapsedCallback`

```c
void HAL_TIM_OC_DelayElapsedCallback (TIM_HandleTypeDef * htim);
```

输出比较事件回调，通过 htim->Channel 判断活动通道。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

来源：[固定头文件L1938](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1938)。

### `HAL_TIM_IC_CaptureCallback`

```c
void HAL_TIM_IC_CaptureCallback (TIM_HandleTypeDef * htim);
```

输入捕获事件或捕获 DMA 完成回调，通过活动通道区分来源。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

来源：[固定头文件L1939](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1939)。

### `HAL_TIM_IC_CaptureHalfCpltCallback`

```c
void HAL_TIM_IC_CaptureHalfCpltCallback (TIM_HandleTypeDef * htim);
```

输入捕获 DMA 半传输回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

来源：[固定头文件L1940](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1940)。

### `HAL_TIM_PWM_PulseFinishedCallback`

```c
void HAL_TIM_PWM_PulseFinishedCallback (TIM_HandleTypeDef * htim);
```

PWM 比较事件或 PWM DMA 完成回调；不把回调次数等同于整个 PWM 周期数。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

来源：[固定头文件L1941](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1941)。

### `HAL_TIM_PWM_PulseFinishedHalfCpltCallback`

```c
void HAL_TIM_PWM_PulseFinishedHalfCpltCallback (TIM_HandleTypeDef * htim);
```

PWM DMA 半传输回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

来源：[固定头文件L1942](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1942)。

### `HAL_TIM_TriggerCallback`

```c
void HAL_TIM_TriggerCallback (TIM_HandleTypeDef * htim);
```

定时器触发事件回调，也供霍尔传感器接口路径使用。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

来源：[固定头文件L1943](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1943)。

### `HAL_TIM_TriggerHalfCpltCallback`

```c
void HAL_TIM_TriggerHalfCpltCallback (TIM_HandleTypeDef * htim);
```

触发相关 DMA 半传输回调。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

来源：[固定头文件L1944](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1944)。

### `HAL_TIM_ErrorCallback`

```c
void HAL_TIM_ErrorCallback (TIM_HandleTypeDef * htim);
```

定时器非阻塞操作错误回调，检查 DMA 句柄与状态。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

来源：[固定头文件L1945](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1945)。

## 句柄状态查询

### `HAL_TIM_Base_GetState`

```c
HAL_TIM_StateTypeDef HAL_TIM_Base_GetState (TIM_HandleTypeDef * htim);
```

返回基本时基句柄状态。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_TIM_StateTypeDef`，即句柄软件状态。

来源：[固定头文件L1963](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1963)。

### `HAL_TIM_OC_GetState`

```c
HAL_TIM_StateTypeDef HAL_TIM_OC_GetState (TIM_HandleTypeDef * htim);
```

返回输出比较句柄状态。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_TIM_StateTypeDef`，即句柄软件状态。

来源：[固定头文件L1964](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1964)。

### `HAL_TIM_PWM_GetState`

```c
HAL_TIM_StateTypeDef HAL_TIM_PWM_GetState (TIM_HandleTypeDef * htim);
```

返回PWM 输出句柄状态。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_TIM_StateTypeDef`，即句柄软件状态。

来源：[固定头文件L1965](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1965)。

### `HAL_TIM_IC_GetState`

```c
HAL_TIM_StateTypeDef HAL_TIM_IC_GetState (TIM_HandleTypeDef * htim);
```

返回输入捕获句柄状态。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_TIM_StateTypeDef`，即句柄软件状态。

来源：[固定头文件L1966](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1966)。

### `HAL_TIM_OnePulse_GetState`

```c
HAL_TIM_StateTypeDef HAL_TIM_OnePulse_GetState (TIM_HandleTypeDef * htim);
```

返回单脉冲句柄状态。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_TIM_StateTypeDef`，即句柄软件状态。

来源：[固定头文件L1967](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1967)。

### `HAL_TIM_Encoder_GetState`

```c
HAL_TIM_StateTypeDef HAL_TIM_Encoder_GetState (TIM_HandleTypeDef * htim);
```

返回编码器接口句柄状态。

- `htim`：TIM 句柄指针，Instance 为 TIM1–TIM4；高级功能仅 TIM1。

返回：`HAL_TIM_StateTypeDef`，即句柄软件状态。

来源：[固定头文件L1968](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1968)。

## 驱动内部辅助函数

### `TIM_Base_SetConfig`

```c
void TIM_Base_SetConfig (TIM_TypeDef * TIMx, TIM_Base_InitTypeDef * Structure);
```

驱动内部辅助函数，写入基本计数时基配置。

- `TIMx`：TIM1、TIM2、TIM3 或 TIM4 寄存器实例；高级寄存器功能仅 TIM1。
- `Structure`：原型所示配置结构指针；字段和合法组合见本章结构说明。

返回：无返回值。

来源：[固定头文件L1982](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1982)。

### `TIM_TI1_SetConfig`

```c
void TIM_TI1_SetConfig (TIM_TypeDef * TIMx, uint32_t TIM_ICPolarity, uint32_t TIM_ICSelection, uint32_t TIM_ICFilter);
```

驱动内部辅助函数，配置 TI1 输入。原文明示 INDIRECT 模式采用通道2路径的 TI2FP1，此时传入的 TIM_ICFilter 和 TIM_ICPolarity 不使用；应保护 CCMR1，避免未初始化的滤波/极性数据覆盖现有配置。

- `TIMx`：TIM1、TIM2、TIM3 或 TIM4 寄存器实例；高级寄存器功能仅 TIM1。
- `TIM_ICPolarity`：输入有效极性。
  - 可用编码：`TIM_ICPOLARITY_RISING`、`TIM_ICPOLARITY_FALLING`。
- `TIM_ICSelection`：TI 输入直接/间接/TRC 映射。
  - 可用编码：`TIM_ICSELECTION_DIRECTTI`、`TIM_ICSELECTION_INDIRECTTI`、`TIM_ICSELECTION_TRC`。
- `TIM_ICFilter`：输入滤波编码 0–15。

返回：无返回值。

来源：[固定头文件L1983](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1983)。

### `TIM_OC2_SetConfig`

```c
void TIM_OC2_SetConfig (TIM_TypeDef * TIMx, TIM_OC_InitTypeDef * OC_Config);
```

驱动内部辅助函数，配置输出比较通道 2。

- `TIMx`：TIM1、TIM2、TIM3 或 TIM4 寄存器实例；高级寄存器功能仅 TIM1。
- `OC_Config`：原型所示配置结构指针；字段和合法组合见本章结构说明。

返回：无返回值。

来源：[固定头文件L1984](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1984)。

### `TIM_ETR_SetConfig`

```c
void TIM_ETR_SetConfig (TIM_TypeDef * TIMx, uint32_t TIM_ExtTRGPrescaler, uint32_t TIM_ExtTRGPolarity, uint32_t ExtTRGFilter);
```

驱动内部辅助函数，配置外部 ETR 的极性、预分频和滤波。

- `TIMx`：TIM1、TIM2、TIM3 或 TIM4 寄存器实例；高级寄存器功能仅 TIM1。
- `TIM_ExtTRGPrescaler`：ETR 预分频 DIV1/2/4/8。
  - 可用编码：`TIM_ETRPRESCALER_DIV1`、`TIM_ETRPRESCALER_DIV2`、`TIM_ETRPRESCALER_DIV4`、`TIM_ETRPRESCALER_DIV8`。
- `TIM_ExtTRGPolarity`：ETR 反相或不反相。
  - 可用编码：`TIM_ETRPOLARITY_INVERTED`、`TIM_ETRPOLARITY_NONINVERTED`。
- `ExtTRGFilter`：输入滤波编码 0–15。

返回：无返回值。

来源：[固定头文件L1985](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1985)。

### `TIM_DMADelayPulseCplt`

```c
void TIM_DMADelayPulseCplt (DMA_HandleTypeDef * hdma);
```

驱动内部输出比较/PWM DMA 全传输回调。

- `hdma`：关联 DMA 句柄指针，其 Parent 应指向所属 TIM 句柄。

返回：无返回值。

来源：[固定头文件L1988](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1988)。

### `TIM_DMADelayPulseHalfCplt`

```c
void TIM_DMADelayPulseHalfCplt (DMA_HandleTypeDef * hdma);
```

驱动内部输出比较/PWM DMA 半传输回调。

- `hdma`：关联 DMA 句柄指针，其 Parent 应指向所属 TIM 句柄。

返回：无返回值。

来源：[固定头文件L1989](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1989)。

### `TIM_DMAError`

```c
void TIM_DMAError (DMA_HandleTypeDef * hdma);
```

驱动内部 DMA 错误回调。

- `hdma`：关联 DMA 句柄指针，其 Parent 应指向所属 TIM 句柄。

返回：无返回值。

来源：[固定头文件L1990](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1990)。

### `TIM_DMACaptureCplt`

```c
void TIM_DMACaptureCplt (DMA_HandleTypeDef * hdma);
```

驱动内部输入捕获 DMA 全传输回调。

- `hdma`：关联 DMA 句柄指针，其 Parent 应指向所属 TIM 句柄。

返回：无返回值。

来源：[固定头文件L1991](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1991)。

### `TIM_DMACaptureHalfCplt`

```c
void TIM_DMACaptureHalfCplt (DMA_HandleTypeDef * hdma);
```

驱动内部输入捕获 DMA 半传输回调。

- `hdma`：关联 DMA 句柄指针，其 Parent 应指向所属 TIM 句柄。

返回：无返回值。

来源：[固定头文件L1992](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1992)。

### `TIM_CCxChannelCmd`

```c
void TIM_CCxChannelCmd (TIM_TypeDef * TIMx, uint32_t Channel, uint32_t ChannelState);
```

驱动内部辅助函数，按 ChannelState 开关指定捕获比较通道。

- `TIMx`：TIM1、TIM2、TIM3 或 TIM4 寄存器实例；高级寄存器功能仅 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`TIM_CHANNEL_1`、`TIM_CHANNEL_2`、`TIM_CHANNEL_3`、`TIM_CHANNEL_4`。
- `ChannelState`：CCxE 新状态，使用 TIM_CCx_ENABLE 或 TIM_CCx_DISABLE。

返回：无返回值。


来源：[固定头文件L1993](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1993)。

[返回定时器主题](../../知识库/06_定时器PWM与同步.md) · [图形关系与来源](图形关系与来源.md)
