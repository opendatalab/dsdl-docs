# 基于DSDL数据的训练推理（OpenMMLab）

## **1. 安装环境**
这里使用mmdetection框架进行模型的训练和推理，用户可以参考mmdetection的官网进行安装，目前mmlab2.0(对应mmdet 3.x版本)已经支持DSDL数据集，这里介绍如何安装3.x版本的mmdet，更多信息以及相关的依赖安装请参考[MMDetection安装文档](https://mmdetection.readthedocs.io/zh_CN/3.x/get_started.html).

```shell
git clone https://gitlab.shlab.tech/research/dataset_standard/openmmlab-dsdl/mmdetection-dsdl -b dev-3.x
cd mmdetection
pip install -v -e .
```

安装完mmdetection后，我们可以将数据集下载到mmdetection/data路径下，这里以VOC数据集为例，下载好后的数据集路径如下所示：

```
mmdetection
└── data                          
    └── VOC07-det
        ├── dsdl
        │   ├── config.py
        │   ├── defs
        │   ├── README.md
        │   ├── set-test
        │   ├── set-train
        │   └── set-val
        └── original
            ├── Annotations
            ├── ImageSets
            ├── JPEGImages
            ├── SegmentationClass
            └── SegmentationObject
```

## **2. 修改配置文件**

mmdet 框架目前支持dsdl数据集的训练，一般只需要对数据集的根目录进行修改即可进行训练。如果是voc，coco等主流数据集，且数据集保存在mmdetection/data路径下，则可以直接使用官网的配置进行训练；如果并非主流数据集，或者数据集没有保存在data路径下，也只需要对配置文件中的路径进行修改即可：

```python

# dataset settings
dataset_type = 'DSDLDetDataset'
data_root = '{path to your dataset}'                                             # 存放数据集的根目录
train_ann = "dsdl/set-train/train.yaml"                                          # 训练的yaml文件
val_ann = "dsdl/set-val/val.yaml"                                                # 验证集的yaml文件
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

## **3 模型训练**

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

当出现如下日志时，表示训练正在进行中：

```shell
2022/12/13 19:00:05 - mmengine - INFO - Checkpoints will be saved to /nvme/wufan/project/mmlab2.x/work_dirs/voc_dsdl.
2022/12/13 19:00:12 - mmengine - INFO - Epoch(train) [1][  50/3104]  lr: 1.0000e-02  eta: 0:26:28  time: 0.1285  data_time: 0.0040  memory: 2581  loss: 0.7176  loss_rpn_cls: 0.1582  loss_rpn_bbox: 0.0301  loss_cls: 0.3771  acc: 92.1875  loss_bbox: 0.1522
2022/12/13 19:00:18 - mmengine - INFO - Epoch(train) [1][ 100/3104]  lr: 1.0000e-02  eta: 0:25:32  time: 0.1204  data_time: 0.0024  memory: 2581  loss: 0.5537  loss_rpn_cls: 0.0577  loss_rpn_bbox: 0.0220  loss_cls: 0.2768  acc: 87.8906  loss_bbox: 0.1972
2022/12/13 19:00:24 - mmengine - INFO - Epoch(train) [1][ 150/3104]  lr: 1.0000e-02  eta: 0:25:12  time: 0.1210  data_time: 0.0025  memory: 2581  loss: 0.6777  loss_rpn_cls: 0.0885  loss_rpn_bbox: 0.0340  loss_cls: 0.3201  acc: 92.6758  loss_bbox: 0.2350
...
```

## **4 模型测试**

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
