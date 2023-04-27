# 数据集可视化

这里提供两种可视化方法，一种是python代码，一种是命令行工具。

## Python

使用PIL库，我们可以方便的对图片进行可视化，这里给出目标检测任务可视化的实例代码：

```python
import random
from dsdl.dataset import DSDLDataset
from PIL import Image, ImageDraw

val_yaml = "~/data/VOC07-det/dsdl/set-val/val.yaml"

loc_config = dict(
    type="LocalFileReader",
    working_dir="~/data/VOC07-det/original"
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

#### Visualize samples

```shell
dsdl view -y <yaml-name>.yaml -c <config.py> -l ali-oss -n 10 -r -v -f Label BBox Attributes
```

The description of each argument is shown below:

| simplified argument | argument        | description                                                                                                                                                                                                                                            |
| ------------------- | --------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -y                  | `--yaml`      | The path of dsdl yaml file.                                                                                                                                                                                                                            |
| -c                  | `--config`    | The path of location configuration file.                                                                                                                                                                                                               |
| -l                  | `--location`  | `local` or `ali-oss`，which means read media from local or aliyun oss.                                                                                                                                                                             |
| -n                  | `--num`       | The number of samples to be visualized.                                                                                                                                                                                                                |
| -r                  | `--random`    | Whether to load the samples in a random order.                                                                                                                                                                                                         |
| -v                  | `--visualize` | Whether to visualize the samples or just print the information in console.                                                                                                                                                                             |
| -f                  | `--field`     | The field type to visualize, e.g.`-f BBox`means show the bounding box in samples, `-f Attributes`means show the attributes of a sample in the console . One can specify multiple field types simultaneously, such as `-f Label BBox Attributes`. |
| -t                  | `--task`      | The task you are working on, for example,`-t detection` is equivalent to `-f Label BBox Polygon Attributes`.                                                                                                                                       |


可视化的结果如下：
<center>
<img src="https://user-images.githubusercontent.com/113978928/232955194-638f0107-fcd4-4d34-bdac-753a6706cf28.png">
</center>