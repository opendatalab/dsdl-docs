# 关键点检测（姿态估计）任务

# 1. 任务调研

## 1.1 任务定义

关键点检测任务目标是标出物体的关键部位，姿态估计任务目标是对物体（通常是人和动物）的姿态（即关键点和关键点之间的连接关系）进行估计。关键点检测和姿态估计通常合在一起讨论，原因是对于人体和动物等其身体部位之间的连接关系是固定的，得到了人体关键点的检测结果，就可以得到姿态估计的结果(是否有姿态估计取决于是否有关键点之间的连接关系)。

<center>
    <img src="images/pose_keypoint/fig3.png"/>
    <br>
    <div style="border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">
        图片取自：Deep High-Resolution Representation Learning for Human Pose Estimation, CVPR19
  	</div>
</center>

## 1.2 评价指标

评价指标一般采用COCO格式的mAP。mAP的计算方式与COCO目标检测中的mAP计算方式类似，对于关键点检测方法检测出的所有物体以及物体中的关键点，首先使用关键点中的OKS度量指标对所有检测出的物体进行分类，分为TP、FP、FN几类，划分完之后，通过改变score的阈值计算P-R曲线，P-R曲线下的面积即为AP的值。

与目标检测mAP计算方式最大的不同在于，目标检测中衡量实例之间的相似度时使用的是检测框之间的IOU，而在关键点检测中，衡量实例相似度使用的是物体关键点之间的OKS距离，OKS的计算方式如下：

<center>
    <img src="images/pose_keypoint/fig1.png"/>
    <br>
    <div style="border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">
        图片取自：https://cocodataset.org/#keypoints-eval
  	</div>
</center>

OKS代表的是一个物体其所有关键点检测结果（prediction）和真实标注（ground truth）之间的相似度，di代表第i个检测出的关键点和真实标注的欧氏距离，s是物体的像素面积，k代表第i种关键点（例如鼻子）的归一化因子，是对已有数据集中所有物体的同种关键点（例如数据集种所有人的鼻子关键点）计算得到的，值越大，代表数据集中这个关键点标注越差即这个关键点越难检测，值越小代表这个关键点标注越好，即这个关键点检测难度较小。有了OKS距离之后，可以计算得到不同OKS阈值下的AP指标。COCO的关键点检测指标如下图所示，与目标检测类似定义：

<center>
    <img src="images/pose_keypoint/fig2.png"/>
    <br>
    <div style="border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">
        图片取自：https://cocodataset.org/#keypoints-eval
  	</div>
</center>

## 1.3 主流数据集调研

根据目标类型的不同，姿态估计（关键点检测）数据集的标注形式也不同。姿态估计（关键点检测）数据集根据目标类型可以分为以下几类：

| 目标类型 | 任务类型 | 代表数据集 |
| - | - | - |
| 人体 | 人体姿态估计/关键点检测 (human body keypoint) | COCO, MPII, MPII-TRB, AI Challenger, CrowdPose, OCHuman, MHP |
| 人体(全身) | 人体(全身)姿态估计/关键点检测 (human wholebody keypoint) | COCO WholeBody, Halpe |
| 人脸 | 人脸关键点检测 (face keypoint) | 300W, WFLW, AFLW, COFW, COCO-WholeBody-Face |
| 手 | 手部关键点检测 (hand keypoint) | OneHand-10K, FreiHand, CMU Panoptic HandDB, InterHand2.6M, RHD, COCO-WholeBody-Hand |
| 衣物 | 衣物关键点检测 (fashion lanmark) | DeepFashion |
| 动物 | 动物姿态估计/关键点检测 (animal keypoint) | Animal-Pose, AP-10K, Horse-10, MacaquePose, Vinegar Fly, Desert Locust, Grévy’s Zebra, ATRW |
    
    
我们调研了10个主流姿态估计/关键点检测数据集，涵盖了所有以上不同类型的数据集。完整的字段调研结果如下表所示：

