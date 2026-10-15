# TIM LL 接口逐项参考

本页按计数、捕获、输出、同步和 DMA 等功能组织 LL 接口，原型对应固定 de129f1 头文件。各接口保留自身的运行条件与版本差异。

索引型Channel参数只接受该接口列出的单一通道。固定头文件TIM_GET_CHANNEL_INDEX对未匹配值回退到索引6（CH4），不会自动返回非法参数；将多个通道按位或传给这类接口可能误操作CH4。Channels位掩码接口则按各自说明处理组合值。

先看[初始化与状态约束](LL初始化边界.md)及[时基、更新和触发](计数时基与更新.md)。高级输出、BDTR、RCR、COM与N通道仅TIM1；单独清CEN不保证实际引脚安全。LL不维护HAL句柄状态或锁，资源所有权须明确。

`__STATIC_INLINE` 表示头文件内联接口。TIMx 为 TIM1、TIM2、TIM3 或 TIM4 的寄存器实例；高级寄存器功能只用于 TIM1，各条目另列更具体的限制。HAL 与 LL 的枚举编码分别使用。

## 本页导航

- [计数与更新](#计数与更新)
- [捕获比较通道控制](#捕获比较通道控制)
- [输出比较与 PWM](#输出比较与-pwm)
- [输入捕获](#输入捕获)
- [外部时钟与同步](#外部时钟与同步)
- [刹车与输出保护](#刹车与输出保护)
- [DMA burst](#dma-burst)
- [事件标志](#事件标志)
- [中断使能](#中断使能)
- [DMA 请求使能](#dma-请求使能)
- [软件事件](#软件事件)
- [初始化与配置结构](#初始化与配置结构)

## 计数与更新

### `LL_TIM_EnableCounter`

```c
__STATIC_INLINE void LL_TIM_EnableCounter (TIM_TypeDef * TIMx);
```

使能定时器计数器 CEN。

固定头文件：[接口定义L1007](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1007)。

### `LL_TIM_DisableCounter`

```c
__STATIC_INLINE void LL_TIM_DisableCounter (TIM_TypeDef * TIMx);
```

清除 CEN，停止计数。

固定头文件：[接口定义L1018](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1018)。

### `LL_TIM_IsEnabledCounter`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledCounter (TIM_TypeDef * TIMx);
```

查询计数器是否使能，返回 0 或 1。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L1029](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1029)。

### `LL_TIM_EnableUpdateEvent`

```c
__STATIC_INLINE void LL_TIM_EnableUpdateEvent (TIM_TypeDef * TIMx);
```

使能更新事件生成。

固定头文件：[接口定义L1040](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1040)。

### `LL_TIM_DisableUpdateEvent`

```c
__STATIC_INLINE void LL_TIM_DisableUpdateEvent (TIM_TypeDef * TIMx);
```

关闭更新事件生成。

固定头文件：[接口定义L1051](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1051)。

### `LL_TIM_IsEnabledUpdateEvent`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledUpdateEvent (TIM_TypeDef * TIMx);
```

查询是否使能更新事件生成。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L1062](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1062)。

### `LL_TIM_SetUpdateSource`

```c
__STATIC_INLINE void LL_TIM_SetUpdateSource (TIM_TypeDef * TIMx, uint32_t UpdateSource);
```

设置更新中断/DMA 请求来源。

- `UpdateSource`：更新请求来源，全部更新原因或仅计数溢出/下溢。
  - 可用编码：`LL_TIM_UPDATESOURCE_REGULAR`、`LL_TIM_UPDATESOURCE_COUNTER`。

固定头文件：[接口定义L1083](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1083)。

### `LL_TIM_GetUpdateSource`

```c
__STATIC_INLINE uint32_t LL_TIM_GetUpdateSource (TIM_TypeDef * TIMx);
```

读取更新中断/DMA 请求来源。

返回：uint32_t，返回编码：`LL_TIM_UPDATESOURCE_REGULAR`、`LL_TIM_UPDATESOURCE_COUNTER`。

固定头文件：[接口定义L1096](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1096)。

### `LL_TIM_SetOnePulseMode`

```c
__STATIC_INLINE void LL_TIM_SetOnePulseMode (TIM_TypeDef * TIMx, uint32_t OnePulseMode);
```

设置单脉冲或重复运行方式。

- `OnePulseMode`：单脉冲单次或重复方式。
  - 可用编码：`LL_TIM_ONEPULSEMODE_SINGLE`、`LL_TIM_ONEPULSEMODE_REPETITIVE`。

固定头文件：[接口定义L1110](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1110)。

### `LL_TIM_GetOnePulseMode`

```c
__STATIC_INLINE uint32_t LL_TIM_GetOnePulseMode (TIM_TypeDef * TIMx);
```

读取单脉冲或重复运行方式。

返回：uint32_t，返回编码：`LL_TIM_ONEPULSEMODE_SINGLE`、`LL_TIM_ONEPULSEMODE_REPETITIVE`。

固定头文件：[接口定义L1123](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1123)。

### `LL_TIM_SetCounterMode`

```c
__STATIC_INLINE void LL_TIM_SetCounterMode (TIM_TypeDef * TIMx, uint32_t CounterMode);
```

设置向上、向下或中心对齐计数方式。

- `CounterMode`：向上/向下/中心对齐计数模式。
  - 可用编码：`LL_TIM_COUNTERMODE_UP`、`LL_TIM_COUNTERMODE_DOWN`、`LL_TIM_COUNTERMODE_CENTER_UP`、`LL_TIM_COUNTERMODE_CENTER_DOWN`、`LL_TIM_COUNTERMODE_CENTER_UP_DOWN`。

固定头文件：[接口定义L1147](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1147)。

### `LL_TIM_GetCounterMode`

```c
__STATIC_INLINE uint32_t LL_TIM_GetCounterMode (TIM_TypeDef * TIMx);
```

读取计数模式CMS与当前方向DIR的组合；中心对齐时返回值随DIR状态变化。

返回：uint32_t，为固定实现读取的CR1中DIR与CMS位的组合，不保证总是等于上述配置常量之一。中心对齐时DIR由硬件更新；因此CMS=01时可读到0x20或0x30，CMS=10时可读到0x40或0x50，CMS=11时可读到0x60或0x70。判断中心模式应提取CMS，方向由DIR单独解释；不能把带当前DIR的整个返回值直接与仅含CMS的中心模式常量比较。

依据：[固定实现L1167–1170](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1167-L1170)、[模式常量L513–517](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L513-L517)、[RM0008 Rev21 CR1 p338](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=338)。表述由读取掩码和器件字段定义推导，未作板端执行验证。

固定头文件：[接口定义L1167](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1167)。

### `LL_TIM_EnableARRPreload`

```c
__STATIC_INLINE void LL_TIM_EnableARRPreload (TIM_TypeDef * TIMx);
```

使能ARR 自动重装预装载。

固定头文件：[接口定义L1178](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1178)。

### `LL_TIM_DisableARRPreload`

```c
__STATIC_INLINE void LL_TIM_DisableARRPreload (TIM_TypeDef * TIMx);
```

关闭ARR 自动重装预装载。

固定头文件：[接口定义L1189](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1189)。

### `LL_TIM_IsEnabledARRPreload`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledARRPreload (TIM_TypeDef * TIMx);
```

查询是否使能ARR 自动重装预装载。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L1200](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1200)。

### `LL_TIM_SetClockDivision`

```c
__STATIC_INLINE void LL_TIM_SetClockDivision (TIM_TypeDef * TIMx, uint32_t ClockDivision);
```

设置死区和数字滤波采样时钟分频 CKD（不是计数器 PSC）。

- `ClockDivision`：CKD 数字滤波与死区采样分频。
  - 可用编码：`LL_TIM_CLOCKDIVISION_DIV1`、`LL_TIM_CLOCKDIVISION_DIV2`、`LL_TIM_CLOCKDIVISION_DIV4`。

固定头文件：[接口定义L1218](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1218)。

### `LL_TIM_GetClockDivision`

```c
__STATIC_INLINE uint32_t LL_TIM_GetClockDivision (TIM_TypeDef * TIMx);
```

读取死区和数字滤波采样时钟分频 CKD（不是计数器 PSC）。

返回：uint32_t，返回编码：`LL_TIM_CLOCKDIVISION_DIV1`、`LL_TIM_CLOCKDIVISION_DIV2`、`LL_TIM_CLOCKDIVISION_DIV4`。

固定头文件：[接口定义L1235](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1235)。

### `LL_TIM_SetCounter`

```c
__STATIC_INLINE void LL_TIM_SetCounter (TIM_TypeDef * TIMx, uint32_t Counter);
```

设置CNT 计数器值。

- `Counter`：CNT 值，0–65535。

固定头文件：[接口定义L1247](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1247)。

### `LL_TIM_GetCounter`

```c
__STATIC_INLINE uint32_t LL_TIM_GetCounter (TIM_TypeDef * TIMx);
```

读取CNT 计数器值。

返回：`uint32_t`，当前 CNT 值，范围 0–65535。

固定头文件：[接口定义L1258](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1258)。

### `LL_TIM_GetDirection`

```c
__STATIC_INLINE uint32_t LL_TIM_GetDirection (TIM_TypeDef * TIMx);
```

读取当前计数方向。

返回：uint32_t，返回编码：`LL_TIM_COUNTERDIRECTION_UP`、`LL_TIM_COUNTERDIRECTION_DOWN`。

固定头文件：[接口定义L1271](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1271)。

### `LL_TIM_SetPrescaler`

```c
__STATIC_INLINE void LL_TIM_SetPrescaler (TIM_TypeDef * TIMx, uint32_t Prescaler);
```

写PSC预装载值；在更新事件装入后，对应除数为PSC+1。调用本身不发UG。

- `Prescaler`：PSC 值，0–65535，实际除数 PSC+1。

固定头文件：[接口定义L1287](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1287)。

### `LL_TIM_GetPrescaler`

```c
__STATIC_INLINE uint32_t LL_TIM_GetPrescaler (TIM_TypeDef * TIMx);
```

读取总线可见PSC值；新值可能尚未装入内部活动预分频器，读回不证明当前分频已改变。

返回：`uint32_t`，总线可见 PSC 值，范围 0–65535。

固定头文件：[接口定义L1298](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1298)。

### `LL_TIM_SetAutoReload`

```c
__STATIC_INLINE void LL_TIM_SetAutoReload (TIM_TypeDef * TIMx, uint32_t AutoReload);
```

写入 16 位 ARR 自动重装值；ARPE 决定是否等待 UEV 装入活动值。

- `AutoReload`：ARR 值，0–65535；零值会阻止正常计数。

固定头文件：[接口定义L1312](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1312)。

### `LL_TIM_GetAutoReload`

```c
__STATIC_INLINE uint32_t LL_TIM_GetAutoReload (TIM_TypeDef * TIMx);
```

读取总线可见的 16 位 ARR 值；启用预装载时，读回值不表示内部活动值已更新。

返回：`uint32_t`，总线可见 ARR 值，范围 0–65535。

固定头文件：[接口定义L1323](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1323)。

### `LL_TIM_SetRepetitionCounter`

```c
__STATIC_INLINE void LL_TIM_SetRepetitionCounter (TIM_TypeDef * TIMx, uint32_t RepetitionCounter);
```

设置TIM1 的 RCR 重复计数值，0–255。

- `TIMx`：选择 TIM1。
- `RepetitionCounter`：TIM1 RCR 值，0–255。

- 适用实例：TIM1。

固定头文件：[接口定义L1337](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1337)。

### `LL_TIM_GetRepetitionCounter`

```c
__STATIC_INLINE uint32_t LL_TIM_GetRepetitionCounter (TIM_TypeDef * TIMx);
```

读取 TIM1 的 RCR 配置值；该值不表示内部正在递减的重复计数状态。

- `TIMx`：选择 TIM1。

返回：`uint32_t`，RCR 配置值，范围 0–255。

- 适用实例：TIM1。

固定头文件：[接口定义L1350](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1350)。

## 捕获比较通道控制

### `LL_TIM_CC_EnablePreload`

```c
__STATIC_INLINE void LL_TIM_CC_EnablePreload (TIM_TypeDef * TIMx);
```

使能TIM1 互补输出控制位预装载（CCxE、CCxNE、OCxM）。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L1373](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1373)。

### `LL_TIM_CC_DisablePreload`

```c
__STATIC_INLINE void LL_TIM_CC_DisablePreload (TIM_TypeDef * TIMx);
```

关闭TIM1 互补输出控制位预装载（CCxE、CCxNE、OCxM）。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L1386](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1386)。

### `LL_TIM_CC_SetUpdate`

```c
__STATIC_INLINE void LL_TIM_CC_SetUpdate (TIM_TypeDef * TIMx, uint32_t CCUpdateSource);
```

设置TIM1 预装载捕获比较控制位的 COM 更新来源。

- `TIMx`：选择 TIM1。
- `CCUpdateSource`：捕获比较控制位的 COM 更新来源，TIM1 专用。
  - 可用编码：`LL_TIM_CCUPDATESOURCE_COMG_ONLY`、`LL_TIM_CCUPDATESOURCE_COMG_AND_TRGI`。

- 适用实例：TIM1。

固定头文件：[接口定义L1402](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1402)。

### `LL_TIM_CC_SetDMAReqTrigger`

```c
__STATIC_INLINE void LL_TIM_CC_SetDMAReqTrigger (TIM_TypeDef * TIMx, uint32_t DMAReqTrigger);
```

设置捕获比较 DMA 请求来自 CC 事件或更新事件。这是CR2.CCDS共享位，影响该实例的CCx DMA请求时机；逐次输入捕获搬运需选CC事件，修改时须协调其他通道。请求选择不改变DMA物理连线或外设地址。

- `DMAReqTrigger`：CC DMA 由比较事件或更新事件请求。
  - 可用编码：`LL_TIM_CCDMAREQUEST_CC`、`LL_TIM_CCDMAREQUEST_UPDATE`。

固定头文件：[接口定义L1416](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1416)。

### `LL_TIM_CC_GetDMAReqTrigger`

```c
__STATIC_INLINE uint32_t LL_TIM_CC_GetDMAReqTrigger (TIM_TypeDef * TIMx);
```

读取捕获比较 DMA 请求来自 CC 事件或更新事件。

返回：uint32_t，返回编码：`LL_TIM_CCDMAREQUEST_CC`、`LL_TIM_CCDMAREQUEST_UPDATE`。

固定头文件：[接口定义L1429](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1429)。

### `LL_TIM_CC_SetLockLevel`

```c
__STATIC_INLINE void LL_TIM_CC_SetLockLevel (TIM_TypeDef * TIMx, uint32_t LockLevel);
```

设置TIM1 的 BDTR 配置写保护级别。

- `TIMx`：选择 TIM1。
- `LockLevel`：TIM1 LOCK OFF/1/2/3，锁定后仅复位可解除。
  - 可用编码：`LL_TIM_LOCKLEVEL_OFF`、`LL_TIM_LOCKLEVEL_1`、`LL_TIM_LOCKLEVEL_2`、`LL_TIM_LOCKLEVEL_3`。

- 适用实例：TIM1。

固定头文件：[接口定义L1448](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1448)。

### `LL_TIM_CC_EnableChannel`

```c
__STATIC_INLINE void LL_TIM_CC_EnableChannel (TIM_TypeDef * TIMx, uint32_t Channels);
```

使能指定捕获比较通道（输入捕获或输出比较，取决于CCxS）。

- `Channels`：捕获比较通道位掩码，可按 API 允许的值组合；互补通道仅 TIM1。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH1N`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH2N`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH3N`、`LL_TIM_CHANNEL_CH4`。

固定头文件：[接口定义L1473](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1473)。

### `LL_TIM_CC_DisableChannel`

```c
__STATIC_INLINE void LL_TIM_CC_DisableChannel (TIM_TypeDef * TIMx, uint32_t Channels);
```

关闭指定捕获比较通道（输入捕获或输出比较，取决于CCxS）。

- `Channels`：捕获比较通道位掩码，可按 API 允许的值组合；互补通道仅 TIM1。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH1N`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH2N`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH3N`、`LL_TIM_CHANNEL_CH4`。

固定头文件：[接口定义L1498](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1498)。

### `LL_TIM_CC_IsEnabledChannel`

```c
__STATIC_INLINE uint32_t LL_TIM_CC_IsEnabledChannel (TIM_TypeDef * TIMx, uint32_t Channels);
```

查询是否使能指定捕获比较通道（输入捕获或输出比较，取决于CCxS）。

- `Channels`：捕获比较通道位掩码，可按 API 允许的值组合；互补通道仅 TIM1。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH1N`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH2N`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH3N`、`LL_TIM_CHANNEL_CH4`。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L1523](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1523)。

补充核对：固定实现比较(CCER & Channels)==Channels；组合掩码要求所有所选位均置位才返回1。零掩码也会返回1，因此参数应为本接口允许的非空通道集合。此返回值只描述通道使能位，不证明MOE、计数器或实际引脚已开启。

## 输出比较与 PWM

### `LL_TIM_OC_ConfigOutput`

```c
__STATIC_INLINE void LL_TIM_OC_ConfigOutput (TIM_TypeDef * TIMx, uint32_t Channel, uint32_t Configuration);
```

将主通道配置为输出，组合设置输出极性和空闲电平。Channel 仅接受 CH1～CH4，不接受 CH1N～CH3N；空闲电平字段只对具有该功能的 TIM1 有意义。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。
- `Configuration`：组合配置位，按下面列出的本功能常量组合。
  - 每组各选一项后按位或：极性 `LL_TIM_OCPOLARITY_HIGH` 或 `LL_TIM_OCPOLARITY_LOW`；空闲状态 `LL_TIM_OCIDLESTATE_LOW` 或 `LL_TIM_OCIDLESTATE_HIGH`。

固定头文件：[接口定义L1560](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1560)。

补充核对：该内联函数没有先关闭CCxE。CCxS方向选择只在对应通道关闭时可写；重配前由调用方建立这一条件，另行处理TIM1的LOCK/CCPC约束。

### `LL_TIM_OC_SetMode`

```c
__STATIC_INLINE void LL_TIM_OC_SetMode (TIM_TypeDef * TIMx, uint32_t Channel, uint32_t Mode);
```

设置输出比较/PWM 的 OCxREF 模式。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。
- `Mode`：输出比较/PWM 工作模式。
  - 可用编码：`LL_TIM_OCMODE_FROZEN`、`LL_TIM_OCMODE_ACTIVE`、`LL_TIM_OCMODE_INACTIVE`、`LL_TIM_OCMODE_TOGGLE`、`LL_TIM_OCMODE_FORCED_INACTIVE`、`LL_TIM_OCMODE_FORCED_ACTIVE`、`LL_TIM_OCMODE_PWM1`、`LL_TIM_OCMODE_PWM2`。

固定头文件：[接口定义L1595](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1595)。

补充核对：固定实现修改掩码同时包含OCxM与CCxS，使用合法Mode时也请求把CCxS清为输出；函数没有先关闭通道。CCxS仅在CCxE=0时可写，LOCK/CCPC还会影响相关字段，不能把一次调用当作任意运行状态下已完成模式切换。

### `LL_TIM_OC_GetMode`

```c
__STATIC_INLINE uint32_t LL_TIM_OC_GetMode (TIM_TypeDef * TIMx, uint32_t Channel);
```

读取输出比较/PWM 的 OCxREF 模式。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

返回：uint32_t，返回编码：`LL_TIM_OCMODE_FROZEN`、`LL_TIM_OCMODE_ACTIVE`、`LL_TIM_OCMODE_INACTIVE`、`LL_TIM_OCMODE_TOGGLE`、`LL_TIM_OCMODE_FORCED_INACTIVE`、`LL_TIM_OCMODE_FORCED_ACTIVE`、`LL_TIM_OCMODE_PWM1`、`LL_TIM_OCMODE_PWM2`。

固定头文件：[接口定义L1624](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1624)。

补充核对：读取掩码同时包含OCxM与CCxS。只有通道处于输出选择CCxS=00时，才可按列出的输出模式枚举解释返回值；输入模式下共享位有输入滤波等其他含义，返回值可不属于此枚举。

### `LL_TIM_OC_SetPolarity`

```c
__STATIC_INLINE void LL_TIM_OC_SetPolarity (TIM_TypeDef * TIMx, uint32_t Channel, uint32_t Polarity);
```

设置指定输出的有效极性。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH1N`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH2N`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH3N`、`LL_TIM_CHANNEL_CH4`。
- `Polarity`：输出有效极性。
  - 可用编码：`LL_TIM_OCPOLARITY_HIGH`、`LL_TIM_OCPOLARITY_LOW`。

固定头文件：[接口定义L1654](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1654)。

### `LL_TIM_OC_GetPolarity`

```c
__STATIC_INLINE uint32_t LL_TIM_OC_GetPolarity (TIM_TypeDef * TIMx, uint32_t Channel);
```

读取指定输出的有效极性。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH1N`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH2N`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH3N`、`LL_TIM_CHANNEL_CH4`。

返回：uint32_t，返回编码：`LL_TIM_OCPOLARITY_HIGH`、`LL_TIM_OCPOLARITY_LOW`。

固定头文件：[接口定义L1682](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1682)。

### `LL_TIM_OC_SetIdleState`

```c
__STATIC_INLINE void LL_TIM_OC_SetIdleState (TIM_TypeDef * TIMx, uint32_t Channel, uint32_t IdleState);
```

设置TIM1 输出空闲电平。

- `TIMx`：选择 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH1N`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH2N`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH3N`、`LL_TIM_CHANNEL_CH4`。
- `IdleState`：TIM1 输出空闲态电平。
  - 可用编码：`LL_TIM_OCIDLESTATE_LOW`、`LL_TIM_OCIDLESTATE_HIGH`。

- 适用实例：TIM1。

固定头文件：[接口定义L1715](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1715)。

### `LL_TIM_OC_GetIdleState`

```c
__STATIC_INLINE uint32_t LL_TIM_OC_GetIdleState (TIM_TypeDef * TIMx, uint32_t Channel);
```

读取TIM1 输出空闲电平。

- `TIMx`：选择 TIM1。
- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH1N`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH2N`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH3N`、`LL_TIM_CHANNEL_CH4`。

返回：uint32_t，返回编码：`LL_TIM_OCIDLESTATE_LOW`、`LL_TIM_OCIDLESTATE_HIGH`。

- 适用实例：TIM1。

固定头文件：[接口定义L1743](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1743)。

### `LL_TIM_OC_EnableFast`

```c
__STATIC_INLINE void LL_TIM_OC_EnableFast (TIM_TypeDef * TIMx, uint32_t Channel);
```

使能PWM1/PWM2 快速响应模式。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

固定头文件：[接口定义L1764](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1764)。

### `LL_TIM_OC_DisableFast`

```c
__STATIC_INLINE void LL_TIM_OC_DisableFast (TIM_TypeDef * TIMx, uint32_t Channel);
```

关闭PWM1/PWM2 快速响应模式。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

固定头文件：[接口定义L1786](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1786)。

### `LL_TIM_OC_IsEnabledFast`

```c
__STATIC_INLINE uint32_t LL_TIM_OC_IsEnabledFast (TIM_TypeDef * TIMx, uint32_t Channel);
```

查询是否使能PWM1/PWM2 快速响应模式。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L1808](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1808)。

### `LL_TIM_OC_EnablePreload`

```c
__STATIC_INLINE void LL_TIM_OC_EnablePreload (TIM_TypeDef * TIMx, uint32_t Channel);
```

使能CCR 比较值预装载。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

固定头文件：[接口定义L1830](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1830)。

### `LL_TIM_OC_DisablePreload`

```c
__STATIC_INLINE void LL_TIM_OC_DisablePreload (TIM_TypeDef * TIMx, uint32_t Channel);
```

关闭CCR 比较值预装载。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

固定头文件：[接口定义L1851](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1851)。

### `LL_TIM_OC_IsEnabledPreload`

```c
__STATIC_INLINE uint32_t LL_TIM_OC_IsEnabledPreload (TIM_TypeDef * TIMx, uint32_t Channel);
```

查询是否使能CCR 比较值预装载。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L1872](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1872)。

### `LL_TIM_OC_EnableClear`

```c
__STATIC_INLINE void LL_TIM_OC_EnableClear (TIM_TypeDef * TIMx, uint32_t Channel);
```

使能外部事件清除 OCxREF 的功能。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

固定头文件：[接口定义L1897](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1897)。

### `LL_TIM_OC_DisableClear`

```c
__STATIC_INLINE void LL_TIM_OC_DisableClear (TIM_TypeDef * TIMx, uint32_t Channel);
```

关闭外部事件清除 OCxREF 的功能。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

固定头文件：[接口定义L1920](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1920)。

### `LL_TIM_OC_IsEnabledClear`

```c
__STATIC_INLINE uint32_t LL_TIM_OC_IsEnabledClear (TIM_TypeDef * TIMx, uint32_t Channel);
```

查询是否使能外部事件清除 OCxREF 的功能。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L1945](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1945)。

### `LL_TIM_OC_SetDeadTime`

```c
__STATIC_INLINE void LL_TIM_OC_SetDeadTime (TIM_TypeDef * TIMx, uint32_t DeadTime);
```

设置TIM1 死区 DTG 编码，范围 0–255。

- `TIMx`：选择 TIM1。
- `DeadTime`：TIM1 死区 DTG 非线性编码，0–255。

- 适用实例：TIM1。

固定头文件：[接口定义L1963](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1963)。

### `LL_TIM_OC_SetCompareCH1`

```c
__STATIC_INLINE void LL_TIM_OC_SetCompareCH1 (TIM_TypeDef * TIMx, uint32_t CompareValue);
```

设置输出通道 1 的 CCR1 比较值。

- `CompareValue`：CCR 比较值，0–65535。

固定头文件：[接口定义L1977](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1977)。

### `LL_TIM_OC_SetCompareCH2`

```c
__STATIC_INLINE void LL_TIM_OC_SetCompareCH2 (TIM_TypeDef * TIMx, uint32_t CompareValue);
```

设置输出通道 2 的 CCR2 比较值。

- `CompareValue`：CCR 比较值，0–65535。

固定头文件：[接口定义L1991](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L1991)。

### `LL_TIM_OC_SetCompareCH3`

```c
__STATIC_INLINE void LL_TIM_OC_SetCompareCH3 (TIM_TypeDef * TIMx, uint32_t CompareValue);
```

设置输出通道 3 的 CCR3 比较值。

- `CompareValue`：CCR 比较值，0–65535。

固定头文件：[接口定义L2005](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2005)。

### `LL_TIM_OC_SetCompareCH4`

```c
__STATIC_INLINE void LL_TIM_OC_SetCompareCH4 (TIM_TypeDef * TIMx, uint32_t CompareValue);
```

设置输出通道 4 的 CCR4 比较值。

- `CompareValue`：CCR 比较值，0–65535。

固定头文件：[接口定义L2019](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2019)。

### `LL_TIM_OC_GetCompareCH1`

```c
__STATIC_INLINE uint32_t LL_TIM_OC_GetCompareCH1 (TIM_TypeDef * TIMx);
```

读取输出通道1总线可见CCR1值，范围 0–65535；OC1PE=1时新预装载值可能尚未成为活动比较值。

返回：`uint32_t`，总线可见 CCR1 比较值，范围 0–65535。

固定头文件：[接口定义L2032](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2032)。

### `LL_TIM_OC_GetCompareCH2`

```c
__STATIC_INLINE uint32_t LL_TIM_OC_GetCompareCH2 (TIM_TypeDef * TIMx);
```

读取输出通道2总线可见CCR2值，范围 0–65535；OC2PE=1时新预装载值可能尚未成为活动比较值。

返回：`uint32_t`，总线可见 CCR2 比较值，范围 0–65535。

固定头文件：[接口定义L2045](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2045)。

### `LL_TIM_OC_GetCompareCH3`

```c
__STATIC_INLINE uint32_t LL_TIM_OC_GetCompareCH3 (TIM_TypeDef * TIMx);
```

读取输出通道3总线可见CCR3值，范围 0–65535；OC3PE=1时新预装载值可能尚未成为活动比较值。

返回：`uint32_t`，总线可见 CCR3 比较值，范围 0–65535。

固定头文件：[接口定义L2058](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2058)。

### `LL_TIM_OC_GetCompareCH4`

```c
__STATIC_INLINE uint32_t LL_TIM_OC_GetCompareCH4 (TIM_TypeDef * TIMx);
```

读取输出通道4总线可见CCR4值，范围 0–65535；OC4PE=1时新预装载值可能尚未成为活动比较值。

返回：`uint32_t`，总线可见 CCR4 比较值，范围 0–65535。

固定头文件：[接口定义L2071](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2071)。

## 输入捕获

### `LL_TIM_IC_Config`

```c
__STATIC_INLINE void LL_TIM_IC_Config (TIM_TypeDef * TIMx, uint32_t Channel, uint32_t Configuration);
```

组合配置输入通道的映射、滤波、预分频和极性。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。
- `Configuration`：以下四组各选一项，再按位或组合；同组编码互斥。
  - 输入映射：`LL_TIM_ACTIVEINPUT_DIRECTTI`、`LL_TIM_ACTIVEINPUT_INDIRECTTI` 或 `LL_TIM_ACTIVEINPUT_TRC`。
  - 预分频：`LL_TIM_ICPSC_DIV1`、`LL_TIM_ICPSC_DIV2`、`LL_TIM_ICPSC_DIV4` 或 `LL_TIM_ICPSC_DIV8`。
  - 滤波：[输入捕获滤波](LL符号表.md#输入捕获滤波)中的 16 档之一。
  - 极性：`LL_TIM_IC_POLARITY_RISING` 或 `LL_TIM_IC_POLARITY_FALLING`。

固定头文件：[接口定义L2117](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2117)。

补充核对：该内联函数没有先关闭CCxE，也不会像结构式LL_TIM_IC_Init那样在末尾启用通道。配置CCxS前须由调用方关闭对应通道，并遵守寄存器写入限制。

### `LL_TIM_IC_SetActiveInput`

```c
__STATIC_INLINE void LL_TIM_IC_SetActiveInput (TIM_TypeDef * TIMx, uint32_t Channel, uint32_t ICActiveInput);
```

设置输入捕获的直接、间接或 TRC 映射。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。
- `ICActiveInput`：输入直接 TI、间接 TI 或 TRC。
  - 可用编码：`LL_TIM_ACTIVEINPUT_DIRECTTI`、`LL_TIM_ACTIVEINPUT_INDIRECTTI`、`LL_TIM_ACTIVEINPUT_TRC`。

固定头文件：[接口定义L2145](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2145)。

补充核对：函数不先关闭通道；CCxS只在CCxE=0时可写。返回void不能证明运行中的输入路由已被硬件接受。

### `LL_TIM_IC_GetActiveInput`

```c
__STATIC_INLINE uint32_t LL_TIM_IC_GetActiveInput (TIM_TypeDef * TIMx, uint32_t Channel);
```

读取输入捕获的直接、间接或 TRC 映射。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

返回：uint32_t，返回编码：`LL_TIM_ACTIVEINPUT_DIRECTTI`、`LL_TIM_ACTIVEINPUT_INDIRECTTI`、`LL_TIM_ACTIVEINPUT_TRC`。

固定头文件：[接口定义L2169](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2169)。

### `LL_TIM_IC_SetPrescaler`

```c
__STATIC_INLINE void LL_TIM_IC_SetPrescaler (TIM_TypeDef * TIMx, uint32_t Channel, uint32_t ICPrescaler);
```

设置输入捕获事件预分频，每 1/2/4/8 次有效事件捕获一次。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。
- `ICPrescaler`：输入捕获事件分频 1/2/4/8。
  - 可用编码：`LL_TIM_ICPSC_DIV1`、`LL_TIM_ICPSC_DIV2`、`LL_TIM_ICPSC_DIV4`、`LL_TIM_ICPSC_DIV8`。

固定头文件：[接口定义L2195](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2195)。

### `LL_TIM_IC_GetPrescaler`

```c
__STATIC_INLINE uint32_t LL_TIM_IC_GetPrescaler (TIM_TypeDef * TIMx, uint32_t Channel);
```

读取输入捕获事件预分频，每 1/2/4/8 次有效事件捕获一次。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

返回：uint32_t，返回编码：`LL_TIM_ICPSC_DIV1`、`LL_TIM_ICPSC_DIV2`、`LL_TIM_ICPSC_DIV4`、`LL_TIM_ICPSC_DIV8`。

固定头文件：[接口定义L2220](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2220)。

### `LL_TIM_IC_SetFilter`

```c
__STATIC_INLINE void LL_TIM_IC_SetFilter (TIM_TypeDef * TIMx, uint32_t Channel, uint32_t ICFilter);
```

设置输入捕获数字滤波采样频率与连续样本数。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。
- `ICFilter`：数字滤波编码，采样分频及连续一致样本数见常量。
  - 可用编码见[输入捕获滤波](LL符号表.md#输入捕获滤波)。

固定头文件：[接口定义L2258](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2258)。

### `LL_TIM_IC_GetFilter`

```c
__STATIC_INLINE uint32_t LL_TIM_IC_GetFilter (TIM_TypeDef * TIMx, uint32_t Channel);
```

读取输入捕获数字滤波采样频率与连续样本数。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

返回：uint32_t，字段编码见[输入捕获滤波](LL符号表.md#输入捕获滤波)。

固定头文件：[接口定义L2295](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2295)。

### `LL_TIM_IC_SetPolarity`

```c
__STATIC_INLINE void LL_TIM_IC_SetPolarity (TIM_TypeDef * TIMx, uint32_t Channel, uint32_t ICPolarity);
```

设置输入捕获有效边沿。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。
- `ICPolarity`：输入有效边沿，RISING 或 FALLING。
  - 可用编码：`LL_TIM_IC_POLARITY_RISING`、`LL_TIM_IC_POLARITY_FALLING`。

固定头文件：[接口定义L2322](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2322)。

### `LL_TIM_IC_GetPolarity`

```c
__STATIC_INLINE uint32_t LL_TIM_IC_GetPolarity (TIM_TypeDef * TIMx, uint32_t Channel);
```

读取输入捕获有效边沿。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。

返回：uint32_t，返回编码：`LL_TIM_IC_POLARITY_RISING`、`LL_TIM_IC_POLARITY_FALLING`。

固定头文件：[接口定义L2348](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2348)。

### `LL_TIM_IC_EnableXORCombination`

```c
__STATIC_INLINE void LL_TIM_IC_EnableXORCombination (TIM_TypeDef * TIMx);
```

使能CH1、CH2、CH3 异或连接到 TI1。

固定头文件：[接口定义L2363](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2363)。

### `LL_TIM_IC_DisableXORCombination`

```c
__STATIC_INLINE void LL_TIM_IC_DisableXORCombination (TIM_TypeDef * TIMx);
```

关闭CH1、CH2、CH3 异或连接到 TI1。

固定头文件：[接口定义L2376](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2376)。

### `LL_TIM_IC_IsEnabledXORCombination`

```c
__STATIC_INLINE uint32_t LL_TIM_IC_IsEnabledXORCombination (TIM_TypeDef * TIMx);
```

查询是否使能CH1、CH2、CH3 异或连接到 TI1。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L2389](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2389)。

### `LL_TIM_IC_GetCaptureCH1`

```c
__STATIC_INLINE uint32_t LL_TIM_IC_GetCaptureCH1 (TIM_TypeDef * TIMx);
```

读取输入通道 1 最近锁存的 CCR1 捕获值；应用还应检查过捕获标志，读值函数本身不检查该标志。但 [ES096](https://www.st.com/resource/en/errata_sheet/es096-stm32f101x8b-stm32f102x8b-and-stm32f103x8b-mediumdensity-device-limitations-stmicroelectronics.pdf) §2.6.5/§2.6.6 规定捕获与 CCR 读取竞争时可能漏报或误报，CCxOF 不能作为完整无丢样证明。

返回：`uint32_t`，CCR1 捕获值，范围 0–65535。

固定头文件：[接口定义L2402](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2402)。

补充核对：在输入捕获模式下，读取CCR1会清除对应CC1IF；该读操作有状态副作用，不能当作不改变标志的纯观察。它不自动检查CC1OF，也不能排除ES096所列捕获/读取竞争。

### `LL_TIM_IC_GetCaptureCH2`

```c
__STATIC_INLINE uint32_t LL_TIM_IC_GetCaptureCH2 (TIM_TypeDef * TIMx);
```

读取输入通道 2 最近锁存的 CCR2 捕获值；应用还应检查过捕获标志，读值函数本身不检查该标志。但 [ES096](https://www.st.com/resource/en/errata_sheet/es096-stm32f101x8b-stm32f102x8b-and-stm32f103x8b-mediumdensity-device-limitations-stmicroelectronics.pdf) §2.6.5/§2.6.6 规定捕获与 CCR 读取竞争时可能漏报或误报，CCxOF 不能作为完整无丢样证明。

返回：`uint32_t`，CCR2 捕获值，范围 0–65535。

固定头文件：[接口定义L2415](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2415)。

补充核对：在输入捕获模式下，读取CCR2会清除对应CC2IF；该读操作有状态副作用，不能当作不改变标志的纯观察。它不自动检查CC2OF，也不能排除ES096所列捕获/读取竞争。

### `LL_TIM_IC_GetCaptureCH3`

```c
__STATIC_INLINE uint32_t LL_TIM_IC_GetCaptureCH3 (TIM_TypeDef * TIMx);
```

读取输入通道 3 最近锁存的 CCR3 捕获值；应用还应检查过捕获标志，读值函数本身不检查该标志。但 [ES096](https://www.st.com/resource/en/errata_sheet/es096-stm32f101x8b-stm32f102x8b-and-stm32f103x8b-mediumdensity-device-limitations-stmicroelectronics.pdf) §2.6.5/§2.6.6 规定捕获与 CCR 读取竞争时可能漏报或误报，CCxOF 不能作为完整无丢样证明。

返回：`uint32_t`，CCR3 捕获值，范围 0–65535。

固定头文件：[接口定义L2428](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2428)。

补充核对：在输入捕获模式下，读取CCR3会清除对应CC3IF；该读操作有状态副作用，不能当作不改变标志的纯观察。它不自动检查CC3OF，也不能排除ES096所列捕获/读取竞争。

### `LL_TIM_IC_GetCaptureCH4`

```c
__STATIC_INLINE uint32_t LL_TIM_IC_GetCaptureCH4 (TIM_TypeDef * TIMx);
```

读取输入通道 4 最近锁存的 CCR4 捕获值；应用还应检查过捕获标志，读值函数本身不检查该标志。但 [ES096](https://www.st.com/resource/en/errata_sheet/es096-stm32f101x8b-stm32f102x8b-and-stm32f103x8b-mediumdensity-device-limitations-stmicroelectronics.pdf) §2.6.5/§2.6.6 规定捕获与 CCR 读取竞争时可能漏报或误报，CCxOF 不能作为完整无丢样证明。

返回：`uint32_t`，CCR4 捕获值，范围 0–65535。

固定头文件：[接口定义L2441](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2441)。

补充核对：在输入捕获模式下，读取CCR4会清除对应CC4IF；该读操作有状态副作用，不能当作不改变标志的纯观察。它不自动检查CC4OF，也不能排除ES096所列捕获/读取竞争。

## 外部时钟与同步

### `LL_TIM_EnableExternalClock`

```c
__STATIC_INLINE void LL_TIM_EnableExternalClock (TIM_TypeDef * TIMx);
```

使能ETR 外部时钟模式 2。

固定头文件：[接口定义L2462](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2462)。

### `LL_TIM_DisableExternalClock`

```c
__STATIC_INLINE void LL_TIM_DisableExternalClock (TIM_TypeDef * TIMx);
```

关闭ETR 外部时钟模式 2。

固定头文件：[接口定义L2475](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2475)。

### `LL_TIM_IsEnabledExternalClock`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledExternalClock (TIM_TypeDef * TIMx);
```

查询是否使能ETR 外部时钟模式 2。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L2488](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2488)。

### `LL_TIM_SetClockSource`

```c
__STATIC_INLINE void LL_TIM_SetClockSource (TIM_TypeDef * TIMx, uint32_t ClockSource);
```

设置计数器内部或外部时钟来源。固定实现的修改掩码同时包含SMCR.SMS与ECE：INTERNAL将两者清零；EXT_MODE1设置SMS=111并清ECE；EXT_MODE2设置ECE并清SMS。因此在已经配置复位/门控/触发从模式后调用它，会覆盖原SMS选择；需要组合时钟与从模式时，应在停止且消费者隔离条件下规划设置次序，再按允许的硬件组合建立最终SMS。选择外部模式1后还须用 LL_TIM_SetTriggerInput 选择 TRGI；TI捕获输入由 LL_TIM_IC_Config 配置，ETR路径则用 LL_TIM_ConfigETR，不能仅调用本函数就假定引脚/滤波已完成。

- `ClockSource`：内部、外部模式 1 或外部模式 2 的计数时钟。
  - 可用编码：`LL_TIM_CLOCKSOURCE_INTERNAL`、`LL_TIM_CLOCKSOURCE_EXT_MODE1`、`LL_TIM_CLOCKSOURCE_EXT_MODE2`。

固定头文件：[接口定义L2512](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2512)。

### `LL_TIM_SetEncoderMode`

```c
__STATIC_INLINE void LL_TIM_SetEncoderMode (TIM_TypeDef * TIMx, uint32_t EncoderMode);
```

设置TI1、TI2 或双输入编码器计数方式。固定实现只修改SMCR.SMS，不清ECE；进入编码器模式前须排除遗留外部时钟模式2，不能认为本入口完成全部时钟切换。符号后缀与实际计数输入的历史差异见[编码器符号核查](LL辅助宏.md#编码器-x2-模式的文档符号冲突)。

- `EncoderMode`：编码器 x2 TI1、x2 TI2 或 x4 TI12。
  - 可用编码：`LL_TIM_ENCODERMODE_X2_TI1`、`LL_TIM_ENCODERMODE_X2_TI2`、`LL_TIM_ENCODERMODE_X4_TI12`。

固定头文件：[接口定义L2529](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2529)。

### `LL_TIM_SetTriggerOutput`

```c
__STATIC_INLINE void LL_TIM_SetTriggerOutput (TIM_TypeDef * TIMx, uint32_t TimerSynchronization);
```

设置供其他外设使用的 TRGO 输出来源。

- `TimerSynchronization`：TRGO 来源。
  - 可用编码：`LL_TIM_TRGO_RESET`、`LL_TIM_TRGO_ENABLE`、`LL_TIM_TRGO_UPDATE`、`LL_TIM_TRGO_CC1IF`、`LL_TIM_TRGO_OC1REF`、`LL_TIM_TRGO_OC2REF`、`LL_TIM_TRGO_OC3REF`、`LL_TIM_TRGO_OC4REF`。

固定头文件：[接口定义L2558](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2558)。

### `LL_TIM_SetSlaveMode`

```c
__STATIC_INLINE void LL_TIM_SetSlaveMode (TIM_TypeDef * TIMx, uint32_t SlaveMode);
```

设置定时器从模式。固定实现只修改SMCR.SMS，保留ECE；选择DISABLED不自动关闭外部时钟模式2，也不单独隔离TIM1的TRGI→COM消费路径。

- `SlaveMode`：从模式选择。
  - 可用编码：`LL_TIM_SLAVEMODE_DISABLED`、`LL_TIM_SLAVEMODE_RESET`、`LL_TIM_SLAVEMODE_GATED`、`LL_TIM_SLAVEMODE_TRIGGER`。

固定头文件：[接口定义L2576](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2576)。

### `LL_TIM_SetTriggerInput`

```c
__STATIC_INLINE void LL_TIM_SetTriggerInput (TIM_TypeDef * TIMx, uint32_t TriggerInput);
```

设置TRGI触发输入来源。固定实现只修改SMCR.TS，不暂停计数或隔离消费者。RM0008 Rev21 p343要求TS仅在未被使用时改变，以免切换时误检测边沿；SMS=000只是手册给出的例子，TIM1还须核对CCUS控制的TRGI→COM路径。

- `TriggerInput`：TRGI 来源；ITR 实际连线取决于定时器实例。
  - 可用编码：`LL_TIM_TS_ITR0`、`LL_TIM_TS_ITR1`、`LL_TIM_TS_ITR2`、`LL_TIM_TS_ITR3`、`LL_TIM_TS_TI1F_ED`、`LL_TIM_TS_TI1FP1`、`LL_TIM_TS_TI2FP2`、`LL_TIM_TS_ETRF`。

固定头文件：[接口定义L2598](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2598)。

### `LL_TIM_EnableMasterSlaveMode`

```c
__STATIC_INLINE void LL_TIM_EnableMasterSlaveMode (TIM_TypeDef * TIMx);
```

使能主从同步模式 MSM。

固定头文件：[接口定义L2611](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2611)。

### `LL_TIM_DisableMasterSlaveMode`

```c
__STATIC_INLINE void LL_TIM_DisableMasterSlaveMode (TIM_TypeDef * TIMx);
```

关闭主从同步模式 MSM。

固定头文件：[接口定义L2624](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2624)。

### `LL_TIM_IsEnabledMasterSlaveMode`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledMasterSlaveMode (TIM_TypeDef * TIMx);
```

查询是否使能主从同步模式 MSM。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L2637](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2637)。

### `LL_TIM_ConfigETR`

```c
__STATIC_INLINE void LL_TIM_ConfigETR (TIM_TypeDef * TIMx, uint32_t ETRPolarity, uint32_t ETRPrescaler, uint32_t ETRFilter);
```

组合配置 ETR 极性、预分频和滤波；ETR 引脚实际可用性还取决于封装与 AFIO 重映射。

- `ETRPolarity`：ETR 反相或不反相。
  - 可用编码：`LL_TIM_ETR_POLARITY_NONINVERTED`、`LL_TIM_ETR_POLARITY_INVERTED`。
- `ETRPrescaler`：ETR 预分频 1/2/4/8。
  - 可用编码：`LL_TIM_ETR_PRESCALER_DIV1`、`LL_TIM_ETR_PRESCALER_DIV2`、`LL_TIM_ETR_PRESCALER_DIV4`、`LL_TIM_ETR_PRESCALER_DIV8`。
- `ETRFilter`：数字滤波编码，采样分频及连续一致样本数见常量。
  - 可用编码见[ETR 滤波](LL符号表.md#etr-滤波)。

固定头文件：[接口定义L2677](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2677)。

## 刹车与输出保护

### `LL_TIM_EnableBRK`

```c
__STATIC_INLINE void LL_TIM_EnableBRK (TIM_TypeDef * TIMx);
```

使能TIM1 刹车输入使能。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L2698](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2698)。

### `LL_TIM_DisableBRK`

```c
__STATIC_INLINE void LL_TIM_DisableBRK (TIM_TypeDef * TIMx);
```

关闭TIM1 刹车输入使能。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L2715](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2715)。

### `LL_TIM_ConfigBRK`

```c
__STATIC_INLINE void LL_TIM_ConfigBRK (TIM_TypeDef * TIMx, uint32_t BreakPolarity);
```

设置 TIM1 刹车输入极性；刹车使能另由 EnableBRK 控制。

- `TIMx`：选择 TIM1。
- `BreakPolarity`：TIM1 BKIN 有效极性。
  - 可用编码：`LL_TIM_BREAK_POLARITY_LOW`、`LL_TIM_BREAK_POLARITY_HIGH`。

- 适用实例：TIM1。

固定头文件：[接口定义L2735](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2735)。

### `LL_TIM_SetOffStates`

```c
__STATIC_INLINE void LL_TIM_SetOffStates (TIM_TypeDef * TIMx, uint32_t OffStateIdle, uint32_t OffStateRun);
```

配置 TIM1 的运行关闭态 OSSR 与空闲关闭态 OSSI；LOCK 生效后可能不可修改。

- `TIMx`：选择 TIM1。
- `OffStateIdle`：TIM1 空闲关闭态 OSSI。
  - 可用编码：`LL_TIM_OSSI_DISABLE`、`LL_TIM_OSSI_ENABLE`。
- `OffStateRun`：TIM1 运行关闭态 OSSR。
  - 可用编码：`LL_TIM_OSSR_DISABLE`、`LL_TIM_OSSR_ENABLE`。

- 适用实例：TIM1。

固定头文件：[接口定义L2759](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2759)。

### `LL_TIM_EnableAutomaticOutput`

```c
__STATIC_INLINE void LL_TIM_EnableAutomaticOutput (TIM_TypeDef * TIMx);
```

设置TIM1的AOE，允许在刹车输入无效且满足条件的更新事件自动置MOE；不要求此前发生过刹车。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L2772](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2772)。

AOE字段允许在刹车无效时的UEV自动置MOE，不要求此前必须发生过刹车。关闭AOE不自动清MOE；读取AOE也不等于读取MOE或引脚状态。
### `LL_TIM_DisableAutomaticOutput`

```c
__STATIC_INLINE void LL_TIM_DisableAutomaticOutput (TIM_TypeDef * TIMx);
```

清TIM1的AOE，关闭更新事件自动置MOE的路径；受LOCK写保护条件约束。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L2785](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2785)。

AOE字段允许在刹车无效时的UEV自动置MOE，不要求此前必须发生过刹车。关闭AOE不自动清MOE；读取AOE也不等于读取MOE或引脚状态。
### `LL_TIM_IsEnabledAutomaticOutput`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledAutomaticOutput (TIM_TypeDef * TIMx);
```

查询TIM1的AOE使能位；返回值不单独表示MOE当前状态或实际输出电平。

- `TIMx`：选择 TIM1。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

- 适用实例：TIM1。

固定头文件：[接口定义L2798](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2798)。

AOE字段允许在刹车无效时的UEV自动置MOE，不要求此前必须发生过刹车。关闭AOE不自动清MOE；读取AOE也不等于读取MOE或引脚状态。
### `LL_TIM_EnableAllOutputs`

```c
__STATIC_INLINE void LL_TIM_EnableAllOutputs (TIM_TypeDef * TIMx);
```

使能TIM1 主输出总使能 MOE。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L2813](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2813)。

实现仅置BDTR.MOE，不替代CCxE/CCxNE、GPIO或计数器配置；有效刹车下不能保证MOE置1，读回还受同步延迟影响。
### `LL_TIM_DisableAllOutputs`

```c
__STATIC_INLINE void LL_TIM_DisableAllOutputs (TIM_TypeDef * TIMx);
```

关闭TIM1 主输出总使能 MOE。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L2828](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2828)。

实现仅清BDTR.MOE，保留AOE、CEN及CCER等配置。AOE=1且刹车无效时，后续UEV仍可重新置MOE，因此单独调用本接口不构成持续锁定关断。MOE=0时引脚还受OSSI/OIS和极性影响，见[输出保护](输出级与保护.md)。
### `LL_TIM_IsEnabledAllOutputs`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledAllOutputs (TIM_TypeDef * TIMx);
```

查询是否使能TIM1 主输出总使能 MOE。

- `TIMx`：选择 TIM1。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

- 适用实例：TIM1。

固定头文件：[接口定义L2841](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2841)。

此查询只测试BDTR.MOE；不检查每个CCxE/CCxNE，也不读取GPIO引脚，返回1不能证明所有通道正在输出，返回0不能证明所有引脚为低。
## DMA burst

### `LL_TIM_ConfigDMABurst`

```c
__STATIC_INLINE void LL_TIM_ConfigDMABurst (TIM_TypeDef * TIMx, uint32_t DMABurstBaseAddress, uint32_t DMABurstLength);
```

配置 DMA 突发起始寄存器和 1–18 项突发长度；访问应落在实例实际存在的寄存器范围内。

- `DMABurstBaseAddress`：DMA 突发起始寄存器编码，非绝对内存地址。
  - 可用编码见[DMA burst 起始寄存器](LL符号表.md#dma-burst-起始寄存器)。
- `DMABurstLength`：DMA 突发长度编码，1–18 次寄存器传输；不得当作未经编码的任意整数。
  - 可用编码见[DMA burst 长度](LL符号表.md#dma-burst-长度)。

固定头文件：[接口定义L2900](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2900)。

## 事件标志

### `LL_TIM_ClearFlag_UPDATE`

```c
__STATIC_INLINE void LL_TIM_ClearFlag_UPDATE (TIM_TypeDef * TIMx);
```

清除更新状态标志。

固定头文件：[接口定义L2923](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2923)。

### `LL_TIM_IsActiveFlag_UPDATE`

```c
__STATIC_INLINE uint32_t LL_TIM_IsActiveFlag_UPDATE (TIM_TypeDef * TIMx);
```

查询更新标志是否置位。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L2934](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2934)。

### `LL_TIM_ClearFlag_CC1`

```c
__STATIC_INLINE void LL_TIM_ClearFlag_CC1 (TIM_TypeDef * TIMx);
```

清除通道 1 捕获比较状态标志。

固定头文件：[接口定义L2945](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2945)。

### `LL_TIM_IsActiveFlag_CC1`

```c
__STATIC_INLINE uint32_t LL_TIM_IsActiveFlag_CC1 (TIM_TypeDef * TIMx);
```

查询通道 1 捕获比较标志是否置位。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L2956](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2956)。

### `LL_TIM_ClearFlag_CC2`

```c
__STATIC_INLINE void LL_TIM_ClearFlag_CC2 (TIM_TypeDef * TIMx);
```

清除通道 2 捕获比较状态标志。

固定头文件：[接口定义L2967](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2967)。

### `LL_TIM_IsActiveFlag_CC2`

```c
__STATIC_INLINE uint32_t LL_TIM_IsActiveFlag_CC2 (TIM_TypeDef * TIMx);
```

查询通道 2 捕获比较标志是否置位。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L2978](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2978)。

### `LL_TIM_ClearFlag_CC3`

```c
__STATIC_INLINE void LL_TIM_ClearFlag_CC3 (TIM_TypeDef * TIMx);
```

清除通道 3 捕获比较状态标志。

固定头文件：[接口定义L2989](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L2989)。

### `LL_TIM_IsActiveFlag_CC3`

```c
__STATIC_INLINE uint32_t LL_TIM_IsActiveFlag_CC3 (TIM_TypeDef * TIMx);
```

查询通道 3 捕获比较标志是否置位。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3000](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3000)。

### `LL_TIM_ClearFlag_CC4`

```c
__STATIC_INLINE void LL_TIM_ClearFlag_CC4 (TIM_TypeDef * TIMx);
```

清除通道 4 捕获比较状态标志。

固定头文件：[接口定义L3011](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3011)。

### `LL_TIM_IsActiveFlag_CC4`

```c
__STATIC_INLINE uint32_t LL_TIM_IsActiveFlag_CC4 (TIM_TypeDef * TIMx);
```

查询通道 4 捕获比较标志是否置位。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3022](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3022)。

### `LL_TIM_ClearFlag_COM`

```c
__STATIC_INLINE void LL_TIM_ClearFlag_COM (TIM_TypeDef * TIMx);
```

清除TIM1 换相状态标志。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L3033](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3033)。

### `LL_TIM_IsActiveFlag_COM`

```c
__STATIC_INLINE uint32_t LL_TIM_IsActiveFlag_COM (TIM_TypeDef * TIMx);
```

查询TIM1 换相标志是否置位。

- `TIMx`：选择 TIM1。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

- 适用实例：TIM1。

固定头文件：[接口定义L3044](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3044)。

### `LL_TIM_ClearFlag_TRIG`

```c
__STATIC_INLINE void LL_TIM_ClearFlag_TRIG (TIM_TypeDef * TIMx);
```

清除触发状态标志。

固定头文件：[接口定义L3055](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3055)。

### `LL_TIM_IsActiveFlag_TRIG`

```c
__STATIC_INLINE uint32_t LL_TIM_IsActiveFlag_TRIG (TIM_TypeDef * TIMx);
```

查询触发标志是否置位。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3066](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3066)。

### `LL_TIM_ClearFlag_BRK`

```c
__STATIC_INLINE void LL_TIM_ClearFlag_BRK (TIM_TypeDef * TIMx);
```

清除TIM1 刹车状态标志。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L3077](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3077)。

### `LL_TIM_IsActiveFlag_BRK`

```c
__STATIC_INLINE uint32_t LL_TIM_IsActiveFlag_BRK (TIM_TypeDef * TIMx);
```

查询TIM1 刹车标志是否置位。

- `TIMx`：选择 TIM1。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

- 适用实例：TIM1。

固定头文件：[接口定义L3088](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3088)。

### `LL_TIM_ClearFlag_CC1OVR`

```c
__STATIC_INLINE void LL_TIM_ClearFlag_CC1OVR (TIM_TypeDef * TIMx);
```

清除通道 1 过捕获状态标志。

固定头文件：[接口定义L3099](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3099)。

### `LL_TIM_IsActiveFlag_CC1OVR`

```c
__STATIC_INLINE uint32_t LL_TIM_IsActiveFlag_CC1OVR (TIM_TypeDef * TIMx);
```

查询通道 1 过捕获标志是否置位。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3110](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3110)。

### `LL_TIM_ClearFlag_CC2OVR`

```c
__STATIC_INLINE void LL_TIM_ClearFlag_CC2OVR (TIM_TypeDef * TIMx);
```

清除通道 2 过捕获状态标志。

固定头文件：[接口定义L3121](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3121)。

### `LL_TIM_IsActiveFlag_CC2OVR`

```c
__STATIC_INLINE uint32_t LL_TIM_IsActiveFlag_CC2OVR (TIM_TypeDef * TIMx);
```

查询通道 2 过捕获标志是否置位。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3132](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3132)。

### `LL_TIM_ClearFlag_CC3OVR`

```c
__STATIC_INLINE void LL_TIM_ClearFlag_CC3OVR (TIM_TypeDef * TIMx);
```

清除通道 3 过捕获状态标志。

固定头文件：[接口定义L3143](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3143)。

### `LL_TIM_IsActiveFlag_CC3OVR`

```c
__STATIC_INLINE uint32_t LL_TIM_IsActiveFlag_CC3OVR (TIM_TypeDef * TIMx);
```

查询通道 3 过捕获标志是否置位。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3154](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3154)。

