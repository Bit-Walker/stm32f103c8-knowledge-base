# SysTick接口参数

范围：硬件语义按 PM0056 Rev 7 §4.5；接口说明对照 UM1850 Rev 3 §10。下述源码行为分别固定到 HAL 提交 `77fbb30b7a1d02533980400083e48c559aae5a4f` 的 `stm32f1xx_hal_cortex.c` 和 CMSIS_5 tag `5.9.0` 的原生 `SysTick_Config`，不是对所有 HAL/CMSIS 组合的保证。若应用采用厂商替换实现，须另查实际调用路径。

## SysTick 计数参数

令 $`f_{\mathrm{ST}}`$ 为 SysTick 输入频率，单位 Hz；$`T`$ 为目标周期，单位 s；$`N`$ 为每个完整周期的输入时钟数，无量纲：

```math
N=f_{\mathrm{ST}}T,\qquad \mathrm{LOAD}=N-1
```

`HAL_SYSTICK_Config(N)` 的参数是时钟数 $`N`$，不是 `LOAD` 寄存器值。$`N`$ 必须为整数；若目标周期换算后不是整数个输入时钟，应按实际采用的整数 $`N`$ 计算周期，不能仍视为精确目标值。

`LOAD` 为 24 位，但配置函数的检查对象是 `N−1`。这使接口数值边界和有效周期边界有所不同：

|传入的 `N`|固定 CMSIS 返回值|结果|
|---|---|---|
|0|1|`N−1` 无符号下溢，检查失败，返回前不写 SysTick 配置|
|1|0|写 `LOAD=0`；没有 1→0 计数转换，不产生周期异常请求或 `COUNTFLAG`|
|2～`0x1000000`|0|写 `LOAD=N−1`；可形成周期计数，异常能否执行仍取决于屏蔽和优先级|
|大于 `0x1000000`|1|超过 24 位重装范围，返回前不写 SysTick 配置|

因此持续周期时基应满足 $`2\le N\le\mathtt{0x1000000}`$；`N` 最大为 16777216，而 `LOAD` 最大为 `0xFFFFFF`。UM1850 p114 把“Reload Value”同时称为 HAL 参数并写上限 `0xFFFFFF`，与固定 CMSIS 按 `N−1` 检查的实现边界并不等同。此处保留文档与实现的区别。

HCLK 为 72 MHz 时，选择 HCLK、目标 1 ms 对应 `N=72000`；选择 HCLK/8 则输入为 9 MHz，对应 `N=9000`。这些是配置计算，不是时钟精度或中断响应时延的测量。

### `HAL_SYSTICK_Config`

```c
uint32_t HAL_SYSTICK_Config(uint32_t TicksNumb);
```

`TicksNumb` 就是上述 $`N`$，HAL 将其直接传给 `SysTick_Config`。通过数值检查后，CMSIS 依次写 `LOAD=N−1`、设置 SysTick 最低可编程优先级、清 `VAL`（同时清 `COUNTFLAG`），再选择 HCLK 并使能计数及异常请求。返回 0 表示配置流程通过，不保证软件毫秒计数已经推进。

每次成功调用都会重新选择 HCLK 并重设优先级；此前手动选的 HCLK/8 或更高优先级不会自动保留。需要不同设置时应随后显式配置。默认 `HAL_InitTick` 也是先调用该函数，再设置所请求的 tick 优先级，不能把两者的参数或完整副作用混为一谈。

### `HAL_SYSTICK_CLKSourceConfig`

```c
void HAL_SYSTICK_CLKSourceConfig(uint32_t CLKSource);
```

`CLKSource` 为 `SYSTICK_CLKSOURCE_HCLK` 或 `SYSTICK_CLKSOURCE_HCLK_DIV8`，分别选 HCLK 或 HCLK/8。固定实现仅对 `CTRL.CLKSOURCE` 做读改写，不重算 `LOAD`、不清 `VAL`、不调整优先级。若 `LOAD` 不变，从 HCLK 改为 HCLK/8 后，完整稳态周期变为原来的 8 倍；切源时的过渡周期不能直接当成从零开始的完整周期。

读取 `CTRL` 会清 `COUNTFLAG`，因此这个读改写调用也会消耗该标志。原文提及的 `__HAL_CORTEX_SYSTICKCLK_CONFIG(...)` 是旧宏表达，工程优先使用这里导出的 `HAL_SYSTICK_CLKSourceConfig()`。配置顺序须注意：先设置时钟源、再调用 `HAL_SYSTICK_Config`，会被后者重新选回 HCLK。

依据：[UM1850 §10.1.1、§10.1.4、§10.2.1](../来源/UM1850.md#src-um1850-r3-cortex)、[CMSIS 5.9.0 固定来源与行号](../来源/驱动实现.md#src-cmsis590-cm3)、[HAL Cortex 固定来源与行号](../来源/驱动实现.md#src-hal-cortex-snapshot)。硬件 `LOAD`、`VAL` 与 `COUNTFLAG` 的完整条件见[内核 SysTick 参数](内核寄存器参数.md#45-systick-24-位系统定时器)。

## HAL 软件时基

硬件周期、中断向量和 HAL 软件计数是三个需要连通的环节。默认 SysTick 方案中，应用的 `SysTick_Handler` 应按工程安排调用 `HAL_IncTick()` 推进毫秒计数；若还需要 HAL 的 SysTick 回调分发，再调用 `HAL_SYSTICK_IRQHandler()`。固定 [`HAL_SYSTICK_IRQHandler` L497–511](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_cortex.c#L497-L511)只调用 `HAL_SYSTICK_Callback()`，默认弱回调为空，不会自动调用 `HAL_IncTick`。

因此仅调用 `HAL_SYSTICK_Config`，或向量中只调用上述默认分发函数，都不能保证 `HAL_GetTick` 前进。使用 RTOS 或[替代 TIM 时基](HAL定时器时基与官方示例边界.md)时，按实际向量与回调安排核对，避免漏计或重复递增；不能不加区分地再插入一次 `HAL_IncTick`。

[HAL 毫秒计数与阻塞延时](HAL毫秒计数与阻塞延时.md)说明 tick 步长、暂停、ISR 抢占条件及 `HAL_Delay` 的整数边界。
