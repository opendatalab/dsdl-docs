# **DSDL数据集验证**

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

## DSDL check模块

目前解析器的检查分三个模块：

* class_dom的检查
* strcut的检查
* 参数的检查

### class_dom的检查

首先明确class_dom的样式：

```YAML
AnnotationDom:
    $def:class_domain
    classes:
      - person
      - ...
  
KeyointDom:
    $def:class_domain
    classes:
      - lefteye.person# 会报DefineSyntaxWarning
      - ...
    skeleton:
      - [14, 16]
      - [5, 6]
      - [10, 12]
      - ...
```

包括：

- class_dom中的categories名和super_categories名字检查，需要保证category[super_category]中super_category在FatherClassDom中存在
- 保证ClassificationClassDom[ClassificationFatherDom]中ClassificationFatherDom是已经定义的父类
- 保证父类名格式和 `classes`里面的类别名格式对应： 比如 `COCO2017ClassDom[COCO2017ClassFatherDom1,COCO2017ClassFatherDom2]:`
  说明有两个类别名，那么classes中的类别定义格式就要是：
  `    classes:`
  `        - airplane[tool][sports tool]`
- 保证skeleton中的字段是list of int

### strcut的检查

```YAML
LocalObjectEntry:
    $def:struct
    $params: ['cdom']
    $fields:
        label: Label[dom=$cdom]
        bbox: BBox
        polygon: Polygon
        rlepolygon: RlePolygon          #与polygon二选一

InstanceSegmentationSample:
    $def:struct
    $params: ['scenedom', 'objectdom']
    $fields:
        image: Image
        sclabel: List[Label[dom=$scenedom]]
        semantic_seg: SegMap[dom=$cdom]
        objects: List[etype=LocalObjectEntry[cdom=$objectdom,optional=True],optional=True]
    $optional: ['semantic_seg']
```

包括：

- struct的名字不能是dsdl的内置类型名（参见下表）
- $def中定义的必须是strcut或class_dom
- $params 参数验证参见单独的参数验证模块
- $fields中检查
    - 是否有字段，没有报错
    - 字段名字是否符合规范： 不能以数字开头，不能包含空格，只能包含字母、数字、下划线
    - 字段类型是否是DSDL中定义的[基本数据类型](../../dsdl_language/lang/basic_types.md)，如果是struct类型，如 **`objects: LocalObjectEntry[cdom=$cdom]`** 需要检查该struct类型是否已经注册（可以在后面再定义，顺序不要紧，但是要有）。
    - 字段类型中的参数是否符合规范：包括参数名字和参数值
- $optional中检查：optional list 中的字段是否是已经注册的，没有就报错
- strcut中的循环引用检查

### 参数检查

包括：

- `$params`中包含的参数名字和下面 `$field`字段中的一一对应
- `$params`中给的参数是否与 `data` section 中 `sample-type`对应， eg. `SceneAndObjectSample[scenedom=COCO2017ClassFatherDom,objectdom=COCO2017ClassDom]`
- 判断带参数的，且用到别的struct的 `$field`字段（如上面例子中的 `objects`）
    - 该引用的struct是否存在（`LocalObjectEntry`是否存在）
    - 是否存在循环引用，如果存在就报错

- 该引用的struct中需要传入的参数是否都已经被定义，是否存在未赋值的参数，有就报错

- 目前不同字段引用同一个strcut也会报错

## 验证结果

  报告分为**3个部分**：

- parser检查结果：结果包括了parse结果是否成功，如果不成功，则可以查看具体的报错信息

* samples实例化检查结果：其中报告说明了当前数据集共有样本个数，正常样本个数，警告样本个数，错误样本个数，并提供了异常样本的具体信息日志。
* 可视化结果：需要肉眼观察可视化结果是否正确，比如bbox位置是否正确，标签内容是否正确等，在图片下面展示了可视化过程中的日志内容，比如是可视化成功还是失败，以及失败日志等。

### Parser部分

#### 1. Class  doamin部分

- **ValidationError： Error with class-dom name,  ** **`{class_dom_name}`** ** must be a valid identifier.
  ** **[1. `Struct` name 2. `Class domain` name 3.name of `$field` in `Struct`]  is considered a valid identifier if it only contains alphanumeric letters (a-z) and (0-9), or underscores (_).
  ****A valid identifier cannot start with a number, or contain any spaces.**
- **ValidationError：Error in **  **`{struct_name}`**  **,  ** **`{filed_name}`** ** must be a valid identifier.
  ** **[1. `Struct` name 2. `Class domain` name 3.name of `$field` in `Struct`]  is considered a valid identifier if it only contains alphanumeric letters (a-z) and (0-9), or underscores (_).
  ****A valid identifier cannot start with a number, or contain any spaces.**

    含义：struct、class domain 的名字（如上面例子里面的 `**AnnotationDom**`等）和strcut中$filed里面的名字都要是一个a valid identifier：即只能包含字母数字或下划线（且不以字母开头），不包含任何空格。

