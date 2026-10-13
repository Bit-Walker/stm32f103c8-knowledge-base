# Smartcard 与 IrDA：配置、句柄、回调与控制宏
来源为固定 HAL F1 v1.1.4 / v1.1.10 的专用头文件。Smartcard两版Init结构均11个uint32_t字段；IrDA两版均6个字段，其中Prescaler为uint8_t，其余为uint32_t。字段集合、类型和顺序已逐项对照。

## 初始化字段
|Smartcard字段|寄存器/含义|边界|
|---|---|---|
|BaudRate|BRR目标位率，bit/s|断言仅上限，必须排除0并检查PCLK条件|
|WordLength|CR1.M|该模块仅接受9B；有效8位载荷加校验|
|StopBits|CR2.STOP|0.5或1.5；具体硬件接收/FE条件见模式页|
|Parity|CR1.PCE/PS|奇或偶校验|
|Mode|CR1.TE/RE|接收、发送或两者的初始化使能组合|
|CLKPolarity|CR2.CPOL|LOW/HIGH字段写值；卡时钟频率另由PSC确定|
|CLKPhase|CR2.CPHA|1EDGE/2EDGE字段写值；不由此推出Smartcard数据位与CK同步|
|CLKLastBit|CR2.LBCL|ENABLE/DISABLE字段写值；普通同步最后数据脉冲语义不外推到卡时钟|
|Prescaler|GTPR.PSC|有效5位，合法1..31；f_CK=f_PCLK/(2×PSC)|
|GuardTime|GTPR.GT|8位保护时间，单位波特率时钟周期；类型uint32_t不等于硬件字段32位|
|NACKState|CR3.NACK|校验错误负应答使能|

f_PCLK为相应USART的APB时钟频率，单位Hz；PSC为无量纲预分频寄存器值；f_CK为向卡输出的时钟频率，单位Hz。SMARTCARD_PRESCALER_SYSCLK_DIVxx的符号名称保留官方拼写；实际时钟源应按RM0008和具体实例PCLK确认，不能从符号名称替换为SYSCLK。
SMARTCARD_SetConfig明确在CR2组合中加入CLKEN。该HAL初始化实现会开启CK输出路径，不提供独立ClockEnable成员。硬件配置范围与该函数的具体写操作分别说明。
GuardTime与Prescaler没有在已查Init/SetConfig中做独立范围断言；本页不在未闭合MODIFY_REG基础定义的前提下推导非法值的精确写溢出结果。

|IrDA字段|寄存器/含义|边界|
|---|---|---|
|BaudRate|BRR目标位率，bit/s|必须正数；专用断言最大115200|
|WordLength|CR1.M|8B/9B；结合Parity确定有效载荷和已查CPU访问条件|
|Parity|CR1.PCE/PS|无、奇、偶|
|Mode|CR1.TE/RE|初始化方向使能；不解除IrDA半双工约束|
|Prescaler|GTPR.PSC，uint8_t|普通模式1；低功耗1..255；0不可用|
|IrDAMode|CR3.IRLP|NORMAL或LOWPOWER|

IrDA结构没有StopBits成员；SetConfig和Init清STOP，采用1停止位。两个Init结构不是可互换布局，不能通过强转替代分别配置。

## 配置符号

以下配置符号的两版定义一致；数值为寄存器编码，不能用字面整数8、9或停止位小数代替对应符号。

### SMARTCARD 配置符号

