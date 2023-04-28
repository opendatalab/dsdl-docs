# 数据集准备

OpenDataLab官网收集了海量公开数据集，对于大部分数据集用户可以在该网站直接下载，与此同时，我们针对主流CV数据集都提供了DSDL规范标注，基于原始公开数据集**媒体文件**和**DSDL标注文件**，用户可以方便地进行模型训练、推理，并且可以使用配套的工具对数据进行分析、处理。

数据集准备分为以下步骤：

- 数据集下载：可以在OpenDataLab官网进行下载，也可以直接使用odl命令进行下载。具体请参考[数据集下载](#数据集下载)部分。
- 数据集组织：数据集下载完成后，请用户自行阅读README.md，参阅README中的原始数据集解压后的目录结构，确认原始数据集下载完整。另外，有部分数据集在dsdl目录下有tools文件夹（包含prepare.py），请按照README指示对数据集进行转换，以保证DSDL正常使用。具体使用请参考[数据集组织](#数据集组织)部分。
- 数据集配置：用户需要根据实际情况，指定config.py文件中媒体文件读取方式和根目录。具体使用请参考[数据集配置](#数据集配置)部分。

<a id="数据集下载"></a>
## 1. 数据集下载

根据（1）是否提供原始数据集下载；（2）是否提供DSDL标注下载，我们将数据集下载分为四类情形进行讨论。

### 1.1 同时提供原始数据集媒体文件和DSDL标注文件

在原始数据集允许分发，且DSDL标注文件已支持的情况下，用户可以同时下载到原始数据集媒体文件和DSDL标注文件。

CLI命令如下：

```shell
odl get <dataset_name>
```

注意这里的`<dataset_name>`需要与[OpenDataLab官网](https://opendatalab.com/)上的名字对应。用户可在官网搜索相关数据集，并在数据集详情页面的CLI部分获取到数据集名称，比如：

```shell
odl get CIFAR-10
```

下载完成后，请用户自行解压dsdl压缩包，组织后的数据集目录如下：

```shell
<root-path>
├── compressed                     # 原始数据集压缩包的文件夹
│   └── ...                        # 原始数据集压缩包
└── dsdl                           # 解压后的DSDL标注文件夹
    ├── defs
    │   ├── task-def.yaml          # 任务类型的struct定义文件
    │   └── class-dom.yaml         # 数据集的类别域
    ├── set-train                  # 训练集
    │   ├── train.yaml             # 训练的yaml文件
    │   └── train_samples.json     # 训练集sample的json文件
    ├── set-val                    # 验证集
    │   ├── val.yaml
    │   └── val_samples.json
    ├── set-test                   # 测试集
    │   ├── test.yaml
    │   └── test_samples.json  
    ├── tools                      # 如果数据集不需要额外的脚本支持，则不存在tools文件夹
    │   └── prepare.py             # 包括解压、转中间格式（如果需要的话）和生成dsdl目录
    ├── config.py                  # 数据集读取路径等config文件
    └── README.md                  # 关于数据集下载、使用、配置的教程
```

其中：

  * defs文件夹和set-xxx文件夹主要包含DSDL数据集的定义文件、类别域文件和数据文件等（详细信息可以参阅[自定义DSDL数据集](./advanced/dsdl_define.md)）；
  * config.py需要修改媒体文件读取方式和路径，具体请查看[数据集配置](#数据集配置)部分。
  * 部分数据集存在tools文件夹，提供了prepare.py工具，能够对数据集进行解压和标准化操作，具体使用方法请查看数据集组织中的[执行解压并转换](#执行解压并转换)部分的命令。
!!! note "注意：如果dsdl下存在tools文件夹，请用户参考[数据集组织](#数据集组织)部分对原始数据集执行解压和标准化操作。"


### 1.2 仅提供DSDL标注文件

如果原始数据集不允许分发，而DSDL已支持，用户需要自行下载原始数据集。

命令如下：

```shell
odl get <dataset_name>
```

下载到的数据集将只有dsdl文件夹，而不包含原始数据集媒体文件。用户可以自行下载数据集并解压，请保证原始数据集的目录格式与README中展示的原始数据集目录格式一致。通过修改config.py中的路径，来指定原始数据集媒体文件的存放位置。注意，如果dsdl目录下存在tools文件夹，请参考数据集组织中[跳过解压](#跳过解压，复制一份原始数据集后执行转换)的两个命令来执行对原始数据集的标准化操作。

### 1.3 仅提供原始数据集媒体和标注文件

[OpenDataLab官网](https://opendatalab.com/)上允许分发的数据集，目前尚有部分暂未支持DSDL标准化标注，但是用户仍然可以下载到原始数据集的媒体和标注文件。

命令如下：

```shell
odl get <dataset_name>
```

下载到的数据集将只有原始数据集压缩包，而不包含dsdl文件夹。

用户如果需要自行将其定义为DSDL数据集，以便使用ODL工具链相关功能和OpenMMLab训练，请参阅[自定义DSDL数据集](./advanced/dsdl_define.md)。

### 1.4 不提供原始数据集媒体文件和DSDL标注文件

如果当前数据集在[OpenDataLab官网](https://opendatalab.com/)上暂不提供下载，且尚未支持DSDL标准化标注，用户需自行到数据集官网进行原始数据集媒体文件和标注文件下载。

另外，用户如果需要自行将其定义为DSDL数据集，以便使用ODL工具链相关功能和OpenMMLab训练，请参阅[自定义DSDL数据集](./advanced/dsdl_define.md)。

<a id="数据集组织"></a>
## 2. 数据集组织

用户下载好数据集后，请自行解压dsdl压缩包，并阅读README，根据是否需要用户运行tools/prepare.py，分为两种情况：

- **DSDL与原始数据集可以直接匹配**：dsdl目录下不包含tools文件夹，README中不包含“prepare the dataset”模块内容，请用户自行解压原始数据集压缩包，即可以直接使用DSDL数据集
- **需要运行prepare.py对数据集做预处理**：dsdl目录下包含tools文件夹，README中包含“prepare the dataset”模块内容，请参阅[2.2小节](#2.2小节)选择适合的CLI命令运行prepare.py

### 2.1 DSDL与原始数据集可以直接匹配

这类数据集的dsdl目录下不包含tools文件夹，并且其README中不包含“prepare the dataset”模块。请用户自行解压原始数据集和DSDL文件夹，并保证其目录结构与README中展示的“原始数据集解压后的目录结构”一致，即可以直接使用DSDL标准化数据集。README内容如下：

<details>
<summary>不包含“prepare the dataset”模块的README</summary>
```
# Data Set Description Language(DSDL) for [dataset_name] dataset

## Data Structure

Please make sure the folder structure of prepared dataset is organized as followed:

<dataset_root>
├── ...               # 原始数据集解压后的目录结构

The folder structure of dsdl annotation is organized as followed:

<dataset_root>
├── ...               # dsdl解压后的目录结构

## config.py

You can load your dataset from local or oss.
From local:

local = dict(
    type="LocalFileReader",
    working_dir="the root path of the prepared dataset",
)

Please change the 'working_dir' to the path of your prepared dataset where media data can be found,
for example: "`<root>`/dataset_name/prepared".

From oss:

ali_oss = dict(
    type="AliOSSFileReader",
    access_key_secret="your secret key of aliyun oss",
    endpoint="your endpoint of aliyun oss",
    access_key_id="your access key of aliyun oss",
    bucket_name="your bucket name of aliyun oss",
    working_dir="the prefix of the prepared dataset within the bucket")

Please change the 'access_key_secret', 'endpoint', 'access_key_id', 'bucket_name' and 'working_dir',
e.g. if the full path of your prepared dataset is "oss://bucket_name/dataset_name/prepared", then the working_dir should be "dataset_name/prepared".

## Related source:

1. Get more information about DSDL: [dsdl-docs](https://opendatalab.github.io/dsdl-docs/)
2. DSDL-SDK official repo: [dsdl-sdk](https://github.com/opendatalab/dsdl-sdk/)
3. Get more dataset: [opendatalab](https://opendatalab.com/)

```
</details>

<a id="2.2小节"></a>
### 2.2 需要运行prepare.py对数据集做预处理

这类数据集的dsdl目录下包含tools文件夹，需要运行tools/prepare.py将数据集转换为DSDL标准后（后文将会详述如何运行该代码），才能正常使用DSDL标准化数据集。
!!! note "注意：在运行tools/prepare.py之前，用户需要[部署dsdl-sdk](../getting_started/install.md)。另外，部分数据集的tools/prepare.py可能还需要安装一些其他的python依赖包。"
这类数据集的README内容如下：
<details>
<summary>包含“prepare the dataset”模块的README</summary>
```

# Data Set Description Language(DSDL) for [dataset_name] dataset

## prepare the dataset

To make sure the DSDL dataset for [task_name] run successfully, the tools/prepare.py should be executed.
For this dataset, the following step will be selected to execute:

- decompress
- prepare dataset and generate DSDL annotation

There are four usage scenarios:

### decompress, convert

python tools/prepare.py <path_to_the_compressed_dataset_folder>

### decompress, copy and convert

python tools/prepare.py -c <path_to_the_compressed_dataset_folder>

### (already decompressed) copy and convert

python tools/prepare.py -d -c <path_to_the_decompressed_dataset_folder>

### (already decompressed) convert, directly overwrite

python tools/prepare.py -d <path_to_the_decompressed_dataset_folder>

For more messages, see [Dataset Prepare Section](https://opendatalab.github.io/dsdl-docs/tutorials/dataset_download/) in DSDL DOC, or use the help option:

python tools/prepare.py --help

## Data Structure

Please make sure the folder structure of prepared dataset is organized as followed:

<dataset_root>
├── ...               # 原始数据集解压后的目录结构

The folder structure of dsdl annotation for [task_name] is organized as followed:

<dataset_root>
├── ...               # dsdl解压后的目录结构

## config.py

You can load your dataset from local or oss.
From local:

local = dict(
    type="LocalFileReader",
    working_dir="the root path of the prepared dataset",
)

Please change the 'working_dir' to the path of your prepared dataset where media data can be found,
for example: "`<root>`/dataset_name/prepared".

From oss:

ali_oss = dict(
    type="AliOSSFileReader",
    access_key_secret="your secret key of aliyun oss",
    endpoint="your endpoint of aliyun oss",
    access_key_id="your access key of aliyun oss",
    bucket_name="your bucket name of aliyun oss",
    working_dir="the prefix of the prepared dataset within the bucket")

Please change the 'access_key_secret', 'endpoint', 'access_key_id', 'bucket_name' and 'working_dir',
e.g. if the full path of your prepared dataset is "oss://bucket_name/dataset_name/prepared", then the working_dir should be "dataset_name/prepared".

## Related source:

1. Get more information about DSDL: [dsdl-docs](https://opendatalab.github.io/dsdl-docs/)
2. DSDL-SDK official repo: [dsdl-sdk](https://github.com/opendatalab/dsdl-sdk/)
3. Get more dataset: [opendatalab](https://opendatalab.com/)

```
</details>

为了满足原始数据集来源不同的用户，prepare.py设定了两个参数，分别指示是否跳过解压 (-d) 以及是否保留一份解压后的原始数据集 (-c)，分为以下四种使用场景：

```shell
### 执行解压并转换
python tools/prepare.py <path_to_the_compressed_dataset_folder>

### 执行解压，复制一份原始数据集后转换
python tools/prepare.py -c <path_to_the_compressed_dataset_folder>

### 跳过解压，复制一份原始数据集后执行转换
python tools/prepare.py -d -c <path_to_the_decompressed_dataset_folder>

### 跳过解压，执行转换（直接覆盖原始数据集）
python tools/prepare.py -d <path_to_the_decompressed_dataset_folder>

```

具体的代码运行场景和细节请查看2.2.1-2.2.4小节。

<a id="执行解压并转换"></a>
#### 2.2.1 执行解压并转换

如果用户是从OpenDataLab上下载到的原始数据集压缩包，可使用以下命令运行prepare.py，请将路径修改为原始数据集压缩包所在的文件夹路径。

```shell
python tools/prepare.py <path_to_the_compressed_dataset_folder>
```

运行该代码后，将会对用户提供的数据集压缩包进行解压，生成prepared文件夹，然后直接对prepared文件夹进行DSDL标准化操作，并生成DSDL标注。执行后的目录结构如下：

```shell
├── <dataset_root>                      # 数据集根目录
    ├── <compressed_dataset_folder>     # OpenDataLab上下载到的原始数据集压缩包所在的文件夹
        ├── ...
    ├── <dsdl_folder>                   # OpenDataLab上下载后自行解压后的dsdl文件夹
        ├── ...
    ├── prepared                        # 对原始数据集压缩包解压并执行DSDL标准化后的数据集文件夹
        ├── ...
```

#### 2.2.2 执行解压，复制一份原始数据集后转换

如果用户希望保留一份解压后的原始数据集，可增加-c参数来指定：

```
python tools/prepare.py -c <path_to_the_compressed_dataset_folder>
```

运行该代码后，将会对用户提供的数据集压缩包进行解压，并保存到original文件夹下，同时会将original复制一份并命名为prepared文件夹，然后再对prepared文件夹的内容进行DSDL标准化操作，并生成DSDL标注。执行后的目录结构如下：

```shell
├── <dataset_root>                      # 数据集根目录
    ├── <compressed_dataset_folder>     # OpenDataLab上下载到的原始数据集压缩包所在的文件夹
        ├── ...
    ├── <dsdl_folder>                   # OpenDataLab上下载后自行解压后的dsdl文件夹
        ├── ...
    ├── original                        # 解压后的原始数据集文件夹
        ├── ...  
    ├── prepared                        # 复制original并执行DSDL标准化后的数据集文件夹
        ├── ...
```

<a id="跳过解压，复制一份原始数据集后执行转换"></a>
#### 2.2.3 跳过解压，复制一份原始数据集后执行转换

如果用户是从别的途径下载的原始数据集或是已解压过的数据集，并且希望转换后生成一个新的DSDL标准数据集文件夹，请用户自行解压数据集后，确保其目录结构与README中展示的“原始数据集解压后的目录结构”一致，然后利用-d参数跳过解压操作，直接执行数据集转换，路径为解压后的原始数据集文件夹：

```shell
python tools/prepare.py -d -c <path_to_the_decompressed_dataset_folder>
```

运行该代码后，将会复制一份用户提供的解压后的原始数据集到同目录下，文件夹名为prepared，然后再对prepared文件夹的内容进行DSDL标准化操作，并生成DSDL标注。用户提供的原始数据集目录下的所有文件都将会保留。执行后的目录结构如下：

```shell
├── <dataset_root>                      # 数据集根目录
    ├── <decompressed_dataset_folder>   # 用户自行解压得到的原始数据集文件夹
        ├── ...
    ├── <dsdl_folder>                   # OpenDataLab上下载后自行解压后的dsdl文件夹
        ├── ... 
    ├── prepared                        # 复制<decompressed_dataset_folder>并执行DSDL标准化后的数据集文件夹
        ├── ...
```

#### 2.2.4 跳过解压，执行转换（直接覆盖原始数据集）

如果用户是从别的途径下载的原始数据集或是已解压过的数据集，并且希望转换后仅保留DSDL标准的数据集，请用户自行解压数据集后，确保其目录结构与README中展示的“原始数据集解压后的目录结构”一致，然后利用-d参数跳过解压操作，直接执行数据集转换，其中路径为解压后的原始数据集文件夹：

```shell
python tools/prepare.py -d <path_to_the_decompressed_dataset_folder>
```

运行该代码后，将会对用户提供的解压后的原始数据集文件夹里的内容进行DSDL标准化操作，并生成DSDL标注。请注意，该操作会使得用户提供的原始数据集的部分媒体文件或标注文件被覆盖，如果不想改变原始数据集的文件，请执行上文中的[跳过解压，复制一份原始数据集后执行转换](#跳过解压，复制一份原始数据集后执行转换)。执行后的目录结构如下：

```shell
├── <dataset_root>                      # 数据集根目录
    ├── <decompressed_dataset_folder>   # 用户自行解压得到的原始数据集文件夹（其中部分文件在标准化过程中已被覆盖）
        ├── ...
    ├── <dsdl_folder>                   # OpenDataLab上下载后自行解压后的dsdl文件夹
        ├── ... 
```

<a id="数据集配置"></a>
## 3. 数据集配置
为了数据集方便分发，我们提出了【媒体数据】和【标注文件】分离这一设计理念，这样即便用户把不同数据保存在不同的存储上，也无需移动文件，仅需修改对应的config文件中媒体文件的存储根目录即可，这里的数据集配置也主要是指对config文件的适配，用户需要修改媒体文件读取方式和读取的根目录。

在 `config.py`中，列举了所支持的媒体文件读取方式，根据实际情况选择并配置文件路径等信息：

1. 本地读取： `local`中的参数 `working_dir`（本地数据所在的目录）
2. 阿里云OSS读取： `ali_oss`中的参数（阿里云OSS的配置 `access_key_secret`, `endpoint`, `access_key_id`；桶名称 `bucket_name`，数据在桶中的目录 `working_dir`。关于阿里云OSS参数配置中相关字段的详细含义和配置方法，请参考其官方文档：[配置教程](https://help.aliyun.com/document_detail/474474.html)）

完整的config.py文件示例如下：

```python
local = dict(
    type="LocalFileReader",
    working_dir="the root path of the prepared dataset",
)

ali_oss = dict(
    type="AliOSSFileReader",
    access_key_secret="your secret key of aliyun oss",
    endpoint="your endpoint of aliyun oss",
    access_key_id="your access key of aliyun oss",
    bucket_name="your bucket name of aliyun oss",
    working_dir="the prefix of the prepared dataset within the bucket")
```
