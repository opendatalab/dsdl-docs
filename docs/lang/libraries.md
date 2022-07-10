## 2.5 库

尽管我们已经试图去简化了DSDL的设计，但是要学习如何在DSDL中定义类仍然需要一些努力。然而我们明白大多数AI研究者或开发者都不想再学习另一门语言。因此我们引入了库的概念来进一步简化数据集描述的过程。

### 2.5.1 定义与导入一个库

我们在*get_started*部分定义的类`ImageClassification`是比较通用，可以应用在其他的数据集中的。因此我们可以将它提取到一个**库文件**当中，从而数据集描述文件可以直接导入它。

总的来讲，一个**库文件**是一个YAML或JSON文件，文件中提供了一些类的定义。

在上面的例子中，我们可以创建一个名为`imageclass.yaml`的库文件，内容如下：

```yaml
# file: imageclass.yaml

# DSDL version is mandatory here.
$dsdl-version: "0.5.0"

# -- below are definitions --

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

> **注意**：
>
> + 这个库文件应该被放在默认的库的路径中，从而系统可以找到它。
> + 用户还可以通过设置环境变量`DSDL_LIBRARY_PATH`来设置额外的库路径。

然后数据集描述文件可以通过导入库来简化，具体描述如下：

```yaml
$dsdl-version: "0.5.0"
$import: 
    - imageclass
meta:
    name: "my-dataset"
    creator: "my-team"
    dataset-version: "1.0.0"
data:
    sample-type: ImageClassificationSample
    samples:
        - { image: "xyz/0001.jpg", label: "cat" }
        - { image: "xyz/0002.jpg", label: "dog" }
```

在这里，我们通过在header部分使用了一个`$import`指令，`$import`指令的内容应该是一个列表，因为用户可以导入多个库文件。

> **注意**：当导入了多个库文件，并且这些库文件中包含了名称相同的若干的定义，则后导入的定义会覆盖先导入的定义。如果发生了这种情况，解析器会报出警告信息。

### 2.5.2 如何更好地使用库

下面提供了定义DSDL库的一些建议：

**Define generic classes**

如同在介绍`parametric_class`时所提到的那样，在通用类的定义中写死了参数设置不是一个好主意。因此，我们强烈建议用户定义一个含参类，并且根据具体的应用场景给定具体的参数设置（比如类别域的设置）。

**Grouped definitions**

我们建议将相同领域的定义放在一个库文件中，这可以令分发和导入更加容易。

**Documentation**

给库中的定义写文档可以令用户更容易理解。

下面的例子中，我们将与视觉识别相关的多个类放在一个库文件当中：

```yaml
# file: visualrecog.yaml

ImageClassificationSample:
    # Each image classification sample contains an image and a label.
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        label: Label[dom=$cdom]

LocalObjectEntry:
    # Each local object entry contains a bounding box and a label.
    $def: struct
    $params: ['cdom']
    $fields:
        bbox: BBox
        label: Label[dom=$cdom]

ObjectDetectionSample:
    # Each object detection sample contains an image and a list of local object entries.
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        objects: List[etype=LocalObjectEntry[cdom=$cdom]]
```

通过使用这个库文件，数据集描述文件可以简化为：

```yaml
$dsdl-version: "0.5.0"
$import: 
    - visualrecog
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
data:
    sample-type: ImageClassificationSample
    samples:
        - { image: "xyz/0001.jpg", label: "cat" }
        - { image: "xyz/0002.jpg", label: "dog" }
```

因为`MyClassDom`是一个具体的定义，只在当前的数据集中被用到。因此将它定义在数据集描述文件当中，并从库文件中导入更加通用的类，这样的作法是没有问题的。

> **注意**：
>
> * `visualrecog`库只是用来做演示的例子。
> * 除了DSDL，我们还提供了一个名字为`cv`的标准库，其中包含了与计算机视觉相关的大量定义，包括各种数据类型以及类别域等等。