<table border="4" >
    <tr>
      <th>姿态估计/关键点检测数据集</th>
      <th>image_id</th>
      <th>height</th>
      <th>width</th>
      <th>instance_id</th>
      <th>category_id</th>
      <th>is_crowd</th>
      <th>area</th>
      <th>num_keypoints</th>
      <th>bbox</th>
      <th>segmentation</th>
      <th>keypoints</th>
      <th>visible</th>
      <th>center</th>
      <th>categories</th>
      <th>super_categories</th>
      <th>keypoint_names</th>
      <th>skeleton</th>
      <th>other</th>
    </tr>
    <tr>
      <th> COCO </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y  </th>
      <th>   </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th>   </th>
    </tr>
    <tr>
      <th> MPII </th>
      <th> Y </th>
      <th>   </th>
      <th>   </th>
      <th>   </th>
      <th>   </th>
      <th>   </th>
      <th>   </th>
      <th>   </th>
      <th>   </th>
      <th>   </th>
      <th> Y </th>
      <th> Y  </th>
      <th> Y </th>
      <th>   </th>
      <th>   </th>
      <th>   </th>
      <th>   </th>
      <th> scale, person, torsoangle </th>
    </tr>
    <tr>
      <th> AIC </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th>  </th>
      <th> Y </th>
      <th> Y  </th>
      <th>   </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th>   </th>
    </tr>
    <tr>
      <th> CrowdPose </th>
      <th> Y </th>
      <th> Y   </th>
      <th> Y   </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th>  </th>
      <th> Y </th>
      <th> Y  </th>
      <th>   </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> crowd index  </th>
    </tr>
    <tr>
      <th> COCO-WholeBody </th>
      <th> Y </th>
      <th> Y   </th>
      <th> Y   </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th>  </th>
      <th> Y </th>
      <th> Y  </th>
      <th>   </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> face valid/kpts/bbox, right hand valid/kpts/bbox, left hand valid/kpts/bbox, foot valid/kpts </th>
    </tr>
    <tr>
      <th> Halpe </th>
      <th> Y </th>
      <th> Y   </th>
      <th> Y   </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th>  </th>
      <th> Y </th>
      <th>  </th>
      <th>  </th>
      <th> Y </th>
      <th> Y  </th>
      <th>   </th>
      <th> Y </th>
      <th> Y </th>
      <th>   </th>
      <th>   </th>
      <th> Hoi  </th>
    </tr>
    <tr>
      <th> 300W </th>
      <th> Y </th>
      <th> Y   </th>
      <th> Y   </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th>  </th>
      <th> Y </th>
      <th> Y  </th>
      <th> Y  </th>
      <th> Y </th>
      <th> Y </th>
      <th>   </th>
      <th>   </th>
      <th>   </th>
    </tr>
    <tr>
      <th> OneHand10K </th>
      <th> Y </th>
      <th> Y   </th>
      <th> Y   </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th>  </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y  </th>
      <th>   </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y  </th>
      <th> Y  </th>
      <th>   </th>
    </tr>
    <tr>
      <th> DeepFashion </th>
      <th> Y </th>
      <th>    </th>
      <th>    </th>
      <th>   </th>
      <th> Y  </th>
      <th>   </th>
      <th>   </th>
      <th>  </th>
      <th> Y </th>
      <th>  </th>
      <th> Y </th>
      <th> Y  </th>
      <th>   </th>
      <th> Y </th>
      <th>  </th>
      <th> Y  </th>
      <th>   </th>
      <th>  variation </th>
    </tr>
    <tr>
      <th> AnimalPose </th>
      <th> Y </th>
      <th>    </th>
      <th>    </th>
      <th>   </th>
      <th> Y  </th>
      <th>   </th>
      <th>   </th>
      <th> Y </th>
      <th> Y </th>
      <th>  </th>
      <th> Y </th>
      <th> Y  </th>
      <th>   </th>
      <th> Y </th>
      <th> Y </th>
      <th> Y  </th>
      <th> Y  </th>
      <th>     </th>
    </tr>
</table>


