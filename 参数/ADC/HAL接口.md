# ADC HAL 接口参考

保留原笔记 35 个接口并补齐 2 个条件回调注册接口，共 37 项；原型按固定 v1.1.4 头文件逐项列出。跨版本控制流差异由链接的专节说明。

公共约定：HAL_StatusTypeDef 返回值须按具体控制流解释；HAL_OK 不额外保证采集完成、配置全部应用、硬件停止或缓冲区可复用。Get 类的 uint32_t 是数据或位图，void 回调无返回值。有效句柄和参数对象的生命周期由调用方保证；assert_param 的存在不代表关闭断言后仍有运行时输入拒绝。

参数结构见[配置字段](HAL配置字段.md)，符号见[符号参考](HAL符号表.md)。DMA 项数、宽度与 Parent 关联须同时满足 DMA 专章。

## HAL_ADC_Init

```c
HAL_StatusTypeDef       HAL_ADC_Init(ADC_HandleTypeDef* hadc);
```

设置 ADC 公共属性和规则组基础配置；RESET 入口才执行 MSP 初始化。连续/间断冲突及错误位保留等边界见[初始化契约](HAL初始化边界.md)。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L896) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L421)

## HAL_ADC_DeInit

```c
HAL_StatusTypeDef       HAL_ADC_DeInit(ADC_HandleTypeDef *hadc);
```

尝试停止并禁用 ADC；成功后清理函数列出的字段、调用 MSP 并复位软件状态。其寄存器写入不等同于完整硬件复位，见[反初始化范围](HAL初始化边界.md)。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L897) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L639)

## HAL_ADC_MspInit

```c
void                    HAL_ADC_MspInit(ADC_HandleTypeDef* hadc);
```

用户实现的底层初始化入口：配置 RCC、模拟 GPIO、DMA 和 NVIC。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

返回：无返回值。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L898) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L787)

## HAL_ADC_MspDeInit

```c
void                    HAL_ADC_MspDeInit(ADC_HandleTypeDef* hadc);
```

用户实现的底层释放入口；仅释放该 ADC 确实拥有的资源。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

返回：无返回值。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L899) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L801)

## HAL_ADC_RegisterCallback

```c
HAL_StatusTypeDef HAL_ADC_RegisterCallback(ADC_HandleTypeDef *hadc, HAL_ADC_CallbackIDTypeDef CallbackID, pADC_CallbackTypeDef pCallback);
```

仅 USE_HAL_ADC_REGISTER_CALLBACKS==1 时可用。 hadc 为 ADC 句柄，CallbackID 为七种已定义 ID 之一，pCallback 为 void (*)(ADC_HandleTypeDef*) 函数指针。NULL 回调返回 HAL_ERROR 并置 INVALID_CALLBACK。 State 包含 READY 位时接受全部有效 ID，State 恰为 RESET 时只接受两种 MSP ID；其余路径报错。完整约束见[回调注册条件](HAL配置字段.md)。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L903) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L830)

## HAL_ADC_UnRegisterCallback

```c
HAL_StatusTypeDef HAL_ADC_UnRegisterCallback(ADC_HandleTypeDef *hadc, HAL_ADC_CallbackIDTypeDef CallbackID);
```

仅 USE_HAL_ADC_REGISTER_CALLBACKS==1 时可用。 hadc 为 ADC 句柄，CallbackID 为待恢复的回调 ID；恢复对应默认弱函数。 State 包含 READY 位时接受全部有效 ID，State 恰为 RESET 时只接受两种 MSP ID；其余路径报错。完整约束见[回调注册条件](HAL配置字段.md)。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L904) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L934)

## HAL_ADC_Start

```c
HAL_StatusTypeDef       HAL_ADC_Start(ADC_HandleTypeDef* hadc);
```

使能 ADC 并启动规则组；软件触发立即开始，外部触发配置则等待触发。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L919) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1046)

## HAL_ADC_Stop

```c
HAL_StatusTypeDef       HAL_ADC_Stop(ADC_HandleTypeDef* hadc);
```

