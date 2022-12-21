
# 计算机视觉-目标检测任务

本教程将使用`PASCAL VOC 2007`检测数据集为例，演示数据处理及模型训练全流程。


## **1. 数据集下载**

```
odl-cli get PascalVOC2007-detection
```

出现如下日志，说明数据集已经下载完成。

```
saving to {your home path}/.dsdl/datasets/PascalVOC2007-detection
preparing...
start download...
Download |██████████████████████████████████████████████████| 100.0%, Eta 0 seconds
Download Complete
register local dataset...
```

如果想了解数据集具体结构，可以切换到下载路径进行查看：

原始数据集目录结构如下：
<details>
<summary>voc数据集原始目录结构</summary>
```
VOC2007/                      # 原始数据集文件夹
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
</details>

对应的DSDL标准化文件的目录结构如下：   

<details>
<summary>dsdl-voc目录结构</summary>
```
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
</details>
PS: 如想了解DSDL，可查看[DSDL教程](../dsdl_language/overview.zh.md)进行学习。


## **2. 数据集准备**

在下载好数据集之后，需要对数据集进行一定的配置和检验，方便后续使用dsdl配套的工具链。
<font color='red'>
考虑将config.py和.dsdl整合过渡，临时两个都使用

- config的目的：原始媒体数据、dsdl标注结果分离，即便用户把不同数据存在不同的存储上，也无需修改dsdl yaml文件，仅需修改对应的config文件即可

- 当前方案：    
    + odl-cli在.dsdl/dsdl.json中配置数据集存储信息    
    + 训练和使用dsdl数据集时，目前使用config.py配置数据集存储信息  

odl-cli工具目前是直接将【原始媒体数据】和【dsdl标注文件】同时下载，所以下载的storage路径可以自动生成。  
但需考虑几个额外情况：  
（1）没有odl-cli，用户应该也可以使用dsdl数据集，例如用户在ceph上已经有原始的VOC2007数据集，没有必要额外下载，用户要在s1/s2集群上训练，只需要在s1/s2集群上下载dsdl文件即可。  
（2）odl-cli下载的数据只有【dsdl标注】文件，媒体数据已经存储在其他  
</font>


### **2.1 数据集配置**

在dsdl中为了数据集方便分发，我们提出了【媒体数据】和【标注文件】分离这一设计理念，这样即便用户把不同数据保存在不同的存储上，也无需修改dsdl yaml文件，仅需修改对应的config文件即可，这里的数据集配置也主要是指对config文件的适配，结合实际情况，有以下两种情况：

1. 在默认情况下，用户通过odl-cli获取的dsdl数据集，同时包含【原始媒体数据】和【dsdl标注文件】，此时配置文件已经根据odl-cli的配置自动生成，用户不需要手动修改；
2. 对于本地或者远端已经拥有下载好的【原始媒体数据】，同时还希望使用dsdl相关配套工具的用户，可以只下载对应数据集的【dsdl标注文件】，同时修改其中的`config.py`文件即可；

在 `config.py`中，列举了所支持的媒体文件读取方式，根据实际情况选择并配置文件路径等信息：

1. 本地读取： `local`中的参数 `working_dir`（本地数据所在的目录）

2. 阿里云OSS读取： `ali_oss`中的参数（阿里云OSS的配置 `access_key_secret`, `endpoint`, `access_key_id`；桶名称 `bucket_name`，数据在桶中的目录 `working_dir`）

完整的config.py文件示例如下：

<details>
<summary>dsdl config 文件示例</summary>

```python
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
```
</details>


### **2.2 数据集检验**（待修改）

<font color='red'>check命令整合到odl-cli中 </font>  

dsdl 支持对数据集进行简单的check，确认可以使用下游的工具链。注意，**检验操作并非必须，我们建议用户针对自己生成的dsdl数据集采用check命令进行检验**。

check 命令如下所示：

```shell
dsdl check -y {path_to_yaml_file} -c {path_to_config.py} -l local -t detection -o ./
```
部分参数的含义如下：

    -l 为指定位置，可以选择使用 ali-oss 或 local
    -t 为指定当前yaml的任务类别，当前支持的任务类别有（detection，segmentation，classification）
    -o 为输出的文件夹，包含图片和md文档

check的结果保存在输出文件夹下的log/output.md中。

### **2.3 数据集分析**

odl-cli支持多种数据集分析指令，这里主要给一下info和select的使用案例

- **info** 查看数据集meta信息即部分统计信息

```
odl-cli info PascalVOC2007-detection
```

meta信息：

