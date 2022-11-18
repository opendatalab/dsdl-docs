
# 目标检测任务
为了制定目标检测任务数据集描述文件的模板，我们对主流的目标检测任务数据集进行了调研，分析其任务的目的和常见标注信息所包含的字段，从中整理出共享字段和独立字段，并在此基础上制定检测任务数据集描述文件的通用模板。
# 1. 任务调研
## 1.1 任务定义
目标检测任务是指在图像中用矩形框的形式检测出物体的位置，并识别其所属类别。其示意图(该图片和标注信息来自coco数据集)如下所示：

![img](img/det_example.png)

## 1.2 评价指标：

目标检测最常用的评价指标就是AP（**A**verage **P**recision），此外还有一些基于AP衍生的指标，这些指标的含义如下：

- **AP**

PR曲线中和横坐标轴围成区域的面积。

- **11-point interpolation**

为了简化AP计算，有时候采用11-point计算方法（如VOC数据集的metric），相当于计算recall=[0, 0.1, 0.2, ... , 1]这11个点处precision值的平均值（某处不存在的话取右侧最大值），计算公式如下：

$$ AP= {1\over11} \sum_{
\begin{subarray}{l}
   i\in\{0, 0.1, 0.2 ..., 1\}\\
\end{subarray}} \rho_{interp}(r) $$

$$ \rho_{interp}(r) = \max_{
\begin{subarray}{l}
   \tilde{r}:\tilde{r}\geq r
\end{subarray}} \rho(\tilde{r}) $$

- **mAP**

所有的类别的AP求平均

- **mAP@0.5 和 mAP@0.5~0.95**

这里的0.5和0.95都是前文介绍混淆矩阵提到的阈值，也就是在不同阈值下进行的AP计算。mAP@0.5也就是阈值等于0.5的时候所计算的mAP，mAP@0.5~0.95则表示阈值从0.5到0.95分别计算mAP，然后在求平均。voc数据集中采用的是mAP@0.5，通常也叫AP_50, coco数据集中采用的是mAP@0.5~0.95，通常简称为mAP。（相同的检测器，mAP一般低于AP_50）

- **mAP_s，mAP_m，mAP_l**

这里的s、m、l代表的是物体尺寸，是coco的metric会把box分为不同尺寸，来查看模型对不同尺寸box的检测效果。

<a id="table-1"></a>

