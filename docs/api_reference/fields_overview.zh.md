# DSDL Field类型简介

Field是DSDL中表达数据的基本单位，在数据集中，每一个样本都遵循一个Struct模板，而Struct的组成内容即为Field（或者嵌套Struct）。

如下所示，一个具体的样本为：

```python
sample = {
    "img": "media/00001.jpg",
    "bbox": [369.3, 253.15, 57.7, 29.96],
    "label": "dog"
}
```

它遵循的Struct为：

```yaml
LocalObjectEntry:
    $def: struct
    $fields:
        bbox: BBox
        label: Label[dom="COCODomain"]
        img: Image
```

其中的BBox、Label、Image都是Field，这些Field规定了样本中各个字段值的类型，比如样本中的`"img"`字段虽然是字符串类型，但由于在Struct定义中该字段被声明为`Image`Field，则dsdl sdk会将其当作一个图像类型来处理。

本章内容会详细介绍DSDL中出现的所有预设的Field。

> 在DSDL中，我们使用jsonschema来规范Field的初始化传入的参数以及规范该Field对应的值的形式。

## 基础类型Field

DSDL中有一些表示基础类型的Field，包括：

### 1. Bool

Bool类型Field用来表示样本中的布尔类型的数据：

+ **声明参数schema**：

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

  > 该schema表示，Bool类型Field在声明的时候不需要传入参数

+ **数据schema**：

  ```python
  data_schema = {
      "$id": "/generic/boolean",
      "title": "BoolField",
      "description": "Bool field in dsdl.",
      "oneOf": [
          {"type": "boolean"},
          {"type": "number", "enum": [0, 1]}
      ]
  }
  ```

  > 该schema表示，Bool类型Field在实例化时可以传入True，False，0，1

+ **实例**：

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          iscrowd: Bool
  ```

  ```python
  # 具体样本
  sample = {
      "iscrowd": True  # True/False/0/1都满足要求
  }
  
  sample = {
      "iscrowd": 2  # 不满足要求
  }
  
  sample = {
      "iscrowd": "True"  # 不满足要求
  }
  ```

### 2. Int

Int类型Field用来表示样本中整数类型的数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

* **数据schema**

  ```python
  data_schema = {
      "$id": "/generic/int",
      "title": "IntField",
      "description": "Int field in dsdl.",
      "type": "integer",
  }
  ```

  > 该schema表示，Int类型Field实例化时只可以传入整数类型

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          count: Int
  ```

  ```python
  # 具体样本
  sample = {
      "count": 1  # correct
  }
  
  sample = {
      "count": "1"  # wrong
  }
  
  sample = {
      "count": True  # wrong
  }
  ```

### 3. Num

Num类型Field用来表示样本中浮点数类型的数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

* **数据schema**

  ```python
  data_schema = {
      "$id": "/generic/num",
      "title": "NumField",
      "description": "Num field in dsdl.",
      "type": "number",
  }
  ```

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          weight: Num
  ```

  ```python
  # 具体样本
  sample = {
      "weight": 1  # correct
  }
  
  sample = {
      "weight": 10.4  # correct
  }
  
  sample = {
      "weight": True  # wrong
  }
  ```

### 4. Str

Str类型Field用来表示样本中字符串类型的数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

* **数据schema**

  ```python
  data_schema = {
      "$id": "/generic/str",
      "title": "StrField",
      "description": "Str field in dsdl.",
      "type": "string",
  }
  ```

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          name: Str
  ```

  ```python
  # 具体样本
  sample = {
      "name": "dsdl"  # correct
  }
  
  sample = {
      "name": 10.4  # wrong
  }
  
  sample = {
      "name": True  # wrong
  }
  ```

### 5. Dict

Dict类型Field用来表示样本中字典类型的数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

* **数据schema**

  ```python
  data_schema = {
      "$id": "/generic/dict",
      "title": "DictField",
      "description": "Dict field in dsdl.",
      "type": "object",
  }
  ```

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          attributes: Dict
  ```

  ```python
  # 具体样本
  sample = {
      "attributes": {"name": "dsdl", "age": 0, "gender": "female"}  # correct
  }
  
  sample = {
      "attributes": 10.4  # wrong
  }
  
  sample = {
      "attributes": "dsdl"  # wrong
  }
  ```

## 特殊类型Field

在DSDL中，我们使用一些特殊的Field来描述bounding box、polygon、keypoint等标注类型，并为其中一些Field实现了相应的基础类，提供了一些常用的方法方便用户调用。

### 1. Coord

Coord类型Field用来表示样本中的二维坐标数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

* **数据schema**

  ```python
  data_schema = {
      "$id": "/special/coord",
      "title": "CoordField",
      "description": "Coord 2D field in dsdl.",
      "type": "array",
      "items": {
          "type": "number",
      },
      "minItems": 2,
      "maxItems": 2
  }
  ```

  > 该schema表示传入的值必须要是一个列表，列表中必须包含两个元素，两个元素的类型必须是数字

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          coordinate: Coord
  ```

  ```python
  # 具体样本
  sample = {
      "coordinate": [10, 12]  # correct
  }
  
  sample = {
      "coordinate": [10, 12, 13]  # wrong
  }
  
  sample = {
      "coordinate": "dsdl"  # wrong
  }
  
  sample = {
      "coordinate": [10, False]  # wrong
  }
  ```

