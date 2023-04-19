# DSDL类型扩展

DSDL已经支持很多基础类型Field（Bool、Int、Num、Str、Dict、Date、Time），标注类型Field（Coord、Coord3D、Interval、BBox、RotatedBBox、Polygon、Label、Keypoint、Text、ImageShape、UniqueID、InstanceID）以及媒体类型Field（Image、LabelMap、InstanceMap）。但在一些特殊情况下，这些预设的Field无法满足用户的开发需求，因此本章节会详解在DSDL中Field是如何定义的，从而方便用户自己拓展DSDL Field。

扩展DSDL Field分为以下几个步骤

1. 设计Field的声明参数的jsonschema；
2. 设计该Field的传入值的jsonschema；
3. 如有必要，还需要设计 参数+值 的联合jsonschema
4. 用户定义该Field对应的geometry类

下面本文将以`RotatedBBoxField`为例，介绍如何自定义一个DSDL Field。

## 1. 任务介绍

用户在定义一个Field之前，需要了解该Field的任务特点，以旋转目标检测为例，它的标注应该是一个旋转的矩形框，在大多数任务中，该矩形框以`[x, y, w, h, theta]`的形式给出，其中x,y分别为矩形框中心点的横纵坐标，`w,h` 分别为举行框的宽和高，`theta`则为矩形框的旋转角度，单位为角度或弧度。而也有很大一部分数据集将旋转矩形框以polygon的形式给出，即将其标注为矩形框4个顶点的xy坐标，表示为`[x1, y1, x2, y2, x3, y3, x4, y4]`。

综上所述，如果我们想要自定义一个比较通用的RotatedBBox Field，需要考虑值是以 xywht形式还是xyxy形式给出，以及xywht形式下的角度的单位是度还是弧度。

幸运的是，dsdl支持在声明Field的同时传入一些参数来规定该Field在不同模式下工作，以 RotatedBBox Field为例，我们一共要为RotatedBBox Field定义3种模式：

```yaml
LocalObjectEntry:
    $def: struct
    $fields:
        rbbox: RotatedBBox[mode=xywht, measure=radian]  # 以xywht的形式给值，且角度单位为弧度

LocalObjectEntry:
    $def: struct
    $fields:
        rbbox: RotatedBBox[mode=xywht, measure=degree]  # 以xywht的形式给值，且角度单位为度
        
LocalObjectEntry:
    $def: struct
    $fields:
        rbbox: RotatedBBox[mode=xyxy]  # 以xyxy的形式给值
```

确定了RotatedBBox的样式，我们下面可以开始定义它的参数jsonschema

## 2. 参数schema定义

在RotatedBBox中，我们定义了`mode`、`measure`两个形参，并规定了`mode`的实参只能是`xywht`或`xyxy`，`measure`的实参只能是`radian`或`degree`。我们可以使用下面的jsonschema来描述该约束：

```python
args_schema = {
    "type": "object",
    "properties": {
        "measure": {"type": "string", "enum": ["radian", "degree"]},
        "mode": {"type": "string", "enum": ["xywht", "xyxy"]}
    },
    "minProperties": 2,
    "maxProperties": 2,
    "required": ["measure", "mode"]
}
```

在上面的jsonschema中，我们约束了RotatedBBox的关键字参数字典中必须包含且只能包含两个键：`measure`和`mode`，并且`measure`键对应的值只能是`"radian"`字符串或是`"xyxy"`字符串；`mode`键对应的值只能是`"xywht"`字符串或`"xyxy"`字符串。

此外有些情况下我们希望在为Field传入参数的时候，Field使用默认参数进行初始化，我们可以定义一个默认传参字典：

```python
default_args = {
    "mode": "xywht",
    "measure": "radian"
}
```

上面的默认字典规定了在不传入参数的情况下，默认`mode="xywht"`，`measure="radian"`

定义完参数schema后，我们则需要规定具体传入的值的jsonschema。

## 3. 值schema定义

