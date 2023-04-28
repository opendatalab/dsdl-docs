# 快速入门

本教程将使用 `PASCAL VOC 2007`检测数据集为例，演示数据处理及模型训练全流程。

## **1. 数据集下载**

```
odl get PASCAL_VOC2007
```

出现如下日志，说明数据集已经下载完成。

```
saving to {your home path}/datasets/PASCAL_VOC2007
preparing...
start download...
Download |██████████████████████████████████████████████████| 100.0%, Eta 0 seconds
Download Complete
register local dataset...
```

下载完成后需要进行解压（解压步骤可以参考教程[数据集准备](../tutorials/dataset_download.md)），解压完成后，原始数据集目录结构如下：

<details>
<summary>voc数据集原始目录结构</summary>
```
original/                     # 原始数据集文件夹
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
dsdl/
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

## **2. 数据集配置**

dsdl采用了【媒体数据】和【标注文件】分离这一设计理念，若用户之前已经下载过相关数据集媒体文件，只需下载dsdl标注文件即可使用该数据集。为了使用下载好的数据集，我们需要修改配置文件`config.py`（位于`PASCAL_VOC2007/dsdl/config.py`）来进行对媒体数据的定位。举例来说，假如下载的`PASCAL_VOC2007`数据集的解压后的媒体文件位于`~/datasets/PASCAL_VOC2007/original`路径下，解压后的DSDL标注文件位于`~/datasets/PASCAL_VOC2007/dsdl/`路径下，则只需要将`~/datasets/PASCAL_VOC2007/dsdl/config.py`中的配置按照如下内容进行修改即可：

```python
local = dict(
    type="LocalFileReader",
    working_dir="~/datasets/PASCAL_VOC2007/original",
)
```

实际上，dsdl也支持从阿里云读取媒体数据，同样也只需要修改`config.py`文件即可，详细内容可以参考[数据集配置教程](../tutorials/config/location_config.md)

## **3. 数据集简单使用**


### **3.1. 数据集初始化**

dsdl将dsdl数据集的使用接口封装进DSDLDataset类，初始化一个DSDLDataset类需要yaml文件和location config，这里仍然假设上面VOC数据集解压后的媒体文件和dsdl标注文件的存放路径分别为`~/datasets/PASCAL_VOC2007/`目录下的`original`和`dsdl`，则初始化代码如下：

```
from dsdl.dataset import DSDLDataset

# 1. 指定要加载数据的dsdl文件
train_yaml = "~/datasets/PASCAL_VOC2007/dsdl/set-train/train.yaml"
val_yaml = "~/datasets/PASCAL_VOC2007/dsdl/set-val/val.yaml"

# 2. 配置数据集路径（支持本地、阿里云oss等主流存储）
loc_config = dict(
    type="LocalFileReader",
    working_dir="~/datasets/PASCAL_VOC2007/original"
)
ds_train = DSDLDataset(dsdl_yaml=train_yaml, location_config=loc_config)
ds_val = DSDLDataset(dsdl_yaml=val_yaml, location_config=loc_config)
```

### **3.2. 获取类别名称**

获取数据集的类别名称列表，代码如下（这里只展示了VOC数据集的前10个标签）：

```
print(ds_val.class_names[0:10])
```
输出如下所示：

```
['aeroplane',
 'bicycle',
 'bird',
 'boat',
 'bottle',
 'bus',
 'car',
 'cat',
 'chair',
 'cow']
```

### **3.3. 获取样本信息**

DSDLDataset使用索引的方式获取样本，如下展示了VOC数据集索引为0的样本的信息：

```
print(ds_val[0])
```
输出的内容如下所示：

```
{'Image': [path:JPEGImages/000005.jpg],
 'Label': [chair, chair, chair, chair, chair],
 'Bbox': [[263.0, 211.0, 324.0, 339.0],
  [165.0, 264.0, 253.0, 372.0],
  [5.0, 244.0, 67.0, 374.0],
  [241.0, 194.0, 295.0, 299.0],
  [277.0, 186.0, 312.0, 220.0]]}
```

在此基础上，也可以获取样本的不同字段，比如要获取图片字段，可以采用如下命令：

```
print(ds_val[0].Image)
```
得到输出如下：

```
[path:JPEGImages/000005.jpg]
```

类似的，要获取所有标注框的类别属性和第一个标注框位置属性，则可以采用下面的语句：
```
print(ds_val[0].Label)
print(ds_val[0].Bbox[0])
```
得到输出分别如下：

```
[chair, chair, chair, chair, chair]

[263.0, 211.0, 324.0, 339.0]
```

## 4. DSDL数据集高阶使用
除了入门教程中提到的功能以外，DSDL的[用户教程](../tutorials/overview.md)中还有一些其他的应用：

* [数据集可视化](../tutorials/visualization.md)
* 模型训练&推理：包含了[OpenMMLab](../tutorials/train_test/openmmlab.md)和[Pytorch](../tutorials/train_test/pytorch.md)
* [高阶教程](../tutorials/advanced/overview.md): 包含了[DSDL数据集模板制定](../tutorials/advanced/dsdl_define.md)、[格式转换](../tutorials/advanced/dsdl_convert.md)和[验证](../tutorials/advanced/dsdl_check.md)的全流程，并且介绍了[自定义DSDL Field](../tutorials/advanced/dsdl_extend.md)的方法
