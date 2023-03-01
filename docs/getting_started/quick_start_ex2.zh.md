# 计算机视觉-目标检测任务

本教程将使用 `PASCAL VOC 2007`检测数据集为例，演示数据处理及模型训练全流程。

## **1. 数据集下载**

```
odl get PASCAL_VOC2007
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

注: DSDL文件目录下各个文件的具体内容和解释可参考[高阶教程](../tutorials/advanced/dsdl_define.md)。

## **2. 数据集准备**

在下载好数据集之后，需要对数据集进行一定的配置和检验，方便后续使用dsdl配套的工具链。

### **2.1 数据集配置**

在dsdl中为了数据集方便分发，我们提出了【媒体数据】和【标注文件】分离这一设计理念，这样即便用户把不同数据保存在不同的存储上，也无需修改dsdl yaml文件，仅需修改对应的config文件即可，这里的数据集配置也主要是指对config文件的适配，结合实际情况，有以下两种情况：

1. 在默认情况下，用户通过odl get获取的dsdl数据集，同时包含【原始媒体数据】和【dsdl标注文件】，此时配置文件已经根据odl-cli的配置自动生成，用户不需要手动修改；
2. 对于本地或者远端已经拥有下载好的【原始媒体数据】，同时还希望使用dsdl相关配套工具的用户，可以只下载对应数据集的【dsdl标注文件】，同时修改其中的 `config.py`文件即可；

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

### **2.2 数据集分析(开发中，暂未开放)**

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
`<font color='red'>`需要针对select命令进行优化，当前过于复杂 `</font>`

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

比如：

```
python tools/train.py config/dsdl/voc2007.py
```

- 集群训练

```shell
./tools/slurm_train.sh {partition} {job_name} {config_file} {work_dir} {gpu_nums}
```

比如：

```bash
bash tools/slurm_train.sh bigdata_s2 test_job config/dsdl/voc2007.py work_dir/voc2007 8
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

比如：

```
python tools/test.py config/dsdl/voc2007.py work_dirs/voc2007/epoch_4.pth
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

目前可以参考[数据集可视化](../tutorials/visualization.md)部分，对数据集样本进行简单的可视化。
