## 2.5 类别域

类别域（class_domain）是对Label（类别标注数据类型）字段的详细定义，Label字段的实例化需要对其中的 `dom`形参赋予具体的类别域（class_domain）。

### 2.5.1 定义一个类别域

在DSDL中，用户可以在数据集描述文件的 `$def`部分自定义类别域。 我们看下面这个示例：

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

+ `$def`：它的值必须是 `class_domain`，表示该YAML对象正在定义一个结构体类。
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

当然也可以一开始用参数 `$xxx`占位（具体可以参见[2.4.3 含参结构体类](structs.zh.md)），例如：

```yaml
ImageClassificationSample:
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        label: Label[dom=$cdom]
```

然后在 `data section`(描述数据集)的时候在 `sample-type`中实例化这个参数，如：

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

在一些数据集当中，类别具有层级关系，dsdl中允许为每个类别指定自己的父类，具体操作为：

直接定义子类class domain，并在每个label前面通过“.”的形式连接该label的父类的具体类别：

```yaml
ClassDom:                        # 声明类别
    $def: class_domain
    classes:
        - vehicle.airplane       # 指明airplane的父类为ParentClassDom中的vehicle
        - food.apple
        - accessory.backpack
        - food.banana
        - sports.baseball_bat    # 类别名存在空格等特殊符号需要转换为下划线
        - sports.baseball_glove
        - animal.bear
        - furniture.bed
        - outdoor.bench
        - vehicle.bicycle
        - animal.bird
        - vehicle.boat
```

在类别定义中，"."是用来分割类别上下位关系的特殊字符，每个标签存在多个单词建议用"_"连接，例如：baseball_bat。若希望类别标签有空格等特殊字符，建议在global-info中存储包含特殊字符原始标签名与转换后存放在class_dom中标签映射关系(关于global-info的定义和存储位置，请参看[数据模块](data_section.zh.md)章节)，具体形式如下：

```
{"global-info":
	{"name_mapping":[
            {
                "name": "baseball_bat.sports"
                "original_name": "baseball bat.sports",
            },
            ...
	]}
}
```
