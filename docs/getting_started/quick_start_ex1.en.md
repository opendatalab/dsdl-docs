## Get Started

#### Use dsdl parser to deserialize the Yaml file to Python code

```shell
dsdl parse --yaml demo/coco_demo.yaml
```

#### Modify the configuration & set the directory of media in dataset

Create a configuration file `config.py` with the following contents（for now dsdl only reading from aliyun oss or local is supported）：

```python
local = dict(
    type="LocalFileReader",
    working_dir="local path of your media",
)

ali_oss = dict(
    type="AliOSSFileReader",
    access_key_secret="your secret key of aliyun oss",
    endpoint="your endpoint of aliyun oss",
    access_key_id="your access key of aliyun oss",
    bucket_name="your bucket name of aliyun oss",
    working_dir="the relative path of your media dir in the bucket")
```

In `config.py`, the configuration of how to read the media in a dataset is defined. One should specify the arguments depending on from where to read the media：

1. read from local： `working_dir` field in `local` should be specified (the directory of local media)
2. read from aliyun oss： all the field in `ali_oss<span> </span>`should be specified (including `access_key_secret`, `endpoint`, `access_key_id`, `bucket_name`, `working_dir`)

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