### 2. Coord3D

Coord3D类型Field用来表示样本中的三维坐标数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

* **数据schema**

  ```python
  data_schema = {
      "$id": "/special/coord3d",
      "title": "Coord3DField",
      "description": "Coord 3D field in dsdl.",
      "type": "array",
      "items": {
          "type": "number",
      },
      "minItems": 3,
      "maxItems": 3
  }
  ```

  > 该schema表示传入的值必须要是一个列表，列表中必须包含3个元素，3个元素的类型必须是数字

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          coordinate: Coord3D
  ```

  ```python
  # 具体样本
  sample = {
      "coordinate": [10, 12, 0]  # correct
  }
  
  sample = {
      "coordinate": [10, 12]  # wrong
  }
  
  sample = {
      "coordinate": "dsdl"  # wrong
  }
  
  sample = {
      "coordinate": [10, False, 12]  # wrong
  }
  ```

### 3. Interval

Interval类型Field用来表示样本中的时间间隔数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

* **数据schema**

  ```python
  data_schema = {  # 无法定义顺序
      "$id": "/special/interval",
      "title": "IntervalField",
      "description": "Interval field in dsdl.",
      "type": "array",
      "items": {
          "type": "number",
      },
      "minItems": 2,
      "maxItems": 2,
  }
  ```

  > 该schema表示传入的值必须要是一个列表，列表中必须包含2个元素，2个元素的类型必须是数字

* **补充校验**

  由于Interval类型还要求列表中的第一个元素小于等于第二个元素，而该规则无法用jsonschema表示，因此dsdl还为这种情况增加了二次校验，Interval Field的二次校验代码为：

  ```python
  def additional_validate(self, value):
      assert value[0] <= value[1]
      return value
  ```

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          interval: Interval
  ```

  ```python
  # 具体样本
  sample = {
      "interval": [10, 12]  # correct
  }
  
  sample = {
      "interval": [12, 10]  # wrong
  }
  
  sample = {
      "interval": "dsdl"  # wrong
  }
  
  sample = {
      "interval": [10, False, 12]  # wrong
  }
  ```

### 4. Date

Date类型Field用来表示样本中的日期数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

* **数据schema**

  ```python
  data_schema = {
      "$id": "/special/date",
      "title": "DateField",
      "description": "Date field in dsdl.",
      "type": "string",
      "format": "date"
  }
  ```

  > 该schema表示传入的值必须要是一个字符串，字符串的形式必须满足[ISO8601 format](https://www.iso.org/iso-8601-date-and-time-format.html)中的Date的格式，即`YYYY-MM-DD`格式

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          date: Date
  ```

  ```python
  # 具体样本
  sample = {
      "date": "2022-12-12"  # correct
  }
  
  sample = {
      "date": "12-12"  # correct
  }
  
  sample = {
      "date": "12"  # wrong
  }
  
  sample = {
      "date": [10, False]  # wrong
  }
  ```

* **数据类**

  在DSDL中，会将传入的满足Date Field规范的值实例化为一个`datetime.date.fromisoformat`对象

### 5. Time

Time类型Field用来表示样本中的时间数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

* **数据schema**

  ```python
  data_schema = {
      "$id": "/special/time",
      "title": "TimeField",
      "description": "Time field in dsdl.",
      "type": "string",
      "format": "time"
  }
  ```

  > 该schema表示传入的值必须要是一个字符串，字符串的形式必须满足[ISO8601 format](https://www.iso.org/iso-8601-date-and-time-format.html)中的Time的格式

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          time: Time
  ```

  ```python
  # 具体样本
  sample = {
      "time": "20:20:39+00:00"  # correct
  }
  
  sample = {
      "time": "20:20:39"  # correct
  }
  
  sample = {
      "time": "12-12"  # wrong
  }
  
  sample = {
      "time": "12::12"  # wrong
  }
  ```

* **数据类**

  在DSDL中，会将传入的满足Time Field规范的值实例化为一个`datetime.time.fromisoformat`对象

### 6. BBox

BBox类型Field用来表示样本中的bounding box数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "properties": {
          "mode": {"type": "string", "enum": ["xywh", "xyxy"]}
      },
      "minProperties": 1,
      "maxProperties": 1,
      "required": ["mode"]
  }
  ```

  > 该jsonschema表示BBox类型传入的参数为`mode`，可以的取值为`xywh`或`xyxy`：
  >
  > 1. `mode=xywh`表示传入的数据会以左上角xy坐标和bbox宽高的形式给出；
  > 2. `mode=xyxy`表示传入的数据会以左上角+右下角的xy坐标的形式给出

* **数据schema**

  ```python
  data_schema = {
      "$id": "/special/bbox",
      "title": "BBoxField",
      "description": "Bounding box field in dsdl.",
      "type": "array",
      "items": {"type": "number"},
      "minItems": 4,
      "maxItems": 4,
  }
  ```

  > 该schema表示传入的值必须要是列表，列表中包含4个元素，这四个元素必须是数字类型。
  >
  > 由于我们希望在mode为`xywh`时，传入的列表的4个元素中，表示wh的后两个元素必须为非负，我们额外为BBox Field设置了一个参数+数据 schema，来规范它的参数与传入数据：
  >
  > ```python
  > whole_schema = {
  >         "type": "object",
  >         "oneOf": [
  >             {
  >                 "properties": {
  >                     "args": {
  >                         "type": "object",
  >                         "properties": {
  >                             "mode": {"type": "string", "enum": ["xywh"]}
  >                         },
  >                         "minProperties": 1,
  >                         "maxProperties": 1,
  >                         "required": ["mode"]
  >                     },
  >                     "value": {
  >                         "type": "array",
  >                         "minItems": 4,
  >                         "maxItems": 4,
  >                         "items": [{"type": "number"}, {"type": "number"}, {"type": "number", "minimum": 0},
  >                                   {"type": "number", "minimum": 0}]
  >                     }
  >                 }
  >             },
  > 
  >             {
  >                 "properties": {
  >                     "args": {"type": "object",
  >                              "properties": {
  >                                  "mode": {"type": "string", "enum": ["xyxy"]}
  >                              },
  >                              "minProperties": 1,
  >                              "maxProperties": 1,
  >                              "required": ["mode"]},
  >                     "value": {"type": "array", "minItems": 4, "maxItems": 4, "items": {"type": "number"}}
  >                 }
  >             }
  >         ],
  >         "required": ["args", "value"]
  >     }
  > ```

* **实例1**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          bbox: BBox
  ```

  ```python
  # 具体样本
  sample = {
      "bbox": [10, 12, 480, 720]  # correct
  }
  
  sample = {
      "bbox": [-1, 12, 40, 80]  # correct
  }
  
  sample = {
      "bbox": [1, 2, -1, 100]  # wrong
  }
  
  sample = {
      "bbox": [1, 2, 10, 10, 1]  # wrong
  }
  ```