停止规则组并关闭 ADC；关闭 ADC 也影响注入组，应先处理注入组的停止。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L920) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1159)

## HAL_ADC_PollForConversion

```c
HAL_StatusTypeDef       HAL_ADC_PollForConversion(ADC_HandleTypeDef* hadc, uint32_t Timeout);
```

CR2.DMA=0 且 SCAN=0、SQR1.L=0 时等待 EOC；其余可进入软件估算路径。Timeout 单位 ms；返回成功不对任意扫描序列提供硬件完成保证。详见[轮询契约](HAL轮询边界.md)。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。
- `Timeout`：等待上限，单位 ms；可用 HAL_MAX_DELAY 表示无限等待，时间基准必须能够推进。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L921) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1203)

## HAL_ADC_PollForEvent

```c
HAL_StatusTypeDef       HAL_ADC_PollForEvent(ADC_HandleTypeDef* hadc, uint32_t EventType, uint32_t Timeout);
```

等待模拟看门狗越界事件；EventType 为 ADC_AWD_EVENT，Timeout 单位 ms。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。
- `EventType`：要等待的 ADC 事件，本章为模拟看门狗越界。
  - 可用编码：`ADC_AWD_EVENT`。
- `Timeout`：等待上限，单位 ms；可用 HAL_MAX_DELAY 表示无限等待，时间基准必须能够推进。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L922) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1334)

## HAL_ADC_Start_IT

```c
HAL_StatusTypeDef       HAL_ADC_Start_IT(ADC_HandleTypeDef* hadc);
```

启动规则组并开放转换完成中断；扫描序列不能依靠末次中断保留各通道全部样本。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L925) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1383)

## HAL_ADC_Stop_IT

```c
HAL_StatusTypeDef       HAL_ADC_Stop_IT(ADC_HandleTypeDef* hadc);
```

停止规则组、关闭转换完成中断并关闭 ADC。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L926) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1494)

## HAL_ADC_Start_DMA

```c
HAL_StatusTypeDef       HAL_ADC_Start_DMA(ADC_HandleTypeDef* hadc, uint32_t* pData, uint32_t Length);
```

启动规则组及 DMA；C8 仅 ADC1 可独立发出 ADC DMA 请求，pData 为目标缓冲区，Length 为传输项数。 所核对实现未传播底层 DMA 启动失败，外层 HAL_OK 不能独立证明 DMA 已接收该请求，见[DMA生命周期](DMA生命周期与恢复.md)。

- `hadc`：独立 DMA 路径在 C8 必须是 ADC1 句柄，并已关联 DMA1 通道1；不能把 ADC2 句柄作为独立 DMA 请求源。
- `pData`：ADC 转换数据的 DMA 目标缓冲区地址；有效长度与对齐由传输项数和 DMA 数据宽度共同决定，直到 DMA 停止前必须有效。
- `Length`：DMA 传输项数，非字节数；数据宽度由 DMA 配置决定。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L929) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1551)

## HAL_ADC_Stop_DMA

```c
HAL_StatusTypeDef       HAL_ADC_Stop_DMA(ADC_HandleTypeDef* hadc);
```

停止独立 ADC 的规则组 DMA 及转换并关闭 ADC；双 ADC 模式改用扩展接口。

- `hadc`：独立 DMA 路径在 C8 必须是 ADC1 句柄，并已关联 DMA1 通道1；不能把 ADC2 句柄作为独立 DMA 请求源。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L930) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1692)

## HAL_ADC_GetValue

```c
uint32_t                HAL_ADC_GetValue(ADC_HandleTypeDef* hadc);
```

读取规则组 DR；读取会清除硬件 EOC，返回值保持所配置的数据对齐方式。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

返回：`uint32_t`，具体数值/位域含义见上方功能说明；Get 类不表示操作成功状态。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L933) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1757)

## HAL_ADC_IRQHandler

```c
void                    HAL_ADC_IRQHandler(ADC_HandleTypeDef* hadc);
```