### `LL_TIM_ClearFlag_CC4OVR`

```c
__STATIC_INLINE void LL_TIM_ClearFlag_CC4OVR (TIM_TypeDef * TIMx);
```

清除通道 4 过捕获状态标志。

固定头文件：[接口定义L3165](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3165)。

### `LL_TIM_IsActiveFlag_CC4OVR`

```c
__STATIC_INLINE uint32_t LL_TIM_IsActiveFlag_CC4OVR (TIM_TypeDef * TIMx);
```

查询通道 4 过捕获标志是否置位。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3176](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3176)。

## 中断使能

### `LL_TIM_EnableIT_UPDATE`

```c
__STATIC_INLINE void LL_TIM_EnableIT_UPDATE (TIM_TypeDef * TIMx);
```

开放更新中断。

固定头文件：[接口定义L3194](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3194)。

### `LL_TIM_DisableIT_UPDATE`

```c
__STATIC_INLINE void LL_TIM_DisableIT_UPDATE (TIM_TypeDef * TIMx);
```

关闭更新中断。

固定头文件：[接口定义L3205](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3205)。

### `LL_TIM_IsEnabledIT_UPDATE`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledIT_UPDATE (TIM_TypeDef * TIMx);
```

查询更新中断是否开放。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3216](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3216)。

### `LL_TIM_EnableIT_CC1`

```c
__STATIC_INLINE void LL_TIM_EnableIT_CC1 (TIM_TypeDef * TIMx);
```

开放通道 1 捕获比较中断。

固定头文件：[接口定义L3227](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3227)。

### `LL_TIM_DisableIT_CC1`

```c
__STATIC_INLINE void LL_TIM_DisableIT_CC1 (TIM_TypeDef * TIMx);
```

关闭通道 1 捕获比较中断。

固定头文件：[接口定义L3238](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3238)。

### `LL_TIM_IsEnabledIT_CC1`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledIT_CC1 (TIM_TypeDef * TIMx);
```