* **实例2**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          bbox: BBox[mode=xyxy]
  ```
  
  ```python
  # 具体样本
  sample = {
      "bbox": [10, 12, 480, 720]  # correct
  }
  
  sample = {
      "bbox": [-1, 12, 40, 80]  # correct
  }
  
  sample = {
      "bbox": [1, 2, -1, 100]  # correct
  }
  
  sample = {
      "bbox": [1, 2, 10, 10, 1]  # wrong
  }
  ```


* **数据类**

  在DSDL中，会将传入的满足BBox Field规范的值实例化为一个`dsdl.geometry.BBox`对象，相应的示例代码为：

  ```python
  from dsdl.fields import BBox  # import BBox field
  field = BBox()  # decare the BBox field
  
  data = [10, 12, 60, 70]  # define the data of a bounding box
  bbox_obj = field.validate(data)  # return a dsdl.geometry.BBox object
  ```

  DSDL为用户预设一些常用方法与属性，可以方便用户对bounding box进行操作：

  ```python
  bbox_obj.xyxy  # 输出该bounding box的xyxy形式
  bbox_obj.area  # 输出该bounding box的面积
  bbox_obj.xmin  # 输出该bounding box的左上角点x坐标
  ...
  ```

  > 其他方法与属性可以参考DSDL API文档的dsdl.geometry.BBox部分。

### 7. RotatedBBox

RotatedBBox类型Field用来表示样本中的旋转bounding box数据：

* **声明参数schema**

  ```python
  args_schema = {  # 参数schema
      "type": "object",
      "properties": {
          "measure": {"enum": ["radian", "degree"]},
          "mode": {"enum": ["xywht", "xyxy"]}
      },
      "minProperties": 2,
      "maxProperties": 2,
      "required": ["measure", "mode"]
  }
  
  default_args = {  # 默认参数
      "mode": "xywht",
      "measure": "radian"
  }
  ```

  > `args_schema`约束了在声明RotatedBBox Field时需要指定参数 `mode`与`measure`：
  >
  > 1. mode：表示传入数据的模式，可以选择`xywht`或`xyxy`，默认为`xywht`
  >    1. `xywht`：传入的旋转目标框的值需要是[x, y, w, h, theta]的形式
  >    2. `xyxy`：传入的旋转目标框的值需要是[x1, y1, x2, y2, x3, y3, x4, y4]的形式
  > 2. measure：表示在`xywht`模式下，传入的角度`theta`的单位是弧度还是度数，可以选择`radian`或`degree`，默认为`radian`：
  >    1. `radian`：`xywht`模式下，传入的角度`theta`的单位是弧度
  >    2. `degree`：`xywht`模式下，传入的角度`theta`的单位是度数

* **数据schema**

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

  > 该schema表示传入的值必须要是列表，列表中包含5个元素（rotated bbox的中心点xy坐标、宽高，旋转角度）或8个元素（rotated bbox的四个顶点的xy坐标），元素类型必须是数字类型。
  >
  > * 由于我们希望在mode为`xywht`时，传入的列表为5个元素；mode为`xyxy`时，传入的列表为8个元素，因此我们额外为RotateBBox Field设置了一个参数+数据 schema，来规范它的参数与传入数据：
  >
  >   ```python
  >   whole_schema = {
  >           "type": "object",
  >           "oneOf": [
  >               {
  >                   "properties": {
  >                       "args": {
  >                           "type": "object",
  >                           "properties": {
  >                               "measure": {"enum": ["radian", "degree"]},
  >                               "mode": {"enum": ["xywht"]}
  >                           },
  >                           "minProperties": 2,
  >                           "maxProperties": 2,
  >                           "required": ["measure", "mode"]
  >                       },
  >                       "value": {
  >                           "type": "array",
  >                           "minItems": 5,
  >                           "maxItems": 5,
  >                           "items": [{"type": "number"}, {"type": "number"}, {"type": "number", "minimum": 0},
  >                                     {"type": "number", "minimum": 0}, {"type": "number"}]
  >                       }
  >                   }
  >               },
  >       
  >               {
  >                   "properties": {
  >                       "args": {"type": "object",
  >                                "properties": {
  >                                    "measure": {"enum": ["radian", "degree"]},
  >                                    "mode": {"enum": ["xyxy"]}
  >                                },
  >                                "minProperties": 2,
  >                                "maxProperties": 2,
  >                                "required": ["measure", "mode"]},
  >                       "value": {"type": "array", "minItems": 8, "maxItems": 8, "items": {"type": "number"}}
  >                   }
  >               }
  >           ],
  >           "required": ["args", "value"]
  >       }
  >   ```
  >
  >   

* **实例1**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          rbbox: RotatedBBox  # 默认情况下 mode=xywht, measure=radian
  ```

  ```python
  # 具体样本
  sample = {
      "rbbox": [10, 12, 480, 720, 3.14]  # correct
  }
  
  sample = {
      "rbbox": [-1, 12, -40, 80， 3.14]  # wrong
  }
  
  sample = {
      "rbbox": [12， 12， 12， 13， 14， 13， 14， 12]  # wrong
  }
  ```
  
