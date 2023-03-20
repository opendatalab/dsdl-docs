# 数据集可视化

这里提供两种可视化方法，一种是python代码，一种是命令行工具。

## Python

使用PIL库，我们可以方便的对图片进行可视化，这里给出目标检测任务可视化的实例代码：

```
from dsdl.dataset import DSDLDataset
from PIL import Image, ImageDraw

# train_yaml = "~/datasets/VOC07-det/dsdl/set-train/train.yaml"
val_yaml = "~/datasets/VOC07-det/dsdl/set-val/val.yaml"

loc_config = dict(
    type="LocalFileReader",
    working_dir="~/datasets/VOC07-det/original"
)

# 初始化Dataset
# ds_train = DSDLDataset(dsdl_yaml=train_yaml, location_config=loc_config)
ds_val = DSDLDataset(dsdl_yaml=val_yaml, location_config=loc_config)

# 获取索引为1的样本
example = ds_val.sample_list[1]

# 提取图片
img = example.media.image.to_image().convert(mode='RGB')

# 定义Draw方法
draw = ImageDraw.Draw(img)

# 迭代绘制标注框及其类别名称
for i in range(len(example.objects)):
    draw.rectangle(example.objects[i].bbox.xyxy, width=2)
    x,y,w,h = example.objects[i].bbox.xywh
    draw.text((x,y), example.objects[i].category.name)

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
