# 字符识别任务

我们通过对字符识别任务进行调研，并总结数据集描述中的字段信息，从而制定出字符识别任务DSDL模板，供大家参考使用。

## 1. 任务调研

### 1.1 任务定义

字符识别OCR （Optical Character Recognition，光学字符识别）是指对图片中的文字进行查找、提取、识别的一种技术，通过检测暗、亮的模式确定其形状，然后用字符识别方法将形状翻译成计算机文字的过程。其示意图如下所示：

<center>
<img src="https://user-images.githubusercontent.com/54258789/211495436-1e881eb2-04e5-4c9d-9938-05e3b6e7cb8d.png">
</center>

OCR任务按照算法可分为几个部分。

- 文字检测/分割，指从场景图片中准确找到文字所在位置，标注形式为polygon、bbox或图片
- 文字识别，指从纯文字图片或上述的检测框中得到文字内容，标注形式为text
- 关键信息提取：从小票、身份证等特殊文件中提取想要的类别
- 其他如表格识别、关系提取、版面分析等。

根据输入图片可分为街景图片、手写图片、文档、网络图片等。

### 1.2 评价指标

#### 1.2.1检测阶段

- 先按照检测框和标注框的IOU评估，IOU大于某个阈值判断为检测准确。这里检测框和标注框不同于一般的通用目标检测框，部分是采用多边形进行表示。

$$
检测精确率= {正确的检测框个数\over模型检测框个数}
$$

$$
检测召回率=\frac {正确的检测框个数}{人工标注框个数}
$$

$$
F1~score = \frac {2*检测精确率*检测召回率}{检测精确率+检测召回率}
$$

#### 1.2.2 识别阶段

 单词识别准确率，只有整行文本识别对才算正确识别。

$$
单词识别准确率 = \frac {正确识别的文本行数量}{人工标注的文本行数量}
$$

#### 1.2.3 端到端统计

$$
端到端精确率=\frac {准确检测并正确识别文本行数量}{模型检测的文本行数量}
$$

$$
端到端召回率=\frac{准确检测并正确识别文本行数量}{人工标注的文本行数量}
$$

### 1.3 主流数据集调研

OCR数据集，其中包含了Total-Text、ICDAR2015等常见数据集。考虑到有些数据集同时包含了不同的OCR子任务，这里对常用的子任务进行了拆分，并且每个子任务只考虑和他相关的标注内容。为了使得模板更加通用，同时也具备拓展能力，我们着重关注各个数据集之间的共性和特性，此外，调研过程会遇到一些名称不同，但是实际含义相同或类似的字段，这些字段我们也视为同一字段，并统一去命名，比如image_id字段一般表示图片的路径或者id，是图片的唯一标识。

#### 1.3.1 文字检测数据集调研

我们调研了ICDAR2013、ICDAR2015、SVT、Total-Text、MSRA-TD50、CUTE80，数据集的标注框信息是必要的，但格式可以为bbox或polygon形式。

<table border="6" >
    <tr>
      <th rowspan="2" align=center colspan="1" align=center>OCR数据集</th>
      <th colspan="3" align=center>共享字段</th>
      <th colspan="2" align=center>独立字段</th>
    </tr>
    <tr>
      <th>image_id</th>
      <th>bbox</th>
      <th>polygon</th>
	  <th>orientation</th>
      <th>isdifficult</th>
    </tr>
    <tr>
      <th width="25%" >ICDAR2013</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
	  <td width="20%" align="center"></td>
	  <td width="20%" align="center"></td>
    </tr>
    <tr>
      <th width="25%" >ICDAR2015</th>
      <td width="20%" align="center">Y</td>
	  <td width="20%" align="center"></td>
      <td width="20%" align="center">Y</td>
	  <td width="20%" align="center"></td>
	  <td width="20%" align="center"></td>
    </tr>
    <tr>
      <th width="25%" >SVT</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center"></td>
	  <td width="20%" align="center"></td>
	  <td width="20%" align="center"></td>
    </tr>
    <tr>
      <th width="25%" >Total-Text</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center"></td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
	  <td width="20%" align="center"></td>
    </tr>
    <tr>
      <th width="25%" >MSRA-TD50</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center"></td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
    </tr>
    <tr>
      <th width="25%" >CUTE80</th>
      <td width="20%" align="center">Y</td>
	  <td width="20%" align="center"></td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center"></td>
      <td width="20%" align="center"></td>
    </tr>
  </table>

