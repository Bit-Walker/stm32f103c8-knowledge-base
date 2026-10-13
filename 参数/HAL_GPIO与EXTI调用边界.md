# HAL GPIO 与 EXTI 调用边界

适用 STM32F103C8T6。以下实现固定为 ST 官方 stm32f1xx-hal-driver 提交 `bd368aa335c529641d2e567574885e02deacc64a`，不代表所有 HAL 版本。核查为源码静态分析，未包含固件编译或实机验收。

## 初始化字段及硬件边界

`GPIO_InitTypeDef` 包含四个 `uint32_t` 字段：

| 字段 | 含义与实现条件 |
|---|---|
| Pin | 引脚位掩码，GPIO_PIN_0～15 对应 bit0～15；多个选中引脚共用本次其余配置 |
| Mode | 普通输入、模拟、推挽/开漏输出、复用推挽/开漏、EXTI 中断或事件及边沿模式 |
| Pull | GPIO_NOPULL、GPIO_PULLUP、GPIO_PULLDOWN；本实现仅在输入与 EXTI 模式分支使用 |
| Speed | GPIO_SPEED_FREQ_LOW、MEDIUM、HIGH；本实现仅在普通输出与复用输出分支使用 |

`GPIO_MODE_AF_INPUT` 是 `GPIO_MODE_INPUT` 的别名。不能由名称推断存在单独的“复用输入寄存器模式”。输入是否悬空还取决于 Pull；GPIO_MODE_INPUT 的浮空注释不能覆盖带上拉/下拉的调用。

输入上拉路径先写 BSRR 置 ODR，输入下拉路径先写 BRR 清 ODR，然后更新 CRL/CRH。GPIO_InitTypeDef 没有初始输出电平字段，输出初始化路径不会代替应用设定目标 ODR。输出或复用输出时填写 Pull 不会自动启用内部上拉/下拉。

头文件是全系列接口，掩码存在不证明引脚在 C8T6 封装引出。速度编码、特殊引脚和复用条件见[GPIO模式与寄存器](GPIO模式与寄存器.md)与[EXTI寄存器与路由](EXTI寄存器与路由.md)。官方驱动开头的“所有引脚都有 EXTI”、DAC 示例等通用描述不能覆盖 C8 的 PD0/PD1 等限制，也不能给 C8 添加 DAC。

来源：[GPIO 头文件，字段、模式与宏](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal_gpio.h#L35-L180)；[初始化实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_gpio.c#L170-L340)。

## 初始化与撤销 EXTI

应用先启用相应 GPIO 端口时钟。HAL_GPIO_Init 的 EXTI 分支启用 AFIO 时钟，配置 EXTICR 路由、RTSR/FTSR 边沿以及 EMR/IMR。该函数不清 EXTI_PR，也不配置 NVIC；应用须按实际切换场景协调屏蔽、旧挂起清理、优先级和使能。

再次调用 HAL_GPIO_Init 改成普通输入或输出时，不进入 EXTI 分支。因此此调用本身不能证明旧路由、触发和屏蔽配置已经撤销。

HAL_GPIO_DeInit 仅在 EXTICR 当前端口选择匹配 GPIOx 时清该线的 EXTI 配置；随后仍将所选 GPIO 的 CRL/CRH 字段恢复为浮空输入并清相应 ODR。函数不清 PR，也不处理 NVIC。共享 IRQ 的关闭和其他使用者须由应用协调。

以上为调用职责，不是声称函数必然有缺陷。端口重配置和共享寄存器更新也不构成整体原子事务。

来源：[官方使用说明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_gpio.c#L20-L100)；[Init 与 DeInit](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_gpio.c#L170-L415)。

## 读、写与翻转

- HAL_GPIO_ReadPin 检查 IDR 与传入掩码的结果是否非零。多位掩码返回的是“至少一位为高”，返回值不是引脚位图。
- HAL_GPIO_WritePin 置位和复位均直接写 BSRR，只改变掩码选中的输出锁存位。
- HAL_GPIO_TogglePin 先读取 ODR，再根据读值计算 BSRR 写值。最终写入原子不等于整个翻转操作原子；同一引脚的并发操作者可能基于相同旧值作出同一次翻转，应用仍需协调所有权。

IDR（Input Data Register，输入数据寄存器）反映输入路径；ODR（Output Data Register，输出数据寄存器）保存输出锁存值；BSRR（Bit Set/Reset Register，位置位/复位寄存器）用于按位更新 ODR。锁存值不证明外部引脚已达到目标电平。

来源：[ReadPin、WritePin 与 TogglePin](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_gpio.c#L420-L499)。

## 共享 EXTI 中断的掩码

HAL_GPIO_EXTI_IRQHandler 的处理顺序为：检查 PR 与输入掩码是否非零；用原输入掩码清 PR；调用一次 HAL_GPIO_EXTI_Callback，并传递原输入掩码。

因此把 GPIO_PIN_5 与 GPIO_PIN_6 的组合一次传入，并不会自动获得两次单线回调，也不能由回调参数判定这两条线都曾挂起。共享 IRQ 可逐条用单线掩码分发；如果自行聚合，必须明确保存的挂起快照与新增边沿之间的时序。

`__HAL_GPIO_EXTI_GET_IT` 只读 PR，不检查 IMR。清位宏直接向 PR 写传入掩码。回调参数只包含引脚掩码，不包含端口，也不提供触发边沿类型；端口需结合路由，双边沿模式不能把事后电平读取当作绝对可靠的边沿记录。

来源：[中断处理函数和 weak 回调](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_gpio.c#L540-L575)；[PR 查询及清位宏](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal_gpio.h#L180-L205)。

## 锁定接口注释差异

HAL_GPIO_LockPin 实际返回 HAL_StatusTypeDef，并按锁位确认结果返回 HAL_OK 或 HAL_ERROR；源码邻近的 retval None 注释不能作为返回类型依据。锁定对象仍是 GPIO 配置，不是 ODR 输出状态。

来源：[锁定函数](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_gpio.c#L500-L538)。

## 来源身份与覆盖范围

GPIO C 文件 Git blob：`9fc5944817cbfe4a23501987c74bf6d74dc968a0`；GPIO 头文件 Git blob：`469a2ea1d14097d4929450f1b59d2c8a4ca9cb49`。本页覆盖上述调用分支与字段，不代替全部 GPIO/AFIO 扩展宏或完整硬件手册。
