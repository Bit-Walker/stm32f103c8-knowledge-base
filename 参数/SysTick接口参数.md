# SysTick接口参数

## SysTick 计数参数

令 `f_ST` 为 SysTick 输入频率，单位 Hz；`T` 为目标中断周期，单位 s：

`N = f_ST × T`，`LOAD = N − 1`。

`HAL_SYSTICK_Config(N)` 参数是 N，而非 LOAD。LOAD 为 24 位；CMSIS 的数值检查可接受 N=1，但此时 LOAD=0，不会发生 1→0 的计数，也就没有周期异常或 COUNTFLAG。需要持续周期时基时应满足 2≤N≤0x1000000（PM0056 §4.5.2）。UM1850 p114把“Reload Value”同时称为HAL参数并写上限0xFFFFFF；这与固定CMSIS实现按N−1检查的边界并不等同。本页采用固定实现：N最大0x1000000，而LOAD最大0xFFFFFF。72 MHz、1 ms 时 N=72000。配置函数默认选 HCLK 且重设最低优先级；需要 HCLK/8 或不同优先级，应随后显式配置并保证周期一致。

原文提及 `__HAL_CORTEX_SYSTICKCLK_CONFIG(...)` 的旧宏表达，工程优先使用本章导出的 `HAL_SYSTICK_CLKSourceConfig()`。C8 没有此通用介绍暗示的可配置 MPU 驱动。


### `HAL_SYSTICK_Config`

```c
uint32_t HAL_SYSTICK_Config (uint32_t TicksNumb);
```

`TicksNumb` 为两次中断间的 SysTick 时钟数，内部 CMSIS 将 LOAD 设为该值减 1，清当前计数，选 HCLK、使能计数及中断并设最低优先级。返回 0 成功、1 配置失败。


### `HAL_SYSTICK_CLKSourceConfig`

```c
void HAL_SYSTICK_CLKSourceConfig (uint32_t CLKSource);
```

`CLKSource` 为 `SYSTICK_CLKSOURCE_HCLK` 或 `SYSTICK_CLKSOURCE_HCLK_DIV8`，分别选 HCLK 或 HCLK/8；切换后需重新计算周期。


[UM1850 §10.1.1；§10.1.4；§10.2.1，p114,115,117,119,120](../来源/UM1850.md#src-um1850-r3-cortex)；[core_cm3_cmsis590.h 对应来源副本行号](../来源/驱动实现.md#src-cmsis590-cm3)；[stm32f1xx_hal_cortex.c 对应来源副本行号](../来源/驱动实现.md#src-hal-cortex-snapshot)