* **实例2**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          rbbox: RotatedBBox[mode=xyxy]  # 默认情况下 measure=radian
  ```
  
  ```python
  # 具体样本
  sample = {
      "rbbox": [10, 12, 480, 720, 3.14]  # wrong
  }
  
  sample = {
      "rbbox": [-1, 12, -40, 80， 3.14]  # wrong
  }
  
  sample = {
      "rbbox": [12， 12， 12， 13， 14， 13， 14， 12]  # correct
  }
  ```
  
  
  
* **数据类**

  在DSDL中，会将传入的满足RotatedBBox Field规范的值实例化为一个`dsdl.geometry.RBBox`对象，相应的示例代码为：

  ```python
  from dsdl.fields import RotatedBBox  # import RotatedBBox field
  field = RotatedBBox(mode="xywht", measure="radian")  # decare the RotatedBBox field
  
  data = [10, 12, 60, 70, 3.14]  # define the data of a rotated bounding box
  rotated_bbox_obj = field.validate(data)  # return a dsdl.geometry.RBBox object
  ```

  DSDL为用户预设一些常用方法与属性，可以方便用户对rotated bounding box进行操作：

  ```python
  rotated_bbox_obj.polygon_value  # 输出该rotated bounding box的xyxy形式
  rotated_bbox_obj.rbbox_value  # 输出该rotated bounding box的xywht形式
  ...
  ```
  
> 其他方法与属性可以参考DSDL API文档的dsdl.geometry.RBBox部分。

### 8. Polygon

Polygon类型Field用来表示样本中的polygon数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

* **数据schema**

  ```python
  data_schema = {
      "$id": "/special/polygon",
      "title": "PolygonField",
      "description": "Polygon field in dsdl.",
      "type": "array",
      "items": {
          "type": "array",
          "items": {
              "type": "array",
              "items": {"type": "number"},
              "minItems": 2,
              "maxItems": 2,
          }
      }
  }
  ```

  > 该schema表示传入的值必须要是列表，列表中的每个元素也是一个列表（代表一个闭合的polygon），该列表中再嵌套一层列表（代表每个point），最里层列表里包含两个元素，都需要是数字类型，代表这个point的xy坐标。即：
  >
  > ```python
  > polygon = [polygon_item1, polygon_item2, ...]
  > polygon_item = [point1, point2, ...]
  > point = [x, y]
  > ```

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          polygon: Polygon
  ```

  ```python
  # 具体样本
  sample = {
      "polygon": [
          [[10, 12], [480, 720], [11, 360]],
          [[45, 34], [90, 12], [11, 56]]  
      ]  # correct
  }
  
  sample = {
      "polygon": [[10, 12], [480, 720], [11, 360]]  # wrong
  }
  
  sample = {
      "polygon": [
          [[10, 12], [480, 720], [11, 360]],
      ]  # correct
  }
  ```

