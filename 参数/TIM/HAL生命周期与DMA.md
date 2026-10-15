# TIM HAL 生命周期、回调与DMA边界

下文明确区分固定旧版共享State与所列新快照的配对通道状态。未执行固件或板端测量。初始化字段与UG另见[初始化约束](HAL初始化边界.md)；输出组合见[输出安全](输出级与保护.md)。


Base 仅管理基本时基；OC、PWM、IC 各有 Init、ConfigChannel、Start/Stop 及中断/DMA变体。OnePulse 以 Init 的 OnePulseMode 决定单次或重复，通道配置指定输入/输出；编码器 Init 同时配置两路输入，其 Start 的 Channel 可选 CH1、CH2 或 ALL。Encoder_Start_DMA 的 pData1/pData2 分别接收 CCR1/CCR2 捕获数据，不是自动输出累计位置数组。

DMA 时 Base 传输到 ARR，OC/PWM 传输到选定 CCR，IC 从 CCR 读入内存；方向必须与 API 一致。普通 Start 不等待完整波形产生；_IT 和 _DMA 也只建立异步操作。Stop 停止该功能后，如果其他通道仍开启，HAL 的共享计数器/主输出保护宏可能不会关闭整个定时器。不要用一个通道的 Stop 推断所有波形均已停止。

**主PWM停止后N端关系可能改变。**在TIM1、CCPC=0、CCxS=00、CCxE=CCxNE=1、MOE=1、GPIO/AFIO已正确配置且没有其他故障/配置变化时，`HAL_TIM_PWM_Stop`先清主CCxE。若CCxNE仍为1，条件宏`__HAL_TIM_MOE_DISABLE`及`__HAL_TIM_DISABLE`均保留MOE/CEN；此时N端不再取反，而是OCxREF经CCxNP极性输出（CCxNP=0时跟随参考）。OSSI在MOE=1时无关；OSSR=0/1只改变已停主端的释放/无效处理，均不阻止上述N端关系改变。CCPC=1须另按COM实际装载时刻分析。