处理当前 ADC 的 EOC、JEOC 与 AWD 路径并分发回调；共享 ADC1_2 中断需由工程正确服务两个实例。v1.1.4 逐分支读寄存器，v1.1.10 使用入口快照，见[IRQ 与数据来源](HAL配置与读数.md)。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

返回：无返回值。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L936) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1774)

## HAL_ADC_ConvCpltCallback

```c
void                    HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc);
```

规则组非阻塞转换完成回调；DMA 下表示缓冲区传输完成。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L937) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1901)

## HAL_ADC_ConvHalfCpltCallback

```c
void                    HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef* hadc);
```

规则组 DMA 半传输回调，可处理已经填满的前半缓冲区。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L938) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1915)

## HAL_ADC_LevelOutOfWindowCallback

```c
void                    HAL_ADC_LevelOutOfWindowCallback(ADC_HandleTypeDef* hadc);
```

模拟看门狗越界回调；只表示所选被监视转换超出窗口。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L939) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1929)

## HAL_ADC_ErrorCallback

```c
void                    HAL_ADC_ErrorCallback(ADC_HandleTypeDef *hadc);
```

ADC 非阻塞路径出错回调；读取 ErrorCode 并检查对应 DMA 状态。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L940) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1944)

## HAL_ADC_ConfigChannel

```c
HAL_StatusTypeDef       HAL_ADC_ConfigChannel(ADC_HandleTypeDef* hadc, ADC_ChannelConfTypeDef* sConfig);
```

设置规则组 Rank 与该物理通道的采样时间。失败可能发生于部分字段已写入之后；内部通路的启动等待须按[配置契约](HAL配置与读数.md)核对。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。
- `sConfig`：原型所示配置结构指针；字段和合法组合见配置字段参考。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L950) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L1992)

## HAL_ADC_AnalogWDGConfig

```c
HAL_StatusTypeDef       HAL_ADC_AnalogWDGConfig(ADC_HandleTypeDef* hadc, ADC_AnalogWDGConfTypeDef* AnalogWDGConfig);
```

设置窗口、监控范围及中断；调用方须保证 LowThreshold≤HighThreshold，初始化合法 Channel，WatchdogNumber 在该固定实现中未使用。见[配置契约](HAL配置与读数.md)。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。
- `AnalogWDGConfig`：原型所示配置结构指针；字段和合法组合见配置字段参考。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L951) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L2102)

## HAL_ADC_GetState

```c
uint32_t                HAL_ADC_GetState(ADC_HandleTypeDef* hadc);
```

返回 HAL ADC 状态位图；可同时含规则组、注入组和错误状态，不应仅按单一枚举比较。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

返回：uint32_t ADC 状态位图，见状态说明。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L961) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L2189)

## HAL_ADC_GetError

```c
uint32_t                HAL_ADC_GetError(ADC_HandleTypeDef *hadc);
```

返回 HAL ADC 错误位图。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

返回：uint32_t ADC 错误位图，见错误说明。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc.h#L962) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc.c#L2200)

## HAL_ADCEx_Calibration_Start

```c
HAL_StatusTypeDef       HAL_ADCEx_Calibration_Start(ADC_HandleTypeDef* hadc);
```

自动校准 ADC。调用前 ADC 处于停止状态；在首次采样前或停机后调用，检查 HAL 返回状态。

**历史实现边界（2026-10-12 源码复核）：**[ST HAL 驱动 v1.1.4 固定源码](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c) 的该函数先停止规则/注入转换并禁用 ADC，将显式“两 ADC 周期”等待放在 ADON=0 阶段，随后调用 ADC_Enable、复位校准并校准，成功后保留 ADC 使能。RM0008 Rev21 §11.4 的硬件要求则是校准前 ADON=1 至少两个 ADC 时钟周期；通用 ADC_Enable 稳定延时不能被直接当成已按 ADC 时钟证明该条件。不能只在函数外预先置 ADON，因为函数内部会再次禁用 ADC。

