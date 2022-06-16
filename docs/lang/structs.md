## 2.4 结构体类

结构体是用来表示混合对象最常用的方法。举例来说，数据集中，一个标准的数据样本就是由多个组件构成的，比如一张图像和一个类别标注。因此，结构非常适合表示数据样本或其复合组件。 

DSDL允许用户去定义结构体类，进而对指定类型的结构体进行抽象。

### 2.4.1 定义一个结构体类（英文文档可能有问题）

在DSDL中，用户可以在数据集描述文件的`$def`部分自定义结构体类。在*get_started*的例子中，我们定义了一个名字叫`ImageClassificationSample`的结构体类：

```yaml
ImageClassificationSample:
    $def: struct
    $fields:
        image: Image
        label: Label[dom=MyClassDom]
```

结构体类是通过一个JSON对象来定义的，其中包含以下属性：

+ `$kind`：它的值必须是`"struct"`，表示该JSON对象正在定义一个结构体类。
+ `$fields`：它的值必须是一个JSON对象，包含了一系列的属性，每个属性对应了一个字段。特别地，`$fields`的每个属性中，键将被作为字段名称，值则为对应字段的类型规范。字段的类型规范可以使用下面两种方式指定：
  + **只指定数据类型名称**：只给定字段的数据类型名称（如果该数据类型是含参数据类型，则参数会使用默认值）。
  + **指定含参数据类型**：用户可以通过JSON对象指定特定的含参数据类型，其中的`$type`属性指定类型的名称，并使用其他属性来设置类型参数。可以查看例子中的`label`字段的声明。

### 2.4.2 嵌套结构体

在DSDL中，结构体可以是嵌套的。举例来说，一个目标检测任务的样本可能由一张图像和多个“局部目标”组成，其中每个局部目标都可以被表示为包含一个bounding box和一个类别标注的结构体。对于这个例子，我们可以像下面这样定义结构体：

```yaml
LocalObjectEntry:
    # Each entry refers to an individual detected object on an image.
    $def: struct
    $fields:
        bbox: BBox
        label: Label[dom=MyClassDom]

ObjectDetectionSample:
    # Each sample contains the detection results on an image.
    $def: struct
    $fields:
        image: Image
        objects: List[etype=LocalObjectEntry]
```

其中`LocalObjectEntry`结构体类嵌套进了`ObjectDetectionSample`类当中。

### 2.4.3 含参结构体类

值得注意的是，在上面的例子中，结构体类`LocalObjectEntry`使用了一个指定好的类别域`MyClassDom`，而结构体类`ObjectDetectionSample`也会像它的内嵌结构体类`LocalObjectEntry`一样，使用`MyClassDom`作为类别域。这样的定义是不通用的，因为为了能使用其他的类别域，用户则不得不重写另一个结构体类。

DSDL提供了含参结构体类来解决上面的问题。具体来说，一个**含参结构体类**可以被认为是一个类模板，允许我们在使用类时设置指定的参数。通过使用含参结构体类，我们可以以一种更通用的方法定义类。

拿目标检测为例，我们可以将上面例子中的类重新定义：

```yaml
LocalObjectEntry:
    $def: struct
    $params: ['cdom']
    $fields:
        bbox: BBox
        label: Label[dom=$cdom]

ObjectDetectionSample:
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        objects: List[etype=LocalObjectEntry[cdom=$cdom]]
```

在结构体类的定义中，我们引入了一个属性`$params`，当`$params`属性被显示地给出，并且非空的话，这个结构体类就是**含参的**。需要注意的是，当一个含参的类被使用时，它的参数必须被给定，从而它才能成为一个**具体的类**。

尤其要指出，在上面的`LocalObjectEntry`类中，我们引入了一个**类参数**`cdom`，用来指明`label`的`domain`属性。需要注意的是，当使用一个类参数时，需要使用`{}`将其围住（problem）。

接着，`ObjectDetectionSample`类也同样被定义为一个含参结构体类，参数为`cdom`，该参数用来指明对象`objects`的类别域。

使用这样的类定义，我们可以将数据集样本按如下格式表示：

```yaml
data:
    sample-type: 
        $type: ObjectDetectionSample
        cdom: MyClassDom
    samples:
        - image: "abc/0001.jpg"
            objects:
            - { bbox: [1, 2, 3, 4], label: 1 }
            - { bbox: [5, 6, 7, 8], label: 2 }
        - image: "abc/0002.jpg"
            objects:
            - { bbox: [1, 2, 3, 4], label: 3 }
            - { bbox: [5, 6, 7, 8], label: 2 }
            - { bbox: [4, 3, 5, 8], label: 3 }
```

需要注意的是，参数`cdom`已经被设为了`MyClassDom`，因此含参结构体类`ObjectDetectionSample`已经成为了一个具体类，并在样本类别字段中被指定。
