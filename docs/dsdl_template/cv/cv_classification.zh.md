# 图像分类任务

我们通过对图像分类任务进行调研，总结该任务中数据集描述字段信息，从而制定出图像分类任务DSDL模板，供大家参考使用。

## 1. 任务调研

### 1.1 任务定义
  图像分类是指给定一张输入图像，输出其语义类别。


### 1.2 评价指标

任务的评价指标一般有两个：$top-5$的准确率和$top-1$的准确率，$准确率 = \frac{正确分类图片数量}{所有图片数量}$。$top-5$准确率指的是前$5$个得分最高的预测类别里有一个是正确的，即为当前样本被正确分类，而$top-1$准确率必须保证分数最高的预测类别是正确的，才算当前样本被正确分类。

<img src='https://user-images.githubusercontent.com/69186975/207549088-26bf0afb-26bd-4065-9a7e-fd28b6acc8a2.png'>

### 1.3 主流数据集调研

我们对$10$个主流分类数据集进行调研，主要对当前任务数据集描述文件（主要是标注字段）进行分析汇总，相同含义的标注字段会以统一命名进行展示，汇总信息如下表所示：


<a id="table-1"></a>

  <table border="4" >
    <tr>
      <th rowspan="2" align=center colspan="1" align=center>图像分类数据集</th>
      <th colspan="2" align=center>共享字段</th>
      <th colspan="2" align=center>独立字段</th>
    </tr>
    <tr>
      <th>image_id</th>
      <th>label_id</th>
      <th>superclass</th>
    </tr>
    <tr>
      <th width="25%" >ImageNet-21K</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center" style="color:red">ImageNet有层级结构，基于WordNet。 @致远修正</td>
    </tr>
    <tr>
      <th width="25%" >ImageNet-1K</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center"></td>
    </tr>
    <tr>
      <th width="25%" >CIFAR10</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center"></td>
    </tr>
    <tr>
      <th width="25%" >CIFAR100</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
    </tr>
    <tr>
      <th width="25%" >MNIST</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center"></td>
    </tr>
    <tr>
      <th width="25%" >Fashion-MNIST</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center"></td>
    </tr>
    <tr>
      <th width="25%" >Caltech-256</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center"></td>
    </tr>
    <tr>
      <th width="25%" >Oxford Flowers-102</th>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center">Y</td>
      <td width="20%" align="center"></td>
    </tr>
  </table>

对图像分类任务的共享字段和独立字段进一步整理，如下表所示：
<table border="4" >
    <tr>
      <th align=center >字段类型</th>
      <th align=center >字段名称</th>
      <th align=center >含义</th>
    </tr>
    <tr>
      <th rowspan="2">共享字段</th>
      <th>image_id</th>
      <td>定位到唯一图片，比如用图片名或者图片路径表示</td>
    <tr>
      <th>label_id</th>
      <td>图片所属的类别，类型为int表示为单标签，类型为List[int]表示多标签</td>
    <tr>
      <th rowspan="1">独立字段</th>
      <th>superclass</th>
      <td>图片所属类别的父类别，比如"dog"的父类可能是"animal"</td>
    </tr>
</table>
可以看到，如果要描述一个分类数据集的样本，image_id和label_id是最基础的字段，同时，也会有类似superclass的特有字段。  

<a id="table-2"></a>

## 2. 模板展示

根据上述调研，图像分类任务中，每个样本有两个最重要的属性：图像文件及对应的语义标签，由此我们定义图像分类模板如下：


#### **`image-classfication.yaml`**
```yaml
$dsdl-version: "0.5.0"

ClassificationSample:
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        label: Label[dom=$cdom]
    $optional: ['label']
```
模板中各字段的含义如下（详细学习请参考[DSDL语言教程](../../dsdl_language/overview.zh.md)）：

  - $dsdl-version: 当前文件对应的dsdl版本号
  - ClassificationSample: 分类任务的样本名

    - $def: 类型定义，当前表示ClassificationSample是一个结构体类
    - $params: 形参定义，可在data/samples中转入具体参数，这里给类别便签提供形参
    - $fields: 结构体类所包含的属性，包括:
        - image 图片路径
        - label 类别信息
    - $optional: field中可选属性，这里只定义了一个字段即label，表示样本中label的存在是可选的，具体data/sample中可为空（如半监督图像部分样本无标签）



## 3. 使用示例

我们以CIFAR-10数据集为例，展示图像分类数据集DSDL描述文件具体内容。

### 3.1 DSDL语法描述类别信息

#### **`cifar10-class-dom.yaml`**
```yaml
$dsdl-version: "0.5.0"

Cifar10ImageClassificationClassDom:
    $def: class_domain
    classes:
        - airplane
        - automobile
        - bird
        - cat
        - deer
        - dog
        - frog
        - horse
        - ship
        - truck
```

<details><summary>类别域定义说明</summary>

```
上面的文件中给出了Cifar10ImageClassificationClassDom的定义，具体包含下列字段：  

- $def: 描述了Cifar10ImageClassificationClassDom的类型，这里即class_domain  
- classes: 描述了该类别域中所包含的类别及其顺序，在cifar10数据集中，则依次为airplane、automobile等等  

这一章节介绍的分类任务模板和cdom模板都可以在我们的模板库[dsdl-sdk repo](https://gitlab.shlab.tech/research/dataset_standard/dsdl-sdk/-/tree/feature-types/dsdl/dsdl_library)中找到，其他任务类型和类别域的模板也欢迎大家尝试使用。

```
</details>


### 3.2 数据集yaml文件定义
#### **`train.yaml`**
```yaml
$dsdl-version: "0.5.0"

$import:
    - cifar10-class-dom  
    - image-classfication

meta:
    name: "cifar10"
    subdata-name: "train"

data:
    sample-type: ClassificationSample[cdom=Cifar10ImageClassificationClassDom]
    sample-path: $local
    samples:
      - image: "images/000000000000.png"
        label: "frog"
      - image: "images/000000000001.png"
        label: "truck"
        ...
```

上面的描述文件中，首先定义了dsdl的版本信息，然后import了两个模板文件，包括任务模板和类别域模板，接着用meta和data字段来描述自己的数据集，具体的字段说明如下所示：  

- $dsdl-version: dsdl版本信息
- $import: 模板导入信息，这里导入分类任务模板和cifar10的class domain，也就是章节[2. 模板展示](#table-2)中展示的两部分内容
- meta: 主要展示数据集的一些元信息，比如数据集名称，创建者等等，用户可以自己添加想要备注的其它信息
- data: data的内容就是按照前面定义好的结构所保存的样本信息，具体如下：  

    - sample-type: 数据的类型定义，在这里用的是从分类任务模板中导入的ClassificationSample类，同时指定了采用的cdom为Cifar10ImageClassificationClassDom
    - sample-path: samples的存放路径，如果实际是一个路径，则samples的内容从该文件读取，如果是$local（这个例子），则从本文件的data.samples字段中直接读取
    - samples: 保存数据集的样本信息，注意只有在sample-path是$local的时候该字段才会生效，否则samples会优先从sample-path中的路径去读取