* **数据类**

  在DSDL中，会将传入的满足Polygon Field规范的值实例化为一个`dsdl.geometry.Polygon`对象，相应的示例代码为：

  ```python
  from dsdl.fields import Polygon  # import Polygon field
  field = Polygon()  # decare the Polygon field
  
  data = [
          [[10, 12], [480, 720], [11, 360]],
          [[45, 34], [90, 12], [11, 56]]  
      ]  # define the data of a polygon
  polygon_obj = field.validate(data)  # return a dsdl.geometry.Polygon object
  ```

  DSDL为用户预设一些常用方法与属性，可以方便用户对bounding box进行操作：

  ```python
  polygon_obj.openmmlabformat  # 将所有的点平铺（与openmmlab存储polygon的格式一致）
  ...
  ```

  > 其他方法与属性可以参考DSDL API文档的dsdl.geometry.Polygon部分。

### 9. Text

Text类型Field用来表示样本中的文本数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

* **数据schema**

  ```python
  data_schema = {
      "$id": "/special/text",
      "title": "TextField",
      "description": "Text field in dsdl.",
      "type": "string"
  }
  ```

  > 该schema表示传入的值必须要字符串类型。

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          txt: Text
  ```

  ```python
  # 具体样本
  sample = {
      "txt": "dsdl"  # correct
  }
  
  sample = {
      "txt": 1  # wrong
  }
  
  sample = {
      "txt": [1, 2, -1, 100]  # wrong
  }
  ```

* **数据类**

  在DSDL中，会将传入的满足Text Field规范的值实例化为一个`dsdl.geometry.Text`对象，相应的示例代码为：

  ```python
  from dsdl.fields import Text  # import Text field
  field = Text()  # decare the Text field
  
  data = "dsdl"  # define the data of a text annotation
  text_obj = field.validate(data)  # return a dsdl.geometry.BBox object
  ```

  DSDL为用户预设一些常用方法与属性，可以方便用户对text标注进行操作：

  ```python
  text_obj.value  # 输出该文本
  ```

  > 其他方法与属性可以参考DSDL API文档的dsdl.geometry.Text部分。

### 10. ImageShape

ImageShape类型Field用来表示样本中的图像尺寸数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "properties": {
          "mode": {
              "type": "string",
              "enum": ["hw", "wh"]
          }
      },
      "minProperties": 1,
      "maxProperties": 1,
      "required": ["mode"]
  }
  
  default_args = {"mode": "hw"}
  ```

  > 声明ImageShape Field需要指定`mode`参数，该参数的值可以是`hw`或`wh`，默认为`hw`：
  >
  > * `hw`：ImageShape传入的值将作为[高，宽]来解析
  > * `wh`：ImageShape传入的值将作为[宽，高]来解析

* **数据schema**

  ```python
  data_schema = {
      "$id": "/special/imageshape",
      "title": "ImageShapeField",
      "description": "ImageShape field in dsdl.",
      "type": "array",
      "items": {"type": "integer", "minimum": 0},
      "minItems": 2,
      "maxItems": 2,
  }
  ```

  > 该schema表示传入的值必须要是列表，元素数目必须是2，元素必须是不小于0的整数。

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          shape: ImageShape[mode=wh]
  ```

  ```python
  # 具体样本
  sample = {
      "shape": [12, 45]  # correct
  }
  
  sample = {
      "shape": [12, -1]  # wrong
  }
  
  sample = {
      "shape": [1, 2, 100]  # wrong
  }
  ```

* **数据类**

  在DSDL中，会将传入的满足ImageShape Field规范的值实例化为一个`dsdl.geometry.ImageShape`对象，相应的示例代码为：

  ```python
  from dsdl.fields import ImageShape  # import ImageShape field
  field = ImageShape()  # decare the ImageShape field
  
  data = [360, 960]  # define the data of a imageshape
  shape_obj = field.validate(data)  # return a dsdl.geometry.ImageShape object
  ```

  DSDL为用户预设一些常用方法与属性，可以方便用户对imageshape标注进行操作：

  ```python
  shape_obj.height  # 输出高
  shape_obj.width  # 输出宽
  ```

  > 其他方法与属性可以参考DSDL API文档的dsdl.geometry.ImageShape部分。

### 11. UniqueID

UniqueID类型Field用来表示样本中的唯一ID数据：

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "properties": {
          "id_type": {"type": ["string", "null"]}
      },
      "minProperties": 1,
      "maxProperties": 1,
      "required": ["id_type"]
  }
  
  default_args = {"id_type": None}
  ```

  > 声明UniqueID Field需要指定`id_type`参数，该参数的值需要是字符串类型或者None，主要用于表示该UniqueID Field是描述什么ID的，默认值为None。