经过整理，关键点检测/姿态估计任务的字段可以分为两种：一种是不同数据集共有的共享字段，一种是不同数据集不同的独立字段。关键点检测/姿态估计任务的共享字段和独立字段如下表所示：

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
      <th>keypoints</th>
      <td>单个目标的关键点标注，包含了一系列坐标点，坐标点用[x, y]或者[x,y,vis]表示（vis代表这个关键点是否可见）</td>
    </tr>
    <tr>
      <th>visible</th>
      <td>表示某个关键点是否可见，使用整数来标识</td>
    </tr>
    <tr>
      <th rowspan="22">独立字段</th>
      <th>height/width</th>
      <td>图像的原始尺寸（长和宽）</td>
    <tr>
      <th>instance_id</th>
      <td>这个目标的id，定位到某个具体的目标</td>
    </tr>
    <tr>
      <th>category_id</th>
      <td>类别id，表示这个目标属于哪个类别</td>
    <tr>
      <th>is_crowd</th>
      <td>标注的是一个对象还是一组对象，使用0或者1来标识，如果是一组对象为1，否则为0，</td>
    </tr>
    <tr>
      <th>area</th>
      <td>这个目标所占的面积，通常使用所占像素个数来表示</td>
    </tr>
    <tr>
      <th>num_keypoints</th>
      <td>关键点个数</td>
    </tr>
    <tr>
      <th>bbox</th>
      <td>目标的矩形框标注，通常使用[x,y,w,h]来表示</td>
    </tr>
    <tr>
      <th>segmentation</th>
      <td>目标的像素级分割标注，通常使用一组[x,y]坐标来表示</td>
    </tr>
    <tr>
      <th>center</th>
      <td>目标的中心点坐标，使用[x,y]来表示，通常代表的是目标矩形框的中心点坐标</td>
    </tr>
    <tr>
      <th>categories</th>
      <td>表示数据集中所包含的类别以及类别编号</td>
    </tr>
    <tr>
      <th>super_categories</th>
      <td>数据集中类别的父类</td>
    </tr>
    <tr>
      <th>keypoint_names</th>
      <td>关键点的名称</td>
    </tr>
    <tr>
      <th>skeleton</th>
      <td>关键点之间的连接关系</td>
    </tr>
    <tr>
      <th>scale</th>
      <td>MPII中字段，表示目标框的缩放比例，MPII中由于目标框是正方形，scale*200px可以还原得到目标框的边长</td>
    <tr>
      <th>person</th>
      <td>MPII中字段，代表图片中人的个数</td>
    <tr>
      <th>torsoangle</th>
      <td>MPII中字段，代表人体躯干的偏转角度</td>
    <tr>
      <th>face/hand/foot valid</th>
      <td>COCO-WholeBody中字段，代表是否有脸/手/脚的标注，值为0或者1</td>
    <tr>
      <th>face/hand/foot kpts</th>
      <td>COCO-WholeBody中字段，表示脸/手/脚的关键点标注，为一组坐标点</td>
    <tr>
      <th>face/hand bbox</th>
      <td>COCO-WholeBody中字段，表示脸/手的矩形框标注，表示为矩形框[x,y,h,w]</td>
    <tr>
      <th>Hoi</th>
      <td>Halpe中字段，使用整型表示，代表的是人体和其他物体发生交互的种类（例如0代表拿起，1代表坐，等等）</td>
    <tr>
      <th>Variation</th>
      <td>DeepFashion中字段，使用整型表示，代表的是任务的姿态</td>
    </tr>
    
</table>


综上所述，需要描述一个关键点检测数据集，最基础的字段包括image_id, keypoints, visible这三个字段，数据集独立字段用户自行添加修改。

## 2. 模板展示

根据上述的调研结果，我们知道对于关键点检测/姿态估计任务，一个样本最重要的属性是图片的id(或路径)、每个目标的关键点标注，以及关键点是否可见这个属性，考虑到每张图片可能包含多个物体，可能有多个关键点标注，我们定义了一个嵌套结构体KeyPointLocalObject，用来表述单个目标的关键点标注的信息（即类别和关键点）。在关键点检测/姿态估计任务结构体的$fields 属性中定义了image和annotations两个字段，其中annotations字段则为多个KeyPointLocalObject结构体构成的列表（列表为空表示图片中没有关键点标注的物体）。最后，考虑到模板需要具有的代表性和可扩展性，在所有的属性中，有一些属性是必须的，其他一些特定数据集中的独立字段是可选的。基于上述考虑，我们制定了关键点检测/姿态估计任务的模板，如下所示：

```yaml
KeypointClassDom:
    $def: class_domain
    classes:
        - person
        - 
        - ...
        
KeypointDescDom:
    $def: class_domain
    classes:
       - "left eye"
       -
       - ...  
    skeleton:
       - [14, 16]
       - [5, 6]
       - [10, 12]
       - ...
```
首先是定义了任务类别域的文件。包括以下几个部分：

1. 定义了目标类别的KeypointClassDom。KeypointClassDom定义了目标的类别域，即这个目标属于哪些类别，比如person等。

2. 定义了目标关键点名称以及连接关系的KeypointDescDom。KeypointDescDom定义了关键点的检测任务中一些事先定义好的域，包括关键点名称和关键点之间的连接关系skeleton。

```yaml
KeyPointLocalObject:   
    $def: struct
    $params: ['cdom1', 'cdom2']
    $fields:
        keypoint: Keypoint[dom=$cdom2]
        label: Label[dom=$cdom1]
    $optional: ["label"]
        
KeyPointSample:
    $def: struct
    $params: ['cdom1', 'cdom2']
    $fields:
        image: Image
        annotations: List[etype=LocalObjectEntry[cdom1=$cdom1, cdom2=$cdom2]]
        
data:
    sample-type: ObjectKeypointSample[cdom1=KeypointClassDom, cdom2=KeypointDescDom]
```