```
# dataset info
+--------------+--------------------------------------------------------------------------------------------------------------------------------------+
| Authors      | Mark Everingham (Leeds) · Luc van Gool (Zurich) · Chris Williams (Edinburgh) · John Winn (MSR Cambridge) · Andrew Zisserman (Oxford) |
+--------------+--------------------------------------------------------------------------------------------------------------------------------------+
| Dataset Name | PascalVOC2007-detection                                                                                                              |
+--------------+--------------------------------------------------------------------------------------------------------------------------------------+
| HomePage     | http://host.robots.ox.ac.uk/pascal/VOC/voc2007/index.html                                                                            |
+--------------+--------------------------------------------------------------------------------------------------------------------------------------+
| LICENSE      | N/A                                                                                                                                  |
+--------------+--------------------------------------------------------------------------------------------------------------------------------------+
| Modality     | Images                                                                                                                               |
+--------------+--------------------------------------------------------------------------------------------------------------------------------------+
| Task         | ObjectDetection                                                                                                                      |
+--------------+--------------------------------------------------------------------------------------------------------------------------------------+
```
统计信息（部分）：

<font color='red'> 
Image Nums/Instance Nums增加占比，例如aeroplane中113 --> 113（xx.xx%）
默认字母排序，可以通过 --sort==ascent/descend进行排序展示。
</font>

```
# train split statistics
+-----------------+--------------+-----------------+
| Category Name   | Image Nums   | Instance Nums   |
+=================+==============+=================+
| aeroplane       | 113          | 156             |
+-----------------+--------------+-----------------+
| bicycle         | 122          | 202             |
+-----------------+--------------+-----------------+
| bird            | 182          | 294             |
+-----------------+--------------+-----------------+
| boat            | 87           | 208             |
+-----------------+--------------+-----------------+
| bottle          | 153          | 338             |
...
```

- **select** 对数据集进行筛选  

例如筛选出PascalVOC2007-detection训练集中图像为dog类别的5张图片： 
<font>需要针对select命令进行优化，当前过于复杂</font>

```shell
odl-cli select PascalVOC2007-detection --split train --filter "len(list_filter(objects,x->struct_extract(x,'category')=='dog')) > 0" --limit 5
```
结果如下：
```shell
                                               media                                            objects
0  {'image': 'JPEGImages/000036.jpg', 'image_shap...  [{'bbox': [27, 79, 292, 265], 'category': 'dog...
1  {'image': 'JPEGImages/000078.jpg', 'image_shap...  [{'bbox': [15, 75, 460, 337], 'category': 'dog...
2  {'image': 'JPEGImages/000112.jpg', 'image_shap...  [{'bbox': [70, 174, 207, 154], 'category': 'do...
3  {'image': 'JPEGImages/000140.jpg', 'image_shap...  [{'bbox': [107, 146, 279, 154], 'category': 'd...
4  {'image': 'JPEGImages/000171.jpg', 'image_shap...  [{'bbox': [1, 290, 127, 117], 'category': 'dog...

```

更多指令欢迎参考odl-cli[官网教程]().

## **3. 模型训练和推理**