在RotatedBBox这个例子中，传入的值只有两种情况：

1. 如果RotatedBBox Field的`mode`是`"xywht"`，则传入的值需要是一个列表，列表中元素数目为5，类型为数字类型，分别代表了旋转框的中心点xy坐标，宽高，以及旋转角度。
2. 如果RotatedBBox Field的`mode`是`xyxy`，则传入的值需要是一个列表，列表中元素数目为8，类型为数字类型，分别代表了旋转框的四个顶点的xy坐标：`[x1, y1, x2, y2, x3, y3, x4, y4]`

因此，值jsonschema的定义如下：

```python
data_schema = {
        "$id": "/special/rotatedbbox",
        "title": "RotatedBBoxField",
        "description": "Rotated bounding box field in dsdl.",
        "type": "array",
        "oneOf": [
            {"minItems": 5, "maxItems": 5,
             "items": [{"type": "number"}, {"type": "number"}, {"type": "number", "minimum": 0},
                       {"type": "number", "minimum": 0}, {"type": "number"}]},
            {"minItems": 8, "maxItems": 8, "items": {"type": "number"}}
        ]
    }
```

上面的jsonschema做出了如下的约束：

1. 传入RotatedBBox Field值必须要是一个列表；
2. 列表的元素约束需要满足下面两种情况之一：
   1. 元素数目为5，类型都是number，且表示宽高的第3个和第4个元素都必须要是大于0的数；
   2. 元素数目为8，类型都是number



此外，在RotatedBBox Field中，我们还需要确定参数schema和值schema之间的对应关系，因为我们需要确保当`mode="xywht"`时传入的值必须是5元素列表；当`mode=xyxy`时，传入的值必须是8元素列表，因此我们需要额外定一个参数+值的整体schema：

```python
whole_schema = {
        "type": "object",
        "oneOf": [
            {
                "properties": {
                    "args": {
                        "type": "object",
                        "properties": {
                            "measure": {"type": "string", "enum": ["radian", "degree"]},
                            "mode": {"type": "string", "enum": ["xywht"]}
                        },
                        "minProperties": 2,
                        "maxProperties": 2,
                        "required": ["measure", "mode"]
                    },
                    "value": {
                        "type": "array",
                        "minItems": 5,
                        "maxItems": 5,
                        "items": [{"type": "number"}, {"type": "number"}, {"type": "number", "minimum": 0},
                                  {"type": "number", "minimum": 0}, {"type": "number"}]
                    }
                }
            },

            {
                "properties": {
                    "args": {"type": "object",
                             "properties": {
                                 "measure": {"type": "string", "enum": ["radian", "degree"]},
                                 "mode": {"type": "string", "enum": ["xyxy"]}
                             },
                             "minProperties": 2,
                             "maxProperties": 2,
                             "required": ["measure", "mode"]},
                    "value": {"type": "array", "minItems": 8, "maxItems": 8, "items": {"type": "number"}}
                }
            }
        ],
        "required": ["args", "value"]
    }
```

> 只有在参数和值的形式一一对应的情况下才需要定义上面的`whole_schema`

为了理解`whole_schema`，我们给出下面几个例子：

```python
data_args = {
    "args": {"mode": "xywht", "measure": "radian"},
    "value": [1,2,3,4,5]
}   # 正确，满足whole_schema的规定

data_args = {
    "args": {"mode": "xywht", "measure": "radian"},
    "value": [1,2,3,4,5,6,7,8]
}   # 错误，value必须是5元素列表，因此mode是"xywht"

data_args = {
    "args": {"mode": "xyxy", "measure": "radian"},
    "value": [1,2,3,4,5,6,7,8]
}   # 正确，满足whole_schema的规定
```

## 4. 数据类的定义

