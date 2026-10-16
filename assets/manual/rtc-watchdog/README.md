# RM0008 Rev21：RTC 与看门狗原图来源

本页记录 RTC 计时核和 WWDG 刷新窗口的两幅原图。来源为 [ST 官方 RM0008 PDF](https://www.st.com/resource/en/reference_manual/cd00171190.pdf)，固定 Rev21（2021-02）；印刷页与 PDF 文件页一致。所用 PDF 为 13,119,424 字节、1136 页，SHA-256：`4c1b8ac2729cc1f45a4685eea9e91e6139e24e58804fba21e27201dfcc2ad149`。原图版权归 STMicroelectronics。

两幅图片保留既有 PNG 原字节，没有重画、覆盖标签、改变箭头或二次缩放。已核对完整原页和相邻正文，并用 PyMuPDF 按 144 dpi（每 point 2 像素）整页 RGB 渲染，验证下列区域与 PNG 逐像素一致。下表坐标以页面左上角为原点，依次为左、上、右、下；右、下边界不包含在裁图内。两页渲染尺寸均为 1190 × 1684 像素。

| 原图 | 印刷/PDF 页 | 裁切坐标 point | 图片尺寸 |
|---|---|---|---|
| [Figure 179](p484-fig179.png) | 484/484 | 115, 323, 555, 640 | 880 × 634 |
| [Figure 184](p502-fig184.png) | 502/502 | 118, 305, 550, 544 | 864 × 478 |

## 完整性与适用条件

- [Figure 179 原页](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=484)保留图号、完整标题 RTC simplified block diagram、图内标识 ai14969b、PRL/DIV/TR_CLK/CNT/ALR 计时链、APB 接口、全部事件支路及 Standby 供电标注。原图没有编号脚注。相邻 p485 的接口同步和配置写入条件仍适用；APB 连线不证明 PRL/ALR 可读，访问差异按[RTC 参数页第 3 节](../../../参数/RTC/软件日历与寄存器读写边界.md#3-prl-已有只写确认alr-冲突仍未解决)分别处理。Standby 供电标注不能代替掉电后的时钟源和备份供电条件，比较器等号不能作为闹钟零延迟的依据。
- [Figure 184 原页](https://www.st.com/resource/en/reference_manual/cd00171190.pdf#page=502)保留图号、完整标题 Window watchdog timing diagram、图内标识 ai17101c、W 阈值、0x3F 阈值、两段刷新区间、T6 与 RESET 波形。原图没有编号脚注。p500 的 T>W 硬件描述、p501 的 T<W 操作文字及预分频相位说明，继续在[WWDG 图旁和时间预算](../../../参数/看门狗/启动刷新与时间预算.md#wwdg-window-original)保留。原页图上方要求写 CR 时 T6=1；图下超时公式及 p503 算例差异由正文第 4 节解释。图中没有单独的 EWI 波形，也不保证中断服务时间充足。

正文位置：[RTC 资源表与分频公式](../../../参数/RTC/软件日历与寄存器读写边界.md#rtc-core-original) · [WWDG 刷新窗口](../../../参数/看门狗/启动刷新与时间预算.md#wwdg-window-original)。技术来源范围见 [RM0008 RTC](../../../来源/RM0008.md#src-rm0008-r21-rtc-calendar-readback) 与 [RM0008 看门狗](../../../来源/RM0008.md#src-rm0008-r21-watchdog-start-window)。以上为原图和文档核对，不构成掉电保持或看门狗实板计时验收。

## PNG SHA-256

- p484-fig179.png：`2ed61c41b91103baed8357e521e53b0b61c3d79e2c989739bc9c45e16b55619b`
- p502-fig184.png：`7c5d94bf9c4c148367141b2b276a3d85434375cb0c85ebddcf71cdba81a0cdce`
