# 计算机视觉 

```{note}
本章节定义的所有类都将通过标准库cv提供。普通用户只需通过import方式导入cv标准库，无需自己写类别定义。

在下面的例子中，我们使用名为``MyClassDom``的类别域。
```

## 图像分类

图像分类任务是给每张图像分配一个类别标签。

**类定义示例:**

```yaml
ImageClassificationSample:
    # Each sample contains an image together with a class label (optional).
    $def: struct
    $params: ['cdom'] 
    $fields:
        image: Image
        label: Label[dom=$cdom]
    $optional: ['label']
```

其中, ``$optional``字段在数据样例中可以被省略。当``$optional``中``label``被忽略时，对应的字段值将被设置成一个空值（对应Python中的``None``）

**数据示例:**

```yaml
data:
    sample-type: ImageClassificationSample[cdom=MyClassDom]
    samples:
        - { image: "xyz/0001.jpg", label: "cat" }
        - { image: "xyz/0002.jpg", label: "dog" }
        - { image: "xyz/0003.jpg" }
```

## 目标检测


目标检测任务是检测给定图像中的有意义目标。每个被检测的目标可以被表示为一个带目标类别信息的边界框。

**类定义示例:**

```yaml
LocalObjectEntry:
    # Each sample contains a bounding box together a class label (optional).
    $def: struct
    $params: ['cdom']
    $fields:
        bbox: BBox
        label: Label[dom=$cdom]
    $optional: ['label']

ObjectDetectionSample:
    # Each sample contains an image together with a list of local objects.
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        objects: List[LocalObjectEntry[cdom=$cdom]]
```

**数据示例:**

```yaml
data:
    sample-type: ObjectDetectionSample[cdom=MyClassDom]
    samples:
        - image: "xyz/0001.jpg"
            objects: 
            - { bbox: [x1, y1, w1, h1], label: 1 }
            - { bbox: [x2, y2, w2, h2], label: 2 }
            - { bbox: [x3, y3, w3, h3], label: 2 }
        - image: "xyz/0002.jpg"
            objects: 
            - { bbox: [x4, y4, w4, h4], label: 3 }
            - { bbox: [x5, y5, w5, h5], label: 4 }
```


## 带场景分类的目标检测

在某些应用中，场景分类（图像级别）及目标检测会组成一个联合任务。对于这样一个任务，我们有两个类别域，这里称为``SceneDom`` 和 ``ObjectDom``，分别限定场景类别和目标类别。

**类定义示例:**

```yaml
SceneAndObjectSample:
    # Each samples contains an image, a scene label (optional)
    # together with a list of local objects.
    $def: struct
    $params: ['scenedom', 'objectdom']
    $fields:
        image: Image 
        sclabel: Label[dom=$scenedom]
        objects: List[LocalObjectEntry[cdom=$objectdom]]
    $optional: ['sclabel']
```

**数据示例:**

```yaml
data:
    sample-type: SceneAndObjectSample[scenedom=SceneDom, objectdom=ObjectDom]
    samples:
        - image: "xyz/0001.jpg"
            sclabel: "street"
            objects: 
            - { bbox: [x1, y1, w1, h1], label: 1 }
            - { bbox: [x2, y2, w2, h2], label: 2 }
            - { bbox: [x3, y3, w3, h3], label: 2 }
        - image: "xyz/0002.jpg"
            sclabel: "river"
            objects: 
            - { bbox: [x4, y4, w4, h4], label: 3 }
            - { bbox: [x5, y5, w5, h5], label: 4 }
```

## 图像分割

图像分割任务是对给定图像中的每个像素点指定像素级标签。惯例是使用标签图，也就是在一个额外的文件中存储一个非结构化目标。

**类定义示例:**

```yaml
ImageSegmentationSample:
    # Each sample contains an image together with a label map.
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        labelmap: LabelMap[dom=$cdom]
```

**数据示例:**

```yaml
data:
    sample-type: ImageSegmentationSample[cdom=MyClassDom]
    samples:
        - { image: "imgs/0001.jpg", labelmap: "maps/0001.ppm" }
        - { image: "imgs/0002.jpg", labelmap: "maps/0002.ppm" }
        - { image: "imgs/0003.jpg", labelmap: "maps/0003.ppm" }
```

## 定义具有层级关系的class domain

### 1. 单继承

在一些数据集当中，类别具有层级关系，dsdl中允许为每个类别指定自己的父类，具体操作为：

1. 首先要定义父类的class domain

```yaml
ParentClassDom:
    $def: class_domain
    classes:
        - accessory
        - animal
        - appliance
        - electronic
        - food
        - furniture
        - indoor
        - kitchen
        - outdoor
        - person
        - sports
        - vehicle
        - fruit
```

2. 然后定义子类class domain时，需要在子类的名称后面声明其属于的父类的class domain，并在每个label后面写上该label的父类的具体类别：

```yaml
ClassDom[ParentClassDom]:  # 声明父类
    $def: class_domain
    classes:
        - airplane[vehicle] # 指明airplane的父类为ParentClassDom中的vehicle
        - apple[food]
        - backpack[accessory]
        - banana[food,fruit] # 指明banana的父类有两个，分别为ParentClassDom中的food和fruit
        - baseball bat[sports]
        - baseball glove[sports]
        - bear[animal]
        - bed[furniture]
        - bench[outdoor]
        - bicycle[vehicle]
        - bird[animal]
        - boat[vehicle]
```

### 2. 多继承

存在一种情况，某个类别的父类来自不同的class domain，dsdl也支持这种多继承的关系：

1. 首先定义两个不同的父类class domain

```yaml
ParentClassDom1:
    $def: class_domain
    classes:
        - fruit
        - tool
        - vegetable
                
ParentClassDom2:
    $def: class_domain
    classes:
        - food
        - sports tool
```

2. 然后定义子类class domain，继承上述两个父类：

```yaml
ClassDom[ParentClassDom1,ParentClassDom2]:  # 声明继承ParentClassDom1和ParentClassDom2两个父类
    $def: class_domain
    classes:
        - airplane[tool][sports tool] # airplane的父类为ParentClassDom1的tool与ParentClassDom2中的sports tool
        - apple[fruit][food]
        - backpack[tool][] # backpack的父类为ParentClassDom1的tool，由于没有属于ParentClassDom2的父类，所以第二个位置为空
        - banana[fruit][food]
        - baseball bat[tool][sports tool]
        - baseball glove[tool][sports tool]
        - tomato[fruit,vegetable][food] # tomato的父类为ParentClassDom1的fruit和vegetable以及ParentClassDom2的food
```