这里使用mmdetection框架进行模型的训练和推理，并默认用户已经安装好了mmdetection框架，如果尚未安装的用户可以参考mmdetection的官网进行安装，目前mmlab2.0(对应mmdet 3.x版本)已经支持DSDL数据集，这里介绍如果安装3.x版本的mmdet，更多信息以及相关的依赖安装请参考[MMDetection安装文档](https://mmdetection.readthedocs.io/zh_CN/3.x/get_started.html).

```shell
git clone https://gitlab.shlab.tech/research/dataset_standard/openmmlab-dsdl/mmdetection-dsdl -b dev
cd mmdetection
pip install -v -e .
```

### **3.1 修改配置文件**

mmdet 框架目前支持dsdl数据集的训练，VOC数据集的配置文件为configs/dsdl/voc2007.py，用户只需要修改和dsdl路径相关的几行即可开始训练，比如，如果用户的数据集是通过odl-cli命令获取的，则在默认情况下，数据集应该存放在home目录下的.dsdl/datasets路径下，数据集的结构如下所示：

```shell
PascalVOC2007-detection
├── JPEGImages
├── ...
└── yml
    ├── defs
    ├── set-test
    ├── set-train
    └── set-val
```

则相关的配置可以按如下进行设置：

```python

# dataset settings
dataset_type = 'DSDLDetDataset'
data_root = '{your home path}/.dsdl/datasets/PascalVOC2007-detection'           # 存放数据集的根目录
train_ann = "yml/set-train/train.yaml"                           # 训练的yaml文件
val_ann = "yml/set-val/val.yaml"                                 # 验证集的yaml文件
```

完整的配置文件如下所示，用户也可以根据自身的需求对其它参数进行修改。

<details>
<summary>dsdl-voc完整训练配置</summary>

```python
_base_ = [
    '../_base_/models/faster-rcnn_r50_fpn.py',
    '../_base_/default_runtime.py'
]

# model setting
model = dict(roi_head=dict(bbox_head=dict(num_classes=20)))

# dataset settings
dataset_type = "DSDLDetDataset"
data_root = "/nvme/wufan/.dsdl/datasets/PascalVOC2007-detection"
train_ann = "yml/set-train/train.yaml"
val_ann = "yml/set-test/test.yaml"

attribute_cfg = dict(
    ignore_train= {
        "difficult": (True, 1)
    }
)

file_client_args = dict(backend='disk')

train_pipeline = [
    dict(type='LoadImageFromFile', file_client_args=file_client_args),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', scale=(1000, 600), keep_ratio=True),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PackDetInputs')
]
test_pipeline = [
    dict(type='LoadImageFromFile', file_client_args=file_client_args),
    dict(type='Resize', scale=(1000, 600), keep_ratio=True),
    # avoid bboxes being resized
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape', 'scale_factor', 'instances')
        )
]
train_dataloader = dict(
    batch_size=2,
    num_workers=2,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    batch_sampler=dict(type='AspectRatioBatchSampler'),
    dataset=dict(
        type=dataset_type,
        attribute_cfg=attribute_cfg,
        data_root=data_root,
        ann_file=train_ann,
        filter_cfg=dict(filter_empty_gt=True, min_size=32, bbox_min_size=32),
        pipeline=train_pipeline)
)

val_dataloader = dict(
    batch_size=1,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        attribute_cfg=attribute_cfg,
        data_root=data_root,
        ann_file=val_ann,
        test_mode=True,
        pipeline=test_pipeline))
test_dataloader = val_dataloader

# Pascal VOC2007 uses `11points` as default evaluate mode, while PASCAL
# VOC2012 defaults to use 'area'.
# val_evaluator = dict(type='VOCMetric', metric='mAP', eval_mode='11points')
val_evaluator = dict(type='CocoMetric', metric='bbox')
test_evaluator = val_evaluator

# training schedule, voc dataset is repeated 3 times, in
# `_base_/datasets/voc0712.py`, so the actual epoch = 4 * 3 = 12
max_epochs = 4
train_cfg = dict(
    type='EpochBasedTrainLoop', max_epochs=max_epochs, val_interval=1)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')

# learning rate
param_scheduler = [
    dict(
        type='MultiStepLR',
        begin=0,
        end=max_epochs,
        by_epoch=True,
        milestones=[3],
        gamma=0.1)
]

# optimizer
optim_wrapper = dict(
    type='OptimWrapper',
    optimizer=dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0001))

# Default setting for scaling LR automatically
#   - `enable` means enable scaling LR automatically
#       or not by default.
#   - `base_batch_size` = (8 GPUs) x (2 samples per GPU).
auto_scale_lr = dict(enable=False, base_batch_size=16)

gpu_ids = range(0, 8)

```

</details>



### **3.2 模型训练**

- 单卡训练

```shell
python tools/train.py {path_to_config_file}
```

- 集群训练

```shell
./tools/slurm_train.sh {partition} {job_name} {config_file} {work_dir} {gpu_nums}
```

当出现如下日志时，表示训练正在进行中：

```shell
2022/12/13 19:00:05 - mmengine - INFO - Checkpoints will be saved to /nvme/wufan/project/mmlab2.x/work_dirs/voc_dsdl.
2022/12/13 19:00:12 - mmengine - INFO - Epoch(train) [1][  50/3104]  lr: 1.0000e-02  eta: 0:26:28  time: 0.1285  data_time: 0.0040  memory: 2581  loss: 0.7176  loss_rpn_cls: 0.1582  loss_rpn_bbox: 0.0301  loss_cls: 0.3771  acc: 92.1875  loss_bbox: 0.1522
2022/12/13 19:00:18 - mmengine - INFO - Epoch(train) [1][ 100/3104]  lr: 1.0000e-02  eta: 0:25:32  time: 0.1204  data_time: 0.0024  memory: 2581  loss: 0.5537  loss_rpn_cls: 0.0577  loss_rpn_bbox: 0.0220  loss_cls: 0.2768  acc: 87.8906  loss_bbox: 0.1972
2022/12/13 19:00:24 - mmengine - INFO - Epoch(train) [1][ 150/3104]  lr: 1.0000e-02  eta: 0:25:12  time: 0.1210  data_time: 0.0025  memory: 2581  loss: 0.6777  loss_rpn_cls: 0.0885  loss_rpn_bbox: 0.0340  loss_cls: 0.3201  acc: 92.6758  loss_bbox: 0.2350
...
```
### **3.3 模型推理**

```shell
python tools/test.py {path_to_config_file} {path_to_checkpoint_file}
```

推理结果如下：

```shell
2022/12/21 11:07:13 - mmengine - INFO - Load checkpoint from work_dirs/voc2007/epoch_4.pth
2022/12/21 11:07:15 - mmengine - INFO - Epoch(test) [  50/4952]    eta: 0:02:17  time: 0.0280  data_time: 0.0028  memory: 348
... 
2022/12/21 11:09:15 - mmengine - INFO - Epoch(test) [4950/4952]    eta: 0:00:00  time: 0.0246  data_time: 0.0009  memory: 360  
2022/12/21 11:09:15 - mmengine - INFO - Converting ground truth to coco format...
2022/12/21 11:09:16 - mmengine - INFO - Evaluating bbox...
2022/12/21 11:09:25 - mmengine - INFO - bbox_mAP_copypaste: 0.454 0.757 0.479 0.123 0.340 0.536
2022/12/21 11:09:25 - mmengine - INFO - Epoch(test) [4952/4952]  coco/bbox_mAP: 0.4540  coco/bbox_mAP_50: 0.7570  coco/bbox_mAP_75: 0.4790  coco/bbox_mAP_s: 0.1230  coco/bbox_mAP_m: 0.3400  coco/bbox_mAP_l: 0.5360
```
## **4. 结果可视化**（待补充）


## **附录. DSDL文件解释**

DSDL数据集包含以下几个重要的文件：

- struct的定义文件（在这个例子里文件名为object-detection-def.yaml）：这个文件主要是对struct做一个明确的定义，可以有sample的结构体和标注的结构体等，需指明包含了哪些field，每个field的类型。

- 类别域（在这个例子为VOCClassDom.yaml）：里面包含了类别列表，对应category的序号（从1开始排序）

- samples文件（在这个例子里分别分为train.yaml和train_samples.json)

    - train.yaml主要是指明引用哪个struct模板和类别域文件，并且指明数据类型和存放路径，另外还有一些meta信息

    - train_samples.json里保存了实际的samples信息，其组织结构必须和之前定义的结构体匹配