|符号|固定头文件定义|
|---|---|
|`SMARTCARD_WORDLENGTH_9B`|`((uint32_t)USART_CR1_M)`|
|`SMARTCARD_STOPBITS_0_5`|`((uint32_t)USART_CR2_STOP_0)`|
|`SMARTCARD_STOPBITS_1_5`|`((uint32_t)(USART_CR2_STOP_0 \| USART_CR2_STOP_1))`|
|`SMARTCARD_PARITY_EVEN`|`((uint32_t)USART_CR1_PCE)`|
|`SMARTCARD_PARITY_ODD`|`((uint32_t)(USART_CR1_PCE \| USART_CR1_PS))`|
|`SMARTCARD_MODE_RX`|`((uint32_t)USART_CR1_RE)`|
|`SMARTCARD_MODE_TX`|`((uint32_t)USART_CR1_TE)`|
|`SMARTCARD_MODE_TX_RX`|`((uint32_t)(USART_CR1_TE \|USART_CR1_RE))`|
|`SMARTCARD_POLARITY_LOW`|`0x00000000U`|
|`SMARTCARD_POLARITY_HIGH`|`((uint32_t)USART_CR2_CPOL)`|
|`SMARTCARD_PHASE_1EDGE`|`0x00000000U`|
|`SMARTCARD_PHASE_2EDGE`|`((uint32_t)USART_CR2_CPHA)`|
|`SMARTCARD_LASTBIT_DISABLE`|`0x00000000U`|
|`SMARTCARD_LASTBIT_ENABLE`|`((uint32_t)USART_CR2_LBCL)`|
|`SMARTCARD_NACK_ENABLE`|`((uint32_t)USART_CR3_NACK)`|
|`SMARTCARD_NACK_DISABLE`|`0x00000000U`|

### IRDA 配置符号

|符号|固定头文件定义|
|---|---|
|`IRDA_WORDLENGTH_8B`|`0x00000000U`|
|`IRDA_WORDLENGTH_9B`|`((uint32_t)USART_CR1_M)`|
|`IRDA_PARITY_NONE`|`0x00000000U`|
|`IRDA_PARITY_EVEN`|`((uint32_t)USART_CR1_PCE)`|
|`IRDA_PARITY_ODD`|`((uint32_t)(USART_CR1_PCE \| USART_CR1_PS))`|
|`IRDA_MODE_RX`|`((uint32_t)USART_CR1_RE)`|
|`IRDA_MODE_TX`|`((uint32_t)USART_CR1_TE)`|
|`IRDA_MODE_TX_RX`|`((uint32_t)(USART_CR1_TE \|USART_CR1_RE))`|
|`IRDA_POWERMODE_LOWPOWER`|`((uint32_t)USART_CR3_IRLP)`|
|`IRDA_POWERMODE_NORMAL`|`0x00000000U`|

Smartcard预分频符号SMARTCARD_PRESCALER_SYSCLK_DIV2、DIV4、…、DIV62共31项，依次对应PSC=1、2、…、31，两版逐项核对一致。完整符号中的SYSCLK保留官方命名，时钟来源仍按前文PCLK解释。

## 句柄成员

|字段|类型或版本差异|含义/限制|
|---|---|---|
|Instance|USART_TypeDef *|器件寄存器实例|
|Init|对应SMARTCARD_InitTypeDef / IRDA_InitTypeDef|两模块配置布局不同|
|pTxBuffPtr|旧uint8_t *；新const uint8_t *|指向发送数据；const限定数据，不禁止驱动移动指针成员|
|TxXferSize|uint16_t|发送长度；单位与CPU/DMA路径条件分别核对|
|TxXferCount|__IO uint16_t|路径维护的发送计数；初始化/更新依具体函数，不替代DMA CNDTR读数|
|pRxBuffPtr|uint8_t *|接收数据指针|
|RxXferSize|uint16_t|接收长度；不自动表示已分配字节数|
|RxXferCount|__IO uint16_t|接收计数；须按具体启动路径确认初始化与更新|
|hdmatx|DMA_HandleTypeDef *|发送DMA关联|
|hdmarx|DMA_HandleTypeDef *|接收DMA关联|
|Lock|HAL_LockTypeDef|软件句柄锁字段；不等于DMA资源状态|
|gState|__IO HAL_SMARTCARD_StateTypeDef / __IO HAL_IRDA_StateTypeDef|全局管理与TX状态|
|RxState|对应的__IO状态枚举类型|接收状态|
|ErrorCode|__IO uint32_t|驱动错误码；清除/按位累加/覆盖因路径而异|

### 条件回调成员

