# **数据集配置**


在dsdl中为了数据集方便分发，我们提出了【媒体数据】和【标注文件】分离这一设计理念，这样即便用户把不同数据保存在不同的存储上，也无需修改dsdl yaml文件，仅需修改对应的config文件即可，这里的数据集配置也主要是指对config文件的适配，结合实际情况，有以下两种情况：

1. 用户通过odl get获取的dsdl数据集，同时包含【原始媒体数据】和【dsdl标注文件】，用户需要；
2. 对于本地或者远端已经拥有下载好的【原始媒体数据】，同时还希望使用dsdl相关配套工具的用户，可以只下载对应数据集的【dsdl标注文件】，同时修改其中的 `config.py`文件即可；

在 `config.py`中，列举了所支持的媒体文件读取方式，根据实际情况选择并配置文件路径等信息：

1. 本地读取： `local`中的参数 `working_dir`（本地数据所在的目录）
2. 阿里云OSS读取： `ali_oss`中的参数（阿里云OSS的配置 `access_key_secret`, `endpoint`, `access_key_id`；桶名称 `bucket_name`，数据在桶中的目录 `working_dir`。关于阿里云OSS参数配置中相关字段的详细含义和配置方法，请参考其官方文档：[配置教程](https://help.aliyun.com/document_detail/474474.html)）

完整的config.py文件示例如下：

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
