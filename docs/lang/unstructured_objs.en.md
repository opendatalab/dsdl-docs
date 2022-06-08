# Unstructured Object Classes

**Unstructured objects**, such as images, videos, audios, point clouds, and texts, are digital representations of real-world objects. Despite their rich internal structures, they are treated as a whole in a data set description and their internal structures are not manifested. 

In DSDL, an **unstructured object class** provides an abstraction for all unstructured objects of a particular kind. 

## Pre-defined unstructured object classes

With the standard library, DSDL provides the following unstructured object classes out of the box:

- ``Image``: each instance is an image that can be represented as a matrix of pixels.
- ``Video``: each instance can be decoded into a sequence of frames, where each frame is an image.
- ``Audio``: each instance an audio signal that can be represented as a wave sequence.
- ``Text``:  each instance is a sequence of words.
- ``PointCloud``: each instance is a set of 3D points, which represents the shape of a 3D entity.
- ``LabelMap``: each instance is a matrix of integer labels, where each label corresponds to a class.


## Describe an unstructured object

In DSDL, an unstructured object can be specified with an object locator together with an optional descriptor that provides additional information about the object. 

Take an image stored at ``abc/0001.jpg`` for example. It can be expressed in either of the following ways:

- **Just the object locator**: simply use the object locator ``"abc/0001.jpg"``. When a variable or a field has an unstructured object class type and its value is a string, then that string will be interpreted as an object locator.

- **With a descriptor**: if one wants to provide additional information, say the size and the color format, then it can be expressed with an JSON object with two properties ``$loc`` and ``$descr``, like the following:

    ```yaml
        $loc: "abc/0001.jpg"
        $descr:
            size: [640, 480]
            color: "rgb"
    ```

Here, the descriptive information is provided via the ``$descr`` field, which will be used by the object loader of the corresponding unstructured object classes.


## Extended unstructured object classes

DSDL allows one to register **extended unstructured object classes** by specifying how to load the object from storage. 

At the client side, this can be accomplished by defining a sub-class of an abstract base class ``UnstructuredObject`` and implementing the ``load`` method for object loading. 

Specifically, in Python, the abstract base class ``UnstructuredObject`` are defined as follows.

```python
from abc import ABC, abstractmethod

class UnstructuredObject(ABC):
    """Abstract base class for unstructured objects."""

    @abstractmethod
    def load(file, descr):
        """Load an unstructured object from a given file-like object.
        
        Arguments:
            file:   file-like, from which the unstructured object is loaded.
            descr:  dict-like, which provides the descriptive information.

        Returns:
            The loaded object.
        """
        pass
```


```{note}
Note here that this ``load`` method accepts an file-like object, which is already open, instead of a file path. The design is based on the "Separation of Concerns" principle: it is the responsibility of the data system to interpret the object locator and construct a file reader accordingly. A specific subclass of ``UnstructuredObject`` only needs to care about how to load, interpret, and validate the object given a file reader. 
```
