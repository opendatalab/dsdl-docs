# 快速入门

该文档将以一个数据集为例（这里暂时以VOC2007为例），跑通整个DSDL流程。


## 数据集下载

```
dsdl get opendatalab/VOC2017
```

这里将对DSDL标注进行下载，下载后文件目录如下：

```
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

如果对原始数据集进行同步下载，其文件目录如下：

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


## 数据集解析

（这一步后续好像已经没有了，暂时按照github上的内容保留，后续可删除）

### 解析器反序列化Yaml文件为Python代码

```shell
dsdl parse --yaml demo/coco_demo.yaml
```

### 配置文件修改，设置读取路径

创建配置文件 `config.py`，内容如下（目前只支持读取阿里云OSS数据与本地数据）：

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

在 `config.py`中，列举了所有支持的媒体文件读取方式，根据实际情况选择并配置文件路径等信息：

1. 本地读取： `local`中的参数 `working_dir`（本地数据所在的目录）
2. 阿里云OSS读取： `ali_oss`中的参数（阿里云OSS的配置 `access_key_secret`, `endpoint`, `access_key_id`；桶名称 `bucket_name`，数据在桶中的目录 `working_dir`）

## 数据集可视化

可视化功能展示

```shell
dsdl view -y <yaml-name>.yaml -c <config.py> -l ali-oss -n 10 -r -v -f Label BBox Attributes
```

每个参数的意义为：

| 参数简写 | 参数全写        | 参数解释                                                                                                                                                         |
| -------- | --------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -y       | `--yaml`      | 定义所有samples的yaml文件的路径                                                                                                                                  |
| -c       | `--config`    | 配置文件（`config.py`）的路径                                                                                                                                  |
| -l       | `--location`  | 只可以指定为 `local`或是 `ali-oss`，分别表示读取本地的数据与读取阿里云的数据                                                                                 |
| -n       | `--num`       | 加载数据集的样本数量                                                                                                                                             |
| -r       | `--random`    | 在加载数据集中的样本时是否随机选取样本，如果不指定的话就按顺序从开始选取样本                                                                                     |
| -v       | `--visualize` | 是否将加载的数据进行可视化展示                                                                                                                                   |
| -f       | `--field`     | 选择需要进行可视化的字段，如 `-f BBox`表示可视化bbox，`-f Attributes`表示对样本的attributes进行可视化等等，可以同时选择多个，如 `-f Label BBox Attributes` |
| -t       | `--task`      | 可以选择当前需要可视化的任务类型，如果选择 `-t detection`，则等价于 `-f Label BBox Polygon Attributes`                                                       |


## 数据集分析

1. 调用方法：

   ```Python
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
2. 报告样式：

  报告分为3个部分：

- parser检查结果：结果包括了parse结果是否成功，如果不成功，则可以查看具体的报错信息

* samples实例化检查结果：其中报告说明了当前数据集共有样本个数，正常样本个数，警告样本个数，错误样本个数，并提供了异常样本的具体信息日志。
* 可视化结果：需要肉眼观察可视化结果是否正确，比如bbox位置是否正确，标签内容是否正确等，在图片下面展示了可视化过程中的日志内容，比如是可视化成功还是失败，以及失败日志等。


## 数据集训练

与OpenMMDetection的对接训练。

### 修改config文件

**faster_rcnn_r101_fpn_voc2007_dsdl_format.py**

