# 基于DSDL数据的训练推理（Pytorch）
这里以MNIST为例，展示dsdl如何在Pytorch框架上进行训练。

## **1. 初始化Dataset**
dsdl提供了DSDLDataset类，可以很好的支持Pytorch训练，只需要dsdl的yaml文件和location config，即可初始化一个DSDLDataset类，代码如下：

```
from dsdl.dataset import DSDLDataset

loc_config = dict(
    type="LocalFileReader",
    working_dir="path to MNIST original"
)

train_yaml = "path to MNIST dsdl train yaml file"
val_yaml = "path to MNIST dsdl val yaml file"

fields_list = ["Image", "Label"]

ds_train = DSDLDataset(dsdl_yaml=train_yaml, location_config=loc_config, required_fields=fields_list)
ds_val = DSDLDataset(dsdl_yaml=val_yaml, location_config=loc_config, required_fields=fields_list)

```

代码中，field_list参数是用来告诉程序，用户所需要的字段是哪些（如果没有给定的话，会默认提取主要字段），这里我们以分类任务为例，提取数据的'Image', 'Label'两个字段。

<a id="pipline"></a>

## **2. 定义预处理pipline并生成Dataloader**

DSDLDataset 支持调用set_transform()方法来定义数据处理pipline，如下所示，我们定义了对图片进行读取 -> 转为tensor -> 标准化等处理流程, 同时也定义了对标签的处理流程。
```
import numpy as np
from torchvision import transforms

T = {
    "Image": transforms.Compose([
        lambda x: x[0].to_image().convert(mode='RGB'),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    "Label": transforms.Compose([
        lambda x: np.array([x[0].index_in_domain() - 1])
    ])
}

ds_train.set_transform(T)
ds_val.set_transform(T)
```

DSDLDatset类拥有直接输出pytorch DataLoader的接口，调用代码如下：

```
dl_train = ds_train.to_pytorch(batch_size=32)
dl_val = ds_val.to_pytorch(batch_size=32)
```
to_pytorch方法同样支持传递一些其他参数，比如shuffle，num_works等等，具体可以参考Pytorch的[DataLoader类](https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader)。

## **3. 定义模型和优化器**

这里我们定义一个简单的resnet18分类器, 并采用SGD优化器，同时定义交叉熵损失函数：

```
import torch
from torchvision import models

model = models.resnet18(pretrained=False)

class_nums = 1000
model.fc = torch.nn.Linear(model.fc.in_features, class_nums)  

device = torch.device("cuda:0")
# device = "cpu" # use cpu if cuda is not available

model.to(device)

criterion = torch.nn.CrossEntropyLoss()

optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.1)
```

## **4. 进行训练**

定义训练流程:

```
import time

def train_one_epoch(model, optimizer, data_loader, device, image_key = 'Image', label_key = 'Label'):

    model.train()

    running_loss = 0.0
    start_time = time.time()
    total = 0
    correct = 0
    
    for i, data in enumerate(data_loader):
        # get the inputs; data is a dict contains image and label
        inputs = data[image_key]
        labels = torch.squeeze(data[label_key])

        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(inputs.float())
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        accuracy = 100 * correct / total
    
        running_loss += loss.item()
        if i % 100 == 0 and i > 0:
            batch_time = time.time()
            cost = (batch_time-start_time)
            print('    [%5d] loss: %.3f, time cost: %.2f, accuracy: %.2f %%' %
                  (i, running_loss, cost, accuracy))

            running_loss = 0.0
            total = 0
            correct = 0
```

开始训练：

```
num_epochs = 5
for epoch in range(num_epochs):
    print("------------------ Training Epoch {} ------------------".format(epoch+1))
    train_one_epoch(model, optimizer, dl_train, device)
```

出现如下训练日志时表示数据正常训练：

