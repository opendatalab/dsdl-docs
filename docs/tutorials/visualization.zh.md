# 数据集可视化

这里提供两种可视化方法，一种是python代码，一种是命令行工具。

## Python

使用PIL库，我们可以方便的对图片进行可视化，这里给出目标检测任务可视化的实例代码：

```python
import random
from dsdl.dataset import DSDLDataset
from PIL import Image, ImageDraw

val_yaml = "~/data/PASCAL_VOC2007/dsdl/set-val/val.yaml"

loc_config = dict(
    type="LocalFileReader",
    working_dir="~/data/PASCAL_VOC2007/original"
)

# 初始化Dataset
ds_val = DSDLDataset(dsdl_yaml=val_yaml, location_config=loc_config)

# 获取索引为0的样本
example = ds_val[0]
# print(example)

# 提取图片
img = example.Image[0].to_image().convert(mode='RGB')

# 定义Draw方法
draw = ImageDraw.Draw(img)

# 迭代绘制标注框及其类别名称
for i in range(len(example.Bbox)):
    color = (random.randint(0,250), random.randint(0,250), random.randint(0,250))
    draw.rectangle(example.Bbox[i].xyxy, width=2, outline=color)
    x,y,w,h = example.Bbox[i].xywh
    draw.text((x,y), example.Label[i].name)

# 展示绘图结果
img
```

## CLI

#### 可视化samples

```shell
dsdl view -y <yaml-name>.yaml -c <config.py> -l ali-oss -n 10 -r -v -f Label BBox Attributes
```

每个参数的描述如下：

| 缩写 | 参数 | 描述 |
| ------------------- | --------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-y`                  | `--yaml`      | dsdl yaml 文件的路径 |
| `-c`                  | `--config`    | config文件的路径 |
| `-l`                  | `--location`  | 可取`local` 或 `ali-oss`，分别代表从本地或阿里云oss读取媒体文件 |
| `-n`                  | `--num`       | 可视化的样本数量 |
| `-r`                  | `--random`    | 是否以随机的方式从数据集中读取一批样本 |
| `-v`                  | `--visualize` | 加上该参数会实际地执行可视化操作，否则仅将样本信息打印到控制台 |
| `-t`                  | `--task`      | 指定当前yaml的任务类别，当前支持的任务类别及可视化的类型将会在后文展示 |
| `-f`                  | `--field`     | 指定可视化的类型，如果不指定-t, 也可以直接指定-f来选择希望可视化的类型，当前支持的可视化类型将会在后文展示 |


当前支持的可视化类型见FIELDS字段，任务类别及其对应的Field种类见TASK_FIELDS字段：
```python
FIELDS = ["image", "label", "bbox", "polygon", "keypoint", "rotatedbbox", "labelmap", "instancemap", "text"]

TASK_FIELDS = {
    "detection": ["image", "label", "bbox", "polygon", "keypoint", "rotatedbbox"],
    "classification": ["image", "label"],
    "semantic-seg": ["image", "labelmap"],
    "panoptic-seg": ["image", "labelmap", "instancemap"],
    "ocr": ["image", "rotatedbbox", "text", "polygon"]
}
```

可视化的结果如下：
<center>
<img src="https://user-images.githubusercontent.com/113978928/232955194-638f0107-fcd4-4d34-bdac-753a6706cf28.png">
</center>