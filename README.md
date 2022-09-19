English | [简体中文](./README-zh_CN.md)

## Introduction

DSDL (Data Set Description Language) is a new generation of AI data set description language, which aims to solve the problem of inconvenient use caused by the non-uniform format of AI data sets. The ultimate goal is to achieve interoperability between different tasks and different modal data in the future to promote the further development of AI.

<details open>
<summary> Design Goals </summary>
  The design of DSDL is driven by three goals, namely generic, portable, extensible. We refer to these three goals together as GPE.

- **Generic**
  This language aims to provide a unified representation standard for data in multiple fields of artificial intelligence, rather than being designed for a single field or task. It should be able to express data sets with different modalities and structures in a consistent format.

- **Portable**
  Write once, distribute everywhere. \\

  Dataset descriptions can be widely distributed and exchanged, and used in different environments without modification of the source files. The achievement of this goal is crucial for creating an open and thriving ecosystem. To this end, we need to carefully examine the details of the design, and remove unnecessary dependencies on specific assumptions about the underlying facilities or organizations.

- **Extensible**
  One should be able to extend the boundary of expression without modifying the core standard. For a programming language such as C++ or Python, its application boundaries can be significantly extended by libraries or packages, while the core language remains stable over a long period. Such libraries and packages form a rich ecosystem, making the language stay alive for a very long time.

</details>

## Documentation

[DSDL Specification and Tutorials](https://opendatalab.github.io/dsdl-docs/)

## License

This project is released under the [Apache 2.0 license](LICENSE)。
