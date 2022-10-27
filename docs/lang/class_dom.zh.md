## 2.5 类别域

类别域（class_domain）是对Label（类别标注数据类型）字段的详细定义，Label字段的实例化需要对其中的`dom`形参赋予具体的类别域（class_domain）。

### 2.5.1 定义一个类别域
在DSDL中，用户可以在数据集描述文件的`$def`部分自定义类别域。 我们看下面这个示例：

**类别域示例:**

```yaml
MyClassDom:
    $def: class_domain
    classes:
        - airplane
        - apple
        - backpack
        - banana
        - baseball bat
        - baseball glove
        - bear
```
结构体类是通过一个YAML对象来定义的，其中包含以下属性：

+ `$def`：它的值必须是`class_domain`，表示该YAML对象正在定义一个结构体类。
+ `classes`：它的值必须是一个YAML的list对象，包含了一系列的类别名，它也是一个字符串，每个类别名对应了一个字段。

### 2.5.2 类别域的引用

类别域是主要用来：实例化结构体类struct中的Label字段，例如：

```yaml
ImageClassificationSample:
    $def: struct
    $fields:
        image: Image
        label: Label[dom=MyClassDom]
```

当然也可以一开始用参数`$xxx`占位（具体可以参见[2.4.3 含参结构体类](structs.zh.md)），例如：

```yaml
ImageClassificationSample:
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        label: Label[dom=$cdom]
```

然后在`data section`(描述数据集)的时候在`sample-type`中实例化这个参数，如：

```yaml
data:
    sample-type: ImageClassificationSample[cdom=MyClassDom]
    sample-path: $local
    samples:
        - image: "xyz/0001.jpg"
          label: "apple"
        - image: "xyz/0002.jpg"
          label: "banana"
```

### 2.5.3 定义具有层级关系的类别域

#### 2.5.3.1. 单继承

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

#### 2.5.3.2. 多继承

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



