# Smartcard 与 IrDA：固定版本 HAL 接口索引

范围为 ST 官方 STM32F1 HAL v1.1.4 与 v1.1.10 的两份专用模块头文件。每版 Smartcard 28条、IrDA 32条声明，共60个不同名称、120条版本声明；其中118条在对应模块C文件找到参数及返回类型一致的定义，另2条为同一个ReInit接口的两版声明。数量包括弱回调及条件注册接口，不含宏、类型、内部static函数，也不表示全部运行行为已经验证。

H表示对应版本头文件行号，C表示对应模块实现起始行；“未见”限于本页指定完整模块C文件，不表示已排除用户工程提供同名实现。原型保留各版本的const差异。

## 声明与实现不一致处

两份头文件均声明HAL_SMARTCARD_ReInit，固定v1.1.4为H617、v1.1.10为H616；对应两份stm32f1xx_hal_smartcard.c未找到该函数定义。不能仅凭头文件声明把它列为已核对的可用重初始化实现；工程链接是否满足仍取决于工程实际源文件/库及用户定义。此处没有进行编译或链接测试。声明位置：[v1.1.4 H617](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_smartcard.h#L617)、[v1.1.10 H616](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_smartcard.h#L616)。

## 回调与编译条件

- RegisterCallback / UnRegisterCallback仅在对应USE_HAL_SMARTCARD_REGISTER_CALLBACKS或USE_HAL_IRDA_REGISTER_CALLBACKS等于1时声明和实现；句柄内注册回调成员也受对应条件控制。
- 标注“弱默认”的MSP和事件回调带__weak默认定义，允许工程覆盖；它们不等同于主动发起传输的函数。
- 其余接口仍受HAL模块启用、头文件及器件适用条件约束。本索引不展开所有工程配置组合。
- 函数名含_IT不保证用户回调一定在外层函数返回后执行；DMA Abort的同步回调与重入限制见专用DMA页。

## Smartcard 接口

v1.1.4固定来源：[头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_smartcard.h)、[实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_smartcard.c)。
v1.1.10固定来源：[头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_smartcard.h)、[实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_smartcard.c)。

### HAL_SMARTCARD_Init

公开接口。定位：v1.1.4 H616 / C296；v1.1.10 H615 / C296。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_Init(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_ReInit

头文件声明；对应模块未见实现。定位：v1.1.4 H617 / C未见；v1.1.10 H616 / C未见。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_ReInit(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_DeInit

公开接口。定位：v1.1.4 H618 / C375；v1.1.10 H617 / C375。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_DeInit(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_MspInit

弱默认回调，可由工程覆盖。定位：v1.1.4 H619 / C419；v1.1.10 H618 / C419。

两版原型相同：

```c
void HAL_SMARTCARD_MspInit(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_MspDeInit

弱默认回调，可由工程覆盖。定位：v1.1.4 H620 / C435；v1.1.10 H619 / C435。

两版原型相同：

```c
void HAL_SMARTCARD_MspDeInit(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_RegisterCallback

条件注册API；仅对应USE_HAL_SMARTCARD_REGISTER_CALLBACKS==1。定位：v1.1.4 H623 / C463；v1.1.10 H622 / C466。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_RegisterCallback(SMARTCARD_HandleTypeDef *hsc, HAL_SMARTCARD_CallbackIDTypeDef CallbackID, pSMARTCARD_CallbackTypeDef pCallback);
```

### HAL_SMARTCARD_UnRegisterCallback

条件注册API；仅对应USE_HAL_SMARTCARD_REGISTER_CALLBACKS==1。定位：v1.1.4 H624 / C576；v1.1.10 H623 / C577。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_UnRegisterCallback(SMARTCARD_HandleTypeDef *hsc, HAL_SMARTCARD_CallbackIDTypeDef CallbackID);
```

### HAL_SMARTCARD_Transmit

公开接口。定位：v1.1.4 H634 / C756；v1.1.10 H633 / C751。

v1.1.4：

```c
HAL_StatusTypeDef HAL_SMARTCARD_Transmit(SMARTCARD_HandleTypeDef *hsc, uint8_t *pData, uint16_t Size, uint32_t Timeout);
```

v1.1.10：

```c
HAL_StatusTypeDef HAL_SMARTCARD_Transmit(SMARTCARD_HandleTypeDef *hsc, const uint8_t *pData, uint16_t Size, uint32_t Timeout);
```

### HAL_SMARTCARD_Receive

公开接口。定位：v1.1.4 H635 / C819；v1.1.10 H634 / C813。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_Receive(SMARTCARD_HandleTypeDef *hsc, uint8_t *pData, uint16_t Size, uint32_t Timeout);
```

### HAL_SMARTCARD_Transmit_IT

公开接口。定位：v1.1.4 H636 / C878；v1.1.10 H635 / C871。

v1.1.4：

```c
HAL_StatusTypeDef HAL_SMARTCARD_Transmit_IT(SMARTCARD_HandleTypeDef *hsc, uint8_t *pData, uint16_t Size);
```

v1.1.10：

```c
HAL_StatusTypeDef HAL_SMARTCARD_Transmit_IT(SMARTCARD_HandleTypeDef *hsc, const uint8_t *pData, uint16_t Size);
```

### HAL_SMARTCARD_Receive_IT

公开接口。定位：v1.1.4 H637 / C926；v1.1.10 H636 / C919。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_Receive_IT(SMARTCARD_HandleTypeDef *hsc, uint8_t *pData, uint16_t Size);
```

### HAL_SMARTCARD_Transmit_DMA

公开接口。定位：v1.1.4 H638 / C971；v1.1.10 H637 / C964。

v1.1.4：

```c
HAL_StatusTypeDef HAL_SMARTCARD_Transmit_DMA(SMARTCARD_HandleTypeDef *hsc, uint8_t *pData, uint16_t Size);
```

v1.1.10：

```c
HAL_StatusTypeDef HAL_SMARTCARD_Transmit_DMA(SMARTCARD_HandleTypeDef *hsc, const uint8_t *pData, uint16_t Size);
```

### HAL_SMARTCARD_Receive_DMA

公开接口。定位：v1.1.4 H639 / C1033；v1.1.10 H638 / C1026。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_Receive_DMA(SMARTCARD_HandleTypeDef *hsc, uint8_t *pData, uint16_t Size);
```

### HAL_SMARTCARD_Abort

公开接口。定位：v1.1.4 H641 / C1103；v1.1.10 H640 / C1096。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_Abort(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_AbortTransmit

公开接口。定位：v1.1.4 H642 / C1167；v1.1.10 H641 / C1160。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_AbortTransmit(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_AbortReceive

公开接口。定位：v1.1.4 H643 / C1209；v1.1.10 H642 / C1202。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_AbortReceive(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_Abort_IT

公开接口。定位：v1.1.4 H644 / C1254；v1.1.10 H643 / C1247。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_Abort_IT(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_AbortTransmit_IT

公开接口。定位：v1.1.4 H645 / C1381；v1.1.10 H644 / C1374。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_AbortTransmit_IT(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_AbortReceive_IT

公开接口。定位：v1.1.4 H646 / C1458；v1.1.10 H645 / C1451。

两版原型相同：

```c
HAL_StatusTypeDef HAL_SMARTCARD_AbortReceive_IT(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_IRQHandler

公开接口。定位：v1.1.4 H648 / C1528；v1.1.10 H647 / C1521。

两版原型相同：

```c
void HAL_SMARTCARD_IRQHandler(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_TxCpltCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H649 / C1670；v1.1.10 H648 / C1663。

两版原型相同：

```c
void HAL_SMARTCARD_TxCpltCallback(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_RxCpltCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H650 / C1686；v1.1.10 H649 / C1679。

两版原型相同：

```c
void HAL_SMARTCARD_RxCpltCallback(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_ErrorCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H651 / C1702；v1.1.10 H650 / C1695。

两版原型相同：

```c
void HAL_SMARTCARD_ErrorCallback(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_AbortCpltCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H652 / C1717；v1.1.10 H651 / C1710。

两版原型相同：

```c
void HAL_SMARTCARD_AbortCpltCallback(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_AbortTransmitCpltCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H653 / C1732；v1.1.10 H652 / C1725。

两版原型相同：

```c
void HAL_SMARTCARD_AbortTransmitCpltCallback(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_AbortReceiveCpltCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H654 / C1747；v1.1.10 H653 / C1740。

两版原型相同：

```c
void HAL_SMARTCARD_AbortReceiveCpltCallback(SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_GetState

公开接口。定位：v1.1.4 H663 / C1782；v1.1.10 H662 / C1775。

v1.1.4：

```c
HAL_SMARTCARD_StateTypeDef HAL_SMARTCARD_GetState(SMARTCARD_HandleTypeDef *hsc);
```

v1.1.10：

```c
HAL_SMARTCARD_StateTypeDef HAL_SMARTCARD_GetState(const SMARTCARD_HandleTypeDef *hsc);
```

### HAL_SMARTCARD_GetError

公开接口。定位：v1.1.4 H664 / C1797；v1.1.10 H663 / C1790。

v1.1.4：

```c
uint32_t HAL_SMARTCARD_GetError(SMARTCARD_HandleTypeDef *hsc);
```

v1.1.10：

```c
uint32_t HAL_SMARTCARD_GetError(const SMARTCARD_HandleTypeDef *hsc);
```


## IrDA 接口

v1.1.4固定来源：[头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Inc/stm32f1xx_hal_irda.h)、[实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/de129f1c0af55ea4b2cfa8ba5686af54b7a51cf9/Src/stm32f1xx_hal_irda.c)。
v1.1.10固定来源：[头文件](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Inc/stm32f1xx_hal_irda.h)、[实现](https://github.com/STMicroelectronics/stm32f1xx-hal-driver/blob/77fbb30b7a1d02533980400083e48c559aae5a4f/Src/stm32f1xx_hal_irda.c)。

### HAL_IRDA_Init

公开接口。定位：v1.1.4 H532 / C292；v1.1.10 H531 / C293。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_Init(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_DeInit

公开接口。定位：v1.1.4 H533 / C366；v1.1.10 H532 / C367。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_DeInit(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_MspInit

弱默认回调，可由工程覆盖。定位：v1.1.4 H534 / C411；v1.1.10 H533 / C412。

两版原型相同：

```c
void HAL_IRDA_MspInit(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_MspDeInit

弱默认回调，可由工程覆盖。定位：v1.1.4 H535 / C427；v1.1.10 H534 / C428。

两版原型相同：

```c
void HAL_IRDA_MspDeInit(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_RegisterCallback

条件注册API；仅对应USE_HAL_IRDA_REGISTER_CALLBACKS==1。定位：v1.1.4 H539 / C457；v1.1.10 H538 / C460。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_RegisterCallback(IRDA_HandleTypeDef *hirda, HAL_IRDA_CallbackIDTypeDef CallbackID, pIRDA_CallbackTypeDef pCallback);
```

### HAL_IRDA_UnRegisterCallback

条件注册API；仅对应USE_HAL_IRDA_REGISTER_CALLBACKS==1。定位：v1.1.4 H540 / C578；v1.1.10 H539 / C578。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_UnRegisterCallback(IRDA_HandleTypeDef *hirda, HAL_IRDA_CallbackIDTypeDef CallbackID);
```

### HAL_IRDA_Transmit

公开接口。定位：v1.1.4 H551 / C770；v1.1.10 H550 / C764。

v1.1.4：

```c
HAL_StatusTypeDef HAL_IRDA_Transmit(IRDA_HandleTypeDef *hirda, uint8_t *pData, uint16_t Size, uint32_t Timeout);
```

v1.1.10：

```c
HAL_StatusTypeDef HAL_IRDA_Transmit(IRDA_HandleTypeDef *hirda, const uint8_t *pData, uint16_t Size, uint32_t Timeout);
```

### HAL_IRDA_Receive

公开接口。定位：v1.1.4 H552 / C855；v1.1.10 H551 / C849。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_Receive(IRDA_HandleTypeDef *hirda, uint8_t *pData, uint16_t Size, uint32_t Timeout);
```

### HAL_IRDA_Transmit_IT

公开接口。定位：v1.1.4 H553 / C945；v1.1.10 H552 / C939。

v1.1.4：

```c
HAL_StatusTypeDef HAL_IRDA_Transmit_IT(IRDA_HandleTypeDef *hirda, uint8_t *pData, uint16_t Size);
```

v1.1.10：

```c
HAL_StatusTypeDef HAL_IRDA_Transmit_IT(IRDA_HandleTypeDef *hirda, const uint8_t *pData, uint16_t Size);
```

### HAL_IRDA_Receive_IT

公开接口。定位：v1.1.4 H554 / C990；v1.1.10 H553 / C984。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_Receive_IT(IRDA_HandleTypeDef *hirda, uint8_t *pData, uint16_t Size);
```

### HAL_IRDA_Transmit_DMA

公开接口。定位：v1.1.4 H555 / C1038；v1.1.10 H554 / C1040。

v1.1.4：

```c
HAL_StatusTypeDef HAL_IRDA_Transmit_DMA(IRDA_HandleTypeDef *hirda, uint8_t *pData, uint16_t Size);
```

v1.1.10：

```c
HAL_StatusTypeDef HAL_IRDA_Transmit_DMA(IRDA_HandleTypeDef *hirda, const uint8_t *pData, uint16_t Size);
```

### HAL_IRDA_Receive_DMA

公开接口。定位：v1.1.4 H556 / C1106；v1.1.10 H555 / C1108。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_Receive_DMA(IRDA_HandleTypeDef *hirda, uint8_t *pData, uint16_t Size);
```

### HAL_IRDA_DMAPause

公开接口。定位：v1.1.4 H557 / C1173；v1.1.10 H556 / C1178。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_DMAPause(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_DMAResume

公开接口。定位：v1.1.4 H558 / C1210；v1.1.10 H557 / C1215。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_DMAResume(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_DMAStop

公开接口。定位：v1.1.4 H559 / C1246；v1.1.10 H558 / C1254。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_DMAStop(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_Abort

公开接口。定位：v1.1.4 H561 / C1298；v1.1.10 H560 / C1306。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_Abort(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_AbortTransmit

公开接口。定位：v1.1.4 H562 / C1362；v1.1.10 H561 / C1370。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_AbortTransmit(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_AbortReceive

公开接口。定位：v1.1.4 H563 / C1404；v1.1.10 H562 / C1412。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_AbortReceive(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_Abort_IT

公开接口。定位：v1.1.4 H564 / C1449；v1.1.10 H563 / C1457。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_Abort_IT(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_AbortTransmit_IT

公开接口。定位：v1.1.4 H565 / C1577；v1.1.10 H564 / C1585。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_AbortTransmit_IT(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_AbortReceive_IT

公开接口。定位：v1.1.4 H566 / C1654；v1.1.10 H565 / C1662。

两版原型相同：

```c
HAL_StatusTypeDef HAL_IRDA_AbortReceive_IT(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_IRQHandler

公开接口。定位：v1.1.4 H568 / C1724；v1.1.10 H567 / C1732。

两版原型相同：

```c
void HAL_IRDA_IRQHandler(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_TxCpltCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H569 / C1869；v1.1.10 H568 / C1877。

两版原型相同：

```c
void HAL_IRDA_TxCpltCallback(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_RxCpltCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H570 / C1901；v1.1.10 H569 / C1909。

两版原型相同：

```c
void HAL_IRDA_RxCpltCallback(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_TxHalfCpltCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H571 / C1885；v1.1.10 H570 / C1893。

两版原型相同：

```c
void HAL_IRDA_TxHalfCpltCallback(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_RxHalfCpltCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H572 / C1917；v1.1.10 H571 / C1925。

两版原型相同：

```c
void HAL_IRDA_RxHalfCpltCallback(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_ErrorCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H573 / C1933；v1.1.10 H572 / C1941。

两版原型相同：

```c
void HAL_IRDA_ErrorCallback(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_AbortCpltCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H574 / C1949；v1.1.10 H573 / C1957。

两版原型相同：

```c
void HAL_IRDA_AbortCpltCallback(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_AbortTransmitCpltCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H575 / C1965；v1.1.10 H574 / C1973。

两版原型相同：

```c
void HAL_IRDA_AbortTransmitCpltCallback(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_AbortReceiveCpltCallback

弱默认回调，可由工程覆盖。定位：v1.1.4 H576 / C1981；v1.1.10 H575 / C1989。

两版原型相同：

```c
void HAL_IRDA_AbortReceiveCpltCallback(IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_GetState

公开接口。定位：v1.1.4 H585 / C2018；v1.1.10 H584 / C2026。

v1.1.4：

```c
HAL_IRDA_StateTypeDef HAL_IRDA_GetState(IRDA_HandleTypeDef *hirda);
```

v1.1.10：

```c
HAL_IRDA_StateTypeDef HAL_IRDA_GetState(const IRDA_HandleTypeDef *hirda);
```

### HAL_IRDA_GetError

公开接口。定位：v1.1.4 H586 / C2033；v1.1.10 H585 / C2041。

v1.1.4：

```c
uint32_t HAL_IRDA_GetError(IRDA_HandleTypeDef *hirda);
```

v1.1.10：

```c
uint32_t HAL_IRDA_GetError(const IRDA_HandleTypeDef *hirda);
```


## 配套实现边界

- [CPU数据宽度与初始化](Smartcard与IrDA数据宽度及初始化.md)：校验组合下的缓冲宽度、两版差异、参数断言和重初始化顺序。
- [DMA启动、完成与错误边界](Smartcard与IrDA_DMA边界.md)：句柄、返回值、循环模式、回调与资源所有权。

本页完整核对的是上述固定头文件的HAL函数声明集合及对应定义原型；不据此宣称完整类型/宏索引、所有接口语义或全部并发路径均已完成审查。

函数声明以外的Init结构、配置编码和30个__HAL控制宏，见[专用配置字段及宏](Smartcard与IrDA配置字段及宏.md)；该页分别限定其覆盖范围。
