# 实例演示- 目标检测

该教程介绍了如何将一个目标检测数据集转换为DSDL格式，这里以VOC为例做一个介绍。主要包含以下几个步骤：

- 数据集调研
- DSDL模板制定
- 数据集转换
- 数据集验证

# 数据集调研

调研需要包含以下内容：

- 原始数据集文件结构
- 原始数据集标注的原始字段及其含义

## 原始数据集文件结构

```Bash
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

我们这里只以检测任务为例生成模板，因此只需要Annotations/、JPEGImages/这两个文件夹，另外，训练测试集划分，需要用ImageSets/Main/train.txt、val.txt、test.txt这三个文件。

## 原始数据集标注的原始字段及其含义

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

```Plain
000012         # 图片名前缀
000017
000023
000026
...
```

# DSDL模板制定

## Yaml格式解释

最终需要转成的yaml数据集格式，在这里做一个详细解释。转成后的DSDL数据集包含以下几个重要的文件：

- struct的定义文件（在这个例子里文件名为object-detetction.yaml）：这个文件主要是对struct做一个明确的定义，可以有sample的结构体和标注的结构体等，需指明包含了哪些field，每个field的类型。
- 类别域（在这个例子为VOC2007ClassDom.yaml）：里面包含了类别列表，对应category的序号（从1开始排序）
- samples文件（在这个例子里分别分为train.yaml和train_samples.json)

  - train.yaml主要是指明引用哪个struct模板和类别域文件，并且指明数据类型和存放路径，另外还有一些meta信息
  - train_samples.json里保存了实际的samples信息，其组织结构必须和之前定义的结构体匹配

后边会对目录结构以及每一个文件的内容进行一个详细展示和解释。

## DSDL数据集目录

```Plain
VOC2007-dsdl/
├── doms/                        
│  ├── object-detection.yaml       # struct定义文件
│  └── VOC2007ClassDom.yaml        # VOC数据集的类别域
├── train/                         # 训练集
│  ├── train.yaml                  # 训练的yaml文件
│  └── train_samples.json          # 训练集sample的json文件
├── val/                           # 验证集
│  ├── val.yaml
│  └── val_samples.json        
└── test/                          # 测试集
   ├── test.yaml
   └── test_samples.json        
```

## 模板及标注文件

1. object-detection.yaml：这个文件主要是定义struct的yaml文件，里面的字段名称可以根据原始数据集进行一个修改和适应（尽量保留原始数据集的字段名称和结构），但是字段类型一定要使用可识别的数据类型（可识别的数据类型详见：https://opendatalab.github.io/dsdl-docs/zh/lang/basic_types/）

```YAML
$dsdl-version: "0.5.0"

LocalObjectEntry:                                  
    $def: struct                                   
    $params: ["cdom"]
    $fields:                                      
        _bbox: BBox
        _category: Label[dom=$cdom]                                           
        pose: Str    
        truncated: Bool
        difficult: Bool

ObjectDetectionSample:
    $def: struct
    $params: ["cdom"]
    $fields:
        media_path: Image
        folder: Str
        source: Dict
        owner: Dict
        height: Int
        width: Int
        depth: Int
        segmented: Bool
        _objects: List[etype=LocalObjectEntry[cdom=$cdom]]
```

**字段含义解释及对应关系：**

（没有提到的字段都是与原数据集同名对应的字段，另外，命名中以下划线开头的一般都是我们自适应的字段，即原数据集没有的字段）

- 在ObjectDetectionSample中：

  - media_path：该字段是我们自适应的字段，用于储存图像的相对路径，主要从原始数据集的filename字段转化而来
  - _objects：该字段对应原始数据集的object字段，以List的形式存储具体bounding box的标注信息
  - source：对应原始数据集的source字段，为一个字典形式，里面的keys分别对应原始数据集里的source字段下的database、annotation、image、flickerid字段
  - owner：对应原始数据集的owner字段，为一个字典形式，里面的keys分别对应原始数据集里的owner字段下的flickerid和name字段
  - width、height、depth：是原始数据集的size字段下的
- 在LocalObjectEntry中：

  - _bbox：对应原数据集的bndbox字段，但转化为bbox标准，即[x,y,w,h]
  - _category：是该目标的类别对应的类别标号，对应的是原数据集的name字段，类别标号可以参见下面的VOC2007ClassDom.yaml

2. VOC2007ClassDom.yaml：这是一个类别定义的Dom文档

```YAML
$dsdl-version: "0.5.0"

VOC2007ClassDom:
    $def: class_domain
    classes:
        - aeroplane                   # 对应category为1
        - bicycle                     # 对应category为2
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

3. train.yaml：这个文档引用了之前定义的两个文档，并且指引了具体的sample路径（test.yaml和val.yaml类似，只是修改对应sample-path和sub_dataset_name字段）

```YAML
$dsdl-version: "0.5.0"

$import:
    - VOC2007ClassDom
    - object-detection

meta:
  dataset_name: "VOC2007"
  protocol_version: "v0.3rc3"
  sub_dataset_name: "train"

data:
    sample-type: ObjectDetectionSample[cdom=VOC2007ClassDom]
    sample-path: train_samples.json
```

4. 其中train_samples.json需要我们写脚本从原始数据集转换来，注意，里面的字段需要和之前定义的struct对应，最终样式如下：