## 1.3 主流数据集调研： 
我们调研了10个主流检测数据集，其中包含了COCO、VOC等常见数据集。为了使得模板更加通用，同时也具备拓展能力，我们着重关注各个数据集之间的共性和特性，此外，调研过程会遇到一些名称不同，但是实际含义相同或类似的字段，这些字段我们也视为同一字段，并统一去称呼，比如image_id字段一般表示图片的路径或者id，他是图片的唯一标识；label_id则表示图片的类别，可以用数字表示，也可以用字符串表示；bbox则表示一个目标边界框的坐标。完整的字段调研结果如下表所示： 
<table border="4" >
        <tr>
      <th rowspan="2" align=center colspan="1" align=center>目标检测数据集</th>
      <th colspan="3" align=center>共享字段</th>
      <th colspan="9" align=center>独立字段</th>
    </tr>
    <tr>
      <th>image_id</th>
      <th>label_id</th>
      <th>bbox</th>
      <th>iscrowd</th>
      <th>istruncated</th>
      <th>isdifficult</th>
      <th>isoccluded</th>
      <th>isdepiction</th>
      <th>isreflected</th>
      <th>isinside</th>
      <th>confidence</th>
      <th>pose</th>
    </tr>
    <tr>
      <th width="15%" >VOC</th>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
    </tr>
    <tr>
      <th width="15%" >COCO</th>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
    </tr>
    <tr>
      <th width="15%" >KITTI</th>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
    </tr>
    <tr>
      <th width="15%" >OpenImages</th>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
    </tr>
    <tr>
      <th width="15%" >Objects365</th>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
    </tr>
    <tr>
      <th width="15%" >ILSVRC2015</th>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
    </tr>
    <tr>
      <th width="15%" >LVIS</th>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center">Y</td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
      <td width="8%" align="center"></td>
    </tr>
  </table>

 - 补充字段总结：
 <table border="4" >
    <tr>
      <th align="center" >字段类型</th>
      <th align="center" >字段名称</th>
      <th align="center" >含义</th>
    </tr>
    <tr>
      <th rowspan="3">共享字段</th>
      <th>image_id</th>
      <td>定位到唯一图片，比如用图片名或者图片路径表示</td>
    <tr>
      <th>label_id</th>
      <td>单个目标所属的类别</td>
    <tr>
      <th>bbox</th>
      <td>定位单个目标的矩形框，比如用[xmin, ymin, xmax, ymax]表示</td>
    </tr>
    <tr>
      <th rowspan="9">独立字段</th>
      <th>iscrowd</th>
      <td>是否为一群密集目标，比如人群，一堆苹果</td>
    <tr>
      <th>istruncated</th>
      <td>目标是否被截断，即目标部分处于图片之外</td>
    </tr>
    <tr>
      <th>isdifficult</th>
      <td>是否为检测困难的目标</td>
    <tr>
      <th>isoccluded</th>
      <td>目标是否被遮挡</td>
    </tr>
    <tr>
      <th>isdepiction</th>
      <td>是否为卡通形象、绘画等等，非实际个体</td>
    </tr>
    <tr>
      <th>isreflected</th>
      <td>是否为镜面目标</td>
    </tr>
    <tr>
      <th>isinside</th>
      <td>是否在别的物体内部，比如一辆车在建筑内部，人在车内部等等</td>
    </tr>
    <tr>
      <th>confidence</th>
      <td>检测框的置信度，为人工标注时通常为1，为自动生成时一般在0.5~1之间</td>
    </tr>
    <tr>
      <th>pose</th>
      <td>拍摄角度，取值为 Unspecified，Frontal，Rear，Left，Right</td>
    </tr>
</table>

可以看到，如果要描述一个检测数据集的样本，image_id、label_id和bbox是最基础的字段，此外还包含了各种描述标注框信息的特殊字段。

<a id="table-2"></a>

# 2. 模板展示

