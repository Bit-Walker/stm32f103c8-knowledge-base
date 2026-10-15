# 来源目录

记录固定版本、真实原章节及图表脚注位置、印刷页与PDF文件页，以及每条事实的支持边界。官方链接可能更新；不以本地中文重组节号冒充原厂编号，不以来源链接推定图片或译文复制许可。

- [DS5319 Rev20，2025-07](DS5319.md)
- [RM0008 Rev21，2021-02](RM0008.md)
- [AN2586 Rev8，2022-12](AN2586.md)
- [AN2867 Rev24，2026-02](AN2867.md)
- [ES096 Rev15，2022-03](ES096.md)
- [PM0056 Rev7，2024-12](PM0056.md)
- [固定器件定义与HAL实现](驱动实现.md)
- [PM0075 Rev2：Flash访问条件](PM0075.md)
- [UM1850 Rev3：HAL/LL接口条件与通用模型](UM1850.md)
- [UM1847 Rev3：CubeF1 工程与 HAL 接入](UM1847.md)
- [AN4724 Rev2：官方示例分类与适用边界](AN4724.md)

DS文件页数与部分印刷总页数不一致，RM的PWR章节页脚总数也有异常，详见相应记录。2026-10-12已核RM0008固定PDF与ST官方同版整份文件逐字节一致；DS5319已核官方版本、文件页数和特定页编号，整份原始字节尚未比对。页码差异的成因仍未确定。来源身份核验不替代技术审查，来源记录也不替代完整原表或全套寄存器说明。

硬件与时钟主题采用各自的事实定位锚点；同一文档的不同支持范围分别保留。固定HAL实现结论只适用于记录中的版本及条件。

## Arm架构与调试接口

- [Arm_DDI0403Eb](Arm_DDI0403Eb.md)
- [Arm_DDI0337E](Arm_DDI0337E.md)
- [IHI0031A](IHI0031A.md)
- [IHI0031D](IHI0031D.md)

GPIO、内核与调试来源按原厂文档归档；各SRC定位标识、适用范围、原文差异及来源文件标识分别保留。

## DMA与缓冲区协作来源

DMA来源按真实文档与固定源码归并，18条支持范围分别使用唯一定位ID。AN2548为Rev9（2024-02）；DMA/ADC源码固定至bd368aa335c529641d2e567574885e02deacc64a。RM0008整份字节身份核验继续沿用本目录上文及其记录中的说明。