```Python
model = dict(
    type='FasterRCNN',
    backbone=dict(
        type='ResNet',
        depth=101,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=1,
        norm_cfg=dict(type='BN', requires_grad=True),
        norm_eval=True,
        style='pytorch',
        init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet101')),
    neck=dict(
        type='FPN',
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        num_outs=5),
    rpn_head=dict(
        type='RPNHead',
        in_channels=256,
        feat_channels=256,
        anchor_generator=dict(
            type='AnchorGenerator',
            scales=[8],
            ratios=[0.5, 1.0, 2.0],
            strides=[4, 8, 16, 32, 64]),
        bbox_coder=dict(
            type='DeltaXYWHBBoxCoder',
            target_means=[0.0, 0.0, 0.0, 0.0],
            target_stds=[1.0, 1.0, 1.0, 1.0]),
        loss_cls=dict(
            type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0),
        loss_bbox=dict(type='L1Loss', loss_weight=1.0)),
    roi_head=dict(
        type='StandardRoIHead',
        bbox_roi_extractor=dict(
            type='SingleRoIExtractor',
            roi_layer=dict(type='RoIAlign', output_size=7, sampling_ratio=0),
            out_channels=256,
            featmap_strides=[4, 8, 16, 32]),
        bbox_head=dict(
            type='Shared2FCBBoxHead',
            in_channels=256,
            fc_out_channels=1024,
            roi_feat_size=7,
            num_classes=20,
            bbox_coder=dict(
                type='DeltaXYWHBBoxCoder',
                target_means=[0.0, 0.0, 0.0, 0.0],
                target_stds=[0.1, 0.1, 0.2, 0.2]),
            reg_class_agnostic=False,
            loss_cls=dict(
                type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
            loss_bbox=dict(type='L1Loss', loss_weight=1.0))),
    train_cfg=dict(
        rpn=dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.7,
                neg_iou_thr=0.3,
                min_pos_iou=0.3,
                match_low_quality=True,
                ignore_iof_thr=-1),
            sampler=dict(
                type='RandomSampler',
                num=256,
                pos_fraction=0.5,
                neg_pos_ub=-1,
                add_gt_as_proposals=False),
            allowed_border=-1,
            pos_weight=-1,
            debug=False),
        rpn_proposal=dict(
            nms_pre=2000,
            max_per_img=1000,
            nms=dict(type='nms', iou_threshold=0.7),
            min_bbox_size=0),
        rcnn=dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.5,
                neg_iou_thr=0.5,
                min_pos_iou=0.5,
                match_low_quality=False,
                ignore_iof_thr=-1),
            sampler=dict(
                type='RandomSampler',
                num=512,
                pos_fraction=0.25,
                neg_pos_ub=-1,
                add_gt_as_proposals=True),
            pos_weight=-1,
            debug=False)),
    test_cfg=dict(
        rpn=dict(
            nms_pre=1000,
            max_per_img=1000,
            nms=dict(type='nms', iou_threshold=0.7),
            min_bbox_size=0),
        rcnn=dict(
            score_thr=0.05,
            nms=dict(type='nms', iou_threshold=0.5),
            max_per_img=100)))

checkpoint_config = dict(interval=1)
file_client_args = dict(backend='petrel')
log_config = dict(interval=50, hooks=[dict(type='TextLoggerHook')])
custom_hooks = [dict(type='NumClassCheckHook')]
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = None
resume_from = None
workflow = [('train', 1)]
opencv_num_threads = 0
mp_start_method = 'fork'
auto_scale_lr = dict(enable=True, base_batch_size=16)
optimizer = dict(type='SGD', lr=0.02, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=None)
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=0.001,
    step=[8, 11])
runner = dict(type='EpochBasedRunner', max_epochs=12)
num_classes = 20
dataset_type = 'DSDLDetectionDataset'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
# 修改data_root为s3路径
train_pipeline = [
    dict(type='LoadImageFromDSDL', file_client_args=file_client_args, data_root='s3://open_dataset_original/PASCALVOC2007/public_datalist_17/VOCdevkit/VOC2007/'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', img_scale=(1333, 800), keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(
        type='Normalize',
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        to_rgb=True),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'])
]
# 修改data_root为s3路径
test_pipeline = [
    dict(type='LoadImageFromDSDL', file_client_args=file_client_args, data_root='s3://open_dataset_original/PASCALVOC2007/public_datalist_17/VOCdevkit/VOC2007/'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(1333, 800),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(
                type='Normalize',
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_rgb=True),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img'])
        ])
]

# 主要修改这个路径
train_yaml_07 = '/mnt/lustre/ouyanglinke/mmdetection/work_dir/VOC2007_dsdl/train/train.yaml'
val_yaml_07 = '/mnt/lustre/ouyanglinke/mmdetection/work_dir/VOC2007_dsdl/val/val.yaml'
test_yaml = '/mnt/lustre/ouyanglinke/mmdetection/work_dir/VOC2007_dsdl/test/test.yaml'
ignore_cfg = dict(Continue=dict(), Ignore=dict(difficult=(True, 1)))
dsdl_library_path = "/mnt/lustre/ouyanglinke/mmdetection/work_dir/VOC2007_dsdl/train/"
local = dict(type="LocalFileReader", working_dir="/mnt/lustre/ouyanglinke/mmdetection/work_dir/VOC2007_dsdl/")
data = dict(
    samples_per_gpu=1,
    workers_per_gpu=32,
    train=dict(
            type='DSDLDetectionDataset',
            ann_file=train_yaml_07,
            location_config=local,
            pipeline=train_pipeline,
            dsdl_library_path=dsdl_library_path),
    val=dict(
        type='DSDLDetectionDataset',
        ann_file=val_yaml_07,
        location_config=local,
        pipeline=test_pipeline,
        dsdl_library_path=dsdl_library_path),
    test=dict(
        type='DSDLDetectionDataset',
        ann_file=test_yaml,
        location_config=local,
        pipeline=test_pipeline,
        dsdl_library_path=dsdl_library_path))
evaluation = dict(interval=1, metric='mAP')
gpu_ids = [0]
work_dir = './work_dirs/voc_dsdl_test'
auto_resume = False
```

