# 数据集分析和统计信息

该文档将包含数据集分析和统计的信息。

也将分为CLI和网页版。


## CLI

（由徐超老师组补充）


## 网页版统计信息展示

（由开发组补充）



## 自动化验证中的统计信息展示

（由于CLI和网页版都还未支持，这里先提供一个我们的数据集验证中的统计信息展示方法）


### 调用方法：

```Python
dsdl check -y xxx.yaml -c config.py -l ali-oss -t detection -p ./ -o ./

### -y 为输入的yaml文件
### -c 为数据集的读取配置（记录了数据集在阿里云/本地的位置），主要形式如下：
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
### -l 为指定位置，可以选择使用 ali-oss 或 local
### -t 为指定当前yaml的任务类别，当前支持的任务类别有（detection，segmentation，classification）
### -p yaml文件导入的库文件所在的路径地址
### -o 为输出的文件夹，包含图片和md文档，注意打包下载
```



### 报告样式：

报告分为3个部分：

- parser检查结果：结果包括了parse结果是否成功，如果不成功，则可以查看具体的报错信息
- samples实例化检查结果：其中报告说明了当前数据集共有样本个数，正常样本个数，警告样本个数，错误样本个数，并提供了异常样本的具体信息日志。
- 可视化结果：需要肉眼观察可视化结果是否正确，比如bbox位置是否正确，标签内容是否正确等，在图片下面展示了可视化过程中的日志内容，比如是可视化成功还是失败，以及失败日志等。
