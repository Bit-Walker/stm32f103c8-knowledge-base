# Arm_DDI0337E 来源记录

按所列文档版本、原厂章节及页码定位技术依据。来源范围不等于整部手册或整章内容已完整收录；在线文件可能更新。

## SRC-ARM-CM3-R1P1-FAULT-W1C

文档：Arm Cortex-M3 TRM DDI0337E；版本：E / r1p1。原厂位置：§8.2.2 NVIC register descriptions / Configurable Fault Status Registers。

印刷页：8-31；PDF文件页：175。

图表与脚注：以所列字段/章节为准。

支持范围：CFSR三个子寄存器故障标志正常读取、写1清；不属于读清。

边界与原文差异：使用对应r1p1旧核TRM；不以通用外设寄存器习惯补齐。

[原厂来源](https://documentation-service.arm.com/static/6036810d5319e554d4ba108e#page=175)

来源文件 SHA-256：`9d9bd79cbd540c27222854c658307d05095c13156acde75948cb4ca0e2e174b9`。

## SRC-DDI0337E-STACK-LAYOUT

文档：Arm Cortex-M3 TRM DDI0337E；版本：E / r1p1。原厂位置：§5.5.1 Stacking。

印刷页：5-11；PDF文件页：105。

图表与脚注：Figure5-1及STKALIGN附加字Note。

支持范围：异常帧从新SP起R0/R1/R2/R3/R12/LR/PC/xPSR，偏移0/4/8/12/16/20/24/28；可有额外对齐字。

边界与原文差异：图示栈上布局不是总线压栈事务时间先后；故障入栈仍可能不完整。

[原厂来源](https://documentation-service.arm.com/static/6036810d5319e554d4ba108e#page=105)

来源文件 SHA-256：`9d9bd79cbd540c27222854c658307d05095c13156acde75948cb4ca0e2e174b9`。

## SRC-DDI0337E-CALIB-SEMANTICS

文档：Arm Cortex-M3 TRM DDI0337E；版本：E / r1p1。原厂位置：§8.2.2 SysTick Calibration Value Register。

印刷页：8-11, 8-12；PDF文件页：155, 156。

图表与脚注：Figure8-5；Table8-6。

支持范围：CALIB地址E000E01C只读；NOREF位31、SKEW位30、TENMS位23:0；SKEW=1表示非精确10ms，TENMS=0表示校准未知。

边界与原文差异：通用核心STCALIB输入定义，不覆盖PM0056/RM0008的C8约1ms校准及固定复位值冲突。

[原厂来源](https://documentation-service.arm.com/static/6036810d5319e554d4ba108e#page=155)

来源文件 SHA-256：`9d9bd79cbd540c27222854c658307d05095c13156acde75948cb4ca0e2e174b9`。

## SRC-DDI0337E-DEBUG-STATE

文档：DDI0337E；版本：r1p1 / E。原厂位置：§10.1 Table10-1；§10.2.1；§10.2.4；§10.2.2。

印刷页：10-2, 10-3, 10-4, 10-5, 10-6, 10-7, 10-8, 10-9, 10-10；PDF文件页：208, 209, 210, 211, 212, 213, 214, 215, 216。

图表与脚注：Tables10-1(a,b),10-2,10-4(a,b)；Figures10-1,10-3；Table10-3续表。

支持范围：S_RESET_ST/S_RETIRE_ST读清；S_RESET_ST在仍受复位时可连续两读为1；DBGKEY=0xA05F；C_DEBUGEN只能AHB-AP写；字段级C_HALT和MON[19:16]复位规则。 DCRSR为word写且REGSEL[4:0]与REGWnR[16]分开。

边界与原文差异：核心r1p1匹配由RM§31.2和ES§2.1支持，不能当C8独立硅实测。p10-3 DHCSR总括、p10-9 MON_PEND中的整寄存器总括与字段脚注存在冲突，原文均须保留。 p10-6具体说明DHCSR不由系统复位复位、仅POR，但C_HALT始终在系统复位清除；与p10-3总括并列保留，不消解源文冲突。

[原厂来源](https://documentation-service.arm.com/static/6036810d5319e554d4ba108e#page=208)

来源文件 SHA-256：`9d9bd79cbd540c27222854c658307d05095c13156acde75948cb4ca0e2e174b9`。

## SRC-DDI0337E-ITM-FIFO

文档：DDI0337E；版本：r1p1 / E。原厂位置：§11.6.1 ITM Stimulus Ports 0–31及TPR；§11.6.1。

印刷页：11-29, 11-30, 11-31, 11-32, 11-33, 11-34, 11-35, 11-36；PDF文件页：249, 250, 251, 252, 253, 254, 255, 256。

图表与脚注：Tables11-19–11-21；轮询示例；Tables11-19–22/26。

支持范围：stimulus端口读bit0=0满、1未满；并发轮询不是原子读改写；端口使能与权限分开。 LAR特权写解锁仅控制区偏移0xE00–0xFFC，其他值重锁；刺激端口读bit0=FIFO未满，轮询再写非原子；TSPrescale编码1/4/16/64。

边界与原文差异：保留p11-30与p11-32非特权权限极性冲突；不把原无限Retry示例照抄成生产应用保证。

[原厂来源](https://documentation-service.arm.com/static/6036810d5319e554d4ba108e#page=249)

来源文件 SHA-256：`9d9bd79cbd540c27222854c658307d05095c13156acde75948cb4ca0e2e174b9`。

## SRC-DDI0337E-TRACE-BOUNDARY

文档：DDI0337E；版本：r1p1 / E。原厂位置：§11.5.1；§13.2.2；§13.2.2。

印刷页：11-27, 13-8, 13-9, 13-10, 13-11, 13-12, 13-13, 13-14；PDF文件页：247, 274, 275, 276, 277, 278, 279, 280。

图表与脚注：DWT_FUNCTION；Table13-8及随后单线formatter文字；Tables13-3、13-7–8。

支持范围：DWT到ETM触发以ETM fitted为条件；单线formatter旁路时仅通过ITM/DWT并丢弃ETM。 TPIU寄存器、格式器与同步的通用定义；RM受限字段优先，不增加C8实现保证。

边界与原文差异：是通用实现条件，不反向保证C8有ETM或ETM到SWO；适用范围仅限所列实现条件。

[原厂来源](https://documentation-service.arm.com/static/6036810d5319e554d4ba108e#page=247)

来源文件 SHA-256：`9d9bd79cbd540c27222854c658307d05095c13156acde75948cb4ca0e2e174b9`。

## SRC-DDI0337E-AHB-AP

文档：DDI0337E；版本：r1p1 / E。原厂位置：§11.7.2。

印刷页：11-38, 11-39, 11-40, 11-41, 11-42, 11-43；PDF文件页：258, 259, 260, 261, 262, 263。

图表与脚注：Tables11-28–34。

支持范围：AHB-AP各偏移与寄存器；BD0–3使用TAR对齐16字节窗口，字访问且无自动递增；F8返回包含低位属性。

边界与原文差异：DRW/BD摘要reset横杠与细分表0口径有差异，不推统一复位0；通用核心定义不增加C8未证明资源。

[原厂来源](https://documentation-service.arm.com/static/6036810d5319e554d4ba108e#page=258)

来源文件 SHA-256：`9d9bd79cbd540c27222854c658307d05095c13156acde75948cb4ca0e2e174b9`。