其次是定义了关键点检测sample的yaml文件。包括以下几个部分：

1. KeyPointSample。KeyPointSample定义了关键点检测中的一个sample对象，包括图像路径image以及标注了的目标列表annotations。

2. KeyPointLocalObject。KeyPointLocalObject定义了一个目标的标注，标注里包括：

      - 目标的类别label，注意这个label所属的域是KeypointClassDom，即目标所属的类别。
  
      - 关键点标注keypoint，即目标的关键点标注，Keypoint标注使用列表[x1,y1,v1,x2,y2,v2,.....]来表示，x1,y1表示关键点的坐标，v1表示这个关键点的可见性（关键点的可见性标注方面，不设定统一的标准，和原始数据集格式保持一致，认为<=0的值即代表不可见且无标注，>1代表有标注）。keypoint所属的域是KeypointDescDom即描述关键点的domain。
  

## 3. 使用方法

下面介绍怎么使用上面定义的模板来描述一个数据集，以COCOKeypoint2017为例，描述了sample的yaml文件keypoint-coco2017.yaml如下：

```yaml
$dsdl-version: "0.5.0"

KeyPointLocalObject:
    $def: struct
    $params: ["cdom0", "cdom1"]
    $fields:
        iscrowd: Int
        area: Num
        category: Label[dom=$cdom0]
        bbox: BBox
        polygon: Polygon
        num_keypoints: Int
        ann_id: Int
        keypoints: Keypoint[dom=$cdom1]

KeyPointSample:
    $def: struct
    $params: ["cdom0", "cdom1"]
    $fields:
        media: Image
        height: Int
        width: Int
        image_id: Int
        annotations: List[etype=KeyPointLocalObject[cdom0=$cdom0, cdom1=$cdom1]]
```

可以看出，COCO2017Keypoints数据集的模板除了关键点检测任务模板中的必须字段外（keypoints， visible， 以及image_id），还有许多数据集特有的独立字段

在检测模板中的一些字段含义如下：
  - $dsdl-version: 描述了该文件对应的dsdl版本。
  
  - ObjectKeypointEntry: 定义了关键点标注的描述方式的嵌套结构体，包含四个字段: 
    - $def: struct, 表示这是一个结构体类型。
    
    - $params: 定义了形参，在这里即class domain。
    
    - $fields: 结构体类所包含的属性，具体包括:
      - is_crowd： 是对一个物体的标注还是多个物体的标注。
      - area： 目标实例的像素面积。
      - category： 物体所属的类别。
      - bbox： 目标的目标框标注，类型为BBox。
      - polygon： 目标的实例分割标注，类型为Polygon。
      - num_keypoints： 代表这个对象关键点的个数。
      - ann_id： 实例标注在整个数据集中的编号。
      - keypoints： 关键点标注的列表，其中每一个元素是一个[x,y,z]的三维坐标，x和y表示关键点位置，z表示这个关键点的可见情况。
      
  - KeypointDetectionSample: 定义了关键点检测/姿态估计任务sample的结构体，包含四个字段:
    - $def: struct, 表示这是一个结构体类型。
    
    - $params: 定义了形参，在这里即class domain。
    
    - $fields: 结构体类所包含的属性，具体包括:
    
        - media 图片的路径。
        - height: 图像的高。
        - width: 图像的宽。
        - image_id: 图像在数据集中的编号。
        - annotations 标注信息，关键点检测/姿态估计任务中，为前面的ObjectKeypointEntry构成的一个列表。
      
      
描述了关键点检测任务的class-dom.yaml文件如下所示：

```yaml
$dsdl-version: "0.5.0"

COCO2017KeypointsClassDom:
    $def: class_domain
    classes: 
        - person

COCO2017KeypointsDescDom[COCO2017KeypointsClassDom]:
    $def: class_domain
    classes:
        - nose[person]
        - left_eye[person]
        - right_eye[person]
        - ...
    skeleton:
        - [16, 14]
        - [14, 12]
        - [17, 15]
        - ...
```

上面的文件中给出了关键点检测任务重类别域的定义，具体包含下列字段：
 - COCO2017KeypointsClassDom：COCO2017Keypoint关键点检测的类别域，只包含了人这一个类别 。
 - COCO2017KeypointsDescDom：COCO2017Keypoint关键点检测的数据集描述信息域，继承了COCO2017KeypointsClassDom，包含了数据集中对person的描述信息，包括关键点名称以及关键点之间的连接关系。
