# DSDL数据集定义

定义一个DSDL数据集，首先需要了解DSDL如何描述一个数据集，详细的内容可以阅读“DSDL语言教程”章节。

本小节主要用一个具体案例（VOC2007，目标检测)，讲解DSDL数据集的定义。

将分为以下几个步骤：

* 原数据集调研（包括数据目录结构、标注字段及含义等）
* DSDL模板制定

## 原始数据集调研

首先需要调研原始数据集的文件结构：

```plaintext
VOC2007/
├── Annotations/              # 里面存放的是每张图片打完标签所对应的XML文件
│  ├── 000001.xml             # 某张图片的标注信息
│  └── ...
├── ImageSets/                # 图片划分的txt存放位置
│  ├── Layout                 # 包含Layout标注信息的图像文件名列表
│  │  ├── test.txt 
│  │  ├── train.txt 
│  │  ├── trainval.txt 
│  │  └── val.txt 
│  ├── Main                   # 包含所有文件的列表和划分
│  │  ├── aeroplane_test.txt  # 按每个类别的训练集、测试集等划分
│  │  ├── aeroplane_train.txt 
│  │  ├── ...
│  │  ├── test.txt            # 全数据集的test划分
│  │  ├── train.txt           # 全数据集的train划分
│  │  ├── trainval.txt 
│  │  └── val.txt 
│  ├── Segmentation           # 包含语义分割信息图像文件的列表和划分
│  │  ├── test.txt 
│  │  ├── train.txt 
│  │  ├── trainval.txt 
│  │  └── val.txt 
├── JPEGImages/               # 存放的是训练与测试的所有图片
│  ├── 000001.jpg             # 图片（序号作为图片名） 
│  └── ...
├── SegmentationClass/        # 语义分割标注
│  ├── 000032.png             # 某张图片的媒体文件 
│  └── ...
└── SegmentationObject/       # 实例分割标注
   ├── 000032.png             # 某张图片的媒体文件 
   └── ...
```

这里只以检测任务为例生成模板，因此只需要Annotations/、JPEGImages/这两个文件夹，另外，训练测试集划分，需要用ImageSets/Main/train.txt、val.txt、test.txt这三个文件。

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

这里以ImageSets/Main/train.txt为例展示一下数据集segment划分的文件内容：

```plaintext
000012         # 图片名前缀
000017
000023
000026
...
```

## DSDL模板制定

最终需要转成的DSDL数据集格式，将包含以下几个重要的文件：

* struct的定义文件（在这个例子里文件名为object-detetction.yaml）：这个文件主要是对struct做一个明确的定义，可以有sample的结构体和标注的结构体等，需指明包含了哪些field，每个field的类型。
* 类别域（在这个例子为VOC2007ClassDom.yaml）：里面包含了类别列表，对应category的序号（从1开始排序）
* samples文件（在这个例子里分别分为train.yaml和train_samples.json)
  * train.yaml主要是指明引用哪个struct模板和类别域文件，并且指明数据类型和存放路径，另外还有一些meta信息
  * train_samples.json里保存了实际的samples信息，其组织结构必须和之前定义的结构体匹配
* config.py：用于指定媒体文件存放位置，在数据集验证的时候将会详细解释

后文会对目录结构以及每一个文件的内容进行一个详细展示和解释。

数据集目录如下：

```Plain
dsdl-voc2007/
├── defs/                    
│  ├── object-detection-def.yaml              # 任务类型的定义
│  └── class-dom.yaml                         # 数据集的类别域
├── set-train/                                # 训练集
│  ├── train.yaml                             # 训练的yaml文件
│  └── train_samples.json                     # 训练集sample的json文件
├── set-val/                                  # 验证集
│  ├── val.yaml
│  └── val_samples.json    
├── set-test/                                 # 测试集
│  ├── test.yaml
│  └── test_samples.json  
├── config.py                                 # 数据集读取路径等config文件
└── README.md                                 # 数据集简介
```

### struct的定义文件

object-detection-def.yaml：这个文件主要是定义struct的yaml文件，里面的字段名称可以根据原始数据集进行一个修改和适应（尽量保留原始数据集的字段名称和结构），但是字段类型一定要使用可识别的数据类型（可识别的数据类型详见“DSDL语言教程”章节）

```YAML
$dsdl-version: "0.5.0"

ImageMedia:
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
* category：是该目标的类别对应的类别标号，对应的是原数据集的name字段，类别标号可以参见下面的VOC2007ClassDom.yaml
* pose，truncated，difficult：标注框的属性，来自于原数据集同名字段

### 类别域

class-dom.yaml：这是一个类别定义的Dom文档

```YAML
$dsdl-version: "0.5.0"

VOCClassDom:
    $def: class_domain
    classes:
        - aeroplane                   # 对应_category为1
        - bicycle                     # 对应_category为2，以此类推
        - bird
        - boat
        - bottle
        - bus
        - car
        - cat
        - chair
        - cow
        - diningtable
        - dog
        - horse
        - motorbike
        - person
        - pottedplant
        - sheep
        - sofa
        - train
        - tvmonitor
```

如果存在标签父类的情况，详细可以见“DSDL语言教程”下的“类别域”部分。

### samples文件

train.yaml：这个文档引用了之前定义的两个文档，并且指引了具体的sample路径（test.yaml和val.yaml类似，只是修改对应sample-path和sub_dataset_name字段）

```YAML
$dsdl-version: "0.5.0"

$import:
    - ../defs/class-domain
    - ../defs/object-detection-def

meta:
   dataset_name: "VOC2007"
   sub_dataset_name: "train"
   task_type: "SemanticSementation"
   dataset_homepage: "http://host.robots.ox.ac.uk/pascal/VOC/voc2007/index.html"
   dataset_publisher: "University of Leeds | ETHZ, Zurich | University of Edinburgh |Microsoft Research Cambridge | University of Oxford"
   OpenDataLab_address: "https://opendatalab.com/PASCAL_VOC2007/download"

data:
    sample-type: ObjectDetectionSample[cdom=VOCClassDom]
    sample-path: train_samples.json
```

train_samples.json需要我们写脚本从原始数据集转换来（转换脚本将在下一小节“数据集转换”中详述）。注意，里面的字段需要和之前定义的struct对应。最终样式如下：

```JSON
{"samples": [
    {
         "media": {
                "_media_path": "JPEGImages/000001.jpg",
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
            "image_shape": [640, 480]
            "depth": 3,
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

### config.py

配置文件为图片文件的位置信息，目前支持本地和oss，具体格式如下：

```Python
local = dict(
    type="LocalFileReader",
    working_dir="path to origin dataset root path",
)

ali_oss = dict(
    type="AliOSSFileReader",
    access_key_secret="your secret key of aliyun oss",
    endpoint="your endpoint of aliyun oss",
    access_key_id="your access key of aliyun oss",
    bucket_name="your bucket name of aliyun oss",
    working_dir="the relative path of your media dir in the bucket")
```

用户需要对应修改其中的values。
