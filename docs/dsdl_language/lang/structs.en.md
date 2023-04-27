# Struct Classes

Structs are the most common way to represent composite entities. For example, a typical sample in a data set is comprised of multiple elements, *e.g.* an image with a class label. Hence, structs are a good fit for representing data samples or its composite components. 

DSDL allows one to define **struct classes** to provide an abstraction for a particular type of structs. 

## Define a struct class

In DSDL, one can define a customized struct class in the ``defs`` section of a data set description file. In the example in {ref}`get_started`, we defined a struct class named ``ImageClassificationSample`` as follows:

```yaml
ImageClassificationSample:
    $def: struct
    $fields:
        image: Image
        label: Label[dom=MyClassDom]
```

This class definition is a JSON object, with the following properties:

- ``$defs``: its value must be ``"struct"``, indicating that it is defining a struct class. 
- ``$fields``: its value must be a JSON object containing a set of properties, each corresponding to a field. In particular, for each property of ``$field``, the key will be considered as the field name, while the value is the specification of the corresponding field. The field specification can be given in two ways:
    - **Just the type name**: just give the type name of the field (if that type involves parameters, then the parameters will be set in the default way).
    - **With parameters**: one can also specify certain type parameters using a JSON object, which contains a ``$type`` property to specify the type name, and other properties to specify the settings of type parameters. See thet ``label`` field specification above.


## Nested structs

In DSDL, structs can be nested. For example, an object detection sample may be comprised of an image together with a set of "local objects", where each local object can be represented by a struct with a bounding box and a class label. For such a sample, we can define a struct class as follows:

```yaml
LocalObjectEntry:
    # Each entry refers to an individual detected object on an image.
    $def: struct
    $fields:
        bbox: BBox
        label: Label[dom=MyClassDom]

ObjectDetectionSample:
    # Each sample contains the detection results on an image.
    $def: struct
    $fields:
        image: Image
        objects: List[etype=LocalObjectEntry]
```

Here, the structs of class ``LocalObjectEntry`` are embedded into the struct of class ``ObjectDetectionSample``. 

## Parametric struct classes

Note that in the example above, the struct class ``LocalObjectEntry`` uses a specific class domain ``MyClassDom``, while the struct class ``ObjectDetectionSample``, as it nests ``LocalObjectEntry``, also assumes the use of this particular class domain. Hence, such definitions are not generic. To use another class domain, one has to rewrite both classes. 

DSDL provides parametric struct classes to address this problem. 
Specifically, a **parametric struct class** can be considered as a class template, which allows the setting of certain parameters when the class is used. With parametric struct classes, we can define classes in a more generic way. 

Take the object detection example for instance. We can re-define the classes above as follows:

```yaml
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
        objects: List[etype=LocalObjectEntry[cdom=$cdom]]
```

Here, we introduce a property ``$params`` in struct class definition. When the ``$params`` property is explicitly given and non-empty, then the corresponding struct class is **parametric**. Note that when a parametric class is used, its parameters must be given in order to make it into a **concrete class**. 

Particularly, in the ``LocalObjectEntry`` class above, we introduce a **class parameter** ``cdom``, which are used in specifying the ``domain`` attribute of ``label``. Note that when a class parameter is used, it should be enclosed by `[]`. 
Then, the class ``ObjectDetectionSample`` is also defined as a parametric struct class with a parameter ``cdom``, and the parameter is used when specifying the type of ``objects``. 

With such class definitions, we can write the set of data samples as follows:

```yaml
data:
    sample-type: 
        $type: ObjectDetectionSample
        cdom: MyClassDom
    samples:
        - image: "abc/0001.jpg"
            objects:
            - { bbox: [1, 2, 3, 4], label: 1 }
            - { bbox: [5, 6, 7, 8], label: 2 }
        - image: "abc/0002.jpg"
            objects:
            - { bbox: [1, 2, 3, 4], label: 3 }
            - { bbox: [5, 6, 7, 8], label: 2 }
            - { bbox: [4, 3, 5, 8], label: 3 }
```

Note that with the parameter ``cdom`` is given as ``MyClassDom``, the parametric class ``ObjectDetectionSample`` is made into a concrete class and used in sample type specification.
