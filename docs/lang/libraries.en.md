# Libraries

Whereas we are already trying to simplify the design of DSDL, some efforts remain needed to learn how to define classes in DSDL.
However, we understand that most AI researchers or developers don't want to learn yet another language. 
Hence, we introduce libraries to further simplify the process of data set description.

## Define and import a library

Consider the example in {ref}`get_started`, the part that defines the class ``ImageClassificationSample`` is quite generic and can be used in many data sets. Hence, we can extract it to a **library file**, while the data set description file can just import it. 

In general, a **library file** is a file in YAML or JSON format that provides a collection of definitions. 

In the example above, we can provide a library file named `imageclass.yaml` as follows:

```yaml
# file: imageclass.yaml

# DSDL version is mandatory here.
$dsdl-version: "0.5.0"

# -- below are definitions --

MyClassDom:
    $def: class_domain
    classes:
        - dog
        - cat
        - fish
        - tiger

ImageClassificationSample:
    $def: struct
    $fields:
        image: Image
        label: Label[dom=MyClassDom]
```

> **Note**: 
>
> * This library file should be placed in the default library path so the system can find it. 
> * One can also supply additional library paths by setting an environment variable ``DSDL_LIBRARY_PATH``.

Then the data set description can be simplified by importing the library, as follows:

```yaml
$dsdl-version: "0.5.0"
$import: 
    - imageclass
meta:
    name: "my-dataset"
    creator: "my-team"
    dataset-version: "1.0.0"
data:
    sample-type: ImageClassificationSample
    samples:
        - { image: "xyz/0001.jpg", label: "cat" }
        - { image: "xyz/0002.jpg", label: "dog" }
```

Here, we use an ``$import`` directive in the header section. The content of ``$import`` should be a list, which means that one can import multiple files. 

> **Note**: When multiple library files being imported contain definitions of the same name, then the definition imported later will overwrite previous ones. In this case, the interpreter should raise a warning. 

## Better Practice of Using Libraries

Here are some good practice for defining a DSDL library:

**Define generic classes:**

As discussed in :ref:`parametric_class`, it is not a good idea to involving specific settings of parameters in a generic class definition. 
Hence, it is strongly suggested that one defines a parametric class if the class requires specific information related to a particular application (*e.g.* class domains) in order to be completed. 

**Grouped definitions:**

It is advisable to put multiple definitions related to a certain area into one library file. 
This is makes it easier to distribute and import.

**Documentation:**

Document the definitions to make it easier for users to understand.

Below is an example where we put multiple classes related to visual recognition into a single library file:

```yaml
# file: visualrecog.yaml

ImageClassificationSample:
    # Each image classification sample contains an image and a label.
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        label: Label[dom=$cdom]

LocalObjectEntry:
    # Each local object entry contains a bounding box and a label.
    $def: struct
    $params: ['cdom']
    $fields:
        bbox: BBox
        label: Label[dom=$cdom]

ObjectDetectionSample:
    # Each object detection sample contains an image and a list of local object entries.
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        objects: List[etype=LocalObjectEntry[cdom=$cdom]]
```

With this library, one can write a data set description as follows:

```yaml
$dsdl-version: "0.5.0"
$import: 
    - visualrecog
meta:
    name: "my-dataset"
    creator: "my-team"
    dataset-version: "1.0.0"
defs:
    MyClassDom:
        $def: class_domain
        classes:
            - dog
            - cat
            - fish
            - tiger
data:
    sample-type: ImageClassificationSample
    samples:
        - { image: "xyz/0001.jpg", label: "cat" }
        - { image: "xyz/0002.jpg", label: "dog" }
```

Since ``MyClassDom`` is a specific definition only used in this dataset. Hence, it is fine to define it in the description file itself as a customized definition, while importing common classes from a library.

> **Note**:
>
> The library ``visualrecog`` is an example just for illustration. Along with DSDL, we provide a standard library named ``cv`` that contains a rich collection of definitions related to computer vision, including various types and commonly used class domains, etc. 
