# STM32CubeF1 官方示例源码导读：把初始化、DMA和中断串起来

## 版本与阅读范围

本文针对 STM32CubeF1 **v1.8.6**（commit `42472d601caa457b02d849c7de5f9792629ee324`），其HAL/LL为 **v1.1.10**（commit `77fbb30b7a1d02533980400083e48c559aae5a4f`），CMSIS Device为v4.3.5。本轮实读12个示例的readme、main、main.h、IRQ文件及存在的MSP文件，并针对争议追到HAL驱动实现；未编译、烧录或声称做过硬件验证。

这些示例的测试板是NUCLEO-F103RB，不是STM32F103C8最小板。借用的是机制和调用链：移植前统一核对芯片容量/链接脚本、引脚、DMA通道冲突、板载LED/按键、HSE来源及实际时钟。本组HAL例子多用HSI PLL得到64MHz，LL及PWMInput例子多用HSE bypass得到72MHz；不能把它们混作一个时钟配置。正式硬件结论仍以对应器件数据手册、RM0008和勘误为准。

## 怎样读一份官方例程

先用readme确认目标与连线，再沿main→main.h资源宏→MSP/LL初始化→IRQ→回调→缓冲区生命周期追踪。遇到说明与源码不一致时记录差异，不替官方说明“补合理化”。下文链接全部固定commit，避免master滚动改变依据。

## 按任务快速查找