备注：其中Total-Text数据集旧版提供了bbox和polygon两个字段，但是新版仅提供polygon，这里以新版为主。

各个字段的含义如下表所示：

<table border="3" >
  <tr>
    <th align="center" >字段类型</th>
    <th align="center" >字段名称</th>
    <th align="center" >含义</th>
  </tr>
  <tr>
    <th rowspan="3">共享字段</th>
    <th align="left" >image_id</th>
    <td>定位到唯一图片，比如用图片名或者图片路径表示</td>
  </tr>
  <tr>
    <th align="left" >bbox</th>
    <td>定位单个目标的矩形框，比如用[xmin, ymin, xmax, ymax]表示</td>
  </tr>
  <tr>
    <th align="left" >polygon</th>
    <td>定位单个目标的多边形框，顶点个数不固定</td>
  </tr>
<tr>
    <th rowspan="2">独立字段</th>
    <th align="left" >orientation</th>
    <td>目标框旋转的角度，或目标框旋转类别：弯曲、水平等</td>
  </tr>
  <tr>
    <th align="left" >isdifficult</th>
    <td>是否为检测困难的目标</td>
  </tr>
</table>

可以看到，在文字检测任务中，image_id和bbox/polygon为最基础的字段，其中bbox和polygon字段需至少选择一种格式。

#### 1.3.2 文字分割数据集调研

支持文字分割的数据集较少，这里我们仅调研了Total-Text，结果如下：

<table border="9" >
    <tr>
      <th rowspan="2" align=center colspan="1" align=center>OCR数据集</th>
      <th colspan="2" align=center>共享字段</th>
    </tr>
    <tr>
      <th>image_id</th>
      <th>segmentation_map</th>
    </tr>
    <tr>
      <th width="25%" >Total-Text</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
    </tr>
  </table>

各个字段的含义如下表所示：

<table border="3" >
  <tr>
    <th align="center" >字段类型</th>
    <th align="center" >字段名称</th>
    <th align="center" >含义</th>
  </tr>
  <tr>
    <th rowspan="2">共享字段</th>
    <th align="left" >image_id</th>
    <td>定位到唯一图片，比如用图片名或者图片路径表示</td>
  </tr>
  <tr>
    <th align="left" >segmentation_map</th>
    <td>分割图，可以是单词分割也可以是字符分割，一般为二值化图</td>
  </tr>
</table>

#### 1.3.3 文字识别数据集调研

我们调研了ICDAR2013、ICDAR2015、SVT、Total-Text、IIIT-5K，结果如下：

<table border="6" >
    <tr>
      <th rowspan="2" align=center colspan="1" align=center>OCR数据集</th>
      <th colspan="2" align=center>共享字段</th>
      <th colspan="1" align=center>独立字段</th>
    </tr>
    <tr>
      <th>image_id</th>
      <th>text</th>
      <th>lexicon</th>
    </tr>
    <tr>
      <th width="25%" >ICDAR2013</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
    </tr>
    <tr>
      <th width="25%" >ICDAR2015</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
    </tr>
    <tr>
      <th width="25%" >SVT</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
    </tr>
    <tr>
      <th width="25%" >Total-Text</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center"></td>
    </tr>
    <tr>
      <th width="25%" >IIIT-5K</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
    </tr>
  </table>

各个字段的含义如下表所示：

<table border="3" >
  <tr>
    <th align="center" >字段类型</th>
    <th align="center" >字段名称</th>
    <th align="center" >含义</th>
  </tr>
  <tr>
    <th rowspan="2">共享字段</th>
    <th align="left" >image_id</th>
    <td>定位到唯一图片，比如用图片名或者图片路径表示</td>
  </tr>
  <tr>
    <th align="left" >text</th>
    <td>目标框中文本内容</td>
  </tr>
  <tr>
    <th rowspan="1">独立字段</th>
    <th align="left" >lexicon</th>
    <td>词汇表，可以是单张图片词汇表，也可以是数据集词汇表</td>
  </tr>
