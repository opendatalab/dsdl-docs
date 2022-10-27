## 2.6 数据模块

我们知道一个数据集描述文件可以被大致分为四个部分：

+ **header**：指明了当前的数据集描述文件需要被如何解析；
+ **meta section**：提供了当前数据集的一些元信息；
+ **defs section**：提供了一些全局的定义，比如：用户定义的[类别域](class_dom.zh.md)（class domain）和[结构体](structs.zh.md)（struct）；
+ **data section**：描述了数据集中的样本数据

前面的章节我们主要介绍了**defs section**，清晰的定义了[类别域](class_dom.zh.md)（class domain）和[结构体](structs.zh.md)（struct）后，我们还需要定义每个具体的样本，这就是**data section**所做的事情。

### 2.4.1 定义具体的data section
在[快速入门](get_started.zh.md)中我们有如下例子：
```yaml
data:
    sample-type: ImageClassificationSample
    sample-path: $local
    samples:
        - { image: "xyz/0001.jpg", label: "cat" }
        - { image: "xyz/0002.jpg", label: "dog" }
        ...
```
可以看到一个`data section`包括三个模块：

+ **sample-type**：数据的类型定义，这里一般是我们定义的某个结构体（struct），如果这个结构体里面包含参数则需要实例化这个参数，具体参见[2.4.3 含参结构体类](structs.zh.md)；此外`sample-type`也可以是任意其他数据类型（Label、Image、Int等等），因为我们知道结构体（struct）也是数据类型的一种。
+ **sample-path**: samples的存放路径，如果实际是一个路径，则samples的内容从该文件读取，如果是`$local`（这个例子），则从本文件的`data.samples`字段中直接读取
+ **samples**: 保存数据集的样本信息，注意只有在`sample-path`是`$local`的时候该字段才会生效，否则samples会优先从`sample-path`中的路径去读取

我们可以看到`data.samples`中的字段是和`data.sample-type`中所给定的数据类型是一一对应的：

回顾一下，上面的例子里面`ImageClassificationSample`定义如下：

```yaml
MyClassDom:
    $def: class_domain
    classes:
        - dog
        - cat
        - fish
        - tiger
ImageClassificationSample:
    $def: struct
    $fields:
        image: Image
        label: Label[dom=MyClassDom]
```

如果我们的数据中有些字段是缺失的，比如上面的`data.samples`部分有的数据中label缺失：
```yaml
data:
    sample-type: ImageClassificationSample
    sample-path: $local
    samples:
        - { image: "xyz/0001.jpg" }
        - { image: "xyz/0002.jpg", label: "dog" }
        - { image: "xyz/0003.jpg"}
        - { image: "xyz/0004.jpg", label: "tiger" }
```
那相应的，我们在定义结构体的时候，我们需要指出，哪些字段是缺失的，方法是：我们可以把可以有缺失值的字段名放在`struct`类型中的`$optional`部分，
`$optional`字段是个列表，格式如下：
```yaml
ImageClassificationSample:
    $def: struct
    $fields:
        image: Image
        label: Label[dom=MyClassDom]
    $optional: ['label']
```

!!! note "注意：当$optional中label被忽略时，对应的字段值可以在`data.samples`缺失，否则会显示警告。"


### 2.4.2 将具体数据单独放在json中

当数据量很大的时候，建议将数据从YAML文件的`data section`部分抽出来单独放在JSON文件中，并在`data section`部分的`sample-path`字段中给出数据存放的JSON文件的具体路径，用字符串表示，示例如下：
```yaml
data:
    sample-type: ImageClassificationSample
    sample-path: /XXX/XXX/samples.json 
```
在`samples.json`中存放我们具体的数据，示例如下：
```json5
[
  {"image": "xyz/0001.jpg", "label": "cat"}, 
  {"image": "xyz/0002.jpg", "label": "dog"}, 
  {"image": "xyz/0003.jpg", "label": "dog"}, 
  {"image": "xyz/0004.jpg", "label": "tiger"},
  ...
]
```