- [软件触发ADC并用DMA取数](#1-adc一次软件触发不等于连续转换)：`ADC_SingleConversion_TriggerSW_DMA`
- [定时器触发ADC采样](#2-adctim3-trgo驱动定时采样)：`ADC_SingleConversion_TriggerTimer_DMA`
- [输出PWM并更新占空比](#3-timpwm输出与预装载的完整开启链)：`TIM_PWMOutput`
- [两次捕获测频率](#4-tim两次输入捕获求频率)：`TIM_InputCapture`
- [测PWM周期与高电平宽度](#5-timpwm-input把周期和高电平宽度分开捕获)：`TIM_PWMInput`
- [核对TIM DMA请求源](#6-timdma先核对dma请求源再解释波形)：`TIM_DMA`
- [串口固定长度中断收发](#7-uart-it回调完成标志与固定长度收发)：`UART_TwoBoards_ComIT`
- [串口DMA收发与中断收尾](#8-uart-dma同时收发仍需要usart中断收尾)：`UART_HyperTerminal_DMA`
- [I2C主从DMA与事件中断](#9-i2c-dmadma搬数据事件错误irq仍参与协议)：`I2C_TwoBoards_ComDMA`
- [SPI全双工DMA收发](#10-spi-dma全双工是同时消费tx和rx缓冲区)：`SPI_FullDuplex_ComDMA`
- [GPIO翻转与HAL时基](#11-gpio时钟输出模式和hal时基)：`GPIO_IOToggle`
- [EXTI端口映射与共享中断](#12-exti端口映射线屏蔽边沿和nvic缺一不可)：`EXTI_ToggleLedOnIT`

## 1. ADC：一次软件触发，不等于连续转换

ADC1通道4（PA4）设为单次转换、软件触发；按键回调每次调用 LL_ADC_REG_StartConversionSWStart。DMA1通道1采用循环模式、外设地址不递增、内存递增、两侧半字宽，默认缓冲区是4个 uint16_t。

初始化顺序是DMA→ADC→使能ADC→等待稳定→校准→等待校准结束。DMA半满回调处理数组前半，满回调处理后半，IRQ先清对应HT/TC/TE标志再调用回调。循环的是DMA地址，并不自动把单次ADC变成连续采样。毫伏换算用固定VDDA_APPLI=3300，是示例假设；Inc/main.h把USE_TIMEOUT设为0，不能把代码里条件编译的超时分支当成默认启用。

源码：[readme.txt](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/ADC/ADC_SingleConversion_TriggerSW_DMA/readme.txt) · [Src/main.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/ADC/ADC_SingleConversion_TriggerSW_DMA/Src/main.c) · [Inc/main.h](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/ADC/ADC_SingleConversion_TriggerSW_DMA/Inc/main.h) · [Src/stm32f1xx_it.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/ADC/ADC_SingleConversion_TriggerSW_DMA/Src/stm32f1xx_it.c)

## 2. ADC：TIM3 TRGO驱动定时采样

TIM3配置Update作为TRGO，ADC触发源选TIM3_TRGO，ADC仍是单次模式；第一次按键仅使能外部触发，随后由定时器持续提供转换节拍。DMA循环缓冲区为64个半字，HT/TC分别处理32个数据。

定时器初始化显式判断APB1分频：不分频取PCLK1，否则取2×PCLK1，再算PSC和ARR。默认 `TIMER_FREQUENCY=1000` 表示目标触发频率为1000 Hz（源码注释明确单位为Hz），整数分频存在量化，不能把目标宏当成精确实测值。它示范“定时器触发ADC”的同步链，不是两个定时器的ITR主从同步。

源码：[readme.txt](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/ADC/ADC_SingleConversion_TriggerTimer_DMA/readme.txt) · [Src/main.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/ADC/ADC_SingleConversion_TriggerTimer_DMA/Src/main.c) · [Inc/main.h](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/ADC/ADC_SingleConversion_TriggerTimer_DMA/Inc/main.h) · [Src/stm32f1xx_it.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/ADC/ADC_SingleConversion_TriggerTimer_DMA/Src/stm32f1xx_it.c)

## 3. TIM：PWM输出与预装载的完整开启链

TIM2_CH1/PA0使用PWM1；依次设置PSC、启用ARR预装载、设置ARR和CCR1、启用CH1比较预装载，随后开启通道、计数器并生成一次UPDATE。ARR和CCR1分别是自动重装载寄存器与通道1比较寄存器的计数值；D是占空比百分数的数值，例如D=50表示50%。初值关系为 `CCR1 = (ARR + 1) / 2`；改变占空比时，源码先令 `T = ARR + 1`，再以整数运算 `P = (D * T) / 100` 求比较值并写入CCR1。

这里值得反向核对官方readme：它写CCR/ARR、APB1分频为1和toggle模式；同目录main实际写ARR+1、APB1÷2和PWM1。学习此版本时以代码和RM0008的计数规则为依据，不能照抄这三处说明。回调所谓“测得占空比”是读配置寄存器计算，并非外部测量。

源码：[readme.txt](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/TIM/TIM_PWMOutput/readme.txt) · [Src/main.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/TIM/TIM_PWMOutput/Src/main.c) · [Inc/main.h](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/TIM/TIM_PWMOutput/Inc/main.h) · [Src/stm32f1xx_it.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/TIM/TIM_PWMOutput/Src/stm32f1xx_it.c)

## 4. TIM：两次输入捕获求频率

TIM3_CH1/PA6直接输入、上升沿、输入捕获分频DIV1；TIM2_CH1/PA0提供可选测试PWM，需外部连线。TIM3 CC1中断取连续两次CCR1，第二值较小时用0xFFFF边界补一次回绕，随后按计数时钟、PSC和捕获分频计算频率。

这是两次捕获差值法；代码没有统计任意多次溢出，也没有完整的超时/失信号/过捕获处理。相等捕获值走错误分支。readme约300kHz上限是该示例处理中断时间的估计，不能推广为所有工程的硬件极限。

源码：[readme.txt](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/TIM/TIM_InputCapture/readme.txt) · [Src/main.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/TIM/TIM_InputCapture/Src/main.c) · [Inc/main.h](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/TIM/TIM_InputCapture/Inc/main.h) · [Src/stm32f1xx_it.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/TIM/TIM_InputCapture/Src/stm32f1xx_it.c)

## 5. TIM：PWM Input把周期和高电平宽度分开捕获

TIM3_CH2/PA7直接输入上升沿，CH1间接输入下降沿；从模式RESET，触发源TI2FP2。CH2捕获周期，CH1捕获高电平时间，CC2处理函数用CCR1/CCR2求占空比、计数时钟/CCR2求频率，并对CCR2=0做保护。

这是HAL初始化、LL处理中断和读捕获值的混合范例。不要给同一个标志再叠加另一套HAL IRQ分发。TIM2仅输出供接线测试的信号，代码把其MasterSlaveMode设为DISABLE；不要将这份例子描述为TIM2通过内部ITR同步TIM3。

源码：[readme.txt](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_MIX/TIM/TIM_PWMInput/readme.txt) · [Src/main.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_MIX/TIM/TIM_PWMInput/Src/main.c) · [Inc/main.h](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_MIX/TIM/TIM_PWMInput/Inc/main.h) · [Src/stm32f1xx_hal_msp.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_MIX/TIM/TIM_PWMInput/Src/stm32f1xx_hal_msp.c) · [Src/stm32f1xx_it.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_MIX/TIM/TIM_PWMInput/Src/stm32f1xx_it.c)

## 6. TIM+DMA：先核对DMA请求源，再解释波形

main配置TIM1_CH3、3个32位比较值、RepetitionCounter=3，并调用HAL_TIM_PWM_Start_DMA；MSP把DMA1通道6设成循环模式，链接到hdma[TIM_DMA_ID_CC3]。

说明与源码差异：readme称“Update DMA请求，每4次更新换值”，但固定HAL v1.1.10的HAL_TIM_PWM_Start_DMA(CH3)实际写CCR3并使能TIM_DMA_CC3。这里不能据readme断言DMA由Update触发。RCR影响更新与比较预装载何时生效，应与请求节拍分开分析。示例只开启普通CH3，不能仅因readme写complementary便宣称CH3N已启用。

源码：[readme.txt](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/TIM/TIM_DMA/readme.txt) · [Src/main.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/TIM/TIM_DMA/Src/main.c) · [Inc/main.h](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/TIM/TIM_DMA/Inc/main.h) · [Src/stm32f1xx_hal_msp.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/TIM/TIM_DMA/Src/stm32f1xx_hal_msp.c) · [Src/stm32f1xx_it.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/TIM/TIM_DMA/Src/stm32f1xx_it.c)

## 7. UART IT：回调完成标志与固定长度收发

USART1，9600、8数据位、无校验、1停止位。TRANSMITTER_BOARD决定先发后收还是先收后发；main流程调用Transmit_IT/Receive_IT后等待UartReady，TxCplt和RxCplt回调置位，下一阶段前清零。

MSP开启USART1 IRQ；向量函数调用HAL_UART_IRQHandler。接收长度固定为发送数组长度减字符串结尾，不是自动识别一行、IDLE或变长报文。数组是全局对象，覆盖整个异步传输寿命。例子仍在main流程忙等，因此“IT API非阻塞”不能直接等同于“应用程序从不等待”。

源码：[readme.txt](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/UART/UART_TwoBoards_ComIT/readme.txt) · [Src/main.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/UART/UART_TwoBoards_ComIT/Src/main.c) · [Inc/main.h](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/UART/UART_TwoBoards_ComIT/Inc/main.h) · [Src/stm32f1xx_hal_msp.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/UART/UART_TwoBoards_ComIT/Src/stm32f1xx_hal_msp.c) · [Src/stm32f1xx_it.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/UART/UART_TwoBoards_ComIT/Src/stm32f1xx_it.c)

## 8. UART DMA：同时收发仍需要USART中断收尾

同一个USART1句柄先启动DMA发送提示，随即启动固定10字节DMA接收；两次启动之间没有等待TX完成，收发可重叠。等待GetState==READY后回发10字节。配置是8位字长加奇校验，即7数据位+1校验位，不是常见8N1。TX/RX分别绑定DMA1通道4/5，字节对齐、内存递增、NORMAL模式。

MSP同时开启两个DMA IRQ及USART IRQ；IRQ分别分发HAL_DMA_IRQHandler和HAL_UART_IRQHandler。对应HAL驱动在NORMAL TX DMA搬运完成时开启USART TC中断，因此只接DMA中断会遗漏串口发送收尾链。不要从此固定长度示例推导循环DMA、IDLE分帧或自动重装接收。

源码：[readme.txt](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/UART/UART_HyperTerminal_DMA/readme.txt) · [Src/main.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/UART/UART_HyperTerminal_DMA/Src/main.c) · [Inc/main.h](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/UART/UART_HyperTerminal_DMA/Inc/main.h) · [Src/stm32f1xx_hal_msp.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/UART/UART_HyperTerminal_DMA/Src/stm32f1xx_hal_msp.c) · [Src/stm32f1xx_it.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/UART/UART_HyperTerminal_DMA/Src/stm32f1xx_it.c)

## 9. I2C DMA：DMA搬数据，事件/错误IRQ仍参与协议

I2C1，PB6/PB7复用开漏，400kHz；这是10位地址0x30F的两板示例，不是可直接套用的7位传感器地址模板。MASTER_BOARD开关决定主从，默认注释为从机。先主发从收，再主收从发；双方用固定长度全局缓冲区。

DMA1通道6/7采用字节NORMAL模式，链接hdmatx/hdmarx；MSP及IRQ同时保留I2C_EV、I2C_ER和DMA TX/RX四条处理链。readme画有外部4.7k上拉；这只是示例连接，不是所有总线速率、电容和电压下的通用选值。main的READY等待循环没有自己的应用层截止时间，不能把readme的“10秒超时”理解为所有等待都必然退出。

源码：[readme.txt](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/I2C/I2C_TwoBoards_ComDMA/readme.txt) · [Src/main.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/I2C/I2C_TwoBoards_ComDMA/Src/main.c) · [Inc/main.h](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/I2C/I2C_TwoBoards_ComDMA/Inc/main.h) · [Src/stm32f1xx_hal_msp.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/I2C/I2C_TwoBoards_ComDMA/Src/stm32f1xx_hal_msp.c) · [Src/stm32f1xx_it.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/I2C/I2C_TwoBoards_ComDMA/Src/stm32f1xx_it.c)

## 10. SPI DMA：全双工是同时消费TX和RX缓冲区

SPI2 PB13/14/15，2线全双工、8位、MSB first、CPOL低/第一边沿、软件NSS；调用TransmitReceive_DMA同时提供两个等长缓冲区。主机/从机由MASTER_BOARD分支选择，从机须先准备接收，主机按键后启动。

TX/RX链接DMA1通道5/4，NORMAL模式，完成及错误回调更新wTransferState。SPI软件NSS示例没有替外部器件管理片选事务边界，不能作为多从机CS协议模板。此版MSP统一把SCK/MISO/MOSI设为AF_PP，没有按主从角色区分；迁移时必须按RM0008的SPI引脚配置重新核对，不能原样背成通用规则。

源码：[readme.txt](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/SPI/SPI_FullDuplex_ComDMA/readme.txt) · [Src/main.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/SPI/SPI_FullDuplex_ComDMA/Src/main.c) · [Inc/main.h](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/SPI/SPI_FullDuplex_ComDMA/Inc/main.h) · [Src/stm32f1xx_hal_msp.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/SPI/SPI_FullDuplex_ComDMA/Src/stm32f1xx_hal_msp.c) · [Src/stm32f1xx_it.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/SPI/SPI_FullDuplex_ComDMA/Src/stm32f1xx_it.c)

## 11. GPIO：时钟、输出模式和HAL时基

GPIO_IOToggle在开启GPIO时钟后初始化PA5为推挽输出，循环TogglePin并HAL_Delay(100)。SysTick_Handler调用HAL_IncTick，形成延时所需的时基。

这个例子适合检查“GPIO时钟→模式→写输出→时基”链是否闭合。100ms是每次翻转间隔，完整明灭周期约200ms；不应当把HAL_Delay当成无中断依赖的精确延时。

源码：[readme.txt](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/GPIO/GPIO_IOToggle/readme.txt) · [Src/main.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/GPIO/GPIO_IOToggle/Src/main.c) · [Inc/main.h](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/GPIO/GPIO_IOToggle/Inc/main.h) · [Src/stm32f1xx_it.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples/GPIO/GPIO_IOToggle/Src/stm32f1xx_it.c)

## 12. EXTI：端口映射、线屏蔽、边沿和NVIC缺一不可

EXTI_ToggleLedOnIT的按键是PC13；main.h里的映射宏明确开启AFIO时钟并用LL_GPIO_AF_SetEXTISource映射EXTI13到GPIOC，然后使能EXTI13、下降沿和EXTI15_10_IRQn。

共享向量里检查的是EXTI13标志，清标志后调用回调翻转PA5。共享IRQ号10–15不等于全部6条线都被这个示例启用。代码未实现按键消抖；一次机械按压不能保证只有一次边沿或一次翻转。

源码：[readme.txt](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/EXTI/EXTI_ToggleLedOnIT/readme.txt) · [Src/main.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/EXTI/EXTI_ToggleLedOnIT/Src/main.c) · [Inc/main.h](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/EXTI/EXTI_ToggleLedOnIT/Inc/main.h) · [Src/stm32f1xx_it.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/42472d601caa457b02d849c7de5f9792629ee324/Projects/STM32F103RB-Nucleo/Examples_LL/EXTI/EXTI_ToggleLedOnIT/Src/stm32f1xx_it.c)

## 跨例程迁移时容易漏的条件

- DMA通道不是每个外设独占的抽象资源：这组选例中USART1 TX/RX与SPI2 RX/TX都使用DMA1通道4/5，TIM1_CH3与I2C1 TX都使用通道6。它们是分别运行的工程，合并时不能直接同时启用冲突配置。
- 示例中的全局/静态DMA句柄与缓冲区寿命贯穿传输；迁移时不要把它们改成启动函数返回后就失效的局部对象。
- IT/DMA启动返回成功与物理传输完成不是同一事件；跟踪正确回调或状态，再复用缓冲区。
- 示例错误处理里的无限循环、ISR里依赖HAL_Delay的闪灯、缺少应用超时等用于演示，不能直接等同于产品级故障恢复。
- UART IT、I2C DMA、SPI DMA例子内的Buffercmp在差异分支返回递减后的BufferLength。具体前提是传入非零长度N、两缓冲区均有至少N个可读字节、比较期间内容稳定，且前N−1字节相同、仅第N字节不同；此时函数仍返回0，调用处会误判相等。学习数据校验时宜改用语义明确的比较结果；这是静态代码检查发现，未做硬件验证。

## 针对说明冲突补读的驱动实现

- [HAL_TIM_PWM_Start_DMA 的固定版本实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_tim.c#L1713)。
- [UART_DMATransmitCplt 的固定版本实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_uart.c#L2988)。