[ST 官方 HAL 发布说明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Release_Notes.html)在 V1.1.9（2023-04-07）的 HAL ADC 条目中记录了校准前 ADON=1 保持至少两个 ADC 时钟周期的修复。这里的 V1.1.9 是 HAL 驱动版本。使用旧驱动应核对使能后的等待；其他分支和自定义移植仍须检查实际源码与时钟条件，HAL_OK 本身不证明校准时序合规。

固定v1.1.10已将显式等待移至使能后，但两版的helper错误返回传递仍有不同边界，见[校准顺序与返回值](HAL初始化边界.md#校准入口的两版顺序与返回值传递)。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L647) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L126)

## HAL_ADCEx_InjectedStart

```c
HAL_StatusTypeDef       HAL_ADCEx_InjectedStart(ADC_HandleTypeDef* hadc);
```

使能 ADC 并启动注入组；按所选软件或外部触发源执行。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L650) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L232)

## HAL_ADCEx_InjectedStop

```c
HAL_StatusTypeDef       HAL_ADCEx_InjectedStop(ADC_HandleTypeDef* hadc);
```

停止独立触发的注入组并禁用 ADC。若规则组正在转换或启用了自动注入，原文要求先用 HAL_ADC_Stop 停止两组；不能假定此函数能只停注入而保持正在运行的规则组。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L651) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L331)

## HAL_ADCEx_InjectedPollForConversion

```c
HAL_StatusTypeDef       HAL_ADCEx_InjectedPollForConversion(ADC_HandleTypeDef* hadc, uint32_t Timeout);
```

JSQR.JL=0 时等待 JEOC；JL 非零时使用软件估算循环，不能由 HAL_OK 推出整个注入序列已完成。成功路径还会清 EOC。详见[轮询契约](HAL轮询边界.md)。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。
- `Timeout`：等待上限，单位 ms；可用 HAL_MAX_DELAY 表示无限等待，时间基准必须能够推进。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L652) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L384)

## HAL_ADCEx_InjectedStart_IT

```c
HAL_StatusTypeDef       HAL_ADCEx_InjectedStart_IT(ADC_HandleTypeDef* hadc);
```

启动注入组并使能注入转换完成中断。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L655) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L502)

## HAL_ADCEx_InjectedStop_IT

```c
HAL_StatusTypeDef       HAL_ADCEx_InjectedStop_IT(ADC_HandleTypeDef* hadc);
```

停止注入组、禁用注入完成中断并禁用 ADC。若规则组正在转换，原文要求用 HAL_ADC_Stop 或 HAL_ADC_Stop_IT 停止两组；自动注入也须通过规则组停止接口停机。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L656) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L601)

## HAL_ADCEx_MultiModeStart_DMA

```c
HAL_StatusTypeDef       HAL_ADCEx_MultiModeStart_DMA(ADC_HandleTypeDef *hadc, uint32_t *pData, uint32_t Length);
```

由 ADC1 主 ADC 启动双 ADC 规则组 DMA，把主从结果以 32 位配对数据送入缓冲区。所核对实现忽略底层 DMA 启动返回值，HAL_OK 不能独立证明 DMA 已接收请求，详见[DMA生命周期](DMA生命周期与恢复.md)。

- `hadc`：必须是主 ADC1 的句柄，不能传入从 ADC2 的句柄。
- `pData`：双 ADC 转换结果的 DMA 目标缓冲区地址；按 32 位配对结果配置并满足对齐，直到 DMA 停止前必须有效。
- `Length`：DMA 传输项数，非字节数；数据宽度由 DMA 配置决定。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L660) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L670)

## HAL_ADCEx_MultiModeStop_DMA

```c
HAL_StatusTypeDef       HAL_ADCEx_MultiModeStop_DMA(ADC_HandleTypeDef *hadc);
```