</table>

## 2. 模板展示

根据上述的调研结果，我们知道对于OCR任务，一个样本最重要的属性是图片的id(或路径)、每个标注框的位置以及文本，考虑到每张图片可能包含多个标注框，我们定义了一个嵌套结构体LocalInstanceEntry（其详细定义可以参考[DSDL入门文档-语言定义-嵌套结构体](http://research.pages.shlab.tech/dataset_standard/dsdl-docs/zh/lang/structs/#242)），用来表述单个标注框的信息（即类别和位置）。这样，我们可以在OCR任务结构体的$fields属性中定义image和instances两个字段，其中instances字段则为多个LocalObjectEntry结构体构成的列表（列表为空表示图片没有标注框）。基于上述考虑，我们制定了不同OCR任务的模板，这里模板为方便理解，将任务进行详细拆分。

### 2.1 文字检测模板

文字检测模板具体可以参考单独的[目标检测文档](http://research.pages.shlab.tech/dataset_standard/dsdl-docs/dsdl_template/cv/cv_detection/)，这里我们制定了OCR检测任务的范例模板，如下所示：

```YAML
$dsdl-version: "0.5.0"

OCRSample:
    $def: struct
    $fields:
        image: Image
        instances: List[Bbox] 
```

在模板中的一些字段含义如下：

- $dsdl-version: 描述了该文件对应的dsdl版本
- OCRSample: 定义了OCR任务sample的结构体，包含四个字段:
    - $def: struct, 表示这是一个结构体类型
    - $fields: 结构体类所包含的属性，具体包括:
        - image 图片的路径
        - instances 标注信息，OCR任务中，为多个标注框构成的一个列表，标注框形式取决于数据集，可以是Bbox，也可以是Polygon

### 2.2 文字分割模板

文字分割模板具体可以参考单独的[图像分割文档](http://research.pages.shlab.tech/dataset_standard/dsdl-docs/dsdl_template/cv/cv_segmentation/)，这里我们制定了OCR分割任务的范例模板，如下所示：

```YAML
$dsdl-version: "0.5.0"

SegClassDom:
    $def: class_domain
    classes:
        - text

OCRSample:
    $def: struct
    $params: ["cdom"]
    $fields:
        image: Image
        word_segmap: LabelMap[dom=$cdom]
        chr_segmap: LabelMap[dom=$cdom]
```

在模板中的一些字段含义如下：

- $dsdl-version: 描述了该文件对应的dsdl版本
- SegClassDom: 定义了分割任务的classdom，包含两个字段：
    - $def: class_domain，表示这是一个class_domain类型
    - classes 包含具体类别，这里只有一个text类别
- OCRSample: 定义了OCR任务sample的结构体，包含四个字段:
    - $def: struct, 表示这是一个结构体类型
    - $params: 定义了形参，在这里即class domain
    - $fields: 结构体类所包含的属性，具体包括:
        - image 图片的路径
        - word_segmap 单词粒度的分割图
        - chr_segmap 字符粒度的分割图

### 2.3 文字识别模板

文字识别模板为OCR任务单独使用，定义了新的字段Text。

```YAML
$dsdl-version: "0.5.0"

OCRSample:
    $def: struct
    $fields:
        word_image: Image
        text: Text
```

在模板中的一些字段含义如下：

- $dsdl-version: 描述了该文件对应的dsdl版本
- OCRSample: 定义了OCR任务sample的结构体，包含四个字段:
    - $def: struct, 表示这是一个结构体类型
    - $fields: 结构体类所包含的属性，具体包括:
        - word_image 图片的路径，注意文字识别任务中图片为裁切图片，即文字检测后的图片
        - annotations 标注信息，OCR任务中，为前面的LocalInstanceEntry构成的一个列表

### 2.4 端到端模板

这里端到端任务以文字检测+文字识别为例：

```YAML
$dsdl-version: "0.5.0"

LocalInstanceEntry:
    $def: struct
    $fields:
        location: Polygon/Bbox 
        text: Text

OCRSample:
    $def: struct
    $fields:
        image: Image
        instances: List[LocalInstanceEntry]
```

在模板中的一些字段含义如下：

- $dsdl-version: 描述了该文件对应的dsdl版本
- LocalInstanceEntry: 定义了标注框的描述方式的嵌套结构体，包含四个字段:
    - $def: struct, 表示这是一个结构体类型
    - $fields: 结构体类所包含的属性，具体包括:
        - polygon 标注框的位置
        - text 标注框的内容
- OCRSample: 定义了检测任务sample的结构体，包含四个字段:
    - $def: struct, 表示这是一个结构体类型
    - $fields: 结构体类所包含的属性，具体包括:
        - image 图片的路径
        - instances 标注信息，为前面的LocalInstanceEntry构成的一个列表

## 3. 使用说明

在这个章节介绍一下如何通过import的方式来引用我们的模板。以SynthText端到端模板为例

目录结构如下：

```
SynthText-dsdl/
├── defs/                        
│  ├── OCR-SynthText.yaml           # struct定义文件
├── train/                          # 该数据集仅有训练集，mmocr中使用其他数据集作为下游测试
│  ├── train.yaml                   # 训练的yaml文件
│  ├── train_samples.json           # 训练集sample的json文件
├── config.py                       # 数据集读取路径等config文件
└── README.md                       # 数据集教程：下载、怎么使用、配置文件的教程。
```

### 3.1 数据集定义文件

OCR-SynthText.yaml如下：

```
$dsdl-version: "0.5.0"

LocalCharEntry:                        # instance内字符标注内容
    $def: struct 
    $fields:
        char_polygon: Polygon
        char_text: Text                 # 标注的字符内容

LocalInstanceEntry:                     # instance标注内容，包括单词和字符          
    $def: struct 
    $fields:        
        polygon: Polygon
        text: Text                      # 标注的单词内容
        charlist: List[LocalCharEntry]

OCRSample:
    $def: struct
    $fields:
        image: Image
        instances: List[LocalInstanceEntry]

```

具体的字段说明如下所示：

- $dsdl-version: 描述了该文件对应的dsdl版本
- LocalCharEntry: 定义了字符粒度的标注结构体，包含两个字段：
    - $def: struct, 表示这是一个结构体类型
    - $fields: 结构体类所包含的属性，具体包括:
        - char_polygon 单个字符的polygon
        - char_text 单个字符的文本标注
- LocalInstanceEntry: 定义了单词粒度的标注结构体，包含两个字段：
    - $def: struct, 表示这是一个结构体类型
    - $fields: 结构体类所包含的属性，具体包括:
        - polygon 单词的polygon
        - text 单词的文本标注
        - charlist 该单词内字符的文本标注,为上面LocalCharEntry构成的一个列表
- OCRSample: 定义了检测任务sample的结构体，包含四个字段:
    - $def: struct, 表示这是一个结构体类型
    - $fields: 结构体类所包含的属性，具体包括:
        - image 图片的路径
        - instances 标注信息，为前面的LocalInstanceEntry构成的一个列表

### 3.2 samples相关文件

train.yaml如下：

```YAML
$dsdl-version: "0.5.2"

$import:
    - ../defs/OCR-SynthText

meta:
    dataset_name: "SynthText"
    creator: "University of Oxford"
    home-page: "https://www.robots.ox.ac.uk/~vgg/data/scenetext/"
    opendatalab-page: "https://opendatalab.com/SynthText"
    sub-name: "train"
    task-type: "Optical Character Recognition"

data:
    sample-type: OCRSample
    sample-path: train_samples.json
```

train_sample.json的内容如下：

```YAML
{"samples": [
    {
        "image": "image":"8/ballet_106_0.jpg",
        "instances": [
            {
                "polygon": [[[420,21],[512,23],[512,42],[420,40]]],
                "text": "Lines",
                "charlist":[
                	{"char_polygon":[[[423,22],[438,22],[436,40],[420,40]]],
                	 "char_text": "L"}
                	{"char_polygon":[[[440,22],[453,22],[450,40],[437,40]]],
                	 "char_text": "i"}
                	 ...
                ]
            },
            ...
        ]
    },
    ...
]}

```
