[English](./README.md) | 简体中文

## 简介

DSDL(Data Set Description Language)是新一代人工智能数据集描述语言, 旨在解决AI数据集格式不统一导致的使用不方便问题。最终目标是在未来做到不同任务、不同模态数据间互通互联，推动人工智能进一步发展。

<details open>
<summary>语言特性</summary>

- **通用性**
  该语言主要目的是提供一种统一表示的标准，可以覆盖各个领域的人工智能数据，而不是基于特定的一种任务或者某个领域设计。该语言应该可以用一致的格式来表达不同模态和结构的数据。

- **便携性**
  写完无需修改，随处分发。

  数据集描述可以被广泛的分发和交换，不需要修改就可以在各种环境下使用。这一目标的实现对于建立开发繁荣生态至关重要。为此我们需要仔细检查实现细节，使其对底层设施或组织无感知，从而去除基于特定假设的无必要依赖。

- **可拓展性**
  在不需要修改核心标准的情况下可以拓展表述的边界。对于C++或者Python等编程语言，应用边界可以通过使用链接库或者软件包得以显著拓展，而核心语法可以在很长的时间内保持稳定。基于链接库和包，可以形成丰富的生态系统，使对应语言可以长时间保持活跃度和发展。

</details>

## 文档

[DSDL入门文档](https://opendatalab.github.io/dsdl-docs/)

## 引用

```bibtex
@misc{wang2024dsdl,
      title={DSDL: Data Set Description Language for Bridging Modalities and Tasks in AI Data}, 
      author={Bin Wang and Linke Ouyang and Fan Wu and Wenchang Ning and Xiao Han and Zhiyuan Zhao and Jiahui Peng and Yiying Jiang and Dahua Lin and Conghui He},
      year={2024},
      eprint={2405.18315},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```

## 开源许可证

该项目采用 [Apache 2.0 开源许可证](LICENSE)。