- **ValidationError： Error with class-dom name,  ** **`{varstr}`**** can't be a Python keyword.
  ****check ****https://docs.python.org/3/reference/lexical_analysis.html#keywords**** for more information.**

    含义：class domain 的名字（如上面例子里面的 `**AnnotationDom**`等）不能是一个python的保留字符串（如：def, del, if, or....., 保留字符串列表详见：https://docs.python.org/3/reference/lexical_analysis.html#keywords）。

- **ValidationError：**  **`{`** `self.name`**`}`**** is dsdl build-in value name, please rename it. Build-in value names are:  Bool, Num, Int, Str, Coord, Coord3D, Interval, BBox, Polygon, Image, InstanceMap, Video, Dict,
  ****Text, InstanceID, Date, Time, Label, LabelMap, Keypoint, List, ImageShape, RotatedBBox, UniqueID. **

    含义：当struct、class domain 的名字（如上面例子里面的 `**AnnotationDom**`等）是dsdl里面的内置类名的时候会报错，dsdl内置类别名包括：Bool, Num, Int, Str, Coord, Coord3D, Interval, BBox, Polygon, Image, InstanceMap, Video, Dict, Text, InstanceID, Date, Time, Label, LabelMap, Keypoint, List, ImageShape, RotatedBBox, UniqueID

- **DefineSyntaxError：Error in skeleton of **  **`{`** `self.class_name` **`}`** **: skeleton must be list of list of int.**

     含义：需要保证skeleton中的字段是list of int

- **DefineSyntaxError：**  **`{`** `label_name`**`}`**** is not allowed. Label in class-dom can't start with dot `.`**

     含义：class domain中的label是不能以 `.`来开始的

- **DefineSyntaxWarning：** **`{label_name}`**** is not recommended.
  ****We recommend using alphanumeric letters (a-z, A-Z and 0-9), and underscores (_)
  ****for label in class-dom (with hierarchical structure).**

     含义：对于有层级结构的class domain的label来说会报这个错误，表示：对于有层级结构的class domain的label，我们推荐使用字母数字和下划线来作为label名，并以 `.`来划分父子类。（带空格会报warning）

- **DefineSyntaxWarning：** **`{label_name}`**** is not recommended.**
  **We recommend using space, alphanumeric letters (a-z, A-Z and 0-9), and underscores (_) "、**
  **for label in class-dom (without hierarchical structure).**

     含义：对于非层级结构的class domain的label来说会报这个错误，表示：对于非层级结构的class domain的label，我们推荐使用空格字母数字和下划线来作为label名。

#### 2. Data section部分

- **DefineSyntaxError：data yaml must contain `meta` section.**

    含义：数据yaml文件中必须包含 `meta`部分 (不管几个yaml文件，数据文件必须包含，strcut、class domain等yaml文件可以没有)，eg.

```Python
$dsdl-version: "0.5.2"

$import:
    - ../defs/image-generation-facade
    - ../defs/style-dom
meta:
    dataset-name: "facade_pix2pix"
    home-page: "http://efrosgans.eecs.berkeley.edu/pix2pix/datasets/"
    creator: "Berkeley AI Research (BAIR) Laboratory, UC Berkeley"
    opendatalab-page: ""
    subset-name: "train"
    task-type: "Image Generation"
data:
    sample-type: FacadeImageSample[cdom=FacadeStyleDomain]
    sample-path: train_samples.json
```

- **DefineSyntaxError: data yaml must contain `data` section and `data` section must have `sample-type`.**

    含义：数据yaml文件中必须包含 `data`部分 (不管几个yaml文件，数据文件必须包含，strcut、class domain等yaml文件可以没有)，如上图所示。同时，`data`部分必须包含 `sample-type`。

- **DefineSyntaxWarning:  `global-info-type` is not defined.**

    含义：`global-info-type` 没有被定义，这是一个warning，可以不管.

- **DefineSyntaxError: **  **`{`** `struct_name/class_dom_name`**`}`**** section must contain "$def" sub-section.**

    含义：strcut和class_dom中必须包含$def字段来定义它的类型。

- **DefineSyntaxError:  error type {** define_type**} in yaml, type must be class_domain or struct.**

    含义：$def字段只能是strcut和class_domain中的一个。

- **DuplicateDefineWarning:  **  **`{`** `struct_name/class_dom_name`**`}`**** has defined.**

    含义：某个strcut/class_domain已经被定义了，这是一个warning，可以不管。如果不管，那后面定义的会覆盖前面定义的内容。

- **DSDLImportError: ****`import_path`**** does not exist in ** **`given_path`** **, please give the right path using `-p`.**

    含义：当用 `-p`指定数据yaml文件中$import路径的时候，如果没找到需要import的文件会报这个问题。

