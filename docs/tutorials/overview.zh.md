在正式进入学习前，我们将简单介绍数据集使用现状及问题，由此提出对应的解决思路和方案，旨在让用户操作数据更加得心应手。

### 数据集现状

对于数据集发布方，由于没有统一的规范和标准约束数据集描述方式及发布途径，使得：    

- 不同的数据集有不同的组织结构，标注格式；  
- 不同的数据集发布方式不同：官网、Github、网盘、邮箱申请等等；  

上述现象使得数据集使用者在数据获取和使用时存在一系列问题：  

- 获取数据集需要基于搜索引擎查看、对比，才能找到想用的数据集；  
- 网络不稳定时无法确定下载数据集完整性；  
- 对数据集分析、查看通常需要自己写脚本处理；  
- 对数据集训练、推理通常需要格式转换或者重写DataLoader；  
- 同一任务的不同数据集，需统一格式转换后才能统一使用；

为了解决数据检索和下载问题，我们搭建**OpenDataLab公开数据集平台**，收集了大量AI数据集，并对LICENSE、元信息等进行整理，提供高效检索和高速下载能力。  

为了解决数据集无统一规范而导致的数据集使用繁杂问题，我们提出了新一代AI数据集描述语言**DSDL**（Data Set Description Language），DSDL可以让不同任务、甚至不同模态的数据标注以相对统一的规范进行描述，用户无需再为格式统一问题而在数据使用的各个环节耗费时间。  

为了方便用户快速的对数据进行检索、下载、管理、统计分析、可视化等操作，我们提供了一整套的数据工具链**ODL** (Open Dataset Library)，可大幅提升用户使用数据效率。


用户教程将对AI模型开发全流程中的数据操作进行展开：

<details>
<summary><font size=5>1.数据集下载</font></summary>
 <ul>
     <li>情形1: 原始数据集+DSDL标注文件可直接下载</li>
     <li>情形2：原始数据集需自行下载</li>
     <li>情形3：DSDL标注文件需自行转换</li>
 </ul>
</details>


<details>
<summary><font size=5>2.数据集分析</font></summary>
 <ul>
     <li>数据集统计信息</li>
     <li>数据集可视化分析</li>
 </ul>
</details>


<details>
<summary><font size=5>3.模型训练</font></summary>
 <ul>
     <li>配置文件准备</li>
     <li>模型训练</li>
 </ul>
</details>


<details>
<summary><font size=5>4.模型推理</font></summary>
 <ul>
     <li>模型推理</li>
     <li>推理结果格式查看</li>
 </ul>
</details>


<details>
<summary><font size=5>5.数据/模型分析</font></summary>
 <ul>
     <li>模型指标评估</li>
     <li>结果可视化分析</li>
 </ul>
</details>


<details>
<summary><font size=5>6.数据集分发</font></summary>
 <ul>
     <li>公开数据集新版本标注共享</li>
     <li>公开数据集上传</li>
 </ul>
</details>

<details>
<summary><font size=5>高阶教程</font></summary>
 <ul>
     <li>1.自定义DSDL数据集</li>
     <li>2.DSDL数据集格式转换</li>
     <li>3.DSDL DataLoader开发</li>
 </ul>
</details>
