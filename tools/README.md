# 离线SVD查询与固定断言校验

完整说明见[来源/SVD寄存器交叉校验](../来源/SVD寄存器交叉校验.md)。只使用Python标准库，不联网、不安装、不操作板卡。厂商包/SVD/PDSC不随仓库分发。

仓库根目录示例：

```sh
python tools/svd_query.py vendor/SVD/STM32F103xx.svd --peripherals TIM2 --register CNT
python tools/svd_query.py vendor/SVD/STM32F103xx.svd --check tools/svd_reference/expected_claims.json
python -m unittest discover -s tools -p test_svd_query.py -v
```

原件可按说明页从Keil官网下载，使用前核对SHA-256。无原件时真实文件测试skip，13项合成测试可独立运行。设置SVD_TEST_FILE可选择原件位置。

期待值是两份SHA-256固定历史页面的654项标量断言，结果649相符、2冲突、3未知；不是当前全库验收。固定检查因已知ARR复位冲突返回exit 1。另有TIM1 DMAB位宽来源冲突，未混入654项。

需要重建历史期待值时：

```sh
python tools/build_svd_expectations.py ./baseline-snapshot
```

构建器会核验固定页面哈希和断言数量，输入改变必须先审查。输出到stdout；是否保存由调用者决定。不要用SVD结果自动覆盖RM0008或ES096结论。