- **DSDLImportError: ****`import_path`** ** does not exist in neither **  **`{`** `current_path`**`}`**** nor `dsdl/dsdl_library`, please check the path or give the right path using `-p`.**

    含义：当不用 `-p`指定数据yaml文件中$import路径的时候，如果在当前文件夹和dsdl库文件（dsdl/dsdl_library）中都没找到需要import的文件会报这个问题。

#### 3. struct部分和参数部分

- **DefineSyntaxError: Error in field with value of `{ field_type }` . check the `{ k_v}` part.**

    含义：struct中的某个类型为{ field_type } 的filed出了问题。(可能还会提示是 { field_type } 中的 k_v部分出了问题)

- **DefineSyntaxError: definition error of `{field_type}` has `{param_list}`, please check field** 

    含义：field_type不在field list和struct list中，视为参数，参数不可以有嵌套的参数列表。

[cdom的报错]

- **DefineSyntaxError：definition error of dom `{cdom_name}` not in $params `{self.struct_params}`，check cdom is defined correctly.**

  含义：调用的cdom_name没有在该struct定义的params中。

- **DefineSyntaxError：`{k_v}` is dom params, should have '='**

  含义：调用的cdom参数，但是没有赋值，必须含‘=’



[List类型的报错]：

- **DefineSyntaxError：`{param}` is list etype params, should have '='**

  含义：List中有etype开头的参数，但是没有赋值，该参数必须赋值。

### Samples实例化部分

#### 1. 是否存在样本

DSDL Check会将所有样本读取到内存中，如果检测到的样本数目为0，该情况异常，会在报告中显示：

```python
{
    "flag": 0,
    "msg": "No samples found, please check the path of json file."
}
```

> 此时用户需要检查Yaml文件中指定的json文件路径是否正确。

如果实例化样本数目大于0，则该字段会显示：

```python
{
    "flag": 1,
    "msg": f"Totally {sample_nums} samples found."
}
```

> 此时需要用户检查样本数目是否正确

#### 2. 是否成功实例化数据集对象

DSDL Check会将所有的样本存储到一个`dsdl.dataset.CheckDataset`对象当中，如果实例化`dsdl.dataset.CheckDataset`对象的过程中成功，会在报告中显示：

```python
{
    "flag": 1,
    "msg": "Dataset init successfully!"
}
```

反之，如果数据集对象实例化失败，则会在报告中显示：

```python
{
    "flag": 0,
    "msg": f"Dataset init error: {e}"
}
```

> 一般情况下，数据集实例化失败的原因可能是在yaml文件中声明的sample_type不存在，举例来说：
>
> ```yaml
> data:
>     sample-type: KeyPointSample[cdom0=KeyPoint_person_ClassDom]
>     sample-path: samples.json
> 
> ```
>
> 在上面的yaml中的如果`KeyPointSample`未定义，或者`KeyPoint_person_ClassDom`未定义，或者`KeyPointSample`的参数名不叫`cdom0`，都会引起数据集实例化报错，用户需要检查是否上述这些内容写错了。

#### 3. 对样本进行实例化

DSDL Check会将所有的样本实例化为`Struct`对象，在这个过程中，如果有样本生成失败，DSDL会将错误信息记录到文档中，方便用户溯源。

具体的报错信息为：

1. **数据不符合schema**

   举例来说，如果Struct中某一个Field为Int，但是给定数据却是字符串类型，则会报以下错误：

   ```python
   ValidationError in {Field_Type} field: 
       Schema is {schema}.
       Data is {data}.
   ```

   上述的报错信息中，告诉了用户是哪一个Field报错，这个Field的schema，以及当前报错样本的具体数据，通过对比具体数据和schema，用户可以知道是哪里出了错。

2. **字段不匹配错误**

   举例来说，有以下的yaml：

   ```yaml
   KeyPointLocalObject:
       $def: struct
       $params: ["cdom0"]
       $fields:
           num_keypoints: Int
           keypoints: Keypoint[dom=$cdom0]
       $optional: ["num_keypoints"]
   ```

   如果具体的数据中，不存在`keypoints`字段，但是由于`keypoints`字段不在`$optional`列表当中，则会报以下的错误：

   ```python
   Required struct instance {key} is missing.
   ```

   这种情况下，用户需要在数据中添加`keypoints`字段信息，或者将`keypoints`字段添加到`$optional`列表当中。

   另一种情况，如果具体的数据中出现了yaml定义以外的字段，则会报以下的错误：

   ```python
   Not defined keys {keys} found in sample, which is not permitted in strict init mode.
   ```

   这种情况下，用户需要将数据中的多余字段去除，或者将该字段在yaml中声明。

> DSDL会将总数据量，成功实例化的数据量，实例化失败的数据量写在报告中。

### 可视化

DSDL为了检测标注信息是否正确，会随机从数据集中选择几个样本进行可视化，在这个步骤中，可能遇到以下问题：

1. 图像路径错误
2. 图像文件损坏
3. 图像格式不支持

具体原因需要根据报错信息确定。
