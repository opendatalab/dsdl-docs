# 目标跟踪任务

我们通过对目标跟踪任务进行调研，并总结数据集描述中的字段信息，从而制定出目标跟踪任务DSDL模板，供大家参考使用。

## 1. 任务调研

### 1.1 任务定义

目标跟踪任务是指在图像中用矩形框的形式检测出物体的位置，并识别出具体的实例，通过一个特殊识别ID对其进行跟踪。分为单目标跟踪和多目标跟踪，有的数据集还会对每个实例的类别进行标注。其示意图如下所示：

| ![img](https://user-images.githubusercontent.com/113978928/209530768-6649565a-bfb3-4fe3-8180-c2cbbafea34f.png) | ![img](https://user-images.githubusercontent.com/113978928/209531549-33aa66ce-0d9e-488e-81fc-d9ba60f3bdbc.png) |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| ![img](https://user-images.githubusercontent.com/113978928/209530832-6df11287-08bb-4b8a-9583-382f3ffc6890.png) | ![img](https://user-images.githubusercontent.com/113978928/209530837-ba9b8648-78c0-42d8-87d6-aeccb2abfa28.png) |

    图1 上面两张图像来自于MOT17，下面两张图像来自于GOT-10k

### 1.2 评价指标

最常用的就是两个：精确度和成功率（比如TrackingNet、UAV123、Nfs、OTB2015、LaSOT、TLP）。

* **成功率（Success Rate/IOU Rate/AOS）**

成功值（ **success** ）计算是计算预测框与Ground Truth的真值框的区域内像素的交并比。成功率（ **Success Rate** ）即在success一定阈值之下，成功个数的比例。由于阈值不同，成功率也会相应变化，因此就有了成功率曲线（ **Success rate plot** ）。通常我们会看到论文中有一个 **AUC** （Area under curve）分数，这个分数实际上计算的是成功率曲线下的面积，达成的效果就相当于考虑到了**不同阈值下**的成功率分数。有的论文也会直接指定阈值（如0.5）。其实当成功率曲线足够光滑，取0.5对应的成功率分数和计算成功率的AUC分数是一样的（中值定理）。

* **精确度**（**Precision）**

精确度是追踪成功的个数比例，计算预测框中心点与Ground Truth框的中心点的欧氏距离，通常阈值为20像素，即它们的欧氏距离在20像素之内就视为追踪成功。

* **归一化精确度（Normalized Precision）**

考虑到Ground Truth框的尺度大小，将*Precision* 进行归一化，得到 *Norm. Prec* 。即判断预测框与Ground Truth框中心点的欧氏距离与Ground Truth框斜边的比例。最终用于检测tracker的是归一化精度曲线取值在[0, 0.5] 之间的AUC（Area under curve）。

### 1.3 主流数据集调研

我们对10个目标检测数据集进行调研，对相关数据集描述文件（主要是标注字段）进行分析汇总，相同含义的标注字段会以统一命名进行展示，汇总信息如下表所示：

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
      <td width="8%" align="center">Y</td>
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
      <td>物体编号，同一物体在整个视频片段中具有唯一的编号</td>
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

可以看到，如果要描述一个检测数据集的样本，instance id、bbox、media_path和frame id是最基础的字段，此外还包含了各种描述边界框信息的特殊字段。

## 2. 模板展示

目标跟踪任务是目标检测任务的拓展，也包含嵌套结构体（其详细定义可以参考[DSDL入门文档-语言定义-嵌套结构体](http://research.pages.shlab.tech/dataset_standard/dsdl-docs/zh/lang/structs/#242)）和类别域（class domain，或者cdom，具体可以参考[DSDL入门文档-语言定义-类别域](https://opendatalab.github.io/dsdl-docs/zh/lang/basic_types/#223-label)），但与之不同的是：根据上述的调研结果，我们知道对于目标跟踪任务重要的属性包括frame_id、media_path、instance_id、bbox和category，而这些属性分别属于 **三个层级的结构体** ，第一层是视频，第二层是视频帧（即图片），第三层是标注。因此我们需要定义三层的嵌套结构体，用来详细描述每个样本的信息。

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
        frame_id: Int
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

* $dsdl-version: 描述了该文件对应的dsdl版本
* LocalObjectEntry: 定义了标注框的描述方式的嵌套结构体，包含四个字段:
  * $def: struct, 表示这是一个结构体类型
  * $params: 定义了形参，在这里即class domain
  * $fields: 结构体类所包含的属性，具体包括:
    * instance_id：物体编号，同一物体在整个视频片段中具有唯一的编号
    * bbox：标注框信息，转化为bbox标准，即[x,y,w,h]
    * category：标注框类别，与ClassDom对应
* FrameSample: 定义了视频帧sample的结构体，包含四个字段:
  * $def: struct, 表示这是一个结构体类型
  * $params: 定义了形参，在这里即class domain
  * $fields: 结构体类所包含的属性，具体包括:
    * frame_id：视频帧序号
    * media_path：视频帧的路径
    * objects：标注信息，为前面的标注框结构体构成的一个列表
* VideoFrame：定义了一个视频sample的结构体，包含四个字段
  * $def: struct, 表示这是一个结构体类型
  * $params: 定义了形参，在这里即class domain
  * $fields: 结构体类所包含的属性，具体包括:
    * video_name：视频的名称（一般是文件夹名字）
    * videoframes：为前面的视频帧sample构成的一个列表
* 除了这些必需字段以外，用户还可以参考“主流数据集调研”中的特殊字段和其他字段，新增对结构体的属性定义。

## 3. 完整示例

我们以TrackingNet数据集为例，展示目标跟踪数据集DSDL描述文件具体内容。

目录结果将如下所示：

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

### 3.1 数据集定义文件

**object-tracking.yaml**

```yaml
$dsdl-version: "0.5.2"

LocalObjectEntry:  
    $def: struct
    $params: ["cdom"]   
    $fields:  
        _bbox: BBox
        _instance_id: InstanceID
        _category: Label[dom=cdom]

ObjectTrackingSample:
    $def: struct
    $params: ["cdom"]
    $fields:
        frame_id: Int
        _media_path: Image
        _image_shape: ImageShape
        _objects: List[LocalObjectEntry[cdom=cdom]]

VideoFrame:
    $def: struct
    $params: ["cdom"]
    $fields:
        _video_name: Str
        _folder: Str
        _videoframes: List[ObjectTrackingSample[cdom=cdom]]
```

**字段含义解释及对应关系：**

（没有提到的字段都是与原数据集同名对应的字段，另外，命名中以下划线开头的一般都是我们自适应的字段，即原数据集没有的字段）

* 在LocalObjectEntry中：
  * _bbox：对应原数据集的bndbox字段，但转化为bbox标准，即[x,y,w,h]
* 在ObjectTrackingSample中：
  * frame_id：帧号
  * _media_path：该字段是我们自适应的字段，用于储存图像的相对路径，主要从原始数据集的filename字段转化而来
  * _image_shape：图片的宽高
  * _objects：该字段对应原始数据集的object字段，以List的形式存储具体bounding box的标注信息
* 在VideoFrame中：
  * _video_name：视频的名称（对应frames下的子目录文件名）
  * _folder: 主要是标识视频来自于哪个文件夹，因为训练集一共分了12个文件夹
  * _videoframes：以列表的形式存储了视频的每一帧的信息

值得注意的是，由于该数据集没有类别信息，因此其实可以不需要category字段，另外，因为是单目标跟踪，instance_id字段也可以省略。

**class-dom.yaml**

```yaml
$dsdl-version: 0.5.2
TrackingNetClassDom:
  $def: class_domain
  classes:
      - object
```

### 3.2 samples相关文件

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

上面的描述文件中，首先定义了dsdl的版本信息，然后import了之前定义的数据集模板文件，包括任务模板，由于该数据集没有类别信息，因此不需要制定和import类别域模板。接着用meta和data字段来描述自己的数据集，具体的字段说明如下所示：

- $dsdl-version: dsdl版本信息
- $import: 模板导入信息，这里导入检测任务模板和VOC的class domain，也就是[2. 模板展示](#table-2)中展示的两部分内容
- meta: 主要展示数据集的一些元信息，比如数据集名称，创建者等等，用户可以自己添加想要备注的其它信息
- data: data的内容就是按照前面定义好的结构所保存的样本信息，具体如下：
  - sample-type: 数据的类型定义，在这里用的是从检测任务模板中导入的ObjectDetectionSample类，同时指定了采用的cdom为VOCClassDom
  - sample-path: samples的存放路径，如果实际是一个路径，则samples的内容从该文件读取，如果是$local（这个例子），则从本文件的data.samples字段中直接读取

**train_samples.json**

其中train_samples.json需要我们写脚本从原始数据集转换来，注意，里面的字段需要和之前定义的struct对应，最终样式如下：

```
{"samples": [
    {
        "_video_name": "0-6LB4FqxoE_0",
        "_folder": "TRAIN_0",
        "_videoframes": [
            {
                "frame_id": 0,
                "_media_path": "TRAIN_0/frames/0-6LB4FqxoE_0/0.jpg",
                "_image_shape": [360, 480],
                "_objects": [
                    {
                        "_instance_id": 000000000001,
                        "_bbox": [120.24, 0.32, 359.76, 596.04], 
                        "_category": 1  
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
