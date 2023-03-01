# 数据集可视化

数据集可视化目前支持CLI版本，后续会开发网页版本。

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