停止双 ADC 规则组 DMA 及相关转换。UM1850 Rev 3 注释称保留双模式；所核两版实现均在主从禁用成功后清DUALMOD，且停止/错误状态处理与独立ADC不同；见[双ADC停止条件](DMA生命周期与恢复.md#3-双adc停止须独立判断)。重启前重配所需双模式。

- `hadc`：必须是主 ADC1 的句柄，不能传入从 ADC2 的句柄。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L661) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L796)

## HAL_ADCEx_InjectedGetValue

```c
uint32_t                HAL_ADCEx_InjectedGetValue(ADC_HandleTypeDef* hadc, uint32_t InjectedRank);
```

读取指定注入 Rank 对应的 JDR 数据；注入偏移可能使结果为负，调用者必须按有符号结果解释。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。
- `InjectedRank`：注入序列 Rank 1–4。
  - 可用编码：`ADC_INJECTED_RANK_1`、`ADC_INJECTED_RANK_2`、`ADC_INJECTED_RANK_3`、`ADC_INJECTED_RANK_4`。

返回：`uint32_t`，具体数值/位域含义见上方功能说明；Get 类不表示操作成功状态。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L665) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L885)

## HAL_ADCEx_MultiModeGetValue

```c
uint32_t                HAL_ADCEx_MultiModeGetValue(ADC_HandleTypeDef *hadc);
```

返回低半字 ADC1、高半字 ADC2。所核两版在 ADC1.CR2.DMA=0 时分别读 ADC1_DR、ADC2_DR 后拼合，非原子配对；硬件单次 ADC1_DR 组合读取的 DMA 位条件另见[读数契约](HAL配置与读数.md)。

- `hadc`：必须是主 ADC1 的句柄，不能传入从 ADC2 的句柄。

返回：`uint32_t`，具体数值/位域含义见上方功能说明；Get 类不表示操作成功状态。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L667) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L922)

## HAL_ADCEx_InjectedConvCpltCallback

```c
void                    HAL_ADCEx_InjectedConvCpltCallback(ADC_HandleTypeDef* hadc);
```

注入组非阻塞转换完成回调；按已配置 Rank 读取各自结果寄存器。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。

返回：无返回值。

- 属于非阻塞回调契约；在中断上下文中避免阻塞。用户覆写公开 HAL 回调，不直接调用驱动内部 DMA 回调。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L671) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L954)

## HAL_ADCEx_InjectedConfigChannel

```c
HAL_StatusTypeDef       HAL_ADCEx_InjectedConfigChannel(ADC_HandleTypeDef* hadc,ADC_InjectionConfTypeDef* sConfigInjected);
```

设置注入通道、序列位置、采样时间、偏移及公共模式；字段 DISABLE 不保证清除旧 JAUTO/JDISCEN，温度等待和部分写入边界见[配置契约](HAL配置与读数.md)。

- `hadc`：ADC 句柄指针，Instance 为 ADC1 或 ADC2；涉及 DMA 时遵守 ADC1 限制。
- `sConfigInjected`：原型所示配置结构指针；字段和合法组合见配置字段参考。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L681) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L996)

## HAL_ADCEx_MultiModeConfigChannel

```c
HAL_StatusTypeDef       HAL_ADCEx_MultiModeConfigChannel(ADC_HandleTypeDef *hadc, ADC_MultiModeTypeDef *multimode);
```

由主 ADC1 配置 DUALMOD；两 ADC 都禁用时才写入，否则置 ERROR_CONFIG 并返回 HAL_ERROR。更改模式及序列时须遵守同步条件。

- `hadc`：必须使用主 ADC1 句柄；双 ADC 模式通过 ADC1_CR1.DUALMOD 配置，ADC2 对应位为保留位。
- `multimode`：原型所示配置结构指针；字段和合法组合见配置字段参考。

[固定头文件声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_adc_ex.h#L683) · [固定实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_adc_ex.c#L1257)


## 底层机制与生命周期

- [DMA启动、停止、错误与恢复](DMA生命周期与恢复.md)
- [六个内部辅助条目与八个导出宏](HAL辅助函数与宏.md)