该路径已核对[HAL v1.1.4 Stop实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim.c#L1332-L1354)、[v1.1.10 Stop实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_tim.c#L1508-L1532)及[同版条件宏](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_tim.h#L1086-L1113)；输出关系依据RM0008 Rev21 p322及p355表83。主/N用于功率级时，应先通过系统既有、已验证的整组或外部驱动关断路径建立安全态，再收回主/N通道、DMA和计数资源；顺次调用两个Stop不保证中间态安全。整组MOE会影响其他通道，MOE=0的电平又受OSSI/OIS/GPIO决定，因此不能用“无条件清MOE”替代系统关断设计。

句柄 State 为 HAL_TIM_StateTypeDef：RESET 未初始化，READY 可用，BUSY 正在处理，TIMEOUT 超时，ERROR 错误。各 GetState 返回同一类软件状态，不能据此代替 CEN、CCxE 或 MOE 的硬件读回。回调中的 htim->Channel 使用 HAL_TIM_ACTIVE_CHANNEL_1/2/3/4 或 CLEARED，和 TIM_CHANNEL_1/2/3/4 的参数编码不同。回调通常处于 IRQ 上下文，应避免阻塞、长延时和对同一锁定句柄递归启动。

DMABurst 的 BurstBaseAddress 是 TIM 寄存器相对索引，不是内存地址；BurstLength 是编码的突发长度，原文这组 Start 要求其解码后的传输项数与 DMA 数据项数一致。缓冲区有效期延续到停止或完成。突发不得跨入实例不存在的高级寄存器。

### TIM 软件枚举与 DMA 关联索引

HAL_TIM_STATE_RESET、HAL_TIM_STATE_READY、HAL_TIM_STATE_BUSY、HAL_TIM_STATE_TIMEOUT、HAL_TIM_STATE_ERROR 分别表示复位、就绪、忙、超时、错误。HAL_TIM_ACTIVE_CHANNEL_1/2/3/4 表示回调当前活动通道，HAL_TIM_ACTIVE_CHANNEL_CLEARED 表示未标记活动通道。

hdma[7] 的索引依次为 TIM_DMA_ID_UPDATE=0、TIM_DMA_ID_CC1=1、TIM_DMA_ID_CC2=2、TIM_DMA_ID_CC3=3、TIM_DMA_ID_CC4=4、TIM_DMA_ID_COMMUTATION=5、TIM_DMA_ID_TRIGGER=6。这些是句柄数组下标，不是 DMA1 物理通道号；物理映射必须另查 DMA 请求表。

### 动态回调注册的完整条件

UM1850 的使用说明还介绍了 `HAL_TIM_RegisterCallback()` 与 `HAL_TIM_UnRegisterCallback()`，虽然本章后续详细函数列表没有展开其原型。这项能力要求编译宏 `USE_HAL_TIM_REGISTER_CALLBACKS=1`；Register 接受句柄、回调 ID、用户函数指针，UnRegister 将对应项恢复为弱函数。应以项目配套头文件核对具体声明，不能仅凭这段说明给旧版本补造函数。

可注册的回调包括：
- Base、IC、OC、PWM、OnePulse、Encoder、HallSensor 各自的 MspInitCallback 和 MspDeInitCallback。
- PeriodElapsedCallback、PeriodElapsedHalfCpltCallback、TriggerCallback、TriggerHalfCpltCallback。
- IC_CaptureCallback、IC_CaptureHalfCpltCallback、OC_DelayElapsedCallback。
- PWM_PulseFinishedCallback、PWM_PulseFinishedHalfCpltCallback、ErrorCallback。
- CommutationCallback、CommutationHalfCpltCallback、BreakCallback。

普通事件回调仅可在 `HAL_TIM_STATE_READY` 注册/注销；MSP 初始化/释放回调还允许在 `HAL_TIM_STATE_RESET` 注册/注销，因此要在 Init/DeInit 前预先注册。RESET 状态执行 Init 时事件回调恢复默认弱函数；MSP 回调是例外，只有指针为空才回落到默认弱函数，已注册非空项会保留并使用。宏为0或未定义时没有动态注册，使用对应弱函数。


## 停机、DMA完成与软件状态的实现边界

这里依据 [HAL v1.1.4 TIM 实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim.c) 和[同版头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h)，保留与 UM1850 接近的状态机边界：

- `Base_Stop`/`Base_Stop_IT`/`Base_Stop_DMA` 经 `__HAL_TIM_DISABLE` 尝试停止计数器。若 CCER 中还有主或互补通道使能，宏不会清 CEN；函数仍可置 READY/返回 OK。停止一条 PWM/OC/IC 通道也不能解释成其他通道或整个定时器已停。需要全停时应先清楚所有用户和输出的停机顺序，并读回所需 CEN/CCER/MOE 状态。
- `Base_Start_DMA`、`PWM_Start_DMA` 等在真正启动 DMA 前已将旧版共享 `htim->State` 设为 BUSY、安装内部回调；底层 DMA 启动失败会返回 ERROR，但并不统一回滚这些软件状态。不要见 ERROR 就直接反复重试；先核对并清理已改变状态及相关 DMA 资源。
- `Encoder_Start_DMA(..., TIM_CHANNEL_ALL, ...)` 依次启动两条 DMA。若第二条失败，第一条可能已经启用；返回 ERROR 不是“两条均未启动”的保证。该旧版 READY 路径还会检查 pData1/pData2 两个指针，即使只选一条通道，也不能据名称假定另一个 NULL 必被接受。
- 旧版的 DMA 全完成回调以及部分半完成回调会把 TIM 的共享 State 置 READY；循环 DMA 中也不能据此判定缓冲区停止。DMA 句柄本身的 BUSY/READY 与 TIM 句柄 State 是不同状态机。普通/循环完成后通常仍保留定时器 CEN、输出和相应请求配置，应由明确 Stop 流程结束。
- `PWM_PulseFinishedCallback` 从 DMA 路径到达时表示 DMA 数据搬运结束，不保证最后一个 PWM 脉冲已经在引脚上完整输出。CCR 预装载和下次更新可能仍待生效；需要在最后波形完成后关闭输出的应用必须按定时器事件另行确认，不能在 DMA TC 时无条件停机截断波形。
- 捕获值读取有清 CCxIF 的硬件副作用；[ES096](https://www.st.com/resource/en/errata_sheet/es096-stm32f101x8b-stm32f102x8b-and-stm32f103x8b-mediumdensity-device-limitations-stmicroelectronics.pdf) §2.6.5/§2.6.6 还允许捕获/读取竞争导致标志漏报或 CCxOF 误报。HAL/LL 函数不能使标志成为无丢样保证，必要时按勘误辅助检测并控制采样速率。

[固定新快照](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_tim.c) 已引入独立通道状态、正常/循环 DMA 的差异处理和部分 const 源指针。具体核对入口为[Base_Start_DMA L526起](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_tim.c#L526-L590)及[脉冲/捕获完成回调 L6499–6653](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_tim.c#L6499-L6653)：列出的完成回调仅在DMA_NORMAL分支把相应通道状态置READY；不能据此推断计数、输出或DMA请求均已关闭。这里不把它们混入 UM1850 Rev3 原型/句柄表，也不把旧版共享状态机泛化为所有版本。工程必须对照实际所用发布包。

## 单脉冲参数与通道成对启停

UM1850 Rev 3 第 36 章逐函数表（第 489–490 页）把四个 `HAL_TIM_OnePulse_Start/Stop`（含 `_IT`）接口的 OutputChannel 列为 CH1/CH2 选择。直接核对 [v1.1.4 函数体](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim.c#L2412-L2563)，四者实际均执行 `UNUSED(OutputChannel)`，同时启用或禁用 CC1E、CC2E；IT 变体同时开关 CC1IE、CC2IE。Start 不置 CEN，计数由 OnePulse_ConfigChannel 建立的从模式触发路径启动。不能靠传不同 OutputChannel 改换输出、只停其中一路，或把 Start 当作立即软件发脉冲。

[固定新快照](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_tim.c#L2768-L2995) 已在注释明确该参数为兼容保留且被忽略，并加入通道状态检查，但上述成对启停和不主动置 CEN 的行为仍相同。这一结论仅针对普通 OnePulse 四接口；`HAL_TIMEx_OnePulseN_*` 使用 OutputChannel 选择 N 通道，不能一并视为忽略。


## Encoder双DMA失败后的配对恢复

既有“ALL第二路启动失败不回滚第一路”的旧版说明继续有效。本次进一步对照[v1.1.4 Encoder Start/Stop](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim.c#L2965-L3143)与[v1.1.10](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_tim.c#L3532-L3799)，补充可观测状态与停止前提。

干净初态下，第二路DMA启动失败时，第一路DMA已BUSY/EN=1，但TIM的CC1DE/CC2DE、CC1E/CC2E、CEN尚未开放；不能把DMA占用写成定时器已开始采集。v1.1.4留下共享htim.State=BUSY；v1.1.10改用配对ChannelState/ChannelNState，四项可BUSY而共享State仍READY。ChannelNState是HAL软件字段，不代表该TIM/封装实际具有互补引脚。

两版Encoder_Stop_DMA(ALL)均丢弃底层两次Abort_IT返回值，并更新TIM状态后返回OK。正常配对恢复仍要求两路DMA属于同一操作，并排除并发或重启型回调；须分别验证停止后的状态。第二路若仍RESET，Stop虽返回OK且TIM状态复位，第二路DMA仍RESET；不先修复初始化而重试，会再次留下第一路已启动。只停CH1也不构成双路恢复，旧版共享READY尤其容易掩盖另一DMA仍BUSY。

恢复前先确认两路DMA都归本操作所有，不能通过Stop(ALL)误停其他事务。Start在尝试底层启动之前已改写相关完成/半满/错误回调，发生争用后不能声称别人的DMA配置仍原样。分别核验两路DMA的EN、状态、锁及中断配置，TIM的请求/通道使能，以及当前版本的配对软件状态；状态不合法时按真实初始化/MSP修复，不能手改READY解锁。其他TIM通道仍使能时，共享保护可保留CEN；编码器双路已停与整颗定时器已停须分开验收。

本篇沿用源码状态边界，不把既有主机检查扩展为板端在途搬运或总线竞争的验证；停止后缓冲区是否仍可能被写入须按实际DMA状态确认。


## DMA burst 请求选择、空指针检查与停止差异

以下直接比较两个固定快照：v1.1.4对应de129f1；v1.1.10对应77fbb30。分析限于函数控制流与传给底层的参数，未执行DMA或固件。

BurstRequestSrc在这些Start/Stop接口中应选择单个TIM_DMA_UPDATE、TIM_DMA_CC1～CC4、TIM_DMA_COM或TIM_DMA_TRIGGER。头文件的IS_TIM_DMA_SOURCE只检查非零和允许位范围，允许多个合法位按位或；函数内部switch却按单个枚举值匹配，不能把断言接受视为接口支持组合请求。

下表Start分支以旧版State或新版DMABurstState初始READY、除所讨论条件外其他参数/关联合法为前提；BUSY等提前返回路径另行判断。

|情形|固定v1.1.4|固定v1.1.10|
|---|---|---|
|Start传组合请求位|switch走default，不启动所列单路DMA；仍写DCR、开放传入请求位、把共享State设READY并返回HAL_OK|WriteStart/ReadStart转入Multi入口；default报HAL_ERROR且不执行末尾DCR/请求使能，但此前DMABurstState可已从READY变BUSY|
|Stop传组合请求位|default不调用各路Abort；默认status仍OK，于是清传入请求位并返回OK|default设HAL_ERROR；不进入末尾请求关闭/DMABurstState复位分支|
|合法单一请求Stop，底层Abort_IT失败|保留失败status并返回；只在status为OK时清TIM请求位|丢弃Abort_IT返回值；仍清TIM请求位、置DMABurstState=READY，并返回HAL_OK|
|合法Start成功|最后共享State被设READY，不代表DMA已结束|使用独立DMABurstState，不沿用旧版共享State规则|

两版TIM层的空缓冲检查都使用“BurstBuffer为NULL且BurstLength>0”。TIM_DMABURSTLENGTH_1TRANSFER的编码恰为0，但实际需要传输1项，所以单项突发时该检查不拒绝NULL。固定新快照的Multi入口仍使用BurstLength作这一判断，不能根据另一个DataLength参数非零就假定检查已补全。合法调用必须自行保证缓冲区非空、可访问、长度和传输宽度匹配；这里只确认TIM层可把零地址继续作为参数传给HAL_DMA_Start_IT，不假定底层及硬件会以某种特定方式成功或失败。

状态也须按入口前提校验：代码只对BUSY提前返回、对READY执行这段检查，其他状态分支不会自动保证拒绝继续配置。底层DMA启动失败前，TIM状态及DMA回调可能已经改变，返回错误不代表无副作用。

来源：[v1.1.4 WriteStart/WriteStop，L3812–4040](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim.c#L3812-L4040)、[ReadStart/ReadStop，L4077–4300](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim.c#L4077-L4300)、[v1.1.10 MultiWriteStart及WriteStop，L4533–4786](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_tim.c#L4533-L4786)、[MultiReadStart及ReadStop，L4869–5121](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_tim.c#L4869-L5121)。单项编码及断言见[旧版头文件L925](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L925)、[L1570](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L1570)与[新版同类断言L1645](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_tim.h#L1645)。

## 回调 ID、句柄字段与默认函数

状态：固定源码核查；未做硬件测试。

### 适用版本与条件

固定来源：[STM32F1 HAL TIM 头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_tim.h#L327-L397)；[注册与注销实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim.c#L5012-L5457)。以下字段及注册接口以 USE_HAL_TIM_REGISTER_CALLBACKS == 1 为编译条件。回调函数类型为 void (*)(TIM_HandleTypeDef *htim)。htim 指向对应定时器句柄。

READY 状态允许注册/注销下表全部 27 项；RESET 状态仅允许 0x00–0x0D 共 14 项 MSP 回调。其余状态、未定义 ID 返回 HAL_ERROR。RegisterCallback 的空函数指针在加锁前返回 HAL_ERROR。锁竞争返回值还依赖 __HAL_LOCK 定义，此补充不新增该依赖的核验结论。UnRegisterCallback 将字段恢复为下表默认弱回调，不清空为 NULL，也不关闭硬件中断或停止 DMA。

| ID | 数值 | TIM_HandleTypeDef 条件字段 | 注销后的默认函数 |
|---|---|---|---|
| HAL_TIM_BASE_MSPINIT_CB_ID | 0x00 | Base_MspInitCallback | HAL_TIM_Base_MspInit |
| HAL_TIM_BASE_MSPDEINIT_CB_ID | 0x01 | Base_MspDeInitCallback | HAL_TIM_Base_MspDeInit |
| HAL_TIM_IC_MSPINIT_CB_ID | 0x02 | IC_MspInitCallback | HAL_TIM_IC_MspInit |
| HAL_TIM_IC_MSPDEINIT_CB_ID | 0x03 | IC_MspDeInitCallback | HAL_TIM_IC_MspDeInit |
| HAL_TIM_OC_MSPINIT_CB_ID | 0x04 | OC_MspInitCallback | HAL_TIM_OC_MspInit |
| HAL_TIM_OC_MSPDEINIT_CB_ID | 0x05 | OC_MspDeInitCallback | HAL_TIM_OC_MspDeInit |
| HAL_TIM_PWM_MSPINIT_CB_ID | 0x06 | PWM_MspInitCallback | HAL_TIM_PWM_MspInit |
| HAL_TIM_PWM_MSPDEINIT_CB_ID | 0x07 | PWM_MspDeInitCallback | HAL_TIM_PWM_MspDeInit |
| HAL_TIM_ONE_PULSE_MSPINIT_CB_ID | 0x08 | OnePulse_MspInitCallback | HAL_TIM_OnePulse_MspInit |
| HAL_TIM_ONE_PULSE_MSPDEINIT_CB_ID | 0x09 | OnePulse_MspDeInitCallback | HAL_TIM_OnePulse_MspDeInit |
| HAL_TIM_ENCODER_MSPINIT_CB_ID | 0x0A | Encoder_MspInitCallback | HAL_TIM_Encoder_MspInit |
| HAL_TIM_ENCODER_MSPDEINIT_CB_ID | 0x0B | Encoder_MspDeInitCallback | HAL_TIM_Encoder_MspDeInit |
| HAL_TIM_HALL_SENSOR_MSPINIT_CB_ID | 0x0C | HallSensor_MspInitCallback | HAL_TIMEx_HallSensor_MspInit |
| HAL_TIM_HALL_SENSOR_MSPDEINIT_CB_ID | 0x0D | HallSensor_MspDeInitCallback | HAL_TIMEx_HallSensor_MspDeInit |
| HAL_TIM_PERIOD_ELAPSED_CB_ID | 0x0E | PeriodElapsedCallback | HAL_TIM_PeriodElapsedCallback |
| HAL_TIM_PERIOD_ELAPSED_HALF_CB_ID | 0x0F | PeriodElapsedHalfCpltCallback | HAL_TIM_PeriodElapsedHalfCpltCallback |
| HAL_TIM_TRIGGER_CB_ID | 0x10 | TriggerCallback | HAL_TIM_TriggerCallback |
| HAL_TIM_TRIGGER_HALF_CB_ID | 0x11 | TriggerHalfCpltCallback | HAL_TIM_TriggerHalfCpltCallback |
| HAL_TIM_IC_CAPTURE_CB_ID | 0x12 | IC_CaptureCallback | HAL_TIM_IC_CaptureCallback |
| HAL_TIM_IC_CAPTURE_HALF_CB_ID | 0x13 | IC_CaptureHalfCpltCallback | HAL_TIM_IC_CaptureHalfCpltCallback |
| HAL_TIM_OC_DELAY_ELAPSED_CB_ID | 0x14 | OC_DelayElapsedCallback | HAL_TIM_OC_DelayElapsedCallback |
| HAL_TIM_PWM_PULSE_FINISHED_CB_ID | 0x15 | PWM_PulseFinishedCallback | HAL_TIM_PWM_PulseFinishedCallback |
| HAL_TIM_PWM_PULSE_FINISHED_HALF_CB_ID | 0x16 | PWM_PulseFinishedHalfCpltCallback | HAL_TIM_PWM_PulseFinishedHalfCpltCallback |
| HAL_TIM_ERROR_CB_ID | 0x17 | ErrorCallback | HAL_TIM_ErrorCallback |
| HAL_TIM_COMMUTATION_CB_ID | 0x18 | CommutationCallback | HAL_TIMEx_CommutCallback |
| HAL_TIM_COMMUTATION_HALF_CB_ID | 0x19 | CommutationHalfCpltCallback | HAL_TIMEx_CommutHalfCpltCallback |
| HAL_TIM_BREAK_CB_ID | 0x1A | BreakCallback | HAL_TIMEx_BreakCallback |

核验方法：逐一比较固定头文件 ID 数值、RegisterCallback switch 对应字段及 UnRegisterCallback 对应字段/默认函数。27 项字段映射一致。HAL_TIM_HALL_SENSOR_MSPINIT_CB_ID 的用途按标识符与实际 switch 映射确定；原头文件该枚举行的 DeInit 注释不能覆盖实际 MspInit 行为。


## 捕获DMA的请求时机与旧配置

输入捕获DMA需同时核对CCxDE与CR2.CCDS：CCxDE允许请求，CCDS决定请求跟随CCx事件（0）还是更新事件（1）。DMA地址指向CCRx，只决定请求到达后访问哪个寄存器，不替代事件源选择。按RM0008 Rev21 CR2字段（TIM1 p341、TIM2～4 p406），需要逐次捕获搬运时应明确建立CCDS=0；沿用CCDS=1不能把DMA传输计数解释为捕获事件计数。

核对固定de129f1和77fbb30的HAL_TIM_IC_Init、HAL_TIM_IC_ConfigChannel与HAL_TIM_IC_Start_DMA及其TIM_Base_SetConfig、CH2配置辅助路径：这些库内路径没有把CR2.CCDS恢复为0。Start_DMA为CH2设置CCR2地址并允许CC2DE；MSP/回调属于应用可自定义边界，可能另作配置，本结论不包括它们。因而“重新调用IC初始化/启动”不足以证明以前的DMA请求时机选择已被清除。

同理，固定TIM_Base_SetConfig更新CR1的DIR/CMS、CKD、ARPE并写PSC/ARR及UG，没有统一清除原OPM/UDIS。连续捕获的配置前提应由应用建立；停止计数后还须先退出使DIR只读的中心/编码器模式，再按目标方向配置。修改实例级状态前应协调所有共享通道。

固定源码：[旧版IC Init L1744–1789](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim.c#L1744-L1789)、[旧版IC Start_DMA L2053–2175](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_tim.c#L2053-L2175)、[新版IC Start_DMA L2364–2510](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_tim.c#L2364-L2510)。这是固定源码控制流与寄存器字段的交叉核查，未执行固件或板测。

[返回定时器主题](../../知识库/06_定时器PWM与同步.md) · [图形关系与来源](图形关系与来源.md)