查询通道 1 捕获比较中断是否开放。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3249](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3249)。

### `LL_TIM_EnableIT_CC2`

```c
__STATIC_INLINE void LL_TIM_EnableIT_CC2 (TIM_TypeDef * TIMx);
```

开放通道 2 捕获比较中断。

固定头文件：[接口定义L3260](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3260)。

### `LL_TIM_DisableIT_CC2`

```c
__STATIC_INLINE void LL_TIM_DisableIT_CC2 (TIM_TypeDef * TIMx);
```

关闭通道 2 捕获比较中断。

固定头文件：[接口定义L3271](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3271)。

### `LL_TIM_IsEnabledIT_CC2`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledIT_CC2 (TIM_TypeDef * TIMx);
```

查询通道 2 捕获比较中断是否开放。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3282](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3282)。

### `LL_TIM_EnableIT_CC3`

```c
__STATIC_INLINE void LL_TIM_EnableIT_CC3 (TIM_TypeDef * TIMx);
```

开放通道 3 捕获比较中断。

固定头文件：[接口定义L3293](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3293)。

### `LL_TIM_DisableIT_CC3`

```c
__STATIC_INLINE void LL_TIM_DisableIT_CC3 (TIM_TypeDef * TIMx);
```

关闭通道 3 捕获比较中断。

固定头文件：[接口定义L3304](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3304)。

### `LL_TIM_IsEnabledIT_CC3`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledIT_CC3 (TIM_TypeDef * TIMx);
```

