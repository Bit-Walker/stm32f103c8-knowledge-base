# HAL 毫秒计数与阻塞延时

范围：固定 HAL 提交 `bd368aa335c529641d2e567574885e02deacc64a` 的默认核心实现。应用覆盖 weak 函数后需要重新核对。依据 [stm32f1xx_hal.c](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal.c#L293-L385) 和 [tick 枚举](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal.h#L45-L61)，属于源码与整数关系审查，未做固件或板卡试验。

## 软件计数与时基周期

`HAL_GetTick()` 返回 `uint32_t` 软件计数 `uwTick`；默认 `HAL_IncTick()` 每次加 `uwTickFreq`。它们不直接测量当前 CPU 周期或墙上时间。

|配置|目标中断周期|每次计数增加量|
|---|---|---|
|HAL_TICK_FREQ_1KHZ|1 ms|1 ms|
|HAL_TICK_FREQ_100HZ|10 ms|10 ms|
|HAL_TICK_FREQ_10HZ|100 ms|100 ms|

默认值为 `HAL_TICK_FREQ_1KHZ`。`HAL_GetTickFreq()` 返回上表枚举，底层数值依次是 1、10、100，表示每次增加的毫秒数，不能把返回数值当成 Hz。

上述对应关系要求时基配置正确、中断得以处理且没有额外写入计数。软件分辨率随步长变化；较粗步长仍以毫秒计数，但不提供 1 ms 分辨率。替代时基必须同时维持中断周期与计数增量的配合，见[官方 TIM2 示例边界](HAL定时器时基与官方示例边界.md)。

## 配置入口与失败边界

- 默认 [`HAL_InitTick(TickPriority)`](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal.c#L234-L254)按 `SystemCoreClock / (1000U / uwTickFreq)` 配置 SysTick，再检查并设置优先级。`TickPriority` 是优先级参数，不是周期；成功时保存到 `uwTickPrio`。时钟数的范围和硬件周期见[SysTick 接口参数](SysTick接口参数.md)。
- [`HAL_SetTickFreq(Freq)`](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal.c#L322-L358)只应传上表三个枚举。值改变时，先写 `uwTickFreq`，再调用 `HAL_InitTick(uwTickPrio)`；失败只恢复旧 `uwTickFreq`，没有通用的硬件回滚。值相同时直接返回 `HAL_OK`，不会修复或重新启动已经失效的时基。
- 默认 `HAL_InitTick` 在验证优先级前已经调用 `HAL_SYSTICK_Config`；优先级非法时返回 `HAL_ERROR`，并不代表 SysTick 未改变。`HAL_SetTickFreq` 的返回值及失败后的实际配置都要检查。参数断言也不能代替应用对合法枚举的约束。

## HAL_Delay 的返回条件

```c
void HAL_Delay(uint32_t Delay);
```

`Delay` 是请求的毫秒延时值；函数阻塞忙等，没有状态返回值。固定实现先读取起始计数，然后把等待阈值设为 `Delay`；只要 `Delay < HAL_MAX_DELAY`，就再加上当前 `uwTickFreq`。随后持续读取计数，以无符号差值判断是否达到阈值。

由此得到：

- `HAL_Delay(0)` 也等待计数前进，不保证立即返回。距离下一个 tick 的相位不同，实际等待时间不同，不能说必定从调用点完整等待一个物理周期。
- 计数暂停、所需中断被屏蔽，或在无法被时基中断抢占的 ISR 内调用，都可能使等待不能结束。使用同一个停止推进的 tick 作为超时依据不能解除这类等待，详见下节。
- 普通短间隔可以跨越计数回绕点进行无符号差值比较；多个完整回绕周期无法由这个 32 位差值区分。长时间抢占、停机及频率变更也不能直接忽略。

## 暂停与中断上下文

默认 [`HAL_SuspendTick` / `HAL_ResumeTick`](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal.c#L397-L417)只清除/置位 SysTick 的 `TICKINT`（异常请求使能），不清除计数使能 `ENABLE`，也不重置 `VAL` 或清除已经挂起的异常。两者对 `CTRL` 的读改写会读取该寄存器，因此也会清 `COUNTFLAG`；这与清除挂起异常不同。暂停不是停止硬件计数器；恢复也不补回暂停期间的全部毫秒。相关寄存器语义见[内核 SysTick 参数](内核寄存器参数.md#45-systick-24-位系统定时器)。采用 TIM 时基时，以覆盖函数的实际行为为准。

在 ISR 中等待 HAL tick，时基中断必须能抢占该 ISR：在所用优先级分组下具有更高抢占优先级，数值更小；只提高子优先级无效。在时基自身 ISR 中等待同一 tick 也不能靠自身再次进入来推进计数。即使优先级正确，屏蔽中断或暂停 tick 仍会阻断这条推进链。工程通常把延时和阻塞轮询移到主循环或任务上下文，ISR 只记录事件。

## 接近 uint32_t 上界时的加法

补偿用的 `wait += uwTickFreq` 是 32 位无符号加法，没有饱和保护。例如 `Delay=0xFFFFFFFE` 时：

|计数增加量|加法后的阈值 wait|
|---|---|
|1 ms|0xFFFFFFFF|
|10 ms|8|
|100 ms|98|

后两行发生回绕。若采用正常匹配的时基、等待期间频率不变且没有其他计数修改，一次 tick 的增加量就足以达到缩小后的阈值，远小于请求的长延时。还存在阈值恰好回绕为 0 的情况：步长 10 ms、`Delay=0xFFFFFFF6`，或步长 100 ms、`Delay=0xFFFFFF9C`，循环条件从一开始就不成立，无需等到下一次 tick。以上为固定实现的整数推导，不是测得延迟。

对会执行补偿加法的参数，需保证 `Delay ≤ UINT32_MAX − uwTickFreq`，才能避免这一步加法回绕；该条件仅覆盖此项算术风险，不保证超长阻塞、计数采样及中断调度整体正确。所有量在这里以毫秒计数值表示，`UINT32_MAX=4294967295` 为 32 位无符号最大值。

## HAL_MAX_DELAY 必须按函数解释

在此 `HAL_Delay` 实现中，`Delay=HAL_MAX_DELAY` 只跳过补偿加法，循环仍比较计数差与 `0xFFFFFFFF`。只有实际读取到这个最大差值时才会退出。若等待期间始终只按固定步长增加 `uwTick`，没有其他计数写入：

|步长|可达的无符号差值|对 `HAL_Delay(HAL_MAX_DELAY)` 的含义|
|---|---|---|
|1 ms|全部 32 位值|最大值可达，但循环若错过该读数，不能在本次回绕前退出|
|10 ms|偶数，最大 `0xFFFFFFFE`|达不到奇数阈值，循环不结束|
|100 ms|4 的倍数，最大 `0xFFFFFFFC`|达不到奇数阈值，循环不结束|

这里的可达差值间隔是步长与 $`2^{32}`$ 的最大公约数，分别为 1、2、4。即使补偿加法没有溢出，超长延时仍可能不可达：例如步长 10 ms、`Delay=UINT32_MAX−10`，补偿后的阈值仍是 `UINT32_MAX`。因此上一节的防溢出条件不是超长延时的完整安全条件。

这些是该循环在固定增量下的行为，不是对其他 API“无限等待”约定的否定，也不是推荐的永久睡眠机制。

部分外设轮询 API 对 `Timeout=HAL_MAX_DELAY` 明确跳过有限超时检查；那是各自的实现分支。查阅 [DMA 轮询](DMA参数与HAL接口.md)、[ADC 轮询](ADC/HAL轮询边界.md)和 [USART 接收](USART/ReceiveToIdle与事件位置.md)时，保留各函数的条件，不能把同名常量的语义跨函数套用。

硬件 SysTick 的 LOAD、计数源和配置接口见[SysTick 接口参数](SysTick接口参数.md)。本页不引入可直接替代原函数的未验证实现。