* **数据schema**

  ```python
  data_schema = {
      "$id": "/special/uniqueid",
      "title": "UniqueIDField",
      "description": "UniqueID field in dsdl.",
      "type": "string"
  }
  ```

  > 该schema表示传入的值必须要是字符串。

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          uid: UniqueID[id_type=image_id]  # 用于表示ImageID
  ```

  ```python
  # 具体样本
  sample = {
      "uid": "image001"  # correct
  }
  
  sample = {
      "uid": [12, -1]  # wrong
  }
  
  sample = {
      "uid": 1  # wrong
  }
  ```

* **数据类**

  在DSDL中，会将传入的满足UniqueID Field规范的值实例化为一个`dsdl.geometry.UniqueID`对象，相应的示例代码为：

  ```python
  from dsdl.fields import UniqueID  # import UniqueID field
  field = UniqueID(id_type="image_id")  # decare the UniqueID field
  
  data = "image001"  # define the data of an image id
  uid_obj = field.validate(data)  # return a dsdl.geometry.UniqueID object
  ```

  DSDL为用户预设一些常用方法与属性，可以方便用户对UniqueID进行操作：

  ```python
  uid_obj.value  # 输出id值
  ```

  > 其他方法与属性可以参考DSDL API文档的dsdl.geometry.UniqueID部分。

### 12. InstanceID

InstanceID类型Field可以看作是一种特殊的UniqueID Field，专门用来表示实例的唯一id：

> InstanceId Field等价于`UniqueID[id_type=InstanceID]`

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          ins_id: InstanceID
  ```

  ```python
  # 具体样本
  sample = {
      "ins_id": "instance_001"  # correct
  }
  
  sample = {
      "ins_id": [12, -1]  # wrong
  }
  
  sample = {
      "ins_id": 1  # wrong
  }
  ```

### 13. Label

Label类型Field用来表示样本中的类别标注类型。

* **声明参数**

  由于Label Field用来规范传入的类别标签数据，因此在声明Label Field时我们需要指明该类别标签的`ClassDomain`。下面举一个简单的例子，首先声明一个ClassDomain，然后使用该ClassDomain来声明Label Field：

  ```yaml
  # 定义一个简单的ClassDomain
  COCOClassDemoDom:
      $def: class_domain
      classes:
          - person
          - bicycle
          - car
          - motorcycle
          - airplane
   
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          category: Label[dom=COCOClassDemoDom]
  ```

  通过上述的声明语句，我们定义了一个ClassDomain为COCOClassDemoDom的Label Field。

* **传入数据**

  在传入具体的label数据时，我们首先需要令数据遵循下面的jsonschema：

  ```python
  data_schema = {
      "$id": "/special/label",
      "title": "LabelField",
      "description": "Label field in dsdl.",
      "type": ["string", "integer"]
  }
  ```

  > 传入的值需要是整数类型或者字符串类型

  * 如果传入的数据是整数类型，则dsdl会将其理解为该Label在ClassDomain中的序号：

    ```python
    data = {"category": 1}  # 表示 COCOClassDemoDom的第1个label（即person）
    data = {"category": 5}  # 表示 COCOClassDemoDom的第5个label（即airplane）
    data = {"category": 6}  # error! COCOClassDemoDom中只有5个label
    ```

  * 如果传入的数据是字符串类型，则dsdl会将其理解为该Label的名称或者`<classdomain name>::<label name>`：

    ```python
    data = {"category": "COCOClassDemoDom::person"}  # 表示 COCOClassDemoDom中的person
    data = {"category": "person"}  # 表示 COCOClassDemoDom中的person
    data = {"category": "OtherDom::person"}  # error! OtherDom没有在Label Field中被声明
    data = {"category": "arrow"} # error! COCOClassDemoDom中不存在 arrow
    ```

* **数据类**

  在dsdl中，会将传入的值实例化为一个`dsd.geometry.Label`对象：

  ```python
  from dsdl.geometry import ClassDomain
  from dsdl.fields import Label
  
  # 定义ClassDomain
  ClassDomain(
      name="COCOClassDemoDom",
      classes=["person", "bicycle", "car", "motorcycle", "airplane"],
  )
  
  # 声明LabelField
  field = Label(dom="COCOClassDemoDom")
  
  # 实例化
  data = "COCOClassDemoDom::car"
  label_obj = field.validate(data)
  ```

  DSDL为用户预设一些常用方法与属性，可以方便用户对Label对象进行操作：

  ```python
  label_obj.index_in_domain()  # 返回3，即该类别在classdomain中的序号
  label_obj.category_name  # 返回 car，即该类别的名称
  ```

  > 其他方法与属性可以参考DSDL API文档的dsdl.geometry.Label部分。

### 14. Keypoint

Keypoint类型Field用来表示样本中的关键点类型的数据。