```JSON
{"samples": [
    {
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
        "height": 640, 
        "width": 480,
        "depth": 3,
        "segmented": 0,
        "_objects": [
            {
                "_bbox": [120.24, 0.32, 359.76, 596.04], 
                "_category": 1, 
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

# 数据集转换

这一节提供了针对之前定义的yaml文件对应生成sample.json文件的转换脚本，这个脚本可以生成训练、测试和验证三个samples.json文件（转换脚本可自行优化）。

需要注意的是，数据集里的每个字段都需要和之前定义的ObjectDetectionSample类对应（无论是字段名，还是其值的类型），不要自行增加或者减少字段。

转换脚本如下：

```Python
#!/usr/bin/env python3
#
# Copyright 2022 Shanghai Artificial Intelligence Laboratory. All rights reserved.
#

"""
This file implements the generator of the VOC2007 DSDL format dataset.
"""
import itertools

import itertools
import yaml
import os
from xml.etree import ElementTree
import json


f = open('train/VOC2007ClassDom.yaml', 'r')
data = yaml.safe_load(f)

category_list = data['VOC2007ClassDom']['classes']
_VOC_CATEGORY_DICT = {_name: (_ind + 1) for _ind, _name in enumerate(category_list)}

root_path = '/home/PJLAB/ouyanglinke/mmdetection-master/data/VOCdevkit/VOC2007'
anno_paths = os.path.join(root_path, "Annotations")
segmentation = ['train', 'val', 'test']
ann_id_gen = itertools.count()
for seg in segmentation:
    seg_path = os.path.join(root_path, 'ImageSets', 'Main', seg + '.txt')
    try:
        with open(seg_path, 'r') as f:
            seg_list = f.readlines()
    except:
        print('The segmentation file {} cannot be open, it will be skipped.'.format(seg_path))
        continue

    samples = []

    for anno_id in seg_list:
        anno_path = os.path.join(root_path, 'Annotations', anno_id.strip() + '.xml')

        try:
            with open(anno_path, 'r') as f:
                anno_tree = ElementTree.parse(f)
        except:
            print('The annotation file {} cannot read, it will be skipped.'.format(anno_path))
            continue

        sample = {
            'media_path': os.path.join('JPEGImages', anno_tree.find('filename').text),
            'folder': '',
            'source': {
                'database': anno_tree.find('source').find('database').text,
                'annotation': anno_tree.find('source').find('annotation').text,
                'flickrid': anno_tree.find('source').find('flickrid').text,
            },
            'owner': {
                'flickrid': anno_tree.find('owner').find('flickrid').text,
                'name': anno_tree.find('owner').find('name').text
            },
            'height': int(anno_tree.find('size').find('height').text),
            'width': int(anno_tree.find('size').find('width').text),
            'depth': int(anno_tree.find('size').find('depth').text),
            'segmented': int(anno_tree.find('segmented').text),
            '_objects': []
        }

        for obj in anno_tree.iter('object'):
            xmin, ymin, xmax, ymax = [float(obj.find('bndbox').find(boxes).text) for boxes in ['xmin', 'ymin', 'xmax', 'ymax']]
            sample['_objects'].append({
                '_bbox': [xmin, ymin, xmax-xmin, ymax-ymin],
                '_category': _VOC_CATEGORY_DICT[obj.find('name').text],
                'pose': obj.find('pose').text,
                'truncated': int(obj.find('truncated').text),
                'difficult': int(obj.find('difficult').text)
            })

        samples.append(sample)

    samples_save = {'samples': samples}
    save_path = os.path.join(seg, seg + '_samples_v2.json')
    with open(save_path, 'w') as f:
        json.dump(samples_save, f)
```

# 数据集验证

我们提供了一个自动验证的方法如下。

```python
dsdl check -y xxx.yaml -c config.py -l ali-oss -t detection -p ./ -o ./

### -y 为输入的yaml文件
### -c 为数据集的读取配置（记录了数据集在阿里云/本地的位置），主要形式如下：
local = dict(
    type="LocalFileReader",
    working_dir="local path of your media",
)

ali_oss = dict(
    type="AliOSSFileReader",
    access_key_secret="your secret key of aliyun oss",
    endpoint="your endpoint of aliyun oss",
    access_key_id="your access key of aliyun oss",
    bucket_name="your bucket name of aliyun oss",
    working_dir="the relative path of your media dir in the bucket")
### -l 为指定位置，可以选择使用 ali-oss 或 local
### -t 为指定当前yaml的任务类别，当前支持的任务类别有（detection，segmentation，classification）
### -p yaml文件导入的库文件所在的路径地址
### -o 为输出的文件夹，包含图片和md文档，注意打包下载
```

最终获得的报告包含以下内容：

- parser检查结果：结果包括了parse结果是否成功，如果不成功，则可以查看具体的报错信息
- samples实例化检查结果：其中报告说明了当前数据集共有样本个数，正常样本个数，警告样本个数，错误样本个数，并提供了异常样本的具体信息日志
- 可视化结果：需要肉眼观察可视化结果是否正确，比如bbox位置是否正确，标签内容是否正确等。在图片下面展示了可视化过程中的日志内容，比如是可视化成功还是失败，以及失败日志等。
