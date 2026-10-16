# USB：PMA 配置、端点开启与软件连接

本文沿官方 CDC 示例核对单缓冲端点的初始化路径。CDC（Communication Device Class，通信设备类）常用于 USB 虚拟串口；PCD（Peripheral Controller Driver）负责 USB 外设驱动，PMA（Packet Memory Area）保存端点收发数据。

## 1 初始化时先关联句柄，再配置 PMA

官方示例的 `USBD_LL_Init()` 先建立两个方向的关联：

- `hpcd.pData` 指向 USB Device 协议栈句柄。
- `pdev->pData` 指向 PCD 句柄。

随后调用 `HAL_PCD_Init()`，再逐个调用 `HAL_PCDEx_PMAConfig()` 设置端点缓冲区位置。PCD 回调通过 `hpcd->pData` 将事件交回协议栈；例如 DataOut 回调传递端点号和接收缓冲区指针。

来源：[官方 usbd_conf.c](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM3210E_EVAL/Applications/USB_Device/CDC_Standalone/Src/usbd_conf.c)，查看 `USBD_LL_Init` 与 `HAL_PCD_DataOutStageCallback`。

## 2 端点地址和 PMA 地址分别表示什么

端点地址中的方向位区分 IN 和 OUT：IN 为设备发往主机，OUT 为主机发往设备。PMA 地址指定该方向的数据缓冲区位置。

官方示例采用以下单缓冲配置：

| 配置对象 | PMA 起始地址 |
|---|---|
| EP0 OUT（端点地址 0x00） | 0x40 |
| EP0 IN（端点地址 0x80） | 0x80 |
| CDC 数据 IN（CDC_IN_EP） | 0xC0 |
| CDC 数据 OUT（CDC_OUT_EP） | 0x110 |
| CDC 通知 IN（CDC_CMD_EP） | 0x100 |

这些地址来自该示例的布局。迁移时应同时核对端点最大包长、缓冲区占用、缓冲描述表与 PMA 总容量，不能只复制起始地址。

`HAL_PCDEx_PMAConfig()` 的单缓冲分支仅设置端点结构体的 `doublebuffer` 和 `pmaadress`。函数内没有完整布局的越界、重叠或容量检查；返回 `HAL_OK` 不代表 PMA 分配已经验证。

来源：[PMA 配置实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_pcd_ex.c)、[示例分配](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM3210E_EVAL/Applications/USB_Device/CDC_Standalone/Src/usbd_conf.c)。

## 3 配置地址之后，还要开启端点

`HAL_PCD_EP_Open()` 设置端点号、方向、最大包长和类型，随后调用 `USB_ActivateEndpoint()`。

在单缓冲路径中，底层激活函数将先前保存的 PMA 地址写入端点的发送或接收缓冲地址配置；接收方向还根据最大包长设置接收计数，并配置端点状态。因此，PMA 地址应在对应端点激活前准备好。

来源：[端点开启](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_pcd.c#L1709-L1757)、[单缓冲激活](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_usb.c#L2090-L2167)。

## 4 软件连接需要板级实现

`HAL_PCD_DevConnect()` 和 `HAL_PCD_DevDisconnect()` 会调用 `HAL_PCDEx_SetConnectionState()`。该钩子的默认 weak 实现为空；此处 USB 外设分支的底层 `USB_DevConnect()` 和 `USB_DevDisconnect()` 也直接返回 `HAL_OK`。

官方评估板示例通过重写连接钩子，控制 PB14 输出电平。PB14 属于该板的连接控制电路，迁移时应按实际原理图确定控制引脚与有效电平。只有硬件具有可控连接电路且钩子正确实现时，才能据此实现相应的软件连接控制。

排查“调用成功却没有重新枚举”时，应检查连接钩子和板上 D+ 上拉控制路径，再观察总线行为。

来源：[HAL 连接入口](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_pcd.c#L1654-L1690)、[默认连接钩子](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_hal_pcd_ex.c)、[USB 底层连接函数](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Src/stm32f1xx_ll_usb.c#L2631-L2666)、[评估板钩子实现](https://github.com/STMicroelectronics/STM32CubeF1/blob/c7656f1fee178058be2f8ebfc8df9eaf91dc565e/Projects/STM3210E_EVAL/Applications/USB_Device/CDC_Standalone/Src/usbd_conf.c)。

## 5 手册接口名要与工程版本核对

UM1734 Rev4 第 58 页将 PMA 接口写为 `HAL_PCD_PMA_Config()`。本次固定版本的头文件、实现和官方示例均使用 `HAL_PCDEx_PMAConfig()`。工程中应采用实际头文件声明的名字。

来源：[UM1734 第 58 页](https://www.st.com/resource/en/user_manual/um1734-stm32cube-usb-device-library-stmicroelectronics.pdf#page=58)、[PCD 扩展接口声明](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/bd368aa335c529641d2e567574885e02deacc64a/Inc/stm32f1xx_hal_pcd_ex.h)。

## 核查范围

本页是初始化、单缓冲 PMA 配置及连接钩子的静态核查，未完成板端枚举验证。官方示例测试板为 STM3210E-EVAL，不能据此声称已经在目标板验证。完整硬件布线、PMA 空间布局计算及 CDC 数据传输生命周期仍需分别核对。

固定源码与手册版本见 [UM1734 来源记录](../../来源/UM1734.md)。

## 容量与传输阶段的补充

[USB 容量与端点副作用](容量与端点副作用.md)补充 PMA 地址/容量编码、应用缓冲访问、端点特殊写入语义和接收计数勘误。该页的软件分析固定于 CubeF1 v1.8.6 配套 HAL v1.1.10；本初始化页仍保留上文列明的独立固定实现和示例板条件，不由新增链接改写版本结论。