查询通道 3 捕获比较中断是否开放。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3315](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3315)。

### `LL_TIM_EnableIT_CC4`

```c
__STATIC_INLINE void LL_TIM_EnableIT_CC4 (TIM_TypeDef * TIMx);
```

开放通道 4 捕获比较中断。

固定头文件：[接口定义L3326](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3326)。

### `LL_TIM_DisableIT_CC4`

```c
__STATIC_INLINE void LL_TIM_DisableIT_CC4 (TIM_TypeDef * TIMx);
```

关闭通道 4 捕获比较中断。

固定头文件：[接口定义L3337](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3337)。

### `LL_TIM_IsEnabledIT_CC4`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledIT_CC4 (TIM_TypeDef * TIMx);
```

查询通道 4 捕获比较中断是否开放。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3348](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3348)。

### `LL_TIM_EnableIT_COM`

```c
__STATIC_INLINE void LL_TIM_EnableIT_COM (TIM_TypeDef * TIMx);
```

开放TIM1 换相中断。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L3359](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3359)。

### `LL_TIM_DisableIT_COM`

```c
__STATIC_INLINE void LL_TIM_DisableIT_COM (TIM_TypeDef * TIMx);
```

关闭TIM1 换相中断。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L3370](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3370)。

### `LL_TIM_IsEnabledIT_COM`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledIT_COM (TIM_TypeDef * TIMx);
```

