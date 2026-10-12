# Arm_DDI0403Eb 来源记录

按所列文档版本、原厂章节及页码定位技术依据。来源范围不等于整部手册或整章内容已完整收录；在线文件可能更新。

## SRC-ARMV7M-EB-MASK

文档：ARM DDI0403E.b；版本：E.b。原厂位置：§B1.5.4 Exception priorities and preemption。

印刷页：B1-583, B1-584, B1-585；PDF文件页：583, 584, 585。

图表与脚注：以所列字段/章节为准。

支持范围：PRIGROUP裁去子优先级；BASEPRI/PRIMASK/FAULTMASK只影响组优先级；FAULTMASK只允许执行优先级≥0置1。

边界与原文差异：依据官方PDF在线内容，未记录对应PDF文件SHA；不混用v8-M。

[原厂来源](https://documentation-service.arm.com/static/5f8fef3af86e16515cdbf816#page=583)

## SRC-ARMV7M-EB-VECTOR

文档：ARM DDI0403E.b；版本：E.b。原厂位置：§B1.5.3 The vector table。

印刷页：B1-581, B1-582；PDF文件页：581, 582。

图表与脚注：以所列字段/章节为准。

支持范围：向量表自然2次幂对齐且不小于异常项数×4，架构最低128字节；除初始SP外入口bit0须1。

边界与原文差异：架构下限不能覆盖STM32文档器件约定；本库继续采用512字节对齐，未对C8采用256字节对齐进行实板验证。

[原厂来源](https://documentation-service.arm.com/static/5f8fef3af86e16515cdbf816#page=581)