* **声明参数**

  由于关键点检测任务需要我们事先指定一个目标中各个关键点的类型名称以及连结关系，因此在dsdl中我们需要在声明Keypoint Field时指定一个ClassDomain，实例如下：

  ```yaml
  # 定义ClassDomain
  KeyPoint_person_ClassDom:
      $def: class_domain
      classes:
          - left_ankle
          - left_ear
          - left_elbow
          - left_eye
          - left_hip
          - left_knee
          - left_shoulder
          - left_wrist
          - nose
          - right_ankle
          - right_ear
          - right_elbow
          - right_eye
          - right_hip
          - right_knee
          - right_shoulder
          - right_wrist
      skeleton:
          - [16, 14]
          - [14, 12]
          - [17, 15]
          - [15, 13]
          - [12, 13]
          - [6, 12]
          - [7, 13]
          - [6, 7]
          - [6, 8]
          - [7, 9]
          - [8, 10]
          - [9, 11]
          - [2, 3]
          - [1, 2]
          - [1, 3]
          - [2, 4]
          - [3, 5]
          - [4, 6]
          - [5, 7]
  
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          kp: Keypoint[dom=KeyPoint_person_ClassDom]
  ```

  > 其中skeleton字段指明了classes字段中各个关键点的连结关系

  通过了上面的yaml语句，我们声明了一个ClassDomain为KeyPoint_person_ClassDom的Keypoint Field。

* **传入数据**

  在传入具体的keypoint数据时，我们首先需要令数据遵循下面的jsonschema：

  ```python
  data_schema = {
      "$id": "/special/keypoint",
      "title": "KeypointField",
      "description": "Keypoint Field in dsdl.",
      "type": "array",
      "items": {
          "type": "array",
          "items": {
              "type": "number"
          },
          "minItems": 3,
          "maxItems": 3,
      }
  }
  ```

  > 该schema规定，传入的keypoint值必须是一个列表
  >
  > * 该列表的元素也必须是一个元素数目为3，类型为数字类型的列表，表示一个关键点的xy坐标以及是否可见

* **实例**

  ```yaml
  # 定义ClassDomain
  KeypointClassDom:
      $def: class_domain
      classes:
          - hand
          - arm
          - shoulder
          - neck
          - head
      skeleton:
          - [1, 2]
          - [2, 3]
          - [3, 4]
          - [4, 5]
          - [5, 6]
  
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          kp: Keypoint[dom=KeypointClassDom]
  ```

  ```python
  # 具体样本
  sample = {
      "kp": [[1,3,1], [1,4,1], [2,3,1], [3,4,0], [5,5,1]]  # correct
  }
  
  sample = {
      "kp": [12, -1]  # wrong
  }
  
  sample = {
      "kp": 1  # wrong
  }
  ```

* **数据类**

  在DSDL中，会将传入的满足Keypoint Field规范的值实例化为一个`dsdl.geometry.Keypoint`对象，相应的示例代码为：

  ```python
  from dsdl.geometry import ClassDomain
  from dsdl.fields import Keypoint
  
  # 定义ClassDomain
  ClassDomain(
      name="KeypointDom",
      classes=["hand", "arm", "shoulder", "neck", "head"],
      skeleton=[[1,2], [2,3], [3,4], [4,5]]
  )
  
  # 声明LabelField
  field = Keypoint(dom="KeypointDom")
  
  # 实例化
  data = [[1,3,1], [1,4,1], [2,3,1], [3,4,0], [5,5,1]]
  kp_obj = field.validate(data)
  ```

  DSDL为用户预设一些常用方法与属性，可以方便用户对Keypoint对象进行操作：

  ```python
  kp_obj.points  # 返回所有点的xy坐标
  kp_obj.visables  # 所有点是否可见
  ```

  > 其他方法与属性可以参考DSDL API文档的dsdl.geometry.Keypoint部分。

## 媒体类型Field

### 1. Image

Image类型Field用来表示图像数据

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