查询TIM1 换相中断是否开放。

- `TIMx`：选择 TIM1。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

- 适用实例：TIM1。

固定头文件：[接口定义L3381](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3381)。

### `LL_TIM_EnableIT_TRIG`

```c
__STATIC_INLINE void LL_TIM_EnableIT_TRIG (TIM_TypeDef * TIMx);
```

开放触发中断。

固定头文件：[接口定义L3392](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3392)。

### `LL_TIM_DisableIT_TRIG`

```c
__STATIC_INLINE void LL_TIM_DisableIT_TRIG (TIM_TypeDef * TIMx);
```

关闭触发中断。

固定头文件：[接口定义L3403](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3403)。

### `LL_TIM_IsEnabledIT_TRIG`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledIT_TRIG (TIM_TypeDef * TIMx);
```

查询触发中断是否开放。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3414](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3414)。

### `LL_TIM_EnableIT_BRK`

```c
__STATIC_INLINE void LL_TIM_EnableIT_BRK (TIM_TypeDef * TIMx);
```

开放TIM1 刹车中断。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L3425](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3425)。

### `LL_TIM_DisableIT_BRK`

```c
__STATIC_INLINE void LL_TIM_DisableIT_BRK (TIM_TypeDef * TIMx);
```

关闭TIM1 刹车中断。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L3436](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3436)。

### `LL_TIM_IsEnabledIT_BRK`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledIT_BRK (TIM_TypeDef * TIMx);
```

