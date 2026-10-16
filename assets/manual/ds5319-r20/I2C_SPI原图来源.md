# DS5319 Rev20：I²C与SPI原图裁切记录

来源：[ST DS5319官方入口](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf)，使用固定Rev20（2025-07）副本，共114个PDF文件页；这里引用页的印刷页与文件页一致，页脚印/115。本次没有重新下载并与当前线上文件逐字节比对。原图版权归STMicroelectronics。

源PDF SHA-256：`1e54ce18e6c34c5b4a78986f26e245e143748c721009fc9af5953795c30686bc`。

按216 dpi整页RGB渲染后整数像素无损截取，不重画、不翻译覆盖标签、不重新排列信号、不改色。坐标单位pt，原点为PDF页左上角，顺序为左、上、右、下；每pt对应3像素。

| 图号 | 印刷/PDF页 | 图内标识 | 裁切坐标pt | 像素尺寸 |
|---|---|---|---|---|
|[Figure32](p69-fig32.png)|69/69|ai14133g|120, 87, 533, 381|1239 × 882|
|[Figure33](p71-fig33.png)|71/71|MSv41658V2|64, 87, 533, 312|1407 × 675|
|[Figure34](p71-fig34.png)|71/71|MSv41659V2|64, 316, 533, 538|1407 × 666|
|[Figure35](p72-fig35.png)|72/72|MSv72626V1|120, 87, 533, 383|1239 × 888|

## 完整性与应用边界

- Figure32保留测量电路、SDA/SCL波形、全部时序箭头及两条原注。0.3/0.7 VDD测量阈值、Rp/Rs/VDD_I2C定义不省略；图内tsu(STO:STA)与Table41的tw(STO:STA)差异保留在正文。
- Figure33/34分别保留CPHA=0/1及各自CPOL=0/1两行SCK、NSS、MISO/MOSI、首位/后续位/末位、访问与禁用时间箭头。两幅图的首位关系不同，不合并为同一波形。
- Figure35保留完整四种CPHA/CPOL时钟行、MISO输入、MOSI输出和NSS input High，不把NSS input改写为应用GPIO片选输出。
- 这些图帮助定位测量边沿，数值和保证类型仍以Table41～43及全部相关条件为准。表42示例与Table41注2的400 kHz供时差异、tSP脚注、PCLK周期表达式、负载与特性评估条件均保持；图片不替代板端测量或时序裕量核算。

## 图片SHA-256

- p69-fig32.png：`9ddc842b36a1995752079914f6eec11ae0daa7566ba02499c05bac0d84277a91`
- p71-fig33.png：`3e43b8047f9e0574ed2c21d72d44d06719ad059a24507db1be09b33839a7e05a`
- p71-fig34.png：`b27610d19519b8f22c8df32935fe08e1b25db1d110ee21f168ea6b7ae94a0e1f`
- p72-fig35.png：`827fbafbc9965c756314b8d5ba722eb601b9c2bb044e0428f76b327b881be6ec`
