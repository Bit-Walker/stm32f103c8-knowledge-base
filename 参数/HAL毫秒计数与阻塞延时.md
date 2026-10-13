# HAL 毫秒计数与阻塞延时

范围：固定 HAL 提交 `bd368aa335c529641d2e567574885e02deacc64a` 的默认核心实现。应用覆盖 weak 函数后需要重新核对。依据 [stm32f1xx_hal.c](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal.c#L293-L385) 和 [tick 枚举](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal.h#L45-L61)，属于源码与整数关系审查，未做固件或板卡试验。

## 软件计数与时基周期

`HAL_GetTick()` 返回 `uint32_t` 软件计数 `uwTick`；默认 `HAL_IncTick()` 每次加 `uwTickFreq`。它们不直接测量当前 CPU 周期或墙上时间。

|配置|正常物理中断周期|每次计数增加量|
|---|---|---|
|HAL_TICK_FREQ_1KHZ|1 ms|1 ms|
|HAL_TICK_FREQ_100HZ|10 ms|10 ms|
|HAL_TICK_FREQ_10HZ|100 ms|100 ms|

上述对应关系要求时基配置正确、中断得以处理且没有额外写入计数。替代时基必须同时维持中断周期与计数增量的配合，见[官方 TIM2 示例边界](HAL定时器时基与官方示例边界.md)。

## HAL_Delay 的返回条件

```c
void HAL_Delay(uint32_t Delay);
```

`Delay` 是请求的毫秒延时值；函数阻塞忙等，没有状态返回值。固定实现先读取起始计数，然后把等待阈值设为 `Delay`；只要 `Delay < HAL_MAX_DELAY`，就再加上当前 `uwTickFreq`。随后持续读取计数，以无符号差值判断是否达到阈值。

由此得到：

- `HAL_Delay(0)` 也等待计数前进，不保证立即返回。距离下一个 tick 的相位不同，实际等待时间不同，不能说必定从调用点完整等待一个物理周期。
- 计数暂停、所需中断被屏蔽，或在无法被时基中断抢占的 ISR 内调用，都可能使等待不能结束。使用同一个停止推进的 tick 作为超时依据不能解除这类等待。
- 普通短间隔可以跨越计数回绕点进行无符号差值比较；多个完整回绕周期无法由这个 32 位差值区分。长时间抢占、停机及频率变更也不能直接忽略。

## 接近 uint32_t 上界时的加法

补偿用的 `wait += uwTickFreq` 是 32 位无符号加法，没有饱和保护。例如 `Delay=0xFFFFFFFE` 时：

|计数增加量|加法后的阈值 wait|
|---|---|
|1 ms|0xFFFFFFFF|
|10 ms|8|
|100 ms|98|

后两行发生回绕。若采用正常匹配的时基、等待期间频率不变且没有其他计数修改，一次 tick 的增加量就足以达到缩小后的阈值，远小于请求的长延时。以上为固定实现的整数推导，不是测得延迟。

对会执行补偿加法的参数，需保证 `Delay ≤ UINT32_MAX − uwTickFreq`，才能避免这一步加法回绕；该条件仅覆盖此项算术风险，不保证超长阻塞、计数采样及中断调度整体正确。所有量在这里以毫秒计数值表示，`UINT32_MAX=4294967295` 为 32 位无符号最大值。

## HAL_MAX_DELAY 必须按函数解释

在此 `HAL_Delay` 实现中，`Delay=HAL_MAX_DELAY` 只跳过补偿加法，循环仍比较计数差与 `0xFFFFFFFF`。它没有专门的永久等待分支，不宜用作可靠的永久睡眠机制。

部分外设轮询 API 对 `Timeout=HAL_MAX_DELAY` 明确跳过有限超时检查；那是各自的实现分支。查阅 [DMA 轮询](DMA参数与HAL接口.md)、[ADC 轮询](ADC/HAL轮询边界.md)和 [USART 接收](USART/ReceiveToIdle与事件位置.md)时，保留各函数的条件，不能把同名常量的语义跨函数套用。

硬件 SysTick 的 LOAD、计数源和配置接口见[SysTick 接口参数](SysTick接口参数.md)。本页不引入可直接替代原函数的未验证实现。
