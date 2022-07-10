# Basic Types

**Basic types** are the types for basic elements in DSDL. The instances of basic types serve as the basic building blocks of a data set description. 

> **Note**: The underlying language, namely JSON and YAML, provides several primitive literals, such as boolean, number, string. 
> While using such literals to express values, DSDL maintains its own basic types. 
> It is important to note that association between DSDL basic types and JSON primitive types is **NOT** one-to-one. 
> Different DSDL basic types can adopt the same primitive type for expressing their values. For example, object locators and labels are of different types (``Loc`` and ``Label`` in this example) in DSDL, but they both use strings for expressing values.

## Generic basic types

DSDL defines four generic basic types. The values of such types are simply interpreted, without special meaning. 

- ``Bool``: boolean type, which can take either of the two values: ``true`` and ``false``.
- ``Int``: integer type, which can take any integral values, such as ``12``, ``-3``, or ``0``. When a number has the ``Int`` type, the DSDL interpreter should verify if it is actually an integer.
- ``Num``: general numeric type, which can take any numeric values, such as ``12.5``, ``-13``, ``1.25e-6``. 
- ``Str``: string type, which can take arbitrary strings, such as ``"hello"``, ``"a"``, ``""``.


## Special basic types

DSDL defines a collection of basic types with special meanings. The values of these types are also expressed as strings or other common JSON forms, but they have specific semantics and DSDL interpreter will interpret them accordingly.

- ``Coord``: 2D coordinate in the form of ``[x, y]``.
- ``Coord3D```: 3D coordinate in the form of ``[x, y, z]``.
- ``Interval``: sequential interval in the form of ``[begin, end]``.
- ``BBox``: bounding box in the form of ``[x, y, w, h]``.
- ``Polygon``: polygon represented in the form of a series of 2D coordinates as ``[[x1, y1], [x2, y2], ...]``.
- ``Date``: date represented by a string, according to the [strftime spec](https://strftime.org/).
- ``Time``: time represented by a string, according to the [strftime spec](https://strftime.org/).

## Label: class label type

Classification is a common way to endow an object with semantic meaning. In this approach, **class labels** are often used to express the category which an object belongs to. In DSDL, class labels are strings with type ``Label``. 

In practice, labels in different classification domains are different. DSDL introduces the concept of **class domain** to represent different contexts for classification. Each class domain provides a class list or a class hierarchy. Given a class domain, the labels are can be expressed in either of the following two forms:

- **name-based**: with format ``"<class-domain>::<class-name>"``, *e.g.* ``"COCO::cat"`` represents the class *cat* in the *COCO* domain.
- **index-based**: with format ``"<class-domain>[class-index]"``, *e.g.* ``"COCO[3]"`` represents thr 3rd class in the *COCO* domain.

For a class domain with a multi-level class hierarchy, the class label can be expressed as a dot-delimited path, such as ``"MyDom::animal.dog.hound"`` or ``"MyDom[3.2.5]"``.

> **Note**: We are working on unifying class systems for specific areas. The efforts would result in a standard classification domain. We reserve the domain name ``std`` for this.

## Loc: object locator type

Object locators are used as references to unstructured objects, such as images, videos, and texts. They are instances of the type ``Loc``, and are represented by a specially-formatted string. Specifically, DSDL supports three ways to express an object locator:

- **relative path**: the path relative to the root data path. This is the default way. When there is no special prefix, an object locator string will be treated as a relative path. For example, ``"abc/001.jpg"`` will be interpreted as ``"<data-root>/abc/001.jpg"``, where ``data-root`` is the root directory where all data objects are stored and can be specified via environment configurations.
- **alias path**: when a data set comprises data objects stored in multiple source directories, one can use alias to simplify the expression of paths, e.g. ``"$mydir1/abc/001.jpg"``, where ``$`` implies that ``mydir1`` is an alias, which should be specified by either by a global variable in the description file or by an environment variable.
- **object id**: a string with prefix ``::``, e.g. ``"::cuhk.ie::abcd1234xyz"``, where ``cuhk.ie`` is the name of a data domain, while ``abcd1234xyz`` is an ID string which uniquely identifies an data object in the data domain. When object ids are used, the data platform needs to provide a Key-value mapping facility to map an ID string to the corresponding actual address.


## Using type parameters

From the standpoint of the DSDL interpretator, the type of an element determines how that element is intepreted and validated. In addition to the type name itself, DSDL allows one to provide **type parameters** to customize how the corresponding elements should be expressed, interpreted, and validated.

**Label type with parameters**

In the example in {ref}`get_started`, the field ``label`` of ``ImageClassificationSample`` has the type specified as ``Label[dom=MyClassDom]``.

Here, ``Label`` is a **parametric type**, which accepts a **type parameter** ``dom``. This ``dom`` parameter specifies the class domain where the label comes from. 

When the domain is explicitly given (here it is given as ``MyClassDom``), there is no need to provide the class domain names in the values, and thus the labels can be expressed as either the class name or the index. For example, a value ``"cat"`` indicates the fully qualified label ``"MyClassDom::cat"``; an integer value ``2`` indicates the class label ``"MyClassDom[2]"``.

**Date and Time types with parameters**

For ``Date`` and ``Time`` types, when no parameters are explicitly provided, the values should conform to the ISO 8601 format. The interpreter will invoke ``date.fromisoformat`` and ``time.fromisoformat`` methods to parse the string.

One can also specify a customized format using the type parameter ``fmt``. For example, one can use a type ``Time[fmt="%H:%M"]``, which requires the value should follow the ``%H:%M`` format, *e.g.* ``"15:32"``. 
When ``fmt`` is explicitly specified, the value of ``fmt`` will be fed to ``strptime`` function to parse the time string. 
Note that this parameter also works for ``Date`` type.


## List type

DSDL provides a parametric type ``List`` to express unordered or ordered lists. 
Specifically, an instance of ``List`` is a list that contains multiple elements of a certain element type.

The parametric type ``List`` has two parameters:

- ``etype``: the type of each individual element. This parameter must be explicitly specified. 
- ``ordered``: whether there is an sequential order among elements. This parameter is optional, and its default value is ``false``. This need should only be set to ``true`` for truly sequential types, *e.g.* sequence of video frames or time series. 

For example, for a list of integers, we can specify the type as ``List[Int]``; for a list of class labels within the domain ``MyClassDom``, we can specify the type as ``List[Label[MyClassDom]]``.
