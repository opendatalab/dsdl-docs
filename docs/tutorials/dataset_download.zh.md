# 数据集下载

OpenDataLab官网收集了海量公开数据集，对于大部分数据集用户可以在该网站直接下载，与此同时，我们针对主流CV数据集都提供了DSDL规范标注，基于原始公开数据集**媒体文件**和**DSDL****标注文件**，用户可以方便地进行模型训练、推理，并且可以使用配套的工具编辑的对数据进行分析、处理。

根据（1）是否提供原始数据集下载；（2）是否提供DSDL标注下载，我们将数据集下载分为四类情形进行讨论。

## 1. 同时提供原始数据集媒体文件和DSDL标注文件

在原始数据集允许分发，且DSDL标注文件已支持的情况下，用户可以同时下载到原始数据集媒体文件和DSDL标注文件。

CLI命令如下：

```
odl-cli get <dataset_name>
```

注意这里的dataset_name需要与[OpenDataLab官网](https://opendatalab.com/)上的名字对应。用户可在官网搜索相关数据集，并在数据集详情页面的CLI部分获取到数据集名称，比如：

```
odl-cli get CIFAR-10
```

下载到的数据集目录如下：

```
<root-path>/
├── original-dataset/             # 原始数据集的路径
│   ├── ...
└── dsdl-dataset/
    ├── defs/  
    │  ├── task-def.yaml          # 任务类型的struct定义文件
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
    ├── tools/                    # 如果不需要其他脚本支持，该文件夹为空
    │  ├── converter.py           # 中间格式转换脚本(比如二进制转中间格式，分割图转标准格式)
    │  └── prepare.sh             # 包括解压和调用converter.py来转中间格式
    ├── config.py                 # 数据集读取路径等config文件
    └── README.md                 # 数据集教程：下载、怎么使用、配置文件的教程。
```

其中，defs文件夹和set-xxx文件夹是DSDL数据集的定义文件、类别域文件和数据文件等，config.py文件里包含原始数据集的绝对路径（详细信息可以参阅[自定义DSDL数据集](./advanced/dsdl_define.md)）。而tools文件下主要是数据集准备过程所需的脚本，详细使用方法见每个数据集的README.md文档。

在此案例中，config文件的内容为（其中的 `<root-path>`需要用户自行修改）：

```
local = dict(
    type="LocalFileReader",
    working_dir="<root-path>/original-dataset",
)
```

## 2. 仅提供DSDL标注文件

如果原始数据集不允许分发，而DSDL已支持，用户需要自行下载原始数据集。

命令如下：

```
odl-cli get <dataset_name>
```

下载到的数据集将只有dsdl-dataset/文件夹，而不包含original-dataset/文件夹。用户可以自行下载数据集，并通过修改config.py中的路径，来指定原始数据集媒体文件的存放位置。建议与上一小节给的目录格式保持一致，以保证tools文件夹下脚本的正常运行。

## 3. 仅提供原始数据集媒体和标注文件

[OpenDataLab官网](https://opendatalab.com/)上允许分发的数据集，目前尚有部分暂未支持DSDL标准化标注，但是用户仍然可以下载到原始数据集的媒体和标注文件。

命令如下：

```
odl-cli get <dataset_name>
```

下载到的数据集将只有original-dataset/，而不包含dsdl-dataset/文件夹。

用户如果需要自行将其定义为DSDL数据集，以便使用ODL工具链相关功能和OpenMMLab训练，请参阅[自定义DSDL数据集](./advanced/dsdl_define.md)。

## 4. 不提供原始数据集媒体文件和DSDL标注文件

如果当前数据集在[OpenDataLab官网](https://opendatalab.com/)上暂不提供下载，且尚未支持DSDL标准化标注，用户需自行到数据集官网进行原始数据集媒体文件和标注文件下载。

另外，用户如果需要自行将其定义为DSDL数据集，以便使用ODL工具链相关功能和OpenMMLab训练，请参阅[自定义DSDL数据集](./advanced/dsdl_define.md)。