在dsdl中，我们使用jsonschema来检查给定的数据是否合规，但是这只是在基础数据类型方面的检查，我们通过这种方式只能确保例如BBox的数据必须为一个4元素列表，或是polygon必须是一个3层嵌套列表这种约束，为了能进一步表示各种不同的数据，将赋予他们语义信息，我们还会将这些通过jsonschema验证的数据封装在一个dsdl数据类（`dsdl.geometry.BaseGeometry`）当中，从而方便用户调用各种方法来对数据进行操作。

对于RotatedBBox Field而言，我们将符合data schema的数据封装在了`dsdl.geometry.RBBox`类当中。因此用户在实现自定义Field时，建议也可以在`dsdl.geometry`包中定义一个数据类。

在本节中，我们将以`dsdl.geometry.RBBox`为例，讲解如何定义一个数据类（在dsdl中，我们将数据类成为`Geometry`类）。

定义一个`Geometry`类包括以下几个步骤：

1. 继承`dsdl.geometry.BaseGeometry`父类
2. 定义初始化方法
3. 定义一些常用的方法
4. 如果当前field需要在dsdl view命令中被可视化展示，则需要重写父类方法中的`visualize`方法（该步骤不会在本文中涉及）

### 4.1 定义初始化方法

```python
from .base_geometry import BaseGeometry

class RBBox(BaseGeometry):
    def __init__(self, value, mode="xywht", measure="radian"):
        assert mode in ("xywht", "xyxy") and measure in ("radian", "degree")
        if mode == "xywht":
            self._polygon = None
            if measure == "degree":
                value = value.copy()
                value[-1] = value[-1] / 180 * math.pi
            self._rbbox = value
        else:
            self._polygon = value
            self._rbbox = None
```

> 需要注意的是，用户定义的Geometry类的初始化方法需要传入的值需要包含：
>
> 1. 具体的数据value
> 2. 该Geometry类对应的Field的声明参数
>
> 具体来说，由于RotatedBBox Field的声明参数包含`mode`和`measure`，因此它对应的Geometry类RBBox的初始化参数除了具体value数据，也必须包含`mode`和`measure`两个参数，且含义与RotatedBBox Field中的一致。

在上面的代码中，我们根据传入的`mode`和`measure`对传入的数据`value`进行相应的处理，比如：

* 如果`measure`为`degree`，则需要将`value`中的角度的值转换为弧度单位；
* 如果`mode`为`xywht`，则需要将value存储为`self._rbbox`属性，如果`mode`为`xyxy`，则需要将value存储为`self._polygon`



### 4.2 定义一些常用的方法

我们有可能想对封装的数据进行一些简单的操作，我们则可以自己定义相应的方法，比如在RBBox中，我们定义了：

```python
@staticmethod
def rbbox2polygon(value):
    x, y, width, height, angle = value
    cosA, sinA = math.cos(angle), math.sin(angle)

    def _rotate(p_):  # clockwise
        x_, y_ = p_
        x_r = (x_ - x) * cosA - (y_ - y) * sinA + x
        y_r = (x_ - x) * sinA + (y_ - y) * cosA + y
        return [x_r, y_r]

    x_l, x_r, y_t, y_b = x - width / 2, x + width / 2, y - height / 2, y + height / 2
    p_lt, p_lb, p_rt, p_rb = [x_l, y_t], [x_l, y_b], [x_r, y_t], [x_r, y_b]

    return [_rotate(p_lt), _rotate(p_lb), _rotate(p_rb), _rotate(p_rt)]

@staticmethod
def polygon2rbbox(value):
    res = cv2.minAreaRect(np.array(value).astype(np.int32))
    x, y = res[0]
    width, height = res[1]  # width is "first edge"
    angle = res[2]
    if width < height:
        width, height = height, width
        angle = angle + 90
    angle = 1 - angle / 180 * math.pi
    return [x, y, width, height, angle]

@property
def polygon_value(self):
    if self._polygon is None:
        self._polygon = self.rbbox2polygon(self._rbbox)
    return self._polygon

@property
def rbbox_value(self):
    if self._rbbox is None:
        self._rbbox = self.polygon2rbbox(self._polygon)
    return self._rbbox
```