当对应USE_HAL_*_REGISTER_CALLBACKS==1时，两个句柄都有TxCpltCallback、RxCpltCallback、ErrorCallback、AbortCpltCallback、AbortTransmitCpltCallback、AbortReceiveCpltCallback、MspInitCallback、MspDeInitCallback；IrDA再有TxHalfCpltCallback和RxHalfCpltCallback。每个成员返回void并接受对应模块句柄指针。注册宏取值会改变结构成员集合，工程与库须使用一致的编译配置。

## 状态枚举

下表后缀分别加HAL_SMARTCARD_STATE_或HAL_IRDA_STATE_，两模块两版数值一致；允许写入对象取自固定头文件注释。

|后缀|值|允许对象/解释|
|---|---|---|
|RESET|0x00|gState、RxState|
|READY|0x20|gState、RxState|
|BUSY|0x24|仅gState，内部处理|
|BUSY_TX|0x21|仅gState|
|BUSY_RX|0x22|仅RxState|
|BUSY_TX_RX|0x23|合成结果，不应直接写为gState或RxState|
|TIMEOUT|0xA0|仅gState|
|ERROR|0xE0|仅gState|

GetState依次读取gState和RxState后按位或返回；函数本体没有对两次读取提供一致快照保护。它反映软件句柄，不读取TC或DMA EN/CNDTR，也不证明IrDA半双工限制已解除。GetError直接返回ErrorCode。

## 错误码

后缀分别加HAL_SMARTCARD_ERROR_或HAL_IRDA_ERROR_；两模块两版位值相同。INVALID_CALLBACK仅对应回调注册配置为1时定义。

|后缀|值|含义|
|---|---|---|
|NONE|0x00|无错误码|
|PE|0x01|校验错误|
|NE|0x02|噪声错误|
|FE|0x04|帧错误|
|ORE|0x08|溢出错误|
|DMA|0x10|DMA错误|
|INVALID_CALLBACK|0x20|回调参数/状态不允许|

## 回调ID

两模块的回调ID不能只按相同数字互换；应使用对应模块的完整符号。以下每个模块的两版值相同。

### Smartcard

|符号|ID|
|---|---|
|`HAL_SMARTCARD_TX_COMPLETE_CB_ID`|0x00|
|`HAL_SMARTCARD_RX_COMPLETE_CB_ID`|0x01|
|`HAL_SMARTCARD_ERROR_CB_ID`|0x02|
|`HAL_SMARTCARD_ABORT_COMPLETE_CB_ID`|0x03|
|`HAL_SMARTCARD_ABORT_TRANSMIT_COMPLETE_CB_ID`|0x04|
|`HAL_SMARTCARD_ABORT_RECEIVE_COMPLETE_CB_ID`|0x05|
|`HAL_SMARTCARD_MSPINIT_CB_ID`|0x08|
|`HAL_SMARTCARD_MSPDEINIT_CB_ID`|0x09|

### IrDA

|符号|ID|
|---|---|
|`HAL_IRDA_TX_HALFCOMPLETE_CB_ID`|0x00|
|`HAL_IRDA_TX_COMPLETE_CB_ID`|0x01|
|`HAL_IRDA_RX_HALFCOMPLETE_CB_ID`|0x02|
|`HAL_IRDA_RX_COMPLETE_CB_ID`|0x03|
|`HAL_IRDA_ERROR_CB_ID`|0x04|
|`HAL_IRDA_ABORT_COMPLETE_CB_ID`|0x05|
|`HAL_IRDA_ABORT_TRANSMIT_COMPLETE_CB_ID`|0x06|
|`HAL_IRDA_ABORT_RECEIVE_COMPLETE_CB_ID`|0x07|
|`HAL_IRDA_MSPINIT_CB_ID`|0x08|
|`HAL_IRDA_MSPDEINIT_CB_ID`|0x09|

## 注册与注销的状态/版本条件