```
------------------ Training Epoch 1 ------------------
    [  100] loss: 77.967, time cost: 4.43, accuracy: 86.63 %
    [  200] loss: 14.327, time cost: 8.68, accuracy: 95.75 %
    [  300] loss: 9.919, time cost: 12.98, accuracy: 97.05 %
    [  400] loss: 8.642, time cost: 17.23, accuracy: 97.47 %
    [  500] loss: 8.459, time cost: 21.56, accuracy: 97.40 %
------------------ Training Epoch 2 ------------------
    [  100] loss: 5.610, time cost: 4.40, accuracy: 98.29 %
    [  200] loss: 4.055, time cost: 8.73, accuracy: 98.83 %
    [  300] loss: 3.560, time cost: 13.00, accuracy: 98.91 %
    [  400] loss: 3.555, time cost: 17.31, accuracy: 98.99 %
    [  500] loss: 3.243, time cost: 21.60, accuracy: 99.09 %
------------------ Training Epoch 3 ------------------
    [  100] loss: 2.235, time cost: 4.37, accuracy: 99.46 %
    [  200] loss: 1.480, time cost: 8.69, accuracy: 99.72 %
    [  300] loss: 1.259, time cost: 12.98, accuracy: 99.73 %
    [  400] loss: 1.315, time cost: 17.27, accuracy: 99.72 %
    [  500] loss: 1.207, time cost: 21.55, accuracy: 99.77 %
------------------ Training Epoch 4 ------------------
    [  100] loss: 0.816, time cost: 4.36, accuracy: 99.88 %
    [  200] loss: 0.483, time cost: 8.67, accuracy: 99.98 %
    [  300] loss: 0.510, time cost: 12.98, accuracy: 99.94 %
    [  400] loss: 0.476, time cost: 17.26, accuracy: 99.94 %
    [  500] loss: 0.407, time cost: 21.56, accuracy: 99.97 %
------------------ Training Epoch 5 ------------------
    [  100] loss: 0.315, time cost: 4.40, accuracy: 99.99 %
    [  200] loss: 0.224, time cost: 8.78, accuracy: 100.00 %
    [  300] loss: 0.237, time cost: 13.09, accuracy: 100.00 %
    [  400] loss: 0.226, time cost: 17.40, accuracy: 100.00 %
    [  500] loss: 0.210, time cost: 21.67, accuracy: 100.00 %
```

## **5. 进行测试**

定义测试流程如下：

```
def test_model(model, data_loader, device, image_key = 'Image', label_key = 'Label'):

    model.eval()

    start_time = time.time()
    total = 0
    correct = 0
    with torch.no_grad():
        for i, data in enumerate(data_loader):
            # get the inputs; data is a dict contains image and label
            inputs = data[image_key]
            labels = torch.squeeze(data[label_key])

            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(inputs.float())

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        accuracy = 100 * correct / total
            
        print('    Testing accuracy: %.2f %%' %(accuracy))
```

开始在测试集上进行测试：

```
test_model(model, dl_val, device)

```
测试结果如下：

```
Testing accuracy: 99.04 %
```

可以看到，MNIST整体相对比较简单，resnet18经过5个epoch的训练，即可在测试集达到99.04的精度。

完整的代码请参考[`pytorch_classification.py`](./demo_code/pytorch/pytorch_classification.py). 


## **拓展阅读**


### A. set_transform 和  pre_transform

DSDLDatset支持两种定义预处理pipline的方法，`pre_transform`和`set_transform`，两者的调用方式完全相同，区别如下：

- **pre_transform**会在定义处理流程的时候将内存中的数据同步走一遍pipline，

- **set_transform**则不会在定义的时候进行，而是在训练迭代的时候才进行pipline操作。

通常情况下，如果数据集不大，且pipline操作是固定的，我们建议采用前者，这会使训练迭代过程加速很多，而如果数据集较大（出现内存不够的情况）或者pipline中需要进行一些随机性的操作（比如进行随机的数据增强），则推荐使用后者。此外，用户也可以同时使用两种方法，只需要注意和pre_transform的输出和set_transform 的输入能够对接即可。


### B. Field的内置方法

在本教程第二节，关于[定义预处理pipline](#pipline)部分的代码，我们使用了两个Field内置方法，分别为Image Field的`to_image()`以及Label Field的`index_in_domain()`方法，前者能获取读取后的图片（PIL读取方式），后者则能快速获取指定类别在ClassDom中的索引信息（从1开始）。实际上，在DSDL中，我们将各个Field常见的处理方法都写进了Field的内置方法，用户能很方便的对其进行转换或者处理。更多Field的内置方法可以参考[API接口文档](../../api_reference/fields_overview.zh.md).