根据上述的[调研结果](#table-1)，我们知道对于检测任务，一个样本最重要的属性是图片的id(或路径)、每个标注框的位置以及类别，考虑到每张图片可能包含多个标注框，我们定义了一个嵌套结构体LocalObjectEntry（其详细定义可以参考[DSDL入门文档-语言定义-嵌套结构体](http://research.pages.shlab.tech/dataset_standard/dsdl-docs/zh/lang/structs/#242)），用来表述单个标注框的信息（即类别和位置）。这样，我们可以在检测任务结构体（结构体的概念请参考[DSDL入门文档-语言定义-结构体](https://opendatalab.github.io/dsdl-docs/zh/lang/structs/#24)部分）的$fields属性中定义image和objects两个字段，其中objects字段则为多个LocalObjectEntry结构体构成的列表（列表为空表示图片没有标注框）；其次，与分类相同，不同的数据集所蕴含的类别是各不相同的，所以在sample中需要有一个形参，来对类别域进行限定（在dsdl中，我们将类别域描述为class domain，或者cdom，具体可以参考[DSDL入门文档-语言定义-类别域](https://opendatalab.github.io/dsdl-docs/zh/lang/basic_types/#223-label)中更详细的定义）。基于上述考虑，我们制定了检测任务的模板，如下所示：
```yaml
$dsdl-version: "0.5.0"

LocalObjectEntry:
    $def: struct
    $params: ['cdom']
    $fields:
        bbox: BBox
        label: Label[dom=$cdom]

ObjectDetectionSample:
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        objects: List[LocalObjectEntry[cdom=$cdom]]
```
在检测模板中的一些字段含义如下：

  - $dsdl-version: 描述了该文件对应的dsdl版本
  - LocalObjectEntry: 定义了标注框的描述方式的嵌套结构体，包含四个字段: 

    - $def: struct, 表示这是一个结构体类型
    - $params: 定义了形参，在这里即class domain
    - $fields: 结构体类所包含的属性，具体包括:

        - bbox 标注框的位置
        - label 标注框的类别
      
  - ObjectDetectionSample: 定义了检测任务sample的结构体，包含四个字段:

    - $def: struct, 表示这是一个结构体类型
    - $params: 定义了形参，在这里即class domain
    - $fields: 结构体类所包含的属性，具体包括:

        - image 图片的路径
        - objects 标注信息，检测任务中，为前面的LocalObjectEntry构成的一个列表

对于模板中提到的类别域cdom，我们在模板库[dsdl-sdk repo](https://gitlab.shlab.tech/research/dataset_standard/dsdl-sdk/-/tree/feature-types/dsdl/dsdl_library)中也提供了常见任务的类别域，这里给出VOC数据集的class domain作为示例：
```yaml
$dsdl-version: "0.5.0"

VOCClassDom:
    $def: class_domain
    classes:
        - horse
        - person
        - bottle
        - tvmonitor
        - chair
        - diningtable
        - pottedplant
        - aeroplane
        - car
        - train
        - dog
        - bicycle
        - boat
        - cat
        - sofa
        - bird
        - sheep
        - motorbike
        - bus
        - cow
```

上面的文件中给出了VOCClassDom的定义，具体包含下列字段：

- $def: 描述了VOCClassDom的类型，这里即class_domain
- classes: 描述了该类别域中所包含的类别及其顺序，在VOC数据集中，则依次为horse、person等等

这一章节介绍的检测任务模板和cdom模板都可以在我们的模板库[dsdl-sdk repo](https://gitlab.shlab.tech/research/dataset_standard/dsdl-sdk/-/tree/feature-types/dsdl/dsdl_library)中找到，其他任务类型和类别域的模板也欢迎大家尝试使用。

# 3. 使用说明
在这个章节介绍一下如何通过import的方式来引用我们的模板。假设现在有一个数据集，其任务类型为目标检测，同时类别域和VOC相同，则可以通过import检测任务模板和VOC的类别域，然后在此基础上来描述自己的数据集, 举例如下：
```yaml
$dsdl-version: "0.5.0"

$import:
    - task/object-detection
    - class/voc-class-domain

meta:
    dataset_name: "VOC2007"
    sub_dataset_name: "train"
    
data:
    sample-type: ObjectDetectionSample[cdom=VOCClassDom]
    sample-path: $local
    samples: 
      - image: "media/000000000000.jpg"
        objects:
          - {bbox: [4.0, 36.0, 496.0, 298.0], label: 12}
      - image: "media/000000000002.jpg"
        objects:
          - {bbox: [440.0, 161.0, 60.0, 81.0], label: 14}   
          - {bbox: [97.0, 159.0, 121.0, 67.0], label: 14}
          - {bbox: [443.0, 116.0, 57.0, 101.0], label: 15}
          - {bbox: [104.0, 113.0, 65.0, 106.0], label: 15}
      ...
```
上面的描述文件中，首先定义了dsdl的版本信息，然后import了两个模板文件，包括任务模板和类别域模板，接着用meta和data字段来描述自己的数据集，具体的字段说明如下所示：  

- $dsdl-version: dsdl版本信息
- $import: 模板导入信息，这里导入检测任务模板和VOC的class domain，也就是章节[2. 模板展示](#table-2)中展示的两部分内容
- meta: 主要展示数据集的一些元信息，比如数据集名称，创建者等等，用户可以自己添加想要备注的其它信息
- data: data的内容就是按照前面定义好的结构所保存的样本信息，具体如下：  

    - sample-type: 数据的类型定义，在这里用的是从检测任务模板中导入的ObjectDetectionSample类，同时指定了采用的cdom为VOCClassDom
    - sample-path: samples的存放路径，如果实际是一个路径，则samples的内容从该文件读取，如果是$local（这个例子），则从本文件的data.samples字段中直接读取
    - samples: 保存数据集的样本信息，注意只有在sample-path是$local的时候该字段才会生效，否则samples会优先从sample-path中的路径去读取