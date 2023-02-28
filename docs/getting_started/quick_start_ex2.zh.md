# 计算机视觉-目标检测任务

本教程将使用 `PASCAL VOC 2007`检测数据集为例，演示数据处理及模型训练全流程。

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
注: DSDL文件目录下各个文件的具体内容和解释可参考该教程的附录部分。

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

### 2.1 数据集配置

在dsdl中为了数据集方便分发，我们提出了【媒体数据】和【标注文件】分离这一设计理念，这样即便用户把不同数据保存在不同的存储上，也无需修改dsdl yaml文件，仅需修改对应的config文件即可，这里的数据集配置也主要是指对config文件的适配，结合实际情况，有以下两种情况：

1. 在默认情况下，用户通过odl-cli获取的dsdl数据集，同时包含【原始媒体数据】和【dsdl标注文件】，此时配置文件已经根据odl-cli的配置自动生成，用户不需要手动修改；
2. 对于本地或者远端已经拥有下载好的【原始媒体数据】，同时还希望使用dsdl相关配套工具的用户，可以只下载对应数据集的【dsdl标注文件】，同时修改其中的 config.py文件即可；

在 config.py中，列举了所支持的媒体文件读取方式，根据实际情况选择并配置文件路径等信息：

1. 本地读取： local中的参数 working_dir（本地数据所在的目录）
2. 阿里云OSS读取： ali_oss中的参数（阿里云OSS的配置 access_key_secret, endpoint, access_key_id；桶名称 bucket_name，数据在桶中的目录 working_dir）

完整的config.py文件示例如下：

### 2.2 数据集分析

odl-cli支持多种数据集分析指令，这里主要给一下info和select的使用案例

- info 查看数据集meta信息即部分统计信息

meta信息：

统计信息（部分）：

- select 对数据集进行筛选

例如筛选出PascalVOC2007-detection训练集中图像为dog类别的5张图片：
<font color='red'>需要针对select命令进行优化，当前过于复杂 </font>

结果如下：

更多指令欢迎参考odl-cli官网教程.

## 3. 模型训练和推理

这里使用mmdetection框架进行模型的训练和推理，并默认用户已经安装好了mmdetection框架，如果尚未安装的用户可以参考mmdetection的官网进行安装，目前mmlab2.0(对应mmdet 3.x版本)已经支持DSDL数据集，这里介绍如果安装3.x版本的mmdet，更多信息以及相关的依赖安装请参考MMDetection安装文档.

### 3.1 修改配置文件

mmdet 框架目前支持dsdl数据集的训练，VOC数据集的配置文件为configs/dsdl/voc2007.py，用户只需要修改和dsdl路径相关的几行即可开始训练，比如，如果用户的数据集是通过odl-cli命令获取的，则在默认情况下，数据集应该存放在home目录下的.dsdl/datasets路径下，数据集的结构如下所示：

则相关的配置可以按如下进行设置：

完整的配置文件如下所示，用户也可以根据自身的需求对其它参数进行修改。

### 3.2 模型训练

- 单卡训练

比如：

- 集群训练

比如：

当出现如下日志时，表示训练正在进行中：

### 3.3 模型推理

比如：

推理结果如下：

## 4. 结果可视化（待补充）

## 附录. DSDL文件解释

注：该小节将对本教程的DSDL目录下的文件进行详细内容的解释，如用户希望了解更多DSDL的数据类型和模块，可查看[DSDL教程](../dsdl_language/overview.zh.md)进行学习。

DSDL数据集包含以下几个重要的文件：

- struct的定义文件（在这个例子里文件名为object-detection-def.yaml）：这个文件主要是对struct做一个明确的定义，可以有sample的结构体和标注的结构体等，需指明包含了哪些field，每个field的类型。
- 类别域（在这个例子为VOCClassDom.yaml）：里面包含了类别列表，对应category的序号（从1开始排序）
- samples文件（在这个例子里分别分为train.yaml和train_samples.json)

  - train.yaml主要是指明引用哪个struct模板和类别域文件，并且指明数据类型和存放路径，另外还有一些meta信息
  - train_samples.json里保存了实际的samples信息，其组织结构必须和之前定义的结构体匹配

### object-detection-def.yaml

这个文件主要是定义struct的yaml文件，里面的字段名称可以根据原始数据集进行一个修改和适应（尽量保留原始数据集的字段名称和结构），但是字段类型一定要使用可识别的数据类型（可识别的数据类型详见官方文档）

字段含义解释及对应关系：

（没有提到的字段都是与原数据集同名对应的字段，另外，命名中以下划线开头的一般都是我们自适应的字段，即原数据集没有的字段）

在ObjectDetectionSample中：

- media：该字段为保存的媒体文件的信息，类型为定义的struct：ImageMedia
- objects：该字段对应原始数据集的object字段，以List的形式存储具体bounding box的标注信息

在ImageMedia中：

- image：用于储存图像的相对路径，主要从原始数据集的filename字段转化而来
- source：对应原始数据集的source字段，为一个字典形式，里面的keys分别对应原始数据集里的source字段下的database、annotation、image、flickerid字段。
- owner：对应原始数据集的owner字段，为一个字典形式，里面的keys分别对应原始数据集里的owner字段下的flickerid和name字段。
- image_shape、depth：对应原始数据集的size字段

在LocalObjectEntry中：

- bbox：对应原数据集的bndbox字段，但转化为bbox标准，即[x,y,w,h]
- category：是该目标的类别对应的类别标号，对应的是原数据集的name字段，类别标号可以参见下面的VOCClassDom.yaml
- pose，truncated，difficult：这个标注框的一些属性

### class-dom.yaml

这是一个类别定义的Dom文档。

### train.yaml

这个文档引用了之前定义的两个文档，并且指引了具体的sample路径（test.yaml和val.yaml类似，只是修改对应sample-path和sub_dataset_name字段）

### train_samples.json

train_samples.json需要我们写脚本从原始数据集转换来，注意，里面的字段需要和之前定义的struct对应，最终样式如下：

注意，"samples"字段是必须的（不可改名），且组织形式也不能改变，即：必须是字典形式，字典有一个键为"samples"，其值为一个列表，列表的每个对象都是一个sample类的实例（即本案例中的ObjectDetectionSample类）。