> 上面的方法实现了`mode`为`xywht`和`xyxy`之间数据的相互转换

## 5. 定义Field类

在完成了上述的操作后，我们需要做的就是将上面定义的内容组装到一个Field类中，即定义Field类本身。

以RotatedBBox Field为例，我们需要在`dsdl.fields`包中定义一个同名的类，并让它继承`dsdl.base_field.BaseField`基类。此外，我们还需要将上面几小节定义的jsonschema设置为它的类属性，分别为：

1. `default_args`：Field声明默认参数
2. `args_schema`：声明Field时传入参数需要遵守的 jsonschema
3. `data_schema`：该Field的实例数据需要遵守的jsonschema
4. `whole_schema`：该Field的声明参数和实例数据需要遵守的整体schema（一般情况下不需要）
5. `geometry_class`：该Field对应的数据类的类名，在上面的例子中，类名为`RBBox`

因此，最终定义的Field类如下所示：

```python
class RotatedBBox(BaseField):
    default_args = {
        "mode": "xywht",
        "measure": "radian"
    }

    data_schema = {
        "$id": "/special/rotatedbbox",
        "title": "RotatedBBoxField",
        "description": "Rotated bounding box field in dsdl.",
        "type": "array",
        "oneOf": [
            {"minItems": 5, "maxItems": 5,
             "items": [{"type": "number"}, {"type": "number"}, {"type": "number", "minimum": 0},
                       {"type": "number", "minimum": 0}, {"type": "number"}]},
            {"minItems": 8, "maxItems": 8, "items": {"type": "number"}}
        ]
    }

    args_schema = {
        "type": "object",
        "properties": {
            "measure": {"type": "string", "enum": ["radian", "degree"]},
            "mode": {"type": "string", "enum": ["xywht", "xyxy"]}
        },
        "minProperties": 2,
        "maxProperties": 2,
        "required": ["measure", "mode"]
    }

    whole_schema = {
        "type": "object",
        "oneOf": [
            {
                "properties": {
                    "args": {
                        "type": "object",
                        "properties": {
                            "measure": {"type": "string", "enum": ["radian", "degree"]},
                            "mode": {"type": "string", "enum": ["xywht"]}
                        },
                        "minProperties": 2,
                        "maxProperties": 2,
                        "required": ["measure", "mode"]
                    },
                    "value": {
                        "type": "array",
                        "minItems": 5,
                        "maxItems": 5,
                        "items": [{"type": "number"}, {"type": "number"}, {"type": "number", "minimum": 0},
                                  {"type": "number", "minimum": 0}, {"type": "number"}]
                    }
                }
            },

            {
                "properties": {
                    "args": {"type": "object",
                             "properties": {
                                 "measure": {"type": "string", "enum": ["radian", "degree"]},
                                 "mode": {"type": "string", "enum": ["xyxy"]}
                             },
                             "minProperties": 2,
                             "maxProperties": 2,
                             "required": ["measure", "mode"]},
                    "value": {"type": "array", "minItems": 8, "maxItems": 8, "items": {"type": "number"}}
                }
            }
        ],
        "required": ["args", "value"]
    }

    geometry_class = "RBBox"
```

通过上述的方式，我们就定义了一个RotatedBBox Field，python代码的使用实例如下：

```python
from dsdl.fields import RotatedBBox  # import RotatedBBox field
field = RotatedBBox(mode="xywht", measure="radian")  # decare the RotatedBBox field

data = [10, 12, 60, 70, 3.14]  # define the data of a rotated bounding box
rotated_bbox_obj = field.validate(data)  # return a dsdl.geometry.RBBox object
```

此时我们就可以调用其方法：

```python
rotated_bbox_obj.polygon_value  # 输出该rotated bounding box的xyxy形式
rotated_bbox_obj.rbbox_value  # 输出该rotated bounding box的xywht形式
...
```