- RegisterCallback检查pCallback非空；空指针会记录INVALID_CALLBACK并返回HAL_ERROR。
- gState=READY允许注册本模块支持的回调ID；gState=RESET只允许MSP Init/DeInit回调，其余状态/不支持ID按错误路径处理。UnRegisterCallback采用同样状态分支，并恢复对应弱默认回调。
- 这四个函数都不检查RxState。只有RX忙而gState保持READY的情形，不会因RxState=BUSY_RX自动被状态分支拒绝；不能把注册成功当作当前收发均已空闲的证明。
- 固定v1.1.4四个Register/UnRegister函数含__HAL_LOCK与__HAL_UNLOCK调用；v1.1.10相应调用已移除。去掉注释/空白及这两类调用后，四对函数体逐对相同。不推断改动动机，也不把旧句柄锁当作中断并发安全证明。
- 更换活动接收将调用的回调，需由应用协调传输生命周期与中断执行；函数的gState检查没有提供完整的接收回调更换同步协议。


## 宏语义
- RESET_HANDLE_STATE只把gState、RxState置RESET；回调注册配置为1时还清MspInitCallback/MspDeInitCallback。它不停止DMA、不清锁、不清错误码、不释放缓冲，也不清全部事件回调。
- FLUSH_DRREGISTER直接读取DR；与软件缓冲指针、计数、DMA状态无关。读取副作用依USART寄存器规定，不能作为缓冲资源交还证明。
- CLEAR_FLAG写SR的位清除形式适用于其文档列出的TC/RXNE；PE/FE/NE/ORE/IDLE使用专门宏执行SR→DR读序列。按别名依次调用多种错误清除宏会重复读DR，应按单次状态快照/处理策略审查。
- GET_FLAG读取SR并比较所给标志位；GET_IT_SOURCE读取CR1/CR2/CR3中的使能掩码，未读取SR。GET_IT_SOURCE返回原掩码结果，应以非零判断使能，不能要求所有已使能项都返回整数1；其“interrupt has occurred”注释不能替代实际事件判定。
- ENABLE_IT / DISABLE_IT的参数含高4位寄存器索引，先选单个CR再操作低位掩码。应分别处理不同寄存器编码，不把跨CR编码按位或作为通用中断集合。编码推导：PE索引1、低位0x100；ERR索引3、低位0x1。按位或后索引为3、低位0x101，会选择CR3，那里bit8是RTSE、bit0是EIE。该推导说明参数编码约束，不声称这是合法单值调用下的驱动缺陷。

证据：Smartcard新版H46–88、H400–405、H424–600、H681–687；IrDA新版H45–72、H314–323、H343–516、H604–609；Smartcard SetConfig C2256–2333。固定CMSIS stm32f103xb.h 的PEIE bit8为L9495–9497，EIE bit0为L9548–9550，RTSE bit8为L9572–9574。全部30个__HAL_SMARTCARD_* / __HAL_IRDA_*宏名的两版定义体已逐项比对，去注释和空白后相同；RESET_HANDLE_STATE的两种回调编译分支分别保留。此处不表示全部私有基础宏已展开闭合。


ENABLE/DISABLE围绕UE操作；Smartcard的DMA_REQUEST_ENABLE/DISABLE围绕CR3请求位操作。它们本身没有调用DMA终止流程、等待TC或完成软件缓冲所有权交接。具体关闭时刻与安全恢复仍需结合硬件和DMA生命周期。

## 宏定位索引

以下行号均为固定专用头文件；斜线分隔RESET的两种编译分支。