查询TIM1 刹车中断是否开放。

- `TIMx`：选择 TIM1。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

- 适用实例：TIM1。

固定头文件：[接口定义L3447](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3447)。

## DMA 请求使能

### `LL_TIM_EnableDMAReq_UPDATE`

```c
__STATIC_INLINE void LL_TIM_EnableDMAReq_UPDATE (TIM_TypeDef * TIMx);
```

开放更新 DMA 请求。

固定头文件：[接口定义L3465](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3465)。

### `LL_TIM_DisableDMAReq_UPDATE`

```c
__STATIC_INLINE void LL_TIM_DisableDMAReq_UPDATE (TIM_TypeDef * TIMx);
```

关闭更新 DMA 请求。

固定头文件：[接口定义L3476](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3476)。

### `LL_TIM_IsEnabledDMAReq_UPDATE`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledDMAReq_UPDATE (TIM_TypeDef * TIMx);
```

查询更新 DMA 请求是否开放。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3487](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3487)。

### `LL_TIM_EnableDMAReq_CC1`

```c
__STATIC_INLINE void LL_TIM_EnableDMAReq_CC1 (TIM_TypeDef * TIMx);
```

开放通道 1 捕获比较 DMA 请求。

固定头文件：[接口定义L3498](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3498)。

### `LL_TIM_DisableDMAReq_CC1`

```c
__STATIC_INLINE void LL_TIM_DisableDMAReq_CC1 (TIM_TypeDef * TIMx);
```

关闭通道 1 捕获比较 DMA 请求。

固定头文件：[接口定义L3509](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3509)。

### `LL_TIM_IsEnabledDMAReq_CC1`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledDMAReq_CC1 (TIM_TypeDef * TIMx);
```

