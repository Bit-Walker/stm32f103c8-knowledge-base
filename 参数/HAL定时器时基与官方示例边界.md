# HAL 定时器时基与官方示例边界

对象：STM32CubeF1 官方 NUCLEO-F103RB 的 HAL_TimeBase_TIM 示例，固定提交 `c7656f1fee178058be2f8ebfc8df9eaf91dc565e`。该例使用 TIM2；迁移到 STM32F103C8T6 时保留下面的资源与版本条件。

该 CubeF1 提交的 [HAL 子模块记录](https://api.github.com/repos/STMicroelectronics/STM32CubeF1/contents/Drivers/STM32F1xx_HAL_Driver?ref=c7656f1fee178058be2f8ebfc8df9eaf91dc565e)固定到 `bd368aa335c529641d2e567574885e02deacc64a`；下文采用此匹配提交的核心及头文件。HAL 核心文件与先前独立核验的 v1.1.10 核心 blob 相同，不据单文件相同推断两个提交的全部内容相同。未编译或运行示例。

另已逐字节比对 [STM32CubeF1 v1.8.6 固定提交 `42472d6` 的同目录示例](https://github.com/STMicroelectronics/STM32CubeF1/tree/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/HAL/HAL_TimeBase_TIM)：时基源文件、`main.c`、配置头和 MDK 项目四文件与本页旧提交完全相同。因此固定 1 ms、未保存 `uwTickPrio` 的示例写法及下述板级时钟字段问题，在该 v1.8.6 的四文件中也存在。该包配套 HAL 为 `77fbb30`；这项比对不把下文 `bd368aa` 驱动分支无条件推广到另一版本。

## 覆盖函数与实际调用链

[官方 readme](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM32F103RB-Nucleo/Examples/HAL/HAL_TimeBase_TIM/readme.txt)说明覆盖 `HAL_InitTick`、`HAL_SuspendTick`、`HAL_ResumeTick`，继续使用 HAL 的 `HAL_IncTick` 和 `HAL_Delay`；周期固定为 1 ms。

[时基源文件 L145–158](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM32F103RB-Nucleo/Examples/HAL/HAL_TimeBase_TIM/Src/stm32f1xx_hal_timebase_tim.c#L145-L158)定义 TIM2 IRQ 分发到 `HAL_TIM_IRQHandler(&TimHandle)`，并在 `HAL_TIM_PeriodElapsedCallback` 中调用 `HAL_IncTick`。TIM2 IRQ 函数就在时基文件中；原例的 [SysTick_Handler 为空](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM32F103RB-Nucleo/Examples/HAL/HAL_TimeBase_TIM/Src/stm32f1xx_it.c)。整合工程时检查向量函数是否重复定义，以及是否还有另一处时基中断重复调用 `HAL_IncTick`。

该全局周期回调没有判断 `htim->Instance`。如果另一个定时器也进入同一个回调，它同样推进 HAL 计数。多定时器工程应将时基计数限定到所选实例，其他实例分别处理。此结论限定为共用该回调的场景，不表示原例只有 TIM2 时必然多计时。启用独立回调注册后，按实际注册关系核对。

## 初始化与时钟变化链

覆盖的 `HAL_InitTick` 不只在开机执行一次。匹配 `bd368aa` 核心与 RCC 的调用顺序及返回处理如下：

|调用者|调用时机与传入值|对时基初始化结果的处理|
|---|---|---|
|`HAL_Init`|设置优先级分组后、`HAL_MspInit` 前，传入 `TICK_INT_PRIORITY`|不检查返回值，最后返回 `HAL_OK`|
|`HAL_RCC_ClockConfig`|更新总线配置和 `SystemCoreClock` 后，传入 `uwTickPrio`|不检查返回值，最后返回 `HAL_OK`|
|`HAL_RCC_DeInit`|切回 HSI、把 `SystemCoreClock` 设为 `HSI_VALUE` 后，传入 `uwTickPrio`|初始化失败则返回 `HAL_ERROR`|
|`HAL_SetTickFreq`|频率枚举改变时，先写 `uwTickFreq`，再传入 `uwTickPrio`|返回初始化状态；失败只恢复旧枚举值|

来源：[HAL 初始化 L142–166](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal.c#L142-L166)、[RCC 时钟配置 L927–948](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_rcc.c#L927-L948)、[RCC 反初始化 L222–244](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_rcc.c#L222-L244)、[tick 频率设置 L322–348](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal.c#L322-L348)。表中 `HAL_OK` 仅指走到相应尾部的路径，不否定 RCC 在前面步骤可能返回其他错误。

示例 `HAL_InitTick` 先设置 TIM2 优先级、使能 NVIC 和 TIM2 时钟，再执行 `HAL_TIM_Base_Init` / `HAL_TIM_Base_Start_IT`。它必须在 `HAL_MspInit` 之前就能工作；失败也不自动撤销前面已完成的配置。重复调用会重写分频、周期并重新启动更新中断，因此在 tick 暂停后更改系统时钟或 tick 频率，也不能假定暂停状态得到保留。

PCLK1 的计算依赖 `SystemCoreClock` 和当前 APB1 分频寄存器（[匹配 RCC L1174–1188](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_rcc.c#L1174-L1188)）。直接修改 RCC、仅调用 `HAL_RCC_OscConfig` 或只更新软件时钟变量，不等同于已完成 TIM 时基重配。迁移时应一并核对时钟变量、TIM 分频及中断状态，不能只据外层 `HAL_OK` 判断 tick 正常。

## 分频与周期条件

[时基源文件 L70–106](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM32F103RB-Nucleo/Examples/HAL/HAL_TimeBase_TIM/Src/stm32f1xx_hal_timebase_tim.c#L70-L106)在 APB1 不分频时取 $`f_{\mathrm{TIM}}=f_{\mathrm{PCLK1}}`$ ，否则取 $`f_{\mathrm{TIM}}=2f_{\mathrm{PCLK1}}`$ ；代码把 $`\left\lfloor\frac{f_{\mathrm{TIM}}}{1{,}000{,}000\,\mathrm{Hz}}\right\rfloor-1`$ 写入 `PSC`，并设置 `ARR = 999`。

其中 $`f_{\mathrm{TIM}}`$ 为 TIM2 输入时钟频率， $`f_{\mathrm{PCLK1}}`$ 为 APB1 时钟频率，单位均为 Hz；`PSC` 为预分频寄存器编码，无量纲，实际除数为 $`\mathrm{PSC}+1`$ ；`ARR` 为自动重装值，无量纲，向上计数周期包含 $`\mathrm{ARR}+1`$ 个计数时钟； $`\lfloor\cdot\rfloor`$ 表示向下取整。

在该向上计数配置下，周期为：

```math
T=\frac{(\mathrm{PSC}+1)(\mathrm{ARR}+1)}{f_{\mathrm{TIM}}}
```

$`T`$ 的单位为秒，其余符号含义同上。要得到精确 1 ms，输入频率必须能按代码分频精确得到 1 MHz，且分频值在有效范围内。例如 $`f_{\mathrm{TIM}}=72\,\mathrm{MHz}`$ 时 `PSC=71`、`ARR=999`； $`f_{\mathrm{TIM}}=8\,\mathrm{MHz}`$ 时 `PSC=7`、`ARR=999`。此处是寄存器关系计算，不是板卡测量。

若输入不足 1 MHz，代码的无符号减法会产生下溢值；若不是 1 MHz 的整数倍，向下取整会使周期偏离 1 ms。原注释 L93 与实际 Period 赋值 L98 的表达不同，按 PSC 和 ARR 联合关系核查。硬件依据见[TIM 计数时基与更新](TIM/计数时基与更新.md)。

## 暂停与恢复

示例 L119–134 只关闭/打开 TIM 更新中断。[匹配 HAL 头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal_tim.h#L1138-L1154)的相应宏只改变 DIER 中指定中断位；`TIM_IT_UPDATE` 对应 UIE。DIER 全称 DMA/interrupt enable register；UIE 为 Update interrupt enable。

因此在采用这组宏定义时，暂停函数不清 CEN、不清 UIF，也不重置 CNT。CEN 为计数使能；UIF 为更新中断标志；CNT 为当前计数值。若恢复时已有有效更新标志，可能很快进入中断，并非一定先等完整周期。单个 UIF 不是累计次数计数器，恢复函数也不补偿暂停时长。不要把暂停软件 tick 等同为停止计数器。更新事件与标志条件见上述硬件页面；[匹配 IRQ 分发 L3951–3960](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_tim.c#L3951-L3960)仅在更新标志与更新中断使能均置位时清标志并调用回调。

## 与核心 tick 配置的配合

[固定 HAL 核心 L293–346](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal.c#L293-L346)中，`HAL_IncTick` 每次增加 `uwTickFreq`；`HAL_SetTickFreq` 更改该值并调用 `HAL_InitTick(uwTickPrio)`。[对应枚举](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal.h#L45-L61)中 1 kHz、100 Hz、10 Hz 分别对应增量 1、10、100 ms。

官方示例的覆盖函数始终以 1 ms 为配置目标，没有读取 `uwTickFreq`。若在该匹配核心上成功切换到每次增量 10 ms 或 100 ms，且实际中断周期确为 1 ms，软件时间分别按物理时间的 10 倍或 100 倍增长；不能只更改枚举而保留原例周期。这里是假设中断正常处理、频率配置成功且计数没有其他修改的静态推导；原例没有主动调用 `HAL_SetTickFreq`。计数及延时边界见[HAL 毫秒计数与阻塞延时](HAL毫秒计数与阻塞延时.md)。

优先级状态需要分三步核对：

1. 示例覆盖函数未写 `uwTickPrio`，而[核心默认实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal.c#L234-L254)会在接受优先级后保存它。若应用也未赋值，该变量保留[初值 `1UL << __NVIC_PRIO_BITS`](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal.c#L79-L81)；[匹配器件头](https://github.com/STMicroelectronics/cmsis-device-f1/blob/c8e9a4a4f16b6d2cb2a2083cbe5161025280fb22/Include/stm32f103xb.h#L51-L52)的优先级位数为 4，因此初值为 16，不是合法的 0～15。
2. `HAL_GetTickPrio()` 此时只返回该软件变量；后续表列的重配置路径也会把 16 传给覆盖函数。因此不能把第一次按 `TICK_INT_PRIORITY` 设置的硬件优先级，当成已经同步保存的 HAL 状态。
3. [`HAL_NVIC_SetPriority`](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_cortex.c#L164-L175)的参数检查是断言，并不返回错误状态。启用 `USE_FULL_ASSERT` 时由应用的 `assert_failed` 决定后续行为；关闭断言时继续进入 CMSIS 优先级编码，不能据此认为优先级 16 有效。

若仍使用 `HAL_Init` 设置的 `NVIC_PRIORITYGROUP_4`、匹配的原生 CMSIS 编码且子优先级为 0，16 经掩码后会编码成 0（[编码实现 L1686–1700](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Drivers/CMSIS/Include/core_cm3.h#L1686-L1700)）。因此移植覆盖函数应校验并同步保存有效优先级，不能靠断言关闭来修复状态。

## 中断内等待与移植范围

官方 readme 要求，在外设 ISR 中使用 `HAL_Delay` 时，TIM2 时基中断必须能以更高抢占优先级执行，数值更小；只调整子优先级不足以打断正在执行的 ISR。若 tick 被暂停或中断被屏蔽，延时与依赖该计数的超时等待也不能据墙上时间自然结束；具体失败分支需看所调用 API。TIM2 的分频、周期、更新中断及句柄也不能被另一项 PWM、捕获或计时配置覆盖，否则这条时基链会被改变。

该例包含 Nucleo BSP、按键、LED 和板级时钟配置；其 `main.c` 不能直接作为目标板的时钟模板。

- MDK 与频率算术：该固定 MDK 项目选择 STM32F103RB，预处理定义未覆盖 `HSE_VALUE`；配置头默认取 8 MHz，而 `main.c` 设置 `PLL_MUL16`。即便显式选择合法的 HSE /1 或 /2，算术结果也分别为 128 MHz 或 64 MHz，不能支持其 72 MHz 注释。
- 初始化遗漏：局部 `RCC_OscInitStruct` 未整体初始化且 `HSEPredivValue` 未赋值，而匹配 RCC 驱动在 HSE→PLL 配置路径使用该字段。因此不能依据原例确定实际工作频率。
- 移植处理：复制前应重建符合板卡和芯片限制的时钟配置，并初始化全部使用字段。迁移时以[时钟主题](../知识库/02_时钟复位与低功耗.md)和实际电路为准。

此处为固定 MDK 配置的静态核查，未覆盖其他工具链或测量外部时钟。

### 板级时钟证据定位

- [MDK 项目预处理宏与源文件列表](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM32F103RB-Nucleo/Examples/HAL/HAL_TimeBase_TIM/MDK-ARM/Project.uvprojx#L336-L450)
- [main.c 的局部结构与 PLL 设置](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM32F103RB-Nucleo/Examples/HAL/HAL_TimeBase_TIM/Src/main.c#L125-L152)
- [配置头中的 HSE_VALUE](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM32F103RB-Nucleo/Examples/HAL/HAL_TimeBase_TIM/Inc/stm32f1xx_hal_conf.h#L72-L86)
- [匹配 RCC 读取 HSEPredivValue 的路径](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_rcc.c#L683-L731)
- [RCCEx 中的 /1、/2 定义](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal_rcc_ex.h#L449-L471)

128 MHz 的条件算术结果不构成允许的工作点；目标芯片系统时钟上限仍为 72 MHz，并须满足电源、Flash 延迟与总线等条件。`HSE_VALUE` 是软件计算常量，不能代替外部时钟测量。
