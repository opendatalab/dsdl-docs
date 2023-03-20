# **dataset configuration**

Users who downloaded original dataset, can pull dsdl file and modify it's location configuration, it works too.

we use `config.py` to set dataset's location configuration, it supports two type locations:

1. load form local： set `type = LocalFileReader`, and change `working_dir` to actual path.
2. load from ali-oss： set `type = AliOSSFileReader`, then input your identification such as `access_key_secret`, `endpoint`, `access_key_id`, you also need to set `bucket_name` and `working_dir` so the loader can find your dataset.

an example of `config.py` file shown as:

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