查询通道 1 捕获比较 DMA 请求是否开放。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3520](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3520)。

### `LL_TIM_EnableDMAReq_CC2`

```c
__STATIC_INLINE void LL_TIM_EnableDMAReq_CC2 (TIM_TypeDef * TIMx);
```

开放通道 2 捕获比较 DMA 请求。

固定头文件：[接口定义L3531](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3531)。

### `LL_TIM_DisableDMAReq_CC2`

```c
__STATIC_INLINE void LL_TIM_DisableDMAReq_CC2 (TIM_TypeDef * TIMx);
```

关闭通道 2 捕获比较 DMA 请求。

固定头文件：[接口定义L3542](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3542)。

### `LL_TIM_IsEnabledDMAReq_CC2`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledDMAReq_CC2 (TIM_TypeDef * TIMx);
```

查询通道 2 捕获比较 DMA 请求是否开放。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3553](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3553)。

### `LL_TIM_EnableDMAReq_CC3`

```c
__STATIC_INLINE void LL_TIM_EnableDMAReq_CC3 (TIM_TypeDef * TIMx);
```

开放通道 3 捕获比较 DMA 请求。

固定头文件：[接口定义L3564](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3564)。

### `LL_TIM_DisableDMAReq_CC3`

```c
__STATIC_INLINE void LL_TIM_DisableDMAReq_CC3 (TIM_TypeDef * TIMx);
```

关闭通道 3 捕获比较 DMA 请求。

固定头文件：[接口定义L3575](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3575)。

### `LL_TIM_IsEnabledDMAReq_CC3`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledDMAReq_CC3 (TIM_TypeDef * TIMx);
```

查询通道 3 捕获比较 DMA 请求是否开放。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3586](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3586)。

### `LL_TIM_EnableDMAReq_CC4`

```c
__STATIC_INLINE void LL_TIM_EnableDMAReq_CC4 (TIM_TypeDef * TIMx);
```

开放通道 4 捕获比较 DMA 请求。

固定头文件：[接口定义L3597](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3597)。

### `LL_TIM_DisableDMAReq_CC4`

```c
__STATIC_INLINE void LL_TIM_DisableDMAReq_CC4 (TIM_TypeDef * TIMx);
```

关闭通道 4 捕获比较 DMA 请求。

固定头文件：[接口定义L3608](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3608)。

### `LL_TIM_IsEnabledDMAReq_CC4`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledDMAReq_CC4 (TIM_TypeDef * TIMx);
```

查询通道 4 捕获比较 DMA 请求是否开放。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3619](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3619)。

### `LL_TIM_EnableDMAReq_COM`

```c
__STATIC_INLINE void LL_TIM_EnableDMAReq_COM (TIM_TypeDef * TIMx);
```

开放TIM1 换相 DMA 请求。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L3630](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3630)。

### `LL_TIM_DisableDMAReq_COM`

```c
__STATIC_INLINE void LL_TIM_DisableDMAReq_COM (TIM_TypeDef * TIMx);
```

关闭TIM1 换相 DMA 请求。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L3641](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3641)。

### `LL_TIM_IsEnabledDMAReq_COM`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledDMAReq_COM (TIM_TypeDef * TIMx);
```

查询TIM1 换相 DMA 请求是否开放。

- `TIMx`：选择 TIM1。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

- 适用实例：TIM1。

固定头文件：[接口定义L3652](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3652)。

### `LL_TIM_EnableDMAReq_TRIG`

```c
__STATIC_INLINE void LL_TIM_EnableDMAReq_TRIG (TIM_TypeDef * TIMx);
```

开放触发 DMA 请求。

固定头文件：[接口定义L3663](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3663)。

### `LL_TIM_DisableDMAReq_TRIG`

```c
__STATIC_INLINE void LL_TIM_DisableDMAReq_TRIG (TIM_TypeDef * TIMx);
```

关闭触发 DMA 请求。

固定头文件：[接口定义L3674](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3674)。

### `LL_TIM_IsEnabledDMAReq_TRIG`

```c
__STATIC_INLINE uint32_t LL_TIM_IsEnabledDMAReq_TRIG (TIM_TypeDef * TIMx);
```

查询触发 DMA 请求是否开放。

返回：uint32_t，0 表示否/未置位，1 表示是/已置位。

固定头文件：[接口定义L3685](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3685)。

## 软件事件

### `LL_TIM_GenerateEvent_UPDATE`

```c
__STATIC_INLINE void LL_TIM_GenerateEvent_UPDATE (TIM_TypeDef * TIMx);
```

通过 EGR 产生一次更新软件事件。

固定头文件：[接口定义L3703](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3703)。

### `LL_TIM_GenerateEvent_CC1`

```c
__STATIC_INLINE void LL_TIM_GenerateEvent_CC1 (TIM_TypeDef * TIMx);
```

通过 EGR 产生一次通道 1 捕获比较软件事件。

固定头文件：[接口定义L3714](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3714)。

### `LL_TIM_GenerateEvent_CC2`

```c
__STATIC_INLINE void LL_TIM_GenerateEvent_CC2 (TIM_TypeDef * TIMx);
```

通过 EGR 产生一次通道 2 捕获比较软件事件。

固定头文件：[接口定义L3725](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3725)。

### `LL_TIM_GenerateEvent_CC3`

```c
__STATIC_INLINE void LL_TIM_GenerateEvent_CC3 (TIM_TypeDef * TIMx);
```

通过 EGR 产生一次通道 3 捕获比较软件事件。

