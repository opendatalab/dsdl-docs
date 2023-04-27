## 2.3 非结构化对象类

**非结构化对象**，比如图像，视频，语音，点云以及文本，这些都是现实世界物体的数字化表示。尽管这些数据的内部结构很丰富，在数据集描述文件中，他们还是被当作是一个整体，其内部结构并不会被表现出来。

在DSDL中，一个**非结构化对象类**是对所有特定类型非结构化对象的抽象。

### 2.3.1 预定义的非结构化对象类

在标准库内，DSDL提供了下面几个开箱即用的非结构化对象类：

+ `Image`：每个实例都是一张图像，可以通过像素的矩阵来表示。
+ `Video`：每个实例可以被解码为一个序列的视频帧，每个视频帧都是一张图像。
+ `Text`：每个实例都是一个单词序列。
+ `PointCloud`：每个实例都是3D点的集合，用来表示一个3D对象的形状。
+ `LabelMap`：每个实例都是整型标注的组成的矩阵，每个整型标注对应了一个类别。

### 2.3.2 描述一个非结构化对象

在DSDL中，一个非结构化对象可以通过一个对象定位器和其他属于该对象的参数来声明。

拿一张路径为`abc/0001.jpg`为例，它可以使用下面的方式来表示：

* **目标定位器**：使用目标定位器`abc/0001.jpg`。当一个变量或者一个字段有一个非结构化目标类的数据类型并且它的值为一个字符串，则该字符串将被解析为一个目标定位器。

### 2.3.3 扩展非结构化对象类

DSDL允许用户通过指定如何从存储中加载对象来注册**扩展非结构化对象类**。

在客户端，可以通过定义一个抽象基类`UnstructuredObject`的子类并实现其`load`方法来进行对象加载，从而实现扩展非结构化对象类。

具体来讲，在Python中，抽象基类`UnstructuredObject`通过下面的方式定义：

```python
from abc import ABC, abstractmethod

class UnstructuredObject(ABC):
    """Abstract base class for unstructured objects."""

    @abstractmethod
    def load(file, descr):
        """Load an unstructured object from a given file-like object.
        
        Arguments:
            file:   file-like, from which the unstructured object is loaded.
            descr:  dict-like, which provides the descriptive information.

        Returns:
            The loaded object.
        """
        pass
```

> **注意**：这里的`load`方法需要接收一个已经打开的文件对象，而不是一个文件路径。该设计是基于“关注点分离”原则：数据系统有责任去解析对象定位器并且构建一个对应的文件阅读器。因此`UnstructuredObject`类的子类只需要考虑在给定一个文件阅读器后，如何加载，解析与验证对象。