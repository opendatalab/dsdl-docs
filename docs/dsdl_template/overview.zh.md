# 任务模板介绍

为了方便用户对任务模板进行使用和定义，我们提供了一系列CV和NLP任务的模板。

以下表格展示了目前提供的任务模板：

- **任务中文名称**
- **任务英文全称**：如果需要调用模板进行数据集的DSDL转换，可以直接利用任务英文全称进行调用，详情请见[数据集转换页面](../tutorials/advanced/dsdl_convert.md)。
- **任务英文简称**：用户从OpenDataLab下载到的DSDL数据集中的DSDL标注将以dsdl_[task_name]_[lite/full]的方式命名，其中的[task_name]即为任务英文简称。
- **任务模板详情页**：用户可以进行任务模板详情页了解任务的具体信息（任务调研和测评指标），以及模板中各个字段的含义。

CV相关的任务模板如下：

<table border="4" >
        <tr>
      <th rowspan="1" align=center colspan="1" align=center>任务中文名称</th>
      <th colspan="1" align=center>任务英文全称</th>
      <th colspan="1" align=center>任务英文简称</th>
      <th colspan="1" align=center>任务模板详情页</th>
    </tr>
    <tr>
      <th width="15%" align="center">图像分类</th>
      <td width="8%" align="center">Image Classification</th>
      <td width="8%" align="center">Cls</th>
      <td width="8%" align="center"><a href="../cv/cv_classification">图像分类</a></th>
    </tr>
    <tr>
      <th width="15%" align="center">目标检测</th>
      <td width="8%" align="center">Object Detection</td>
      <td width="8%" align="center">Det</td>
      <td width="8%" align="center"><a href="../cv/cv_detection">目标检测</a></td>
    </tr>
    <tr>
      <th width="15%" align="center">语义分割</th>
      <td width="8%" align="center">Semantic Segmentation</td>
      <td width="8%" align="center">SemSeg</td>
      <td width="8%" align="center" rowspan="4"><a href="../cv/cv_segmentation">图像分割</a></td>
    </tr>
    <tr>
      <th width="15%" align="center">实例分割-polygon标注</th>
      <td width="8%" align="center">Instance Segmentation-polygon</td>
      <td width="8%" align="center">SemSeg</td>
    </tr>
    <tr>
      <th width="15%" align="center">实例分割-分割图标注</th>
      <td width="8%" align="center">Instance Segmentation-segmap</td>
      <td width="8%" align="center">SemSeg</td>
    </tr>
    <tr>
      <th width="15%" align="center">全景分割</th>
      <td width="8%" align="center">Panoptic Segmentation</td>
      <td width="8%" align="center">PanSeg</td>
    </tr>
    <tr>
      <th width="15%" align="center">关键点检测</th>
      <td width="8%" align="center">Keypoint Detection</td>
      <td width="8%" align="center">KeyDet</td>
      <td width="8%" align="center"><a href="../cv/cv_keypoint_detection">关键点检测</a></td>
    </tr>
    <tr>
      <th width="15%" align="center">目标跟踪</th>
      <td width="8%" align="center">Object Tracking</td>
      <td width="8%" align="center">SOT</td>
      <td width="8%" align="center"><a href="../cv/cv_object_tracking">目标跟踪</a></td>
    </tr>
    <tr>
      <th width="15%" align="center">旋转目标检测</th>
      <td width="8%" align="center">Rotated Object Detection</td>
      <td width="8%" align="center">RotDet</td>
      <td width="8%" align="center"><a href="../cv/cv_rotated_detection">旋转目标检测</a></td>
    </tr>
    <tr>
      <th width="15%" align="center">光学字符识别-检测</th>
      <td width="8%" align="center">Optical Character Recognition-detection</td>
      <td width="8%" align="center">OCR</td>
      <td width="8%" align="center" rowspan="4"><a href="../cv/cv_ocr">光学字符识别(OCR)</a></td>
    </tr>
    <tr>
      <th width="15%" align="center">光学字符识别-分割</th>
      <td width="8%" align="center">Optical Character Recognition-segmentation</td>
      <td width="8%" align="center">OCR</td>
    </tr>
    <tr>
      <th width="15%" align="center">光学字符识别-识别</th>
      <td width="8%" align="center">Optical Character Recognition-recognition</td>
      <td width="8%" align="center">OCR</td>
    </tr>
    <tr>
      <th width="15%" align="center">光学字符识别-端到端</th>
      <td width="8%" align="center">Optical Character Recognition-end_to_end</td>
      <td width="8%" align="center">OCR</td>
    </tr>
    <tr>
      <th width="15%" align="center">图像生成</th>
      <td width="8%" align="center">Image Generation</td>
      <td width="8%" align="center">Gen</td>
      <td width="8%" align="center"><a href="../cv/cv_generation">图像生成</a></td>
    </tr>
  </table>
