### **环境依赖**

- Python3.8+

### **DSDL-SDK安装**

为了使用DSDL相关的功能，我们推荐安装DSDL-SDK。提供两种安装方式：

#### 1. pip 安装

```shell
pip install dsdl
```

#### 2. 源码安装（推荐）

由于DSDL正在开发内测阶段，推荐使用源码安装，以获取最新的版本更新。

```shell
git clone -b dev-alg https://github.com/opendatalab/dsdl-sdk.git
cd dsdl
python setup.py install
```

### **OpenDataLab-CLI安装**

为了更方便地获取原始数据集和DSDL数据集，推荐用户下载OpenDataLab CLI工具。

#### 1. pip 安装

```shell
# 安装
pip install opendatalab

# 版本升级
pip install -U opendatalab
```

#### 2. 数据集获取

```shell
odl login                       # 登录
odl info <数据集唯一标识名>      # 查看此数据集的元数据
odl ls   <数据集唯一标识名>      # 查看此数据集的文件列表
odl get  <数据集唯一标识名>      # 下载此数据集
```

数据集唯一标识名可以在[OpenDataLab官网](https://opendatalab.com/)获取，此外，数据集也可以从网页端直接下载。