### object-detection-def.yaml

这个文件主要是定义struct的yaml文件，里面的字段名称可以根据原始数据集进行一个修改和适应（尽量保留原始数据集的字段名称和结构），但是字段类型一定要使用可识别的数据类型（可识别的数据类型详见[官方文档](https://opendatalab.github.io/dsdl-docs/zh/lang/basic_types/)）

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

（没有提到的字段都是与原数据集同名对应的字段，另外，命名中以下划线开头的一般都是我们自适应的字段，即原数据集没有的字段）

- 在ObjectDetectionSample中：

    - media：该字段为保存的媒体文件的信息，类型为定义的struct：ImageMedia

    - objects：该字段对应原始数据集的object字段，以List的形式存储具体bounding box的标注信息

- 在ImageMedia中：

    - image：用于储存图像的相对路径，主要从原始数据集的filename字段转化而来

    - source：对应原始数据集的source字段，为一个字典形式，里面的keys分别对应原始数据集里的source字段下的database、annotation、image、flickerid字段。

    - owner：对应原始数据集的owner字段，为一个字典形式，里面的keys分别对应原始数据集里的owner字段下的flickerid和name字段。

    - image_shape、depth：对应原始数据集的size字段

- 在LocalObjectEntry中：

    - bbox：对应原数据集的bndbox字段，但转化为bbox标准，即[x,y,w,h]

    - category：是该目标的类别对应的类别标号，对应的是原数据集的name字段，类别标号可以参见下面的VOCClassDom.yaml

    - pose，truncated，difficult：这个标注框的一些属性

### class-dom.yaml

这是一个类别定义的Dom文档。

```YAML
$dsdl-version: "0.5.0"

VOCClassDom:
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

### train.yaml

这个文档引用了之前定义的两个文档，并且指引了具体的sample路径（test.yaml和val.yaml类似，只是修改对应sample-path和sub_dataset_name字段）

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

### train_samples.json

train_samples.json需要我们写脚本从原始数据集转换来，注意，里面的字段需要和之前定义的struct对应，最终样式如下：

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