固定头文件：[接口定义L3736](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3736)。

### `LL_TIM_GenerateEvent_CC4`

```c
__STATIC_INLINE void LL_TIM_GenerateEvent_CC4 (TIM_TypeDef * TIMx);
```

通过 EGR 产生一次通道 4 捕获比较软件事件。

固定头文件：[接口定义L3747](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3747)。

### `LL_TIM_GenerateEvent_COM`

```c
__STATIC_INLINE void LL_TIM_GenerateEvent_COM (TIM_TypeDef * TIMx);
```

通过 EGR 产生一次TIM1 换相软件事件。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L3758](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3758)。

### `LL_TIM_GenerateEvent_TRIG`

```c
__STATIC_INLINE void LL_TIM_GenerateEvent_TRIG (TIM_TypeDef * TIMx);
```

通过 EGR 产生一次触发软件事件。

固定头文件：[接口定义L3769](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3769)。

补充核对：对应EGR.TG，手册明确的作用是置TIF并产生已允许的触发请求；不据函数名保证模拟TRGI电平、启动从模式计数或重置CNT。见[软件事件语义](事件与DMA窗口.md#2-egr软件事件的不同作用)。

### `LL_TIM_GenerateEvent_BRK`

```c
__STATIC_INLINE void LL_TIM_GenerateEvent_BRK (TIM_TypeDef * TIMx);
```

通过 EGR 产生一次TIM1 刹车软件事件。

- `TIMx`：选择 TIM1。

- 适用实例：TIM1。

固定头文件：[接口定义L3780](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3780)。

## 初始化与配置结构

### `LL_TIM_DeInit`

```c
ErrorStatus LL_TIM_DeInit (TIM_TypeDef * TIMx);
```

按支持实例调用APB外设ForceReset/ReleaseReset。与HAL_TIM_Base_DeInit的MSP依赖路径分开理解。

返回：支持实例走复位路径并返回SUCCESS，未匹配实例返回ERROR。此函数会调用RCC总线复位接口，不负责配置GPIO或NVIC。

固定头文件：[接口定义L3794](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3794)。

### `LL_TIM_StructInit`

```c
void LL_TIM_StructInit (LL_TIM_InitTypeDef * TIM_InitStruct);
```

填充时基结构默认值，不访问定时器。Autoreload默认0xFFFFFFFF，须按 16 位 ARR 范围重新选择；各默认字段见[初始化约束](LL初始化边界.md#3-structinit的默认值与芯片适用范围)。

- `TIM_InitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

固定头文件：[接口定义L3795](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3795)。

### `LL_TIM_Init`

```c
ErrorStatus LL_TIM_Init (TIM_TypeDef * TIMx, LL_TIM_InitTypeDef * TIM_InitStruct);
```

按时基结构写PSC、ARR、计数模式、时钟分频和适用的RCR，并调用GenerateEvent_UPDATE。没有先停止CEN或隔离TRGO；UG事件的装载、标志和下游触发须按配置分别判断。

- `TIM_InitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：该固定实现的正常返回路径为SUCCESS；参数断言及硬件状态检查须独立处理。不会配置GPIO或NVIC，不能据返回值判定全部硬件写入已接受。

固定头文件：[接口定义L3796](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3796)。

### `LL_TIM_OC_StructInit`

```c
void LL_TIM_OC_StructInit (LL_TIM_OC_InitTypeDef * TIM_OC_InitStruct);
```

填充输出比较配置结构默认值。

- `TIM_OC_InitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

固定头文件：[接口定义L3797](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3797)。

### `LL_TIM_OC_Init`

```c
ErrorStatus LL_TIM_OC_Init (TIM_TypeDef * TIMx, uint32_t Channel, LL_TIM_OC_InitTypeDef * TIM_OC_InitStruct);
```

按输出比较结构配置指定通道，包括比较值、极性和输出使能。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。
- `TIM_OC_InitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：`SUCCESS` 或 `ERROR`；不会替应用配置 RCC、GPIO 或 NVIC。

固定头文件：[接口定义L3798](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3798)。

补充核对：有效CH1～CH4分派到对应助手并返回SUCCESS，未匹配通道返回ERROR。助手仅按结构OCState/OCNState设置开关，不保证所有输出最终关闭，亦不统一停止CEN。

### `LL_TIM_IC_StructInit`

```c
void LL_TIM_IC_StructInit (LL_TIM_IC_InitTypeDef * TIM_ICInitStruct);
```

填充输入捕获配置结构默认值。

- `TIM_ICInitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

固定头文件：[接口定义L3799](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3799)。

### `LL_TIM_IC_Init`

```c
ErrorStatus LL_TIM_IC_Init (TIM_TypeDef * TIMx, uint32_t Channel, LL_TIM_IC_InitTypeDef * TIM_IC_InitStruct);
```

按输入捕获结构配置指定通道。

- `Channel`：所选定时器通道；使用本接口列出的通道常量，不能混用 HAL 和 LL 编码。
  - 可用编码：`LL_TIM_CHANNEL_CH1`、`LL_TIM_CHANNEL_CH2`、`LL_TIM_CHANNEL_CH3`、`LL_TIM_CHANNEL_CH4`。
- `TIM_IC_InitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：`SUCCESS` 或 `ERROR`；不会替应用配置 RCC、GPIO 或 NVIC。

固定头文件：[接口定义L3800](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3800)。

补充核对：有效CH1～CH4分派到对应助手，助手先关闭CCxE，配置后启用CCxE；正常返回SUCCESS。未匹配通道返回ERROR。与不负责通道使能的LL_TIM_IC_Config区别对待。

### `LL_TIM_ENCODER_StructInit`

```c
void LL_TIM_ENCODER_StructInit (LL_TIM_ENCODER_InitTypeDef * TIM_EncoderInitStruct);
```

填充编码器接口配置结构默认值。

- `TIM_EncoderInitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

固定头文件：[接口定义L3801](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3801)。

### `LL_TIM_ENCODER_Init`

```c
ErrorStatus LL_TIM_ENCODER_Init (TIM_TypeDef * TIMx, LL_TIM_ENCODER_InitTypeDef * TIM_EncoderInitStruct);
```

配置TI1/TI2编码器接口及输入参数，结束时启用CC1E/CC2E。SetEncoderMode修改SMS，未清ECE；切换前须显式检查先前外部时钟模式2，不能假定该初始化覆盖全部旧时钟配置。

- `TIM_EncoderInitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：该固定实现的正常返回路径为SUCCESS；参数断言及硬件状态检查须独立处理。不会配置GPIO或NVIC，不能据返回值判定全部硬件写入已接受。

固定头文件：[接口定义L3802](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3802)。

### `LL_TIM_HALLSENSOR_StructInit`

```c
void LL_TIM_HALLSENSOR_StructInit (LL_TIM_HALLSENSOR_InitTypeDef * TIM_HallSensorInitStruct);
```

填充霍尔传感器配置结构默认值。

- `TIM_HallSensorInitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

固定头文件：[接口定义L3803](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3803)。

### `LL_TIM_HALLSENSOR_Init`

```c
ErrorStatus LL_TIM_HALLSENSOR_Init (TIM_TypeDef * TIMx, LL_TIM_HALLSENSOR_InitTypeDef * TIM_HallSensorInitStruct);
```

目标配置为CH1–CH3异或、TI1F_ED复位、CH1捕获TRC、CH2 PWM2延时与OC2REF触发。固定实现没有清旧MMS及CC2S，复用既有配置时不能保证后两项成立，详见[初始化约束](LL初始化边界.md#2-hall初始化的两项历史状态依赖)。CCR1时间与CCR2延时的物理解释以实际寄存器配置正确为前提。

- `TIM_HallSensorInitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：该固定实现的正常返回路径为SUCCESS；参数断言及硬件状态检查须独立处理。不会配置GPIO或NVIC，不能据返回值判定全部硬件写入已接受。

固定头文件：[接口定义L3804](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3804)。

### `LL_TIM_BDTR_StructInit`

```c
void LL_TIM_BDTR_StructInit (LL_TIM_BDTR_InitTypeDef * TIM_BDTRInitStruct);
```

填充刹车死区配置结构默认值。

- `TIM_BDTRInitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

- 适用实例：TIM1。

固定头文件：[接口定义L3805](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3805)。

### `LL_TIM_BDTR_Init`

```c
ErrorStatus LL_TIM_BDTR_Init (TIM_TypeDef * TIMx, LL_TIM_BDTR_InitTypeDef * TIM_BDTRInitStruct);
```

配置 TIM1 刹车和死区；第一次写入时一并设置所有将受 LOCK 保护的字段。

- `TIMx`：选择 TIM1。
- `TIM_BDTRInitStruct`：原型指定的 LL 配置结构指针；StructInit 写入默认值，Init 读取配置。

返回：该固定实现的正常返回路径为SUCCESS；参数断言及硬件状态检查须独立处理。不会配置GPIO或NVIC，不能据返回值判定全部硬件写入已接受。

- 适用实例：TIM1。

固定头文件：[接口定义L3806](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_ll_tim.h#L3806)。

### 原文兼容性检查宏

原文在相关API注明可用 `IS_TIM_COUNTER_MODE_SELECT_INSTANCE`、`IS_TIM_CLOCK_DIVISION_INSTANCE`、`IS_TIM_REPETITION_COUNTER_INSTANCE`、`IS_TIM_COMMUTATION_EVENT_INSTANCE`、`IS_TIM_BREAK_INSTANCE`、`IS_TIM_CC1_INSTANCE` 至 `IS_TIM_CC4_INSTANCE`、`IS_TIM_OCXREF_CLEAR_INSTANCE`、`IS_TIM_XOR_INSTANCE`、`IS_TIM_CLOCKSOURCE_ETRMODE1_INSTANCE`、`IS_TIM_CLOCKSOURCE_ETRMODE2_INSTANCE`、`IS_TIM_ENCODER_INTERFACE_INSTANCE`、`IS_TIM_MASTER_INSTANCE`、`IS_TIM_SLAVE_INSTANCE`、`IS_TIM_ETR_INSTANCE`、`IS_TIM_DMABURST_INSTANCE` 检查实例能力。它们检查硬件实例类别，不检查LQFP48是否引出所选信号，也不代替运行状态/锁定/时钟条件检查。

[返回定时器主题](../../知识库/06_定时器PWM与同步.md) · [图形关系与来源](图形关系与来源.md)