- [SRC-DS5319-R20-DMA-C8-RESOURCES](DS5319.md#src-ds5319-r20-dma-c8-resources)：C8中容量DMA1七通道、ADC1/2、TIM1及TIM2～4资源边界
- [SRC-RM0008-R21-DMA-REQUEST-MAPPING](RM0008.md#src-rm0008-r21-dma-request-mapping)：DMA1七通道全部36个请求源
- [SRC-ES096-R15-DMA-REGISTER-ACCESS](ES096.md#src-es096-r15-dma-register-access)：DMA寄存器始终对齐32位word访问
- [SRC-RM0008-R21-DMA-WIDTH-ALIGNMENT](RM0008.md#src-rm0008-r21-dma-width-alignment)：NDT按项、非零1～65535
- [SRC-RM0008-R21-DMA-REGISTERS-LIFECYCLE](RM0008.md#src-rm0008-r21-dma-registers-lifecycle)：请求应答、配置、普通/循环、MEM2MEM与CIRC互斥
- [SRC-UM1850-R3-DMA-HAL-CONTRACT](UM1850.md#src-um1850-r3-dma-hal-contract)：DMA结构体、API原型/参数、常量、DMA1标志和TIM句柄索引
- [SRC-RM0008-R21-DMA-USART-COMPLETION](RM0008.md#src-rm0008-r21-dma-usart-completion)：DMA把数据写入DR的完成与USART移位发送结束TC是不同条件
- [SRC-RM0008-R21-DMA-CIRCULAR-BUFFER](RM0008.md#src-rm0008-r21-dma-circular-buffer)：循环重装、HT/TC标志及剩余计数的硬件基础
- [SRC-RM0008-R21-DMA-ADC-CONTRACT](RM0008.md#src-rm0008-r21-dma-adc-contract)：规则序列逐项DR→DMA
- [SRC-AN2548-R9-DMA-BUS-COMPETITION](AN2548.md#src-an2548-r9-dma-bus-competition)：主设备轮转、通道固定优先级、低优先级饿死、CPU同APB竞争
- [SRC-AN2548-R9-DMA-SERVICE-TIMING](AN2548.md#src-an2548-r9-dma-service-timing)：tS=tA+tRD+tWR
- [SRC-AN2548-R9-DMA-RESOURCE-BUDGET](AN2548.md#src-an2548-r9-dma-resource-budget)：预计负载外50%余量，约三分之一能力保留
- [SRC-RM0008-R21-DMA-TIM-BURST](RM0008.md#src-rm0008-r21-dma-tim-burst)：TIM1 DCR.DBA/DBL编码与DMAR地址重定向
- [SRC-ES096-R15-DMA-GLOBAL-FLAG-ERRATUM](ES096.md#src-es096-r15-dma-global-flag-erratum)：活动通道清GIF与TE同周期会漏TEIF、禁用失败
- [SRC-UM1850-R3-DMA-HAL-LL-OWNERSHIP](UM1850.md#src-um1850-r3-dma-hal-ll-ownership)：同实例LL可使HAL句柄镜像失真
- [SRC-HAL-BD368AA-DMA-DMA-LIFECYCLE](驱动实现.md#src-hal-bd368aa-dma-dma-lifecycle)：READY/BUSY门控
- [SRC-HAL-BD368AA-DMA-ADC-START](驱动实现.md#src-hal-bd368aa-dma-adc-start)：设置内部DMA回调，先CR2.DMA再Start_IT且丢弃返回，再开EXTTRIG/SWSTART，不能只信外层HAL_OK
- [SRC-RM0008-R21-DMA-BUS-TOPOLOGY](RM0008.md#src-rm0008-r21-dma-bus-topology)：ICode直达FLITF

## ADC采集与精度来源

- [RM0008硬件与寄存器](RM0008.md#src-rm0008-r21-adc-hardware)
- [DS5319电气表与图注](DS5319.md#src-ds5319-r20-adc-electrical)
- [ES096注入耦合与触发条件](ES096.md#src-es096-r15-adc-coupling-trgo)
- [UM1850接口范围](UM1850.md#src-um1850-r3-adc-hal-ll)
- [固定HAL/LL与器件定义](驱动实现.md#src-adc-fixed-implementations)
- [AN2834前端与精度](AN2834.md)
- [AN3116模式与应用](AN3116.md)

## 定时器、PWM与同步来源

- [RM0008时基、通道与寄存器](RM0008.md#src-rm0008-r21-tim-hardware)
- [DS5319资源与时序表](DS5319.md#src-ds5319-r20-tim-c8)
- [ES096定时器边界](ES096.md#src-es096-r15-tim-boundaries)
- [UM1850接口范围](UM1850.md#src-um1850-r3-tim-interfaces)
- [HAL/LL固定源码](驱动实现.md#src-tim-fixed-implementations)
- [AN4013模式与同步](AN4013.md)
- [AN4776测量与波形应用](AN4776.md)


## USART硬件与驱动来源

- [固定HAL/LL实现与完整文件身份](驱动实现.md#src-usart-fixed-safety-boundaries)
- [ES096 USART六条限制](ES096.md#src-es096-r15-usart-boundaries)
- [RM0008硬件、24幅图与8张表](RM0008.md#src-rm0008-r21-usart-hardware)
- [主题图形关系与范围](../参数/USART/图形关系与来源.md)

## I²C 时序与驱动

- [AN2824 Rev4：优化收发示例与 HAL 对照](AN2824.md)

## USB 设备库与端点配置

- [UM1734 Rev4 与固定 CubeF1 实现](UM1734.md)

## ROM 串口引导

- [AN2606 与 AN3155：连接、握手和能力查询](ROM串口引导资料.md)
