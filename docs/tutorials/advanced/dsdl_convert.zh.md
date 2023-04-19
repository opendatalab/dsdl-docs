# 数据集转换

用户在完成了[数据集模板的制定](./dsdl_define.md)后，即可进行数据集转换阶段。我们为用户提供了[DSDL SDK](https://github.com/opendatalab/dsdl-sdk)工具，辅助数据集转换的流程，请先[安装SDK](../../getting_started/install.md)。

本教程包含两个模板：

- [数据集转换流程及脚本模板](#数据集转换流程及脚本模板)：转换者仅需要实现几个特定函数，即可直接生成DSDL数据集目录。
- [实际示例](#实际示例)：VOC转DSDL的实际案例，供用户参考。

<a id="数据集转换流程及脚本模板"></a>
## 1. 数据集转换流程及脚本模板

转换者需要准备好原始数据集压缩包文件夹和DSDL文件夹，推荐按照以下的目录结构来整理：

```
├── <dataset_name>
    ├── compressed
        └── ...                                   # 原始数据集的压缩包  
    ├── dsdl                                      # 存放DSDL标注的文件夹   
        ├── defs/
            ├── template.yaml                    # 任务模板，可以直接从模板库调用   
        ├── tools/  
            └── prepare.py                       # 数据集准备脚本，可参考本小节提供的模板
```

以上的目录中的template.yaml为[DSDL数据集模板制定](./dsdl_define.md)小节中制定的模板，用户可以自定义模板，也可以在DSDL SDK中直接调用任务模板（后文的转换脚本模板中会标明用法）。

我们为用户准备了prepare.py的模板，用户只需要按照实际情况实现部分函数即可。**prepare.py中包含的模块如下**：

- prepare函数：该脚本主要是用于解压原始数据集压缩包。该脚本需要传入的参数为原始数据集压缩包的文件夹路径，即`<dataset_name>/compressed/`。我们已提供了模板，内置zip和tar.gz格式，如需要支持其他格式，只需要修改解压部分的命令即可（在代码模板中有标明）。
- get_subset_samples_list函数：主要是用于生成`class-dom.yaml`和`set-<segment>.yaml`/`set-<segment>_samples.json`，请自行修改以适应不同数据集的标注内容提取。另外，需要注意的是，为了防止class-dom中出现不合规的命名，需要对所有类别名做转换（由replace_special_characters函数实现）。
- （可选）dataset_converter函数：中间格式转换，用于对数据集的媒体文件或标注文件进行必要的中间格式转换，在此举两个实例：
    - 比如像在分割数据集中，由于目前DSDL标准里要求分割数据集以单通道Int值图存储mask，需要把三波段的label map映射为单通道的Int值图，因此需要对数据集的标注文件做转换的替换。
    - 比如CIFAR10存储的图片格式是TFrecord，多个图片存在同一个TFrecord里，而DSDL的Image path需要一一对应关系，因此我们需要将每个图片提取出来转成PNG。
- main函数中必填的参数：
    - meta_info：包括数据集名称(Dataset Name)、官网(HomePage)、媒体文件的模态(Modality)、任务名称(Task)，注意，如果希望直接调用已有的任务模板，Task Name需要符合规范，可调用的Task Name请参考[任务模板介绍](../../dsdl_template/overview.md)页面中的**任务英文全称**。
    - flag_middle_format：如果实现了dataset_converter函数，则需要将flag_middle_format改为True，以生成更加规范的README
    - class_dom_names_original：以list的形式，将数据集的类别存储在该字段中，注意，其排列顺序决定了class_id的生成，其中排在首位的class_id为1，第二位为2，以此类推。
    - subset_name_list：数据集子集的列表，比如['train', 'val']，根据数据集实际情况修改。
    - 转换和生成的步骤：这部分的DSDL SDK中已实现了大部分的函数，大部分情况下，转换者无需修改，如果想要了解各个函数的功能，请参考[DSDL SDK](https://github.com/opendatalab/dsdl-sdk)。

具体的prepare.py的模板如下：

```python
import argparse
import os
import re
import shutil
import sys
import tarfile
import zipfile
from itertools import chain
from multiprocessing import Pool, cpu_count
from pathlib import Path

import numpy as np
from PIL import Image
from dsdl.converter.mllm import generate_config_file
from dsdl.converter.mllm import generate_readme_with_middle_format
from dsdl.converter.mllm import generate_readme_without_middle_format
from dsdl.converter.mllm import generate_tree_string
from dsdl.converter.utils import check_dsdl_meta_info
from dsdl.converter.utils import check_task_template_file
from dsdl.converter.utils import generate_class_dom
from dsdl.converter.utils import generate_subset_yaml_and_json
from dsdl.converter.utils import replace_special_characters
from dsdl.converter.utils import get_dsdl_template_from_lib

from tqdm import tqdm


#############生成DSDL标注，用户需要实现该函数#############################
def get_subset_samples_list(*args, **kwargs):
    samples_list = []
    ## 返回的列表示例如下：
    ## 注意每个字段名称要与template.yaml中定义的字段和结构完全相同，比如：
    # [{
    #     "media": {
    #         "image": "images/train/1.jpg",
    #         "image_shape": [405,720]
    #     },
    #     "objects": [
    #         {
    #             "bbox": [220,183,154,104],
    #             "label": "holothurian",
    #             "iscrowd": false,
    #             "segmentation": [[
    #                     [220,183],
    #                     [374,183],
    #                     [374,287],
    #                     [220,287]]]
    #         },
    #         ...,
    #  },
    #  ...
    # ]
    return samples_list


###########数据集中间格式转换，如果需要的话，用户需要实现该函数#############################
def dataset_to_middle_format(*args, **kwargs):
    # 有些数据集需要转换成中间格式，
    # 在这个函数中编写转换代码，并记录中间格式的文件夹树形结构和转换结果描述。
    ## 1. 确定中间格式数据保存路径
    middle_data_path = args[0]

    ## 2. 把数据集转换成中间格式
    ## 实现代码这里编写
    pass

##########################用户不需要修改##########################
def parse_args():
    """命令行参数解析"""
    parse = argparse.ArgumentParser(
        description='Prepare the dsdl_SemSeg_full dataset from original dataset.'
    )
    parse.add_argument(
        '--decompressed', '-d', action='store_true',
        help='This argument decides whether the dataset files are decompressed. '
             'Add "-d" argument to skip decompress process, '
             'and directly pass the decompressed dataset. '
             'The default is need decompress process.'
    )
    parse.add_argument(
        '--copy', '-c', action='store_true',
        help='This argument decides whether the decompressed dataset files will be copied as a backup and then run the converter. '
             'Add "-c" argument to create a copy, and then run the converter. '
             'The default is not to create a copy and directly overwrite the original data.'
    )
    parse.add_argument(
        'path', type=str,
        help='The original dataset path, a folder with compressed files if "-d" doesn\'t exist, '
             'or decompressed folder when "-d" exists.'
    )
    args = parse.parse_args()
    args.path = Path(args.path).absolute().resolve().as_posix()
    return args


###########需要修改prepare函数中的解压操作###########
def prepare(args):
    """根据不同的命令行参数执行解压、复制操作,并调用数据集文件转换和dsdl标注生成。"""
    SCRIPT_PATH = Path(__file__).absolute().resolve().parent
    DSDL_PATH = SCRIPT_PATH.parent
    if args.decompressed:
        ORIGINAL_PATH = Path(args.path)
        if args.copy:
            PREPARED_PATH = ORIGINAL_PATH.parent / "prepared"
            if PREPARED_PATH.exists():
                raise Exception(f"Path {PREPARED_PATH.as_posix()} already exists.")
            shutil.copytree(ORIGINAL_PATH, PREPARED_PATH)
        else:
            if flag_middle_format:
                print("The operation will directly overwrite the dataset files with no backup.")
                while True:
                    confirm = input("Input [yes] to continue, or [quit] to exit.  ")
                    if confirm.lower() == "quit":
                        sys.exit(0)
                    elif confirm.lower() == "yes":
                        break
            PREPARED_PATH = ORIGINAL_PATH
    else:
        COMPRESSED_PATH = Path(args.path)
        PREPARED_PATH = COMPRESSED_PATH.parent / "prepared"
        if PREPARED_PATH.exists():
            raise Exception(f"Path {PREPARED_PATH.as_posix()} already exists.")
        PREPARED_PATH.mkdir()

        found_compressed = False
        #######需要修改:解压操作，内置zip和tar.gz格式，其他格式需要修改#############
        for file in COMPRESSED_PATH.rglob("*.zip"):
            found_compressed = True
            zf = zipfile.ZipFile(file)
            zf.extractall(PREPARED_PATH)
        for file in chain(
            COMPRESSED_PATH.rglob("*.tar.gz"),
            COMPRESSED_PATH.rglob("*.tgz"),
            COMPRESSED_PATH.rglob("*.tar")
        ):
            found_compressed = True
            tf = tarfile.open(file)
            tf.extractall(PREPARED_PATH)

        if not found_compressed:
            raise Exception('Compressed file not found. Check the file path.')

        # 如果解压后发现prepared文件夹中仍有一层数据集名称的嵌套文件夹，
        # 使用以下代码删除这层嵌套，将数据集文件直接放在prepared文件夹中。
        # for file in (PREPARED_PATH / "foldername").iterdir():
        #     file.rename(file.parent.parent / file.name)
        # (PREPARED_PATH / "foldername").rmdir()
        #############################################################################

        if args.copy:
            ORIGINAL_PATH = COMPRESSED_PATH.parent / "original"
            if ORIGINAL_PATH.exists():
                raise Exception(f"Path {ORIGINAL_PATH.as_posix()} already exists.")
            shutil.copytree(PREPARED_PATH, ORIGINAL_PATH)

    return PREPARED_PATH.as_posix(), DSDL_PATH.as_posix()


if __name__ == "__main__":
    #########################必填的参数##########################
    meta_info = {
        "Dataset Name": "",  # e.g., VOC2012
        "HomePage": "",  # e.g., http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html
        "Modality": "",  # e.g., Images
        "Task": ""
    }  # e.g., Object Detection

    flag_middle_format = False  # 数据集是否需要转换成中间格式(是的话，修改为True)
    class_dom_names_original = []  # 需要修改, e.g., ['dog','cat']，可以自行实现函数提取
    subset_name_list = []  # 数据集的子集名称列表，e.g., ['train', 'val']

    args = parse_args()
    root_path, save_path = prepare(args)

    ## 说明：
    ## 因为模板文件template.yaml是dsdl中定义数据集结构和字段的文件。
    ## 所以必须先生成template.yaml才能进行后续转换。
    ## template.yaml的位置位于: save_path/defs/template.yaml
    ## 用户可以直接调用已有的模板，或手动创建template.yaml，并拷贝到save_path/defs/目录下。
    ## 以下示例是调用已有的任务模板：
    get_dsdl_template_from_lib(meta_info["Task"], save_path)
    ## 注意，这里的meta_info["Task"]需要满足DSDL任务模板页面的“任务英文全称”

    ###########以下是转换和生成的步骤，可根据实际情况修改#############
    ###########一般情况下，只需要修改get_subset_samples_list所需的参数###########
    check_dsdl_meta_info(meta_info)  # 检验meta信息是否存在错误
    check_task_template_file(save_path)  # 检验保存路径中是否已经存在模板文件

    # 1. 生成原始数据集目录结构树形字符串
    original_tree_str = generate_tree_string(root_path)

    # 2. 数据集中间格式转换，调用dataset_to_middle_format（如有需要请实现该函数）
    if flag_middle_format:
        ## 先实现一个函数把数据集转换成中间格式
        ## 可参考dataset_to_middle_format()中注释
        ## 需要对middle_format_tree_str和converter_description赋值
        dataset_to_middle_format(root_path)  # 需要自行修改所需的参数

    # 3. 生成class-dom
    class_dom_names = []
    for name in class_dom_names_original:
        class_dom_names.append(replace_special_characters(name))  # 将不合规的label名字做转换
    generate_class_dom(save_path, class_dom_names)  # 生成class-dom.yaml文件

    # 4. 生成<segment>_samples.json,调用get_subset_samples_list（必须实现该函数）
    for subset_name in subset_name_list:
        meta_info["Subset Name"] = subset_name
        print(f"processing data in {subset_name}.")
        subset_samples_list = get_subset_samples_list(root_path, subset_name)  # 需要自行修改所需的参数
        if len(subset_samples_list) == 0:
            raise ResourceWarning(
                "No samples found. Check if the file path is correct. "
                "If the dataset is not decompressed, remove -d option and try again."
            )
        # 示例：subset_samples_list = get_subset_samples_list(root_path, subset_name)
        generate_subset_yaml_and_json(
            meta_info,
            save_path,
            subset_samples_list
        )
        print(f"Sample list for {subset_name} is generated.")
    dsdl_tree_str = generate_tree_string(save_path, display_num=100)  # 生成转后的dsdl数据集目录结构树形字符串

    generate_config_file(save_path)  # 生成config.py

    # 5. 生成README.md
    if flag_middle_format:
        generate_readme_with_middle_format(
            save_path,
            meta_info["Dataset Name"],
            meta_info["Task"],
            original_tree_str,
            dsdl_tree_str,
        )
    else:
        generate_readme_without_middle_format(
            save_path,
            meta_info["Dataset Name"],
            meta_info["Task"],
            original_tree_str,
            dsdl_tree_str
        )

```

转换者完善了必要的函数的和必填的字段后，可以运行如下命令：

```
python tools/prepare.py <path_to_compressed_dataset_folder>
```

运行该代码后，将会对用户提供的数据集压缩包进行解压，生成prepared文件夹，然后直接对prepared文件夹进行DSDL标准化操作，并生成DSDL标注。执行后的目录结构如下：

```
├── <dataset_name>
    ├── compressed
        └── ...                              # 原始数据集的压缩包(真正的原始数据集）,后面提供给OSS
    ├── prepared                             # 原始数据集解压后的所有文件
        ├── ...                              # 由prepare.sh运行后生成
        └── ...  
    ├── dsdl                                 # 存放DSDL标注的文件夹  
        ├── defs/
            ├── template.yaml                # 任务模板
            ├── class-dom.yaml               # 数据集的类别域   
        ├── set-train/                       # 训练集
            ├── train.yaml                   # 训练集的定义文件
            ├── train_samples.json           # 实际标注文件
        ├── tools/  
           └── prepare.py                    # 包括解压、转中间格式（如果需要的话）和生成dsdl目录
        ├── README.md   
        └── config.py                        # 数据集读取路径等config文件
```

<a id="实际示例"></a>
## 2. 实际示例

该示例中，将直接利用[目标检测模板](../../dsdl_template/cv/cv_detection.md)来对VOC进行[精简版DSDL转换](./dsdl_define.md#精简版DSDL)。

主要步骤如下:

- 原始数据集调研：包括目录结构、标注文件等
- 数据集转换脚本实现：通过目标检测任务模板和数据集转换脚本模板，实现VOC转DSDL

### 2.1 原始数据集调研

首先需要调研原始数据集的文件结构：

```plaintext
VOC2007/
├── Annotations/              # 里面存放的是每张图片打完标签所对应的XML文件
│  ├── 000001.xml             # 某张图片的标注信息
│  └── ...
├── ImageSets/                # 图片划分的txt存放位置
│  ├── Layout                 # 包含Layout标注信息的图像文件名列表
│  │  ├── test.txt 
│  │  ├── train.txt 
│  │  ├── trainval.txt 
│  │  └── val.txt 
│  ├── Main                   # 包含所有文件的列表和划分
│  │  ├── aeroplane_test.txt  # 按每个类别的训练集、测试集等划分
│  │  ├── aeroplane_train.txt 
│  │  ├── ...
│  │  ├── test.txt            # 全数据集的test划分
│  │  ├── train.txt           # 全数据集的train划分
│  │  ├── trainval.txt 
│  │  └── val.txt 
│  ├── Segmentation           # 包含语义分割信息图像文件的列表和划分
│  │  ├── test.txt 
│  │  ├── train.txt 
│  │  ├── trainval.txt 
│  │  └── val.txt 
├── JPEGImages/               # 存放的是训练与测试的所有图片
│  ├── 000001.jpg             # 图片（序号作为图片名） 
│  └── ...
├── SegmentationClass/        # 语义分割标注
│  ├── 000032.png             # 某张图片的媒体文件 
│  └── ...
└── SegmentationObject/       # 实例分割标注
   ├── 000032.png             # 某张图片的媒体文件 
   └── ...
```

这里只以检测任务为例生成模板，因此只需要Annotations/、JPEGImages/这两个文件夹，另外，训练测试集划分，需要用ImageSets/Main/train.txt、val.txt、test.txt这三个文件。

标注类型如下（以Annotations/000001.xml为例）：

```XML
<annotation>
   <folder>VOC2007</folder>                         # 文件夹
   <filename>000001.jpg</filename>                  # 图片文件名
   <source>                                         # 图像元信息
      <database>The VOC2007 Database</database>     # 数据集名称
      <annotation>PASCAL VOC2007</annotation>       # 标注类型
      <image>flickr</image>                         # 来源
      <flickrid>341012865</flickrid>                # 来源ID
   </source>
   <owner>                                          # 源信息
      <flickrid>Fried Camels</flickrid>
      <name>Jinky the Fruit Bat</name>
   </owner>
   <size>
      <width>353</width>                            # 图片宽
      <height>500</height>                          # 图片高 
      <depth>3</depth>                              # 图片通道数
   </size>
   <segmented>0</segmented>                         # 是否用于分割
   <object>                                         # 标注部分 
      <name>dog</name>                              # 标签
      <pose>Left</pose>                             # 姿态
      <truncated>1</truncated>                      # 物体是否被部分遮挡（>15%）
      <difficult>0</difficult>                      # 是否为难以辨识的物体
      <bndbox>
         <xmin>48</xmin>                            # 左上角点的x
         <ymin>240</ymin>                           # 左上角点的y
         <xmax>195</xmax>                           # 右下角点的x
         <ymax>371</ymax>                           # 右下角点的y
      </bndbox>
   </object>
   ...
</annotation>
```

这里以ImageSets/Main/train.txt为例展示一下数据集segment划分的文件内容：

```plaintext
000012         # 图片名前缀
000017
000023
000026
...
```

### 2.2 数据集转换脚本实现

根据该数据集的目录结构和标注类型，prepare.py脚本的实现如下：

```python
import argparse
import os
import shutil
import sys
from pathlib import Path
import tarfile
import zipfile
from itertools import chain

from dsdl.converter.mllm import generate_config_file
from dsdl.converter.mllm import generate_readme_with_middle_format
from dsdl.converter.mllm import generate_readme_without_middle_format
from dsdl.converter.mllm import generate_tree_string
from dsdl.converter.utils import check_dsdl_meta_info
from dsdl.converter.utils import check_task_template_file
from dsdl.converter.utils import generate_class_dom
from dsdl.converter.utils import generate_subset_yaml_and_json
from dsdl.converter.utils import replace_special_characters
from dsdl.converter.utils import get_dsdl_template_from_lib

#!/usr/bin/env python3
"""
This file implements the generator of the VOC2007 DSDL format dataset.
"""
  
import itertools
from xml.etree import ElementTree
import json  

#############提取原始数据集字段，生成sample list#############################
def get_subset_samples_list(root_path, seg, category_list):
    samples_list = []  
    anno_paths = os.path.join(root_path, "Annotations")
    ann_id_gen = itertools.count()
    _VOC_CATEGORY_DICT = {_name: (_ind + 1) for _ind, _name in enumerate(category_list)}
  
    seg_path = os.path.join(root_path, 'ImageSets', 'Main', seg + '.txt')
    try:
        with open(seg_path, 'r') as f:
            seg_list = f.readlines()
    except:
        print('The segmentation file {} cannot be open, it will be skipped.'.format(seg_path))

    for anno_id in seg_list:
        anno_path = os.path.join(root_path, 'Annotations', anno_id.strip() + '.xml')

        try:
            with open(anno_path, 'r') as f:
                anno_tree = ElementTree.parse(f)
        except:
            print('The annotation file {} cannot read, it will be skipped.'.format(anno_path))
            continue
  
        sample = {
            'image': os.path.join('JPEGImages', anno_tree.find('filename').text),
            'objects': []}

        for obj in anno_tree.iter('object'):
            xmin, ymin, xmax, ymax = [float(obj.find('bndbox').find(boxes).text) for boxes in ['xmin', 'ymin', 'xmax', 'ymax']]
            sample['objects'].append({
                'bbox': [xmin, ymin, xmax-xmin, ymax-ymin],
                'label': _VOC_CATEGORY_DICT[obj.find('name').text]
            })

        samples_list.append(sample)
    return samples_list

def parse_args():
    """命令行参数解析"""
    parse = argparse.ArgumentParser(
        description='Prepare the dsdl_SemSeg_full dataset from original dataset.'
    )
    parse.add_argument(
        '--decompressed', '-d', action='store_true',
        help='This argument decides whether the dataset files are decompressed. '
             'Add "-d" argument to skip decompress process, '
             'and directly pass the decompressed dataset. '
             'The default is need decompress process.'
    )
    parse.add_argument(
        '--copy', '-c', action='store_true',
        help='This argument decides whether the decompressed dataset files will be copied as a backup and then run the converter. '
             'Add "-c" argument to create a copy, and then run the converter. '
             'The default is not to create a copy and directly overwrite the original data.'
    )
    parse.add_argument(
        'path', type=str,
        help='The original dataset path, a folder with compressed files if "-d" doesn\'t exist, '
             'or decompressed folder when "-d" exists.'
    )
    args = parse.parse_args()
    return args


def prepare(args):
    """根据不同的命令行参数执行解压、复制操作,并调用数据集文件转换和dsdl标注生成。"""
    SCRIPT_PATH = Path(__file__).resolve().absolute().parent
    DSDL_PATH = SCRIPT_PATH.parent
    if args.decompressed:
        ORIGINAL_PATH = Path(args.path)
        if args.copy:
            PREPARED_PATH = ORIGINAL_PATH.parent / "prepared"
            if PREPARED_PATH.exists():
                raise Exception(f"Path {PREPARED_PATH.absolute().as_posix()} already exists.")
            shutil.copytree(ORIGINAL_PATH, PREPARED_PATH)
        else:
            if flag_middle_format:
                print("The operation will directly overwrite the dataset files with no backup.")
                while True:
                    confirm = input("Input [yes] to continue, or [quit] to exit.  ")
                    if confirm.lower() == "quit":
                        sys.exit(0)
                    elif confirm.lower() == "yes":
                        break
            PREPARED_PATH = ORIGINAL_PATH
    else:
        COMPRESSED_PATH = Path(args.path)
        PREPARED_PATH = COMPRESSED_PATH.parent / "prepared"
        if PREPARED_PATH.exists():
            raise Exception(f"Path {PREPARED_PATH.absolute().as_posix()} already exists.")
        PREPARED_PATH.mkdir()

        found_compressed = False
        #######需要修改:解压操作，内置zip和tar.gz格式，其他格式需要修改#############
        for file in COMPRESSED_PATH.rglob("*.zip"):
            found_compressed = True
            zf = zipfile.ZipFile(file)
            zf.extractall(PREPARED_PATH)
        for file in chain(
            COMPRESSED_PATH.rglob("*.tar.gz"),
            COMPRESSED_PATH.rglob("*.tgz"),
            COMPRESSED_PATH.rglob("*.tar")
        ):
            found_compressed = True
            tf = tarfile.open(file)
            tf.extractall(PREPARED_PATH)

        if not found_compressed:
            raise Exception('Compressed file not found. Check the file path.')

        for file in (PREPARED_PATH / "VOCdevkit"/ "VOC2007").iterdir():
            file.rename(file.parent.parent.parent / file.name)
        shutil.rmtree(PREPARED_PATH / "VOCdevkit")
        #############################################################################

        if args.copy:
            ORIGINAL_PATH = COMPRESSED_PATH.parent / "original"
            if ORIGINAL_PATH.exists():
                raise Exception(f"Path {ORIGINAL_PATH.absolute().as_posix()} already exists.")
            shutil.copytree(PREPARED_PATH, ORIGINAL_PATH)

    return PREPARED_PATH.absolute().as_posix(), DSDL_PATH.absolute().as_posix()

if __name__ == "__main__":
    meta_info = {
        "Dataset Name": "VOC2007",
        "HomePage": "http://host.robots.ox.ac.uk/pascal/VOC/voc2007/index.html",
        "Modality": "Images", 
        "Task": "Object Detection"
    }

    flag_middle_format = False
    class_dom_names_original = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
    subset_name_list = ['train', 'val', 'test']
    args = parse_args()
    root_path, save_path = prepare(args)

    ## 说明：
    ## 因为模板文件template.yaml是dsdl中定义数据集结构和字段的文件。
    ## 所以必须先生成template.yaml才能进行后续转换。
    ## template.yaml的位置位于: save_path/defs/template.yaml
    ## 用户可以直接调用已有的模板，或手动创建template.yaml，并拷贝到save_path/defs/目录下。
    ## 以下示例是调用已有的模板：
    get_dsdl_template_from_lib(meta_info["Task"], save_path)
    ## 注意，这里的task_name可以在数据集模板介绍页面的表格中的“任务英文全称”获取

    ###########以下是转换和生成的步骤，可根据实际情况修改#############
    ###########一般情况下，只需要修改get_subset_samples_list所需的参数###########
    check_dsdl_meta_info(meta_info)  # 检验meta信息是否存在错误
    check_task_template_file(save_path)  # 检验保存路径中是否已经存在模板文件

    # 1. 生成原始数据集目录结构树形字符串
    original_tree_str = generate_tree_string(root_path)

    # 2. 数据集中间格式转换，调用dataset_to_middle_format（如有需要请实现该函数）
    if flag_middle_format:
        ## 先实现一个函数把数据集转换成中间格式
        ## 可参考dataset_to_middle_format()中注释
        ## 需要对middle_format_tree_str和converter_description赋值
        dataset_to_middle_format(root_path)  # 需要自行修改所需的参数

    # 3. 生成class-dom
    class_dom_names = []
    for name in class_dom_names_original:
        class_dom_names.append(replace_special_characters(name))  # 将不合规的label名字做转换
    generate_class_dom(save_path, class_dom_names)  # 生成class-dom.yaml文件

    # 4. 生成<segment>_samples.json,调用get_subset_samples_list（必须实现该函数）
    for subset_name in subset_name_list:
        meta_info["Subset Name"] = subset_name
        print(f"processing data in {subset_name}.")
        subset_samples_list = get_subset_samples_list(root_path, subset_name, class_dom_names_original)  # 需要自行修改所需的参数
        # 示例：subset_samples_list = get_subset_samples_list(root_path, subset_name)
        generate_subset_yaml_and_json(
            meta_info,
            save_path,
            subset_samples_list
        )
        print(f"Sample list for {subset_name} is generated.")
    dsdl_tree_str = generate_tree_string(save_path,display_num=100)  # 生成转后的dsdl数据集目录结构树形字符串

    generate_config_file(save_path)  # 生成config.py

    # 5. 生成README.md
    if flag_middle_format:
        generate_readme_with_middle_format(
            save_path,
            meta_info["Dataset Name"],
            meta_info["Task"],
            original_tree_str,
            dsdl_tree_str,
        )
    else:
        generate_readme_without_middle_format(
            save_path,
            meta_info["Dataset Name"],
            meta_info["Task"],
            original_tree_str,
            dsdl_tree_str
        )

```

运行了tools/prepare.py后，得到的DSDL数目录如下：

```Plain
dsdl-voc2007/
├── defs/  
│  ├── template.yaml                          # 检测任务模板
│  └── class-dom.yaml                         # 数据集的类别域
├── set-train/                                # 训练集
│  ├── train.yaml                             # 训练的yaml文件
│  └── train_samples.json                     # 训练集sample的json文件
├── set-val/                                  # 验证集
│  ├── val.yaml
│  └── val_samples.json  
├── set-test/                                 # 测试集
│  ├── test.yaml
│  └── test_samples.json  
├── config.py                                 # 数据集读取路径等config文件
└── README.md                                 # 数据集简介
```

包含以下几个重要的文件：

- struct的定义文件（在这个例子里文件名为template.yaml）：这个文件主要是对struct做一个明确的定义，可以有sample的结构体和标注的结构体等，需指明包含了哪些field，每个field的类型。
- 类别域（在这个例子为class-dom.yaml）：里面包含了类别列表，对应category的序号（从1开始排序）
- samples文件（在这个例子里分别分为train.yaml和train_samples.json)
    - train.yaml主要是指明引用哪个struct模板和类别域文件，并且指明数据类型和存放路径，另外还有一些meta信息
    - train_samples.json里保存了实际的samples信息，其组织结构必须和之前定义的结构体匹配

<a id="VOC2007ClassDom"></a>
#### 2.2.1 类别域

class-dom.yaml：这是一个类别定义的Dom文档

```YAML
$dsdl-version: "0.5.0"

ClassDom:
    $def: class_domain
    classes:
        - aeroplane                   # 对应_category为1
        - bicycle                     # 对应_category为2，以此类推
        - bird
        - boat
        - bottle
        - bus
        - car
        - cat
        - chair
        - cow
        - diningtable
        - dog
        - horse
        - motorbike
        - person
        - pottedplant
        - sheep
        - sofa
        - train
        - tvmonitor

```

#### 2.2.2 set-train文件夹

train.yaml：这个文档引用了之前定义的两个文档，并且指引了具体的sample路径（test.yaml和val.yaml类似，只是修改对应sample-path和sub_dataset_name字段）

```YAML
$dsdl-version: "0.5.0"

$import:
    - ../defs/class-domain
    - ../defs/object-detection-def

meta:
   Dataset Name: "VOC2007",
   HomePage: "http://host.robots.ox.ac.uk/pascal/VOC/voc2007/index.html",
   Modality: "Images", 
   Task: "Object Detection"

data:
    sample-type: ObjectDetectionSample[cdom=VOCClassDom]
    sample-path: train_samples.json
```

train_samples.json需要我们写脚本从原始数据集转换来（转换脚本将在下一小节“数据集转换”中详述）。注意，里面的字段需要和之前定义的struct对应。最终样式如下：

```JSON
{"samples": [
    {
        "image": "JPEGImages/000001.jpg",
        "objects": [
            {
                "bbox": [120.24, 0.32, 359.76, 596.04], 
                "label": 1
            }, 
            ...
         ]
    },
    ...
]}
```

注意，"samples"字段是必须的（不可改名），且组织形式也不能改变，即：必须是字典形式，字典有一个键为"samples"，其值为一个列表，列表的每个对象都是一个sample类的实例（即本案例中的ObjectDetectionSample类）。

#### 2.2.3 config

config.py的内容如下：

```
local = dict(
    type="LocalFileReader",
    working_dir="the root path of the prepared dataset",
)

ali_oss = dict(
    type="AliOSSFileReader",
    access_key_secret="your secret key of aliyun oss",
    endpoint="your endpoint of aliyun oss",
    access_key_id="your access key of aliyun oss",
    bucket_name="your bucket name of aliyun oss",
    working_dir="the prefix of the prepared dataset within the bucket")
```

请根据实际情况，修改媒体文件读取方式和路径。

#### 2.2.4 README.md

该数据集最终将字段生成README，其内容如下：

```
# Data Set Description Language(DSDL) for VOC2007 dataset

## Data Structure
Please make sure the folder structure of prepared dataset is organized as followed:

<dataset_root>
├── Annotations
│   ├── 000001.xml
│   ├── 000002.xml
│   ├── 000003.xml
│   └── ...
├── ImageSets
│   ├── Layout
│   │   ├── test.txt
│   │   ├── train.txt
│   │   ├── trainval.txt
│   │   └── ...
│   ├── Main
│   │   ├── aeroplane_test.txt
│   │   ├── aeroplane_train.txt
│   │   ├── aeroplane_trainval.txt
│   │   └── ...
│   └── Segmentation
│       ├── test.txt
│       ├── train.txt
│       ├── trainval.txt
│       └── ...
├── JPEGImages
│   ├── 000001.jpg
│   ├── 000002.jpg
│   ├── 000003.jpg
│   └── ...
└── ...

The folder structure of dsdl annotation for Object Detection is organized as followed:

<dsdl_root>
├── defs
│   ├── class-dom.yaml
│   └── template.yaml
├── tools
│   └── prepare.py
├── set-train
│   ├── train.yaml
│   └── train_samples.json
├── set-val
│   ├── val.yaml
│   └── val_samples.json
└── set-test
    ├── test.yaml
    └── test_samples.json

## config.py
You can load your dataset from local or oss.
From local:

local = dict(
    type="LocalFileReader",
    working_dir="the root path of the prepared dataset",
)

Please change the 'working_dir' to the path of your prepared dataset where media data can be found,
for example: "<root>/dataset_name/prepared".

From oss:

ali_oss = dict(
    type="AliOSSFileReader",
    access_key_secret="your secret key of aliyun oss",
    endpoint="your endpoint of aliyun oss",
    access_key_id="your access key of aliyun oss",
    bucket_name="your bucket name of aliyun oss",
    working_dir="the prefix of the prepared dataset within the bucket")

Please change the 'access_key_secret', 'endpoint', 'access_key_id', 'bucket_name' and 'working_dir',
e.g. if the full path of your prepared dataset is "oss://bucket_name/dataset_name/prepared", then the working_dir should be "dataset_name/prepared".

## Related source:
1. Get more information about DSDL: [dsdl-docs](https://opendatalab.github.io/dsdl-docs/)
2. DSDL-SDK official repo: [dsdl-sdk](https://github.com/opendatalab/dsdl-sdk/)
3. Get more dataset: [OpenDataLab](https://opendatalab.com/)

```

数据集转换完成后，建议运行[数据集验证](./dsdl_check.md)，以保证DSDL数据集可正常使用。