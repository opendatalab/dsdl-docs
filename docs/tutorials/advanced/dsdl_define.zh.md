# DSDL数据集模板制定

定义一个DSDL数据集，首先需要了解DSDL如何描述一个数据集，详细的内容可以阅读[DSDL语言教程](../../dsdl_language/overview.md)章节。

本章用两个案例解释DSDL数据集的定义：1. 用DSDL描述已有的数据集（VOC为例）；2. 利用任务模板定义一个新的数据集。

该教程将在[数据集转换](./dsdl_convert.md)小节详述如何通过该章定义的模板进行数据集的DSDL标准化转换。

## 1. 用DSDL描述已有的数据集

本小节主要用一个具体案例（VOC2007，目标检测)，讲解DSDL数据集的定义。

将分为以下几个步骤：

* [原数据集调研](#原始数据集调研)：标注字段及含义
* DSDL模板制定：分为[详细版](#详细版DSDL)和[精简版](#精简版DSDL)

<a id="原始数据集调研"></a>

### 1.1 原始数据集调研

标注类型如下（以Annotations/000001.xml为例）：

```XML
<annotation>
   <folder>VOC2007</folder>                         # 文件夹
   <filename>000001.jpg</filename>                  # 图片文件名
   <source>                                         # 图像元信息
      <database>The VOC2007 Database</database>     # 数据集名称
      <annotation>PASCAL VOC2007</annotation>       # 标注类型
      <image>flickr</image>                         # 来源
      <flickrid>341012865</flickrid>                # 来源ID
   </source>
   <owner>                                          # 源信息
      <flickrid>Fried Camels</flickrid>
      <name>Jinky the Fruit Bat</name>
   </owner>
   <size>
      <width>353</width>                            # 图片宽
      <height>500</height>                          # 图片高 
      <depth>3</depth>                              # 图片通道数
   </size>
   <segmented>0</segmented>                         # 是否用于分割
   <object>                                         # 标注部分 
      <name>dog</name>                              # 标签
      <pose>Left</pose>                             # 姿态
      <truncated>1</truncated>                      # 物体是否被部分遮挡（>15%）
      <difficult>0</difficult>                      # 是否为难以辨识的物体
      <bndbox>
         <xmin>48</xmin>                            # 左上角点的x
         <ymin>240</ymin>                           # 左上角点的y
         <xmax>195</xmax>                           # 右下角点的x
         <ymax>371</ymax>                           # 右下角点的y
      </bndbox>
   </object>
   ...
</annotation>
```

<a id="详细版DSDL"></a>

### 1.2 DSDL模板制定（详细版DSDL）

#### 1.2.1 struct的定义文件

根据原始数据集的信息，我们可以制定如下的数据集模板（该模板中保留了原始数据集所有的字段名称和结构），注意，字段类型一定要使用可识别的数据类型，详情可以参考[Field文档](../../api_reference/fields_overview.md)。

```YAML
$dsdl-version: "0.5.0"

ImageMedia:
    $def: struct  
    $fields:
        image: Image 
        image_shape: ImageShape
        depth: Int
        folder: Str
        source: Dict
        owner: Dict
        segmented: Bool
  
LocalObjectEntry:  
    $def: struct   
    $params: ["cdom"]
    $fields:  
        bbox: BBox
        category: Label[dom=$cdom]   
        pose: Str  
        truncated: Bool
        difficult: Bool

ObjectDetectionSample:
    $def: struct
    $params: ["cdom"]
    $fields:
        media: ImageMedia
        objects: List[etype=LocalObjectEntry[cdom=$cdom]] 
```

**字段含义解释及对应关系：**

在ObjectDetectionSample中：

* media：该字段为保存的媒体文件的信息，类型为定义的struct：ImageMedia
* objects：该字段对应原始数据集的object字段，以List的形式存储具体bounding box的标注信息

在ImageMedia中：

* image：用于储存图像的相对路径，主要从原始数据集的filename字段转化而来
* source：对应原始数据集的source字段，为一个字典形式，里面的keys分别对应原始数据集里的source字段下的database、annotation、image、flickerid字段。
* owner：对应原始数据集的owner字段，为一个字典形式，里面的keys分别对应原始数据集里的owner字段下的flickerid和name字段。
* image_shape、depth：是原始数据集的size字段下的同名字段

在LocalObjectEntry中：

* bbox：对应原数据集的bndbox字段，但转化为bbox标准，即[x,y,w,h]
* category：是该目标的类别对应的类别标号，对应的是原数据集的name字段，类别标号可以参见数据集转换页面的[VOC2007ClassDom.yaml](./dsdl_convert.zh.md#VOC2007ClassDom)
* pose，truncated，difficult：标注框的属性，来自于原数据集同名字段

#### 1.2.3 samples文件

根据上一小节制定的模板，最终的samples.json的结构将与其完全对应，具体组织形式如下：

```JSON
{"samples": [
    {
         "media": {
                "image": "JPEGImages/000001.jpg",
                "image_shape": [640, 480],
                "depth": 3,
                "folder": "VOC2007",
                "source": {
                    "database": "The VOC2007 Database", 
                    "annotation": "PASCAL VOC2007",
                    "flickrid": "341012865"
                },
                "owner":{
                    "flickrid": "Fried Camels",
                    "name": "Jinky the Fruit Bat"
            },
            "segmented": 0,
            },
        "objects": [
            {
                "bbox": [120.24, 0.32, 359.76, 596.04], 
                "category": 1, 
                "pose": "Left", 
                "truncated": 1, 
                "difficult": 0   
            }, 
            ...
         ]
    },
    ...
]}
```

注意，"samples"字段是必须的（不可改名），且组织形式也不能改变，即：必须是字典形式，字典有一个键为"samples"，其值为一个列表，列表的每个对象都是一个sample类的实例（即本案例中的ObjectDetectionSample类）。

<a id="精简版DSDL"></a>

### 1.3 DSDL模板制定（精简版DSDL）

除了1.2小节中保留原始数据集所有原始字段的做法，我们还可以利用已有的[任务模板](../../dsdl_template\overview.md)作为数据集模板（该模板中仅保留了该任务的必需字段）。

在[任务模板](../../dsdl_template\overview.md)页面，展示了目前DSDL预先制定的一些主流任务的模板，用户可根据需要使用。

#### 1.3.1 struct的定义文件

在此案例中，我们可以选用[目标检测模板](../../dsdl_template/cv/cv_detection.md)：

```yaml
$dsdl-version: "0.5.0"

LocalObjectEntry:
    $def: struct
    $params: ['cdom']
    $fields:
        bbox: BBox
        label: Label[dom=$cdom]

ObjectDetectionSample:
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        objects: List[LocalObjectEntry[cdom=$cdom]]
```

在检测模板中的一些字段含义如下（详细学习请参考 [DSDL语言教程](../../dsdl_language/overview.zh.md)）

- $dsdl-version: 描述了该文件对应的dsdl版本
- LocalObjectEntry: 定义了边界框的描述方式的嵌套结构体，包含四个字段:
    - $def: struct, 表示这是一个结构体类型
    - $params: 定义了形参，在这里即class domain
    - $fields: 结构体类所包含的属性，具体包括:
        - bbox 边界框的位置
        - label 边界框的类别
- ObjectDetectionSample: 定义了检测任务sample的结构体，包含四个字段:
    - $def: struct, 表示这是一个结构体类型
    - $params: 定义了形参，在这里即class domain
    - $fields: 结构体类所包含的属性，具体包括:
        - image 图片的路径
        - objects 标注信息，检测任务中，为前面的LocalObjectEntry构成的一个列表

#### 1.3.2 samples文件

根据上一小节制定的模板，最终的samples.json的结构将与其完全对应，具体组织形式如下：

```JSON
{"samples": [
    {
        "image": "JPEGImages/000001.jpg",
        "objects": [
            {
                "bbox": [120.24, 0.32, 359.76, 596.04], 
                "label": 1
            }, 
            ...
         ]
    },
    ...
]}
```

注意，"samples"字段是必须的（不可改名），且组织形式也不能改变，即：必须是字典形式，字典有一个键为"samples"，其值为一个列表，列表的每个对象都是一个sample类的实例（即本案例中的ObjectDetectionSample类）。

## 2. 利用任务模板定义一个新的DSDL数据集

我们在[任务模板](../../dsdl_template\overview.zh.md)板块，介绍了目前我们已经制定的一些任务的模板，用户可以根据需要选择所需的模板进行使用。

本小节以目标跟踪数据集为例，解释如何直接导入[目标跟踪模板](../../dsdl_template/cv/cv_object_tracking.md#table-2)对数据集进行描述。

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
- $import: 模板导入信息，这里导入[目标跟踪任务模板](../../dsdl_template/cv/cv_object_tracking.md#table-2)和数据集的class domain
- meta: 主要展示数据集的一些元信息，比如数据集名称，任务类型等等，用户可以自己添加想要备注的其它信息
- data: data的内容就是按照前面定义好的结构所保存的样本信息，具体如下：
    - sample-type: 数据的类型定义，在这里用的是从[目标跟踪任务模板](../../dsdl_template/cv/cv_object_tracking.md#table-2)中导入的VideoFrame类，同时指定了采用的cdom为New_dataset_classdom
    - sample-path: samples的存放路径，如果实际是一个路径，则samples的内容从该文件读取，如果是$local，则从本文件的data.samples字段中直接读取
    - samples：保存数据集的样本信息，其组织结构与[目标跟踪任务模板](../../dsdl_template/cv/cv_object_tracking.md#table-2)中定义的struct结构一致，注意只有在sample-path是$local的时候该字段才会生效，否则samples会优先从sample-path中的路径去读取

**class-dom.yaml**

```yaml
$dsdl-version: 0.5.2

New_dataset_classdom:
  $def: class_domain
  classes:
      - dog
      - cat
```

用户可以自定义类别域中包含的类型，在该示例中，数据集包含"dog"和"cat"两个类别，其标号分别是1和2。

另外，用户也可根据自己的需求，自行修改[目标跟踪任务模板](../../dsdl_template/cv/cv_object_tracking.md#table-2)，添加相应字段。可以参考[主流数据集调研](../../dsdl_template/cv/cv_object_tracking.md#table-1)中的一些常用的独立字段（比如absence、visilibility等）。