* **传入数据schema**

  ```python
  data_schema = {
      "$id": "/unstructure/image",
      "title": "ImageField",
      "description": "Image field in dsdl.",
      "type": "string",
  }
  ```

  > Image Field的传入数据只要求是字符串即可，该字符串一般是图像的相对路径

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          img: Image
  ```

  ```python
  # 具体样本
  sample = {
      "img": "dsdl.jpg"  # correct
  }
  
  sample = {
      "img": 10.4  # wrong
  }
  
  sample = {
      "img": True  # wrong
  }
  ```

* **数据类**

  在DSDL中，会将传入的满足Image Field规范的值实例化为一个`dsdl.geometry.Image`对象，相应的示例代码为：

  ```python
  from dsdl.fields import Image  # import Image field
  from dsdl.objectio import LocalFileReader
  field = Image()  # declare the Image field
  file_reader = LocalFileReader(working_dir="the/dir/of/images")
  field.set_file_reader(file_reader)  # declare the file reader
  data = "1.jpg"
  img_obj = field.validate(data)  # return a dsdl.geometry.Image object
  ```

  > 由于在标注文件中，一般情况下只会提供Image的相对路径，所以我们在上面的代码中需要为Image Field对象指定一个file reader对象，从而告诉dsdl从哪里读取该图片

  DSDL为用户预设一些常用方法与属性，可以方便用户对Image对象进行操作：

  ```python
  img_obj.to_image()  # 将图像转换为PIL.Image对象
  img_obj.to_array()  # 将图像转换为numpy.ndarray对象
  ...
  ```

  > 其他方法与属性可以参考DSDL API文档的`dsdl.geometry.Image`部分。

### 2. LabelMap

LabelMap类型Field用来表示语义分割图

* **声明参数**

  由于语义分割任务需要事先指定一个ClassDomain，因此在声明LabelMap Field时需要指定它的ClassDomain。指定方法和Label Field、Keypoint Field类似：

  ```yaml
  # 定义一个简单的ClassDomain
  COCOClassDemoDom:
      $def: class_domain
      classes:
          - person
          - bicycle
          - car
          - motorcycle
          - airplane
   
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          labelmap: LabelMap[dom=COCOClassDemoDom]
  ```

  > 通过上面的yaml语句，声明了一个class domain为COCOClassDemoDom的LabelMap Field

* **传入数据schema**

  ```python
  data_schema = {
      "$id": "/unstructure/labelmap",
      "title": "LabelMapField",
      "description": "LabelMap field in dsdl.",
      "type": "string",
  }
  ```

  > LabelMap Field的传入数据只要求是字符串即可，该字符串一般是图像的相对路径

* **实例**

  ```yaml
  # 定义一个简单的ClassDomain
  COCOClassDemoDom:
      $def: class_domain
      classes:
          - person
          - bicycle
          - car
          - motorcycle
          - airplane
   
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          labelmap: LabelMap[dom=COCOClassDemoDom]
  ```

  ```python
  # 具体样本
  sample = {
      "labelmap": "dsdl_label.jpg"  # correct
  }
  
  sample = {
      "labelmap": 10.4  # wrong
  }
  
  sample = {
      "labelmap": True  # wrong
  }
  ```

* **数据类**

  在DSDL中，会将传入的满足LabelMap Field规范的值实例化为一个`dsdl.geometry.LabelMap`对象，相应的示例代码为：

  ```python
  from dsdl.fields import LabelMap, ClassDomain  # import LabelMap field
  from dsdl.objectio import LocalFileReader
  
  # 定义ClassDomain
  ClassDomain(
      name="COCOClassDemoDom",
      classes=["person", "bicycle", "car", "motorcycle", "airplane"],
  )
  
  field = LabelMap(dom="COCOClassDemoDom")  # declare the LabelMap field
  file_reader = LocalFileReader(working_dir="the/dir/of/label/images")
  field.set_file_reader(file_reader)  # declare the file reader
  data = "1.jpg"
  labelmap_obj = field.validate(data)  # return a dsdl.geometry.LabelMap object
  ```

  > 由于在标注文件中，一般情况下只会提供Image的相对路径，所以我们在上面的代码中需要为LabelMap Field对象指定一个file reader对象，从而告诉dsdl从哪里读取该图片

  DSDL为用户预设一些常用方法与属性，可以方便用户对labelmap image对象进行操作：

  ```python
  labelmap_obj.to_image()  # 将分割图像转换为PIL.Image对象
  labelmap_obj.to_array()  # 将分割图像转换为numpy.ndarray对象
  ...
  ```

  > 其他方法与属性可以参考DSDL API文档的`dsdl.geometry.LabelMap`部分。

### 3. InstanceMap

InstanceMap类型Field用来表示实例分割图

* **声明参数schema**

  ```python
  args_schema = {
      "type": "object",
      "minProperties": 0,
      "maxProperties": 0,
  }
  ```

* **传入数据schema**

  ```python
  data_schema = {
      "$id": "/unstructure/instancemap",
      "title": "InstanceMapField",
      "description": "InstanceMap field in dsdl.",
      "type": "string",
  }
  ```

  > InstanceMap Field的传入数据只要求是字符串即可，该字符串一般是图像的相对路径

* **实例**

  ```yaml
  # Struct 定义
  LocalObjectEntry:
      $def: struct
      $fields:
          insmap: InstanceMap
  ```

  ```python
  # 具体样本
  sample = {
      "insmap": "dsdl_instance.jpg"  # correct
  }
  
  sample = {
      "insmap": 10.4  # wrong
  }
  
  sample = {
      "insmap": True  # wrong
  }
  ```

* **数据类**

  在DSDL中，会将传入的满足Image Field规范的值实例化为一个`dsdl.geometry.InstanceMap`对象，相应的示例代码为：

  ```python
  from dsdl.fields import InstanceMap  # import InstanceMap field
  from dsdl.objectio import LocalFileReader
  field = InstanceMap()  # declare the InstanceMap field
  file_reader = LocalFileReader(working_dir="the/dir/of/instance_images")
  field.set_file_reader(file_reader)  # declare the file reader
  data = "1.jpg"
  ins_obj = field.validate(data)  # return a dsdl.geometry.Image object
  ```

  > 由于在标注文件中，一般情况下只会提供InstanceMap的相对路径，所以我们在上面的代码中需要为InstanceMap Field对象指定一个file reader对象，从而告诉dsdl从哪里读取该图片

  DSDL为用户预设一些常用方法与属性，可以方便用户对Instance 图像进行操作：

  ```python
  ins_obj.to_image()  # 将实例图像转换为PIL.Image对象
  ins_obj.to_array()  # 将实例图像转换为numpy.ndarray对象
  ...
  ```

  > 其他方法与属性可以参考DSDL API文档的`dsdl.geometry.InstanceMap` 部分。
