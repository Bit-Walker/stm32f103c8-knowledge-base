# SVD寄存器交叉校验

SVD适合校验寄存器地址、字段位段、复位值等结构化事实。它是辅助证据，不能代替RM0008、ES096和具体器件的数据手册。这里提供离线只读脚本、固定期待值与逐项结果，不附厂商原件。

## 官方来源与器件映射

- [Arm Keil官方目录](https://www.keil.arm.com/packs/stm32f1xx_dfp-keil/versions/)
- [Keil.STM32F1xx_DFP.2.4.1.pack官方下载](https://www.keil.com/pack/Keil.STM32F1xx_DFP.2.4.1.pack)：版本2.4.1，发布日期2023-05-12，取得日期2026-10-16
- 包内 `Keil.STM32F1xx_DFP.pdsc` 的 `device Dname="STM32F103C8"` 直接指定 `debug svd="SVD/STM32F103xx.svd"`，编译定义为 `STM32F10X_MD`，Flash 65536字节、SRAM 20480字节
- SVD内器件名为 `STM32F103xx`，版本1.3。PDSC没有单列完整订单号STM32F103C8T6；这里确认的是C8器件级映射，T6封装/温度范围及引脚仍由DS5319界定

原始包大小50,237,740字节，SHA-256：

`807ea15da5b172b916bbc47b2b87f1e621240ad208d38e82a417a2ef8191e9d1`

SVD大小867,312字节，SHA-256：

`1d92b65aaf397a18a599fb6a840812015ad379cdcc0cc3687f673f63e7445367`

完整来源身份和文件哈希见[清单](../tools/svd_reference/source_manifest.json)。该SVD是家族级描述，实例适用范围须按C8核对，不能直接当作C8的功能列表。本次只检查DMA1、TIM1、TIM2。

没有找到覆盖该SVD的明确再分发许可：SVD无licenseText，PDSC无包license元素，包内StdPeriph_Driver的许可不能推及SVD。因此本目录仅提供自产脚本、检查数据和官方获取路径。

## 固定检查范围与结果

[654项逐项结果](../tools/svd_reference/crosscheck_results.json)：649相符、2冲突、3未知。它们是标量断言，不能解释成654个寄存器，也不是全库覆盖率。

- 72个寄存器视图的地址偏移全部相符：DMA1 30、TIM1 22、TIM2 20。CCMR输入/输出分别计为一个视图
- 72个复位值断言中70相符、2冲突
- 238个字段的位偏移与位宽，共476项相符
- DMA1基址和30个寄存器size，共31项相符
- 3项副作用探针未知

### ARR复位值冲突

TIM1、TIM2的SVD ARR复位值均为0，而[RM0008 Rev21 §14.4.12/p356](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=356)及[§15.4.12/p419](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=419)为0xFFFF；寄存器地图也支持手册结论。知识库保留0xFFFF，并记录SVD冲突。

### 缺失的副作用语义

DMA1 IFCR.CGIF1写1清、TIM2 SR.UIF写0清、TIM2 CCR1读取影响外部状态的行为，没有在所查SVD机器字段中表达，返回unknown。CCR1探针只寻找readAction=modifyExternal，不能据此推导输入/输出条件、被清标志或ES096捕获竞争行为。未知不等于不存在副作用。

### 另行发现：DMAR必须分实例

以下未纳入原654项，不改变该计数：

- TIM1：RM0008 §14.4.20/p362及表84/p364将DMAB定义为[31:0]；SVD同名字段为16位，是额外字段宽度冲突
- TIM2：RM0008 §15.4.18/pp421–422及表88/p424将DMAB定义为[15:0]、上16位保留，与SVD相符

SVD把两者的size都写32，不能用这一表示宽度消解字段宽度的差异。也不能把DMA的ES096窄访问限制泛化到TIM。

## 历史基线与适用边界

[期待值](../tools/svd_reference/expected_claims.json)取自[固定历史提交 53f8548343b114f424dc39b4686e8982318b8393](https://github.com/Bit-Walker/stm32f103c8-knowledge-base/commit/53f8548343b114f424dc39b4686e8982318b8393)中的两份确定内容，同时以文件SHA-256校验身份：

- 参数/TIM/硬件参数表.md：`276f896495ad8c4fe4157bf8a541f27017c952705dc2bfbf29ed3b6782a7a818`
- 参数/DMA参数与HAL接口.md：`28f6e61d76c8c1ac8692a3cae1616689ccfc2bd67dba37da8c5b7e6570a86bd3`

期待值独立于SVD，从寄存器地图、明确位表和DMA公式提取。[重建脚本](../tools/build_svd_expectations.py)锁定上述原始文件哈希及654个唯一断言；页面修订后会拒绝直接重建，必须先审查新基线。这是历史固定断言的可复跑记录，不表示当前所有页面已通过校验。每条source中的section_label是人工阅读定位提示，不是网页锚点。

未核验触发互联、DMA物理请求映射、全部CCMR/CCER位、滤波编码、时钟树、HAL/LL生命周期、实机行为或整颗芯片的访问语义。例：TIM2.CNT地址0x40000024、size32、CNT字段16位；这支持16位有效计数范围，不能推导32位计数器或允许的CPU访问粒度。

## 离线使用

取得并解压官方包后，在仓库根目录运行。`vendor/SVD/STM32F103xx.svd`是用户取得原件的位置示例，不属于仓库发布文件：

```sh
python tools/svd_query.py vendor/SVD/STM32F103xx.svd --peripherals TIM2 --register CNT
python tools/svd_query.py vendor/SVD/STM32F103xx.svd --peripherals TIM1 TIM2 --register ARR
python tools/svd_query.py vendor/SVD/STM32F103xx.svd --check tools/svd_reference/expected_claims.json
python tools/build_svd_expectations.py ./baseline-snapshot
python -m unittest discover -s tools -p test_svd_query.py -v
```

校验原件SHA-256后再比较记录。脚本不会联网获取、安装或执行厂商代码，也不会访问板卡；只读输入，向标准输出返回JSON。

检查模式：全部相符exit 0；存在冲突exit 1；解析/不支持结构错误exit 2；仅未知且无冲突exit 3。本固定数据有两项已知冲突，exit 1是预期结果，不能称全通过。普通缺失查询返回显式unknown对象。

测试含13项合成测试及1项可选真实原件测试；没有原件时后者明确skip。可用环境变量 `SVD_TEST_FILE` 指向原件后重跑，脚本不要求再分发SVD。

## 有限解析器的边界

[查询脚本](../tools/svd_query.py)仅用Python标准库，限制XML为UTF-8、16MiB，拒绝DTD、ENTITY、NUL，不获取外部schema。支持明确列出的外围/寄存器/字段和寄存器默认值继承；字段readAction、modifiedWriteValues支持从register继承并返回来源。

选中内容含derivedFrom、dim或cluster会拒绝；重复受支持单值属性、多种位范围表示、不完整范围、字段超过寄存器size、多组enumeratedValues、register级writeConstraint也会拒绝。field级writeConstraint只展示原始XML，不解算有效约束。缺失属性保持未知，不补成无副作用。本工具不声称实现完整CMSIS-SVD标准。
