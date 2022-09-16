## 2.1 快速入门

在DSDL中，一个数据集会通过一个*数据集描述文件*来表示。

下面的例子为一个标准的数据集描述文件。

数据集描述文件可以是JSON格式或是YAML格式。

**JSON格式：**

```json
{
    "$dsdl-version": "0.5.0",
    "meta": {
        "name": "my-dataset",
        "creator": "my-team",
        "dataset-version": "1.0.0"
    },
    "defs": {
        "MyClassDom": {
            "$def": "class_domain",
            "classes": [
                "dog",
                "cat",
                "fish",
                "tiger"
            ]
        },
        "ImageClassificationSample" : {
            "$def": "struct",
            "$fields": {
                "image": "Image",
                "label": "Label[dom=MyClassDom]"
            }
        }
    },
    "data": {
        "sample-type": "ImageClassificationSample",
        "samples": [
            { "image": "xyz/0001.jpg", "label": "cat" },
            { "image": "xyz/0002.jpg", "label": "dog" }
        ]
    }
}
```

**YAML格式：**

```yaml
$dsdl-version: "0.5.0"
meta:
    name: "my-dataset"
    creator: "my-team"
    dataset-version: "1.0.0"
defs:
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
data:
    sample-type: ImageClassificationSample
    samples:
        - { image: "xyz/0001.jpg", label: "cat" }
        - { image: "xyz/0002.jpg", label: "dog" }
```

JSON和YAML格式的数据集描述文件都可以**准确地描述相同的**数据结构。

由于YAML格式的内容更加简洁，并且允许注释，因此我们使用YAML格式作为本文档中后续示例的默认格式。YAML格式也可以很容易地转换为等价的JSON格式。

首先，一个数据集描述文件可以被大致分为四个部分：

+ **header**：指明了当前的数据集描述文件需要被如何解析；
+ **meta section**：提供了当前数据集的一些元信息；
+ **defs section**：提供了一些全局的定义，比如：用户定义的类别；
+ **data section**：描述了数据集中的样本数据

> **注意**：
>
> + 带有前缀`$`的属性名为在DSDL中预留的有特殊含义的属性名。
> + DSDL版本（header中属性名为`$dsdl-version`）必须被明确地指明。因为DSDL解释器需要通过该属性知道当前文件的版本信息，从而正确的解析当前的数据集描述文件。
> + 通常情况下，一些通用类型的定义一般在标准库或扩展库中有提供。大多数情况下，用户不需要自己定义类别。在上面的例子中，我们定义`ImageClassificationSample`只是为了演示以及使该例子具有独立性。

