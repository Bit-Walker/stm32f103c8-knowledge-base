# HAL 定时器时基与官方示例边界

对象：STM32CubeF1 官方 NUCLEO-F103RB 的 HAL_TimeBase_TIM 示例，固定提交 `c7656f1fee178058be2f8ebfc8df9eaf91dc565e`。该例使用 TIM2；迁移到 STM32F103C8T6 时保留下面的资源与版本条件。

另以 HAL 驱动固定提交 `77fbb30b7a1d02533980400083e48c559aae5a4f` 核对核心时基语义。两组来源独立列出；本文未确认该 CubeF1 提交的 HAL 子模块恰为此驱动版本，也未编译或运行示例。

## 覆盖函数与实际调用链

[官方 readme](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM32F103RB-Nucleo/Examples/HAL/HAL_TimeBase_TIM/readme.txt)说明覆盖 `HAL_InitTick`、`HAL_SuspendTick`、`HAL_ResumeTick`，继续使用 HAL 的 `HAL_IncTick` 和 `HAL_Delay`；周期固定为 1 ms。

[时基源文件 L145–158](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM32F103RB-Nucleo/Examples/HAL/HAL_TimeBase_TIM/Src/stm32f1xx_hal_timebase_tim.c#L145-L158)定义 TIM2 IRQ 分发到 `HAL_TIM_IRQHandler(&TimHandle)`，并在 `HAL_TIM_PeriodElapsedCallback` 中调用 `HAL_IncTick`。TIM2 IRQ 函数就在时基文件中；原例的 [SysTick_Handler 为空](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM32F103RB-Nucleo/Examples/HAL/HAL_TimeBase_TIM/Src/stm32f1xx_it.c)。整合工程时检查向量函数是否重复定义，以及是否还有另一处时基中断重复调用 `HAL_IncTick`。

该全局周期回调没有判断 `htim->Instance`。如果另一个定时器也进入同一个回调，它同样推进 HAL 计数。多定时器工程应将时基计数限定到所选实例，其他实例分别处理。此结论限定为共用该回调的场景，不表示原例只有 TIM2 时必然多计时。启用独立回调注册后，按实际注册关系核对。

## 分频与周期条件

[时基源文件 L70–106](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM32F103RB-Nucleo/Examples/HAL/HAL_TimeBase_TIM/Src/stm32f1xx_hal_timebase_tim.c#L70-L106)在 APB1 不分频时取 PCLK1，否则取 2×PCLK1；代码计算 PSC = floor(f_TIM / 1,000,000) − 1，ARR = 999。

其中 f_TIM 为 TIM2 输入时钟，单位 Hz；PSC 为预分频寄存器编码，无量纲，实际除数为 PSC+1；ARR 为自动重装值，无量纲，向上计数周期包含 ARR+1 个计数时钟；floor 表示向下取整。

在该向上计数配置下，周期 T = (PSC+1)×(ARR+1)/f_TIM。T 的单位为秒，其余符号含义同上。要得到精确 1 ms，输入频率必须能按代码分频精确得到 1 MHz，且分频值在有效范围内。例如 f_TIM=72 MHz 时 PSC=71、ARR=999；f_TIM=8 MHz 时 PSC=7、ARR=999。此处是寄存器关系计算，不是板卡测量。

若输入不足 1 MHz，代码的无符号减法会产生下溢值；若不是 1 MHz 的整数倍，向下取整会使周期偏离 1 ms。原注释 L93 与实际 Period 赋值 L98 的表达不同，按 PSC 和 ARR 联合关系核查。硬件依据见[TIM 计数时基与更新](TIM/计数时基与更新.md)。

## 暂停与恢复

示例 L119–134 只关闭/打开 TIM 更新中断。[独立固定 HAL 头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_tim.h#L1137-L1153)的相应宏只改变 DIER 中指定中断位；`TIM_IT_UPDATE` 对应 UIE。DIER 全称 DMA/interrupt enable register；UIE 为 Update interrupt enable。

因此在采用这组宏定义时，暂停函数不清 CEN、不清 UIF，也不重置 CNT。CEN 为 Counter enable；UIF 为 Update interrupt flag；CNT 为 Counter。不要把暂停软件 tick 等同为停止计数器，也不能把恢复视为必定从全新完整周期开始。更新事件与标志条件见上述硬件页面。

## 与核心 tick 配置的配合

[固定 HAL 核心 L293–346](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal.c#L293-L346)中，`HAL_IncTick` 每次增加 `uwTickFreq`；`HAL_SetTickFreq` 更改该值并调用 `HAL_InitTick(uwTickPrio)`。[对应枚举](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal.h#L45-L61)中 1 kHz、100 Hz、10 Hz 分别对应增量 1、10、100 ms。

官方示例的覆盖函数始终配置 1 ms，没有读取 `uwTickFreq`。若与上述固定核心组合并成功切换到每次增量 10 ms，实际中断仍每 1 ms 发生，软件时间就会加快；不能只更改枚举而保留原例周期。这里是版本组合条件下的静态推导。

同一覆盖函数未写 `uwTickPrio`，而核心默认实现会在接受优先级后保存它；使用 `HAL_GetTickPrio` 或再次重设时基前，还需核对覆盖函数与核心状态变量的一致性。

固定核心的 `HAL_Init` 调用 `HAL_InitTick` 后未检查返回值，最后仍返回 `HAL_OK`（[L142–166](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal.c#L142-L166)）。不能仅据这个外层返回值证明自定义时基初始化成功。

## 中断内等待与移植范围

官方 readme 要求，在外设 ISR 中使用 `HAL_Delay` 时，TIM2 时基中断必须能以更高抢占优先级执行。若 tick 被暂停或中断被屏蔽，延时与依赖该计数的超时等待也不能据墙上时间自然结束；具体失败分支需看所调用 API。

该例包含 Nucleo BSP、按键、LED 和板级时钟配置；其 main.c 不能直接作为 C8T6 时钟模板。该文件的 72 MHz 注释、PLL 配置和未显式设置的时钟字段尚需与项目编译宏、外部时钟和匹配驱动共同复核，本页不宣称原例实际运行频率。迁移时以[C8 时钟主题](../知识库/02_时钟复位与低功耗.md)和实际电路为准。
