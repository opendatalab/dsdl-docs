# **DSDL数据集验证**

**<font color='red'>check命令整合到odl-cli中 </font>**

DSDL支持对数据集进行简单的check，并生成检测报告。DSDL check将检查模板定义的规范性，并对模板与实际标注数据的匹配关系进行检查，同时可对媒体文件和标注进行可视化，供用户检查可视化结果。通过DSDL check后的DSDL数据集才可保证使用下游的工具链。

check 命令如下所示：

```shell
dsdl check -y {path_to_yaml_file} -c {path_to_config.py} -l local -p {path_to_defs} -t detection -o ./
```

部分参数的含义如下：

    -y 为需检查的模板定义文件
    -c 为指定媒体文件存放位置的config文件（可指定ali-oss路径和local路径）
    -l 为指定位置，可以选择使用 ali-oss 或 local，与config文件对应
    -p 如果在模板定义文件内部的import没有使用相对路径，需要指定import的根目录
    -t 为指定当前yaml的任务类别，当前支持的任务类别有（detection，segmentation，classification）
    -o 为指定输出的文件夹，包含图片和md文档，check的结果保存在输出文件夹下的log/output.md中

## 实际案例

假设DSDL数据集和原始数据集的目录结构如下，用户需要分别对train.yaml、val.yaml和test.yaml进行验证：

```
root-path/
├── original-dataset/            # 原始数据集的路径
│   ├── ...
└── dsdl-dataset/
    ├── defs/                  
    │  ├── detction-def.yaml      # 任务类型的struct定义文件,task为检测任务
    │  └── class-dom.yaml         # 数据集的类别域
    ├── set-train/                # 训练集
    │  ├── train.yaml             # 训练的yaml文件
    │  └── train_samples.json     # 训练集sample的json文件
    ├── set-val/                  # 验证集
    │  ├── val.yaml
    │  └── val_samples.json  
    ├── set-test/                 # 测试集
    │  ├── test.yaml
    │  └── test_samples.json
    └── config.py                 # 数据集读取路径等config文件
```

config.py文件的内容为：

```
local = dict(
    type="LocalFileReader",
    working_dir="root-path/original-dataset",
)
```

check命令如下：

```
dsdl check -y set-train/train.yaml -c config.py -l local -t detection -p defs/ -o ./
```

其中，如果train.yaml中的import部分写了相对路径的话（如下），可以省略-p参数：

```yaml
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

## 验证结果

### 报告样式：

  报告分为3个部分：

- parser检查结果：结果包括了parse结果是否成功，如果不成功，则可以查看具体的报错信息

* samples实例化检查结果：其中报告说明了当前数据集共有样本个数，正常样本个数，警告样本个数，错误样本个数，并提供了异常样本的具体信息日志。
* 可视化结果：需要肉眼观察可视化结果是否正确，比如bbox位置是否正确，标签内容是否正确等，在图片下面展示了可视化过程中的日志内容，比如是可视化成功还是失败，以及失败日志等。

### 报错信息解读：

**（这一块需要怡颖将出现各个报错的触发条件写一下）**
