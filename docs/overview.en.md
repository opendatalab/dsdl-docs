# Overview


Data is the cornerstone of artificial intelligence. The efficiency of data acquisition, exchange, and application directly impacts the advances in technologies and applications. Over the long history of AI, a vast quantity of data sets have been developed and distributed. However, these datasets are defined in very different forms, which incurs significant overhead when it comes to exchange, integration, and utilization -- it is often the case that one needs to develop a new customized tool or script in order to incorporate a new dataset into a workflow.

To overcome such difficulties, we develop **Data Set Description Language (DSDL)**.

## Design Goals

The design of **DSDL** is driven by three goals, namely *generic*, *portable*, *extensible*. We refer to these three goals together as **GPE**.

**Generic**

This language aims to provide a unified representation standard for data in multiple fields of artificial intelligence, rather than being designed for a single field or task. It should be able to express data sets with different modalities and structures in a consistent format.

**Portable**

Write once, distribute everywhere.

Dataset descriptions can be widely distributed and exchanged, and used in different environments without modification of the source files. The achievement of this goal is crucial for creating an open and thriving ecosystem. To this end, we need to carefully examine the details of the design, and remove unnecessary dependencies on specific assumptions about the underlying facilities or organizations. 

**Extensible**

One should be able to extend the boundary of expression without modifying the core standard. For a programming language such as C++ or Python, its application boundaries can be significantly extended by libraries or packages, while the core language remains stable over a long period. Such libraries and packages form a rich ecosystem, making the language stay alive for a very long time.

## Design Overview

A data set is essentially a data structure stored in persistent storages. In general, it comprises unstructured objects, *e.g.* images, videos, and texts, together with associated annotations. Such elements are aggregated in certain ways into a data set. 

It is noteworthy that the unstructured objects mentioned above usually contain large volume of data. To facilitate quick distribution of data sets, our design separates the structured description of a dataset from the content of unstructured objects. 

Below is an overall summary of the language design:

### Basic data model

DSDL describes a data set with a collection of basic elements organized via containers such as *structs*, *lists*, and *sets*. 

* **Basic elements** are individual units in a data set description, which include not only the primitives such as numbers, strings, but also those elements that facilitate the expression of object locations, annotations, etc.
* **Unstructured objects** such as images, videos, and texts, are special basic elements, as they are *indivisible* in a data set description. In particular, an unstructured object is represented by an object locator which tells where it is stored instead of being embedded into the description entirely. Optionally, additional descriptors can be used to provide additional information about the object, *e.g.* the format or resolution of an image.
* **Aggregates** are used to organize basic elements into a data structure. DSDL provides list and struct types to express aggregate data structures. In particular, individual samples are represented by a struct (an aggregate of multiple fields), while a data set consists of a list of samples.

### Extensible type system

All elements and structured units in DSDL have types. 

DSDL adopts a *simple* yet *extensible* type systems. Specifically, there are three kinds of types in DSDL:

* **Primitive types** are the types of primitive values such as booleans, numbers, and strings. DSDL provides a large collection of primitive types, which serve as the basic building blocks of the description.  Note that different primitive types in DSDL can be expressed in the same form. For example, object locators and time stamps both use strings as their expression form, but the string values will be interpreted diffferently depending on the underlying types.
* **Unstructured object classes** are the abstractions for unstructured objects, such as images, videos, audios, point clouds, texts, etc. Such objects, despite their rich internal structures, are considered as indivisible units in data set definitions.  DSDL provides a collection of pre-defined unstructured object classes to cover common applications, while allowing 3rd parties to extend this collection by registering new unstructured object classes via a minimal set of interfaces. 
* **Struct classes** are the abstractions for aggregate data structures in DSDL. Each instance of a struct class is called a **struct**, which contains multiple fields, each with its own type. An important application of structs are to represent data samples. DSDL comes with a collection of predefined struct classes for commonly seen tasks in the standard library, while allowing users to define their own struct classes for special tasks.

```{note}
Types need to be defined (either builtin, by 3rd parties, or by the user) before they are used. Circular references are not allowed in this version of DSDL.
```

### Object locators

As mentioned, unstructured objects are not embedded entirely into the data set description. Instead, they are referred to by **object locators**. In particular, an object locator is a string with special format, which will be converted into an actual address by the DSDL interpreter when the corresponding object is to be loaded. 

The introduction of object locators is the key to separating the structured description of the data set from the unstructured media content. This way not only enables light-weight distribution of data set descriptions without moving the large volume of media data, but also allows quick manipulation of a data set, *e.g.* combining multiple sets, merging properties, or taking a subset.

### Based on JSON or YAML

DSDL is a **domain-specific language** based on popular data exchange languages: [JSON](https://www.json.org/) or [YAML](https://yaml.org/). Note that the elements in JSON or YAML are not associated with specific meanings at the language level. By endowing such elements with semantics, DSDL can describe a data set in a meaningful manner. 

This design choice allows one to leverage the rich tool systems already available for JSON and YAML. With such tools, one can readily build a full-fledged system that fully supports interpretation, validation, and query, and as well as the interoperability with the Internet ecosystem.
