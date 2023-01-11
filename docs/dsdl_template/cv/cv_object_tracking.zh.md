# 目标跟踪任务

我们通过对目标跟踪任务进行调研，并总结数据集描述中的字段信息，从而制定出目标跟踪任务DSDL模板，供大家参考使用。

## 1. 任务调研

### 1.1 任务定义

目标跟踪任务是指在图像中检测出物体的位置，并识别出具体的实例，通过一个特殊识别ID对其进行跟踪。分为单目标跟踪和多目标跟踪，有的数据集还会对每个实例的类别进行标注。其示意图如下所示：

| ![gif](https://user-images.githubusercontent.com/113978928/209652879-91183966-40f0-43cd-82da-7b9ff84d3a7f.gif) | ![gif](https://user-images.githubusercontent.com/113978928/209652898-3b9b9a5a-a301-4bfd-8650-4842259d4eb6.gif) |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| 图1 GOT10k 单目标跟踪                                                                                        | 图2 MOT17 多目标跟踪                                                                                         |

### 1.2 评价指标

最常用的就是两个：精确度和成功率（比如TrackingNet、UAV123、Nfs、OTB2015、LaSOT、TLP）。

* **成功率（Success Rate/IOU Rate/AOS）**

成功值 (**success**)计算是计算预测框与标注框的区域内像素的交并比。成功率 (**Success Rate**)即在success一定阈值之下，成功个数的比例。在不同的阈值下，成功率也会相应变化，以阈值为x，成功率为y，可作出成功率曲线 (**Success rate plot)**。**AUC**(Area under curve)分数即为成功率曲线下的面积。有的论文也会直接指定阈值，由于中值定理，最常用的阈值是0.5。

* **精确度**（**Precision）**

精确度是追踪成功的个数比例。为了计算追踪成功的个数，需要计算预测框中心点与标注框的中心点的之间欧氏距离，通常阈值为20像素，即它们的欧氏距离在20像素之内就视为追踪成功。

* **归一化精确度（Normalized Precision）**

考虑到标注框的尺度大小将影响对精确度的判断（比如，对于较小的标注框，预测框和标注框的中心点相隔20像素，两者的交并比已经下降到一个非常低的值），因此，将精确度 (Precision)根据标注框大小进行了归一化，得到了归一化精确度 (Normalized Precision)。

<a id="table-1"></a>

### 1.3 主流数据集调研

我们对4个目标检测数据集进行调研，对相关数据集描述文件（主要是标注字段）进行分析汇总，相同含义的标注字段会以统一命名进行展示，汇总信息如下表所示：

<table border="4" >
        <tr>
      <th rowspan="2" align=center colspan="1" align=center>目标跟踪数据集</th>
      <th colspan="5" align=center>共享字段</th>
      <th colspan="9" align=center>独立字段</th>
    </tr>
    <tr>
      <th>instance_id</th>
      <th>bbox</th>
      <th>category</th>
      <th>media_path</th>
      <th>frame_ID</th>
      <th>width</th>
      <th>height</th>
      <th>frameRate</th>
      <th>seqLength</th>
      <th>absence</th>
      <th>Visibility/Cover/Occluded</th>
      <th>truncated/cut_by_image</th>
      <th>ignore_flag</th>
    </tr>
    <tr>
      <th width="15%" >TrackingNet</th>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
    </tr>
    <tr>
      <th width="15%" >GOT10k</th>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
    </tr>
    <tr>
      <th width="15%" >MOT17</th>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
    </tr>
    <tr>
      <th width="15%" >KITTI-tracking</th>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
    </tr>
  </table>

 对共享字段和独立字段进行汇总，得到下表：

<table border="4" >
    <tr>
      <th align="center" >字段类型</th>
      <th align="center" >字段名称</th>
      <th align="center" >含义</th>
    </tr>
    <tr>
      <th rowspan="5">共享字段</th>
      <th>instance_id</th>
      <td>目标编号，同一目标在整个视频片段中具有唯一的编号，在多目标跟踪里为必需字段</td>
    <tr>
      <th>bbox</th>
      <td>定位单个目标的矩形框，比如用[xmin, ymin, xmax, ymax]表示</td>
    <tr>
      <th>category</th>
      <td>单个目标所属的类别</td>
    </tr>
    <tr>
      <th>media_path</th>
      <td>媒体文件路径</td>
    </tr>
    <tr>
      <th>frame_ID</th>
      <td>帧号，用于视频序列排序</td>
    </tr>
    <tr>
      <th rowspan="9">独立字段</th>
      <th>width</th>
      <td>图片的宽</td>
    <tr>
      <th>height</th>
      <td>图片的高</td>
    </tr>
    <tr>
      <th>frameRate</th>
      <td>帧率，有的数据集也叫anno_fps</td>
    <tr>
      <th>seqLength</th>
      <td>视频帧序列长度/张数</td>
    </tr>
    <tr>
      <th>absence</th>
      <td>指示该帧是否存在该对象</td>
    </tr>
    <tr>
      <th>Visibility/Cover/Occluded</th>
      <td>遮挡度。在不同数据集有不同的表示方法，可以是Cover（遮挡度、级别范围为0~8），也可以是visibility（物体可见程度，取值在 0~1 之间）,还可以是Occluded（当前标注是否有被遮挡。0 表示 "fully visiable"；1 表示 "partly occluded"；2 表示 "largely occluded"；3 表示 "unknown"）</td>
    </tr>
    <tr>
      <th>truncated/cut_by_image</th>
      <td>当前标注的对象是否正被图像边缘截断,1表示被截断</td>
    </tr>
    <tr>
      <th>ignore_flag</th>
      <td>当前标注在评估中是否被考虑，若 flag = 1，则考虑当前标注，若 flag = 0，则忽略</td>
    </tr>
</table>

可以看到，如果要描述一个检测数据集的样本，instance_id、bbox、media_path和frame_id是最基础的字段，此外还包含了各种描述边界框信息的特殊字段。

<a id="table-2"></a>

## 2. 模板展示

目标跟踪任务是目标检测任务的拓展，也包含嵌套结构体（其详细定义可以参考[DSDL入门文档-语言定义-嵌套结构体](../../dsdl_language/lang/structs.md)）和类别域（class domain，或者cdom，具体可以参考[DSDL入门文档-语言定义-类别域](../../dsdl_language/lang/class_dom.zh.md)），但与之不同的是：根据上述的调研结果，我们知道对于目标跟踪任务重要的属性包括frame_id、media_path、instance_id、bbox和category，而这些属性分别属于 **三个层级的结构体** ，第一层是视频，第二层是视频帧（即图片），第三层是标注。因此我们需要定义三层的嵌套结构体，用来详细描述每个样本的信息。

基于上述考虑，我们制定了目标跟踪任务的模板，如下所示：

**object-tracking.yaml**

```yaml
$dsdl-version: "0.5.0"

LocalObjectEntry:  
    $def: struct   
    $params: ["cdom"]
    $fields: 
        instance_id: InstanceID
        bbox: BBox
        category: Label[dom=$cdom]

FrameSample:
    $def: struct
    $params: ["cdom"]
    $fields:
        frame_id: UniqueID
        media_path: Image
        objects: List[etype=LocalObjectEntry[cdom=$cdom]]

VideoFrame:
    $def: struct
    $params: ["cdom"]
    $fields:
        video_name: Str
        videoframes: List[etype=FrameSample[cdom=$cdom]]
```

在目标跟踪模板中的一些字段含义如下（详细学习请参考 [DSDL语言教程](../../dsdl_language/overview.zh.md)）

- $dsdl-version: 描述了该文件对应的dsdl版本
- LocalObjectEntry: 定义了标注框的描述方式的嵌套结构体，包含四个字段:
    - $def: struct, 表示这是一个结构体类型
    - $params: 定义了形参，在这里即class domain
    - $fields: 结构体类所包含的属性，具体包括:
        - instance_id：物体编号，同一物体在整个视频片段中具有唯一的编号
        - bbox：标注框信息，转化为bbox标准，即[x,y,w,h]
        - category：标注框类别，与ClassDom对应
- FrameSample: 定义了视频帧sample的结构体，包含四个字段:
    - $def: struct, 表示这是一个结构体类型
    - $params: 定义了形参，在这里即class domain
    - $fields: 结构体类所包含的属性，具体包括:
        - frame_id：视频帧序号，类型为UniqueID，如有多个层级包含UniqueID，可指定参数id_type，比如UniqueID[id_type='frame']
        - media_path：视频帧的路径
        - objects：标注信息，为前面的标注框结构体构成的一个列表
- VideoFrame：定义了一个视频sample的结构体，包含四个字段
    - $def: struct, 表示这是一个结构体类型
    - $params: 定义了形参，在这里即class domain
    - $fields: 结构体类所包含的属性，具体包括:
        - video_name：视频的名称（一般是文件夹名字）
        - videoframes：为前面的视频帧sample构成的一个列表
除了这些必需字段以外，用户还可以参考“主流数据集调研”中的特殊字段和其他字段，新增对结构体的属性定义。

## 3. 完整示例

根据上述调研和总结，我们制定了[目标跟踪任务模板](#table-2)，用户在进行数据集转换或者新构建数据集时可以直接使用模板。以下将以具体示例，介绍如何定义新数据集、以及如何参考模板用DSDL对已有数据集进行描述。

<a id="table-3"></a>

### 3.1 定义新的DSDL数据集

在定义一个新的目标跟踪数据集时，可以直接导入模板对数据集进行描述。

**train.yaml**

```yaml
$dsdl-version: "0.5.2"

$import:
    - object-tracking
    - class-dom

meta:
  dataset_name: "New_dataset"
  sub_dataset_name: "train"
  task_name: "single-object tracking" 

data:
    sample-type: VideoFrame[cdom=New_dataset_classdom]
    sample-path: $local
    samples:
        - video_name: "example_video_1"
          videoframes:
                - frame_id: "1"
                  media_path: "train/example_video_1/00001.jpg"
                  objects:
                      - instance_id: "0"
                        bbox: [25, 36, 103, 122]
                        category: "dog"
                      - instance_id: "1"
                        ...
                - frame_id: "2"
                  ...
        - video_name: "example_video_2"
          ...
```

上面的描述文件中，首先定义了dsdl的版本信息，然后import了之前定义的数据集模板文件，包括任务模板和类别域模板。接着用meta和data字段来描述自己的数据集，具体的字段说明如下所示：

- $dsdl-version: dsdl版本信息
- $import: 模板导入信息，这里导入[目标跟踪任务模板](#table-2)和数据集的class domain
- meta: 主要展示数据集的一些元信息，比如数据集名称，任务类型等等，用户可以自己添加想要备注的其它信息
- data: data的内容就是按照前面定义好的结构所保存的样本信息，具体如下：
    - sample-type: 数据的类型定义，在这里用的是从[目标跟踪任务模板](#table-2)中导入的VideoFrame类，同时指定了采用的cdom为New_dataset_classdom
    - sample-path: samples的存放路径，如果实际是一个路径，则samples的内容从该文件读取，如果是$local，则从本文件的data.samples字段中直接读取
    - samples：保存数据集的样本信息，其组织结构与[目标跟踪任务模板](#table-2)中定义的struct结构一致，注意只有在sample-path是$local的时候该字段才会生效，否则samples会优先从sample-path中的路径去读取



**class-dom.yaml**

```
$dsdl-version: 0.5.2

New_dataset_classdom:
  $def: class_domain
  classes:
      - dog
      - cat
```

用户可以自定义类别域中包含的类型，在该示例中，数据集包含"dog"和"cat"两个类别，其标号分别是1和2。


另外，用户也可根据自己的需求，自行修改[目标跟踪任务模板](#table-2)，添加相应字段。可以参考[主流数据集调研](#table-1)中的一些常用的独立字段（比如absence、visilibility等）。


### 3.2 用DSDL对已有数据集进行描述

我们以TrackingNet数据集为例，展示目标跟踪数据集DSDL描述文件具体内容。

TrackingNet是一个单目标跟踪数据集，其目录结构如下：

```plaintext
dataset_root                    # 数据集中包含了TEST，TRAIN_0，TRAIN_1，...，TRAIN_11，一共13个目录，代表了一个测试集和12个训练子集
├── TEST                        # 每个目录中都包含了 anno 和 frames两个子目录
│   ├── anno                    # anno中放了若干个 .txt 文件，
│   │   ├── 0-6LB4FqxoE_0.txt   # 每个 .txt 文件都标注了一段视频，被标注的视频与该 .txt 文件名称相同，存储在frames目录当中
│   │   ├── 07Ysk1C0ZX0_0.txt
│   │   └── ...
│   └── frames                  # frames中放了若干个子目录，每个子目录代表一段视频，存储了该视频的每一帧图像
│       ├── 0-6LB4FqxoE_0
│       │   ├── 0.jpg           # 每帧图像的命名形如：0.jpg，1.jpg
│       │   ├── 1.jpg
│       │   └── ...
│       ├── 07Ysk1C0ZX0_0
│       │   └── ...
│       └── ...
├── TRAIN_0                     # 训练集，目录结构与TEST类似
│   ├── anno
│   │   └── ...
│   └── frames
│       └── ...
├── TRAIN_1
│   └── ...
└── ...

```

每个视频都有一个相应的txt文件来储存标注信息，具体格式如下：

```plaintext
308.00, 1.00,173.00,275.00
307.97, 1.10,172.60,274.92
307.94, 1.20,172.20,274.84
307.91, 1.30,171.80,274.76
309.12, 1.00,171.88,275.48
309.40, 1.00,171.60,275.60
309.68, 1.00,171.32,275.72
306.27,-1.16,173.20,280.16
309.22,-1.04,172.80,280.04
315.11,-2.00,173.48,282.08
313.81,-3.50,175.60,285.20
314.45,-2.08,173.84,282.48
314.49,-1.86,173.28,282.16
314.53,-1.64,172.72,281.84
...

```

每一行对应每一帧中目标的矩形框的[x,y,w,h]。



通过分析原始数据集的标注信息，我们可以利用DSDL对其进行描述和数据集格式转换。其转换后的目录将如下所示：

```
TrackingNet-dsdl/
├── defs/  
│  ├── object-tracking.yaml        # struct定义文件
│  └── TrackingNetClassDom.yaml    # TrackingNet数据集的类别域(默认类别)
├── set-train/                     # 训练集
│  ├── train.yaml                  # 训练的yaml文件
│  └── train_samples.json          # 训练集sample的json文件 
└── set-test/                      # 测试集
   ├── test.yaml
   └── test_samples.json 
```



其中，struct定义文件可以参考[目标跟踪任务模板](#table-2)，并根据实际情况对字段进行增删，本示例中的模板及字段对应关系如下：

**object-tracking.yaml**

```yaml
$dsdl-version: "0.5.0"

LocalObjectEntry:  
    $def: struct   
    $params: ["cdom"]
    $fields: 
        instance_id: InstanceID
        bbox: BBox
        category: Label[dom=$cdom]

FrameSample:
    $def: struct
    $params: ["cdom"]
    $fields:
        frame_id: UniqueID
        media_path: Image
        _image_shape: ImageShape
        objects: List[etype=LocalObjectEntry[cdom=$cdom]]

VideoFrame:
    $def: struct
    $params: ["cdom"]
    $fields:
        video_name: Str
        _folder: Str
        videoframes: List[etype=FrameSample[cdom=$cdom]]
```

**字段含义解释及对应关系：**

（以下划线开头的字段是[目标跟踪任务模板](#table-2)中没有包含的字段）

- 在LocalObjectEntry中：
    - bbox：对应原数据集txt标注文件中的标注框坐标，即[x,y,w,h]
- 在ObjectTrackingSample中：
    - frame_id：视频帧序号，类型为UniqueID，这里对应的是原数据集的视频帧文件名，比如“0.jpg"对应的frame_id为“0”。
    - media_path：该字段是我们自适应的字段，用于储存图像的相对路径，主要从原始数据集的filename字段转化而来
    - _image_shape：图片的宽高信息，格式为[height, width]，TrackingNet中并没有直接提供图片宽高属性，但是为了方便odl工具的筛选等操作，建议添加该字段
    - objects：该字段对应原始数据集的object字段，以List的形式存储具体bounding box的标注信息
- 在VideoFrame中：
    - video_name：视频的名称（对应frames下的子目录文件名）
    - _folder: 主要是标识视频来自于哪个文件夹，因为训练集一共分了12个文件夹，模板中没有该字段，为新增字段
    - videoframes：以列表的形式存储了视频的每一帧的信息

值得注意的是，由于该数据集没有类别信息，因此其实可以不需要category字段和类别域文件，另外，因为是单目标跟踪，instance_id字段也可以省略。但为了保证示例的完整性，在此皆保留，供用户参考。


类别域的文件示例如下所示，由于TrackingNet没有类别标注，在这里用默认类别"object"作为单一类别信息。

**class-dom.yaml**

```yaml
$dsdl-version: 0.5.2
TrackingNetClassDom:
  $def: class_domain
  classes:
      - object
```


在[定义新的DSDL数据集](#table-3)的示例中，我们已经了解了如何从yaml文件读取样本具体标注信息，在该示例中将展示如何从外部读取样本具体标注信息。

**train.yaml**

```yaml
$dsdl-version: "0.5.2"

$import:
    - ../defs/object-tracking
    - ../defs/class-dom

meta:
  dataset_name: "TrackingNet"
  creator: "King Abdullah University of Science and Technology"
  home-page: "https://tracking-net.org/"  
  opendatalab-page: "https://opendatalab.com/TrackingNet"
  sub_dataset_name: "train"
  task_name: "single-object tracking" 

data:
    sample-type: VideoFrame[cdom=TrackingNetClassDom]
    sample-path: train_samples.json
```

上面的描述文件中，首先定义了dsdl的版本信息，然后import了之前定义的数据集模板文件，包括任务模板和类别域模板。接着用meta和data字段来描述自己的数据集，具体的字段说明如下所示：

- $dsdl-version: dsdl版本信息
- $import: 模板导入信息，这里导入检测任务模板和TrackingNet的class domain
- meta: 主要展示数据集的一些元信息，比如数据集名称，创建者等等，用户可以自己添加想要备注的其它信息
- data: data的内容就是按照前面定义好的结构所保存的样本信息，具体如下：
    - sample-type: 数据的类型定义，在这里用的是从目标跟踪任务模板中导入的VideoFrame类，同时指定了采用的cdom为TrackingNetClassDom
    - sample-path: samples的存放路径，这里给了实际的json文件路径，因此samples的内容将从该文件读取

**train_samples.json**

train_samples.json需要我们写脚本从原始数据集转换来，注意，里面的字段需要和之前定义的struct对应，最终样式如下：

```
{"samples": [
    {
        "video_name": "0-6LB4FqxoE_0",
        "_folder": "TRAIN_0",
        "videoframes": [
            {
                "frame_id": “0”,
                "media_path": "TRAIN_0/frames/0-6LB4FqxoE_0/0.jpg",
                "_image_shape": [360, 480],
                "objects": [
                    {
                        "instance_id": 000000000001,
                        "bbox": [120.24, 0.32, 359.76, 596.04], 
                        "category": 1  
                    }, 
                    ...
                 ]
            },
            ...
        ]
     },
     ...  
]}
```

我们后续将提供多个已完成DSDL标准化转换的数据集下载链接，敬请期待。