|宏名|v1.1.4行号|v1.1.10行号|
|---|---|---|
|`__HAL_SMARTCARD_CLEAR_FEFLAG`|500|499|
|`__HAL_SMARTCARD_CLEAR_FLAG`|480|479|
|`__HAL_SMARTCARD_CLEAR_IDLEFLAG`|521|520|
|`__HAL_SMARTCARD_CLEAR_NEFLAG`|507|506|
|`__HAL_SMARTCARD_CLEAR_OREFLAG`|514|513|
|`__HAL_SMARTCARD_CLEAR_PEFLAG`|487–493|486–492|
|`__HAL_SMARTCARD_DISABLE`|581|580|
|`__HAL_SMARTCARD_DISABLE_IT`|552–553|551–552|
|`__HAL_SMARTCARD_DMA_REQUEST_DISABLE`|601|600|
|`__HAL_SMARTCARD_DMA_REQUEST_ENABLE`|591|590|
|`__HAL_SMARTCARD_ENABLE`|574|573|
|`__HAL_SMARTCARD_ENABLE_IT`|536–537|535–536|
|`__HAL_SMARTCARD_FLUSH_DRREGISTER`|444|443|
|`__HAL_SMARTCARD_GET_FLAG`|461|460|
|`__HAL_SMARTCARD_GET_IT_SOURCE`|567|566|
|`__HAL_SMARTCARD_RESET_HANDLE_STATE`|426–431 / 433–436|425–430 / 432–435|
|`__HAL_IRDA_CLEAR_FEFLAG`|425|424|
|`__HAL_IRDA_CLEAR_FLAG`|403|402|
|`__HAL_IRDA_CLEAR_IDLEFLAG`|449|448|
|`__HAL_IRDA_CLEAR_NEFLAG`|433|432|
|`__HAL_IRDA_CLEAR_OREFLAG`|441|440|
|`__HAL_IRDA_CLEAR_PEFLAG`|411–417|410–416|
|`__HAL_IRDA_DISABLE`|517|516|
|`__HAL_IRDA_DISABLE_IT`|482–484|481–483|
|`__HAL_IRDA_ENABLE`|509|508|
|`__HAL_IRDA_ENABLE_IT`|465–467|464–466|
|`__HAL_IRDA_FLUSH_DRREGISTER`|364|363|
|`__HAL_IRDA_GET_FLAG`|382|381|
|`__HAL_IRDA_GET_IT_SOURCE`|500–501|499–500|
|`__HAL_IRDA_RESET_HANDLE_STATE`|345–350 / 352–355|344–349 / 351–354|

## 固定来源

- [Smartcard旧版注册/注销L463–663](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_smartcard.c#L463-L663)、[新版L466–658](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_smartcard.c#L466-L658)。
- [IrDA旧版注册/注销L457–672](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_irda.c#L457-L672)、[新版L460–666](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_irda.c#L460-L666)。
- [Smartcard GetState/GetError](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_smartcard.c#L1775-L1797)、[IrDA GetState/GetError](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_irda.c#L2025-L2046)。


- [Smartcard v1.1.4头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_smartcard.h)、[v1.1.10头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_smartcard.h)。
- [IrDA v1.1.4头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_irda.h)、[v1.1.10头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_irda.h)。
- [Smartcard SetConfig固定新版](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_smartcard.c#L2256-L2333)。
- [固定CMSIS器件位定义](https://github.com/STMicroelectronics/cmsis-device-f1/blob/c8e9a4a4f16b6d2cb2a2083cbe5161025280fb22/Include/stm32f103xb.h#L9495-L9574)。
- [RM0008 Rev21，GTPR p826](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=826)、[Smartcard CK p810](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=810)。

配套：[初始化顺序与CPU访问边界](Smartcard与IrDA数据宽度及初始化.md)、[DMA生命周期](Smartcard与IrDA_DMA边界.md)、[HAL函数接口索引](Smartcard与IrDA_HAL接口索引.md)、[硬件寄存器](寄存器与访问副作用.md)。

范围：已覆盖这两份固定专用头文件的Init成员、所列配置符号与30个__HAL控制宏；另已核对两模块各14个常规句柄字段、条件回调成员、状态/错误码及回调ID；全部私有校验宏与基础宏依赖未在本页逐项列完。没有新增固件执行或实机验证。

句柄版本比较：两版成员名称、顺序及类型逐项核对，pTxBuffPtr从uint8_t *变为const uint8_t *，其余已列成员类型一致。启用回调成员时Smartcard共22字段、IrDA共24字段；数字是成员计数，不是结构字节数。