### 开始训练

打开terminal运行：

```Shell
conda activate openmmlab    # 安装了dsdl和mmdetection的conda环境
srun -p bigdata_s2 --quotatype=auto --gres=gpu:1 python tools/train.py configs/dsdl_detection/faster_rcnn_r101_fpn_voc2007_dsdl_format.py 
```

最终结果精度：AP50: 0.6680, mAP: 0.6680


## 补充内容

### DSDL文件解释

DSDL数据集包含以下几个重要的文件：

* struct的定义文件（在这个例子里文件名为object-detetction.yaml）：这个文件主要是对struct做一个明确的定义，可以有sample的结构体和标注的结构体等，需指明包含了哪些field，每个field的类型。
* 类别域（在这个例子为VOC2007ClassDom.yaml）：里面包含了类别列表，对应category的序号（从1开始排序）
* samples文件（在这个例子里分别分为train.yaml和train_samples.json)

  * train.yaml主要是指明引用哪个struct模板和类别域文件，并且指明数据类型和存放路径，另外还有一些meta信息
  * train_samples.json里保存了实际的samples信息，其组织结构必须和之前定义的结构体匹配

#### object-detection.yaml

这个文件主要是定义struct的yaml文件，里面的字段名称可以根据原始数据集进行一个修改和适应（尽量保留原始数据集的字段名称和结构），但是字段类型一定要使用可识别的数据类型（可识别的数据类型详见：https://opendatalab.github.io/dsdl-docs/zh/lang/basic_types/）

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

* 在ObjectDetectionSample中：

  * media_path：该字段是我们自适应的字段，用于储存图像的相对路径，主要从原始数据集的filename字段转化而来
  * _objects：该字段对应原始数据集的object字段，以List的形式存储具体bounding box的标注信息
  * source：对应原始数据集的source字段，为一个字典形式，里面的keys分别对应原始数据集里的source字段下的database、annotation、image、flickerid字段
  * owner：对应原始数据集的owner字段，为一个字典形式，里面的keys分别对应原始数据集里的owner字段下的flickerid和name字段
  * width、height、depth：是原始数据集的size字段下的
* 在LocalObjectEntry中：

  * _bbox：对应原数据集的bndbox字段，但转化为bbox标准，即[x,y,w,h]
  * _category：是该目标的类别对应的类别标号，对应的是原数据集的name字段，类别标号可以参见下面的VOC2007ClassDom.yaml

#### VOC2007ClassDom.yaml

这是一个类别定义的Dom文档。

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

#### train.yaml

这个文档引用了之前定义的两个文档，并且指引了具体的sample路径（test.yaml和val.yaml类似，只是修改对应sample-path和sub_dataset_name字段）

```YAML
$dsdl-version: "0.5.0"

$import:
    - VOC2007ClassDom
    - object-detection

meta:
  dataset_name: "VOC2007"
  sub_dataset_name: "train"

data:
    sample-type: ObjectDetectionSample[cdom=VOC2007ClassDom]
    sample-path: train_samples.json
```

#### train_samples.json

train_samples.json需要我们写脚本从原始数据集转换来，注意，里面的字段需要和之前定义的struct对应，最终样式如下：

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
