# Computer Vision Examples

```{note}
All classes defined in this section will be provided in a standard library
named ``cv``. General users just need to import ``cv``, and don't need to 
write the class definitions by themselves.

Through out the example below, we use a class domain named ``MyClassDom``.
```

## Image Classification

The task of image classification is to assign a class label to each image.

**Sample class definition:**

```yaml
ImageClassificationSample:
    # Each sample contains an image together with a class label (optional).
    $def: struct
    $params: ['cdom'] 
    $fields:
        image: Image
        label: Label[dom=$cdom]
    $optional: ['label']
```

Here, the fields in the ``$optional`` list can be omitted in the data samples. 
When ``label`` is omitted, the corresponding field value will be set to a null value (in Python it is ``None``).


**Data samples:**

```yaml
data:
    sample-type: ImageClassificationSample[cdom=MyClassDom]
    samples:
        - { image: "xyz/0001.jpg", label: "cat" }
        - { image: "xyz/0002.jpg", label: "dog" }
        - { image: "xyz/0003.jpg" }
```

## Object Detection

The task of object detection is to detect meaningful objects on an image.
Each detected object can be represented by a bounding box together with an object class label.

**Sample class definition:**

```yaml
LocalObjectEntry:
    # Each sample contains a bounding box together a class label (optional).
    $def: struct
    $params: ['cdom']
    $fields:
        bbox: BBox
        label: Label[dom=$cdom]
    $optional: ['label']

ObjectDetectionSample:
    # Each sample contains an image together with a list of local objects.
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        objects: List[LocalObjectEntry[cdom=$cdom]]
```

**Data samples:**

```yaml
data:
    sample-type: ObjectDetectionSample[cdom=MyClassDom]
    samples:
        - image: "xyz/0001.jpg"
            objects: 
            - { bbox: [x1, y1, w1, h1], label: 1 }
            - { bbox: [x2, y2, w2, h2], label: 2 }
            - { bbox: [x3, y3, w3, h3], label: 2 }
        - image: "xyz/0002.jpg"
            objects: 
            - { bbox: [x4, y4, w4, h4], label: 3 }
            - { bbox: [x5, y5, w5, h5], label: 4 }
```


## Object Detection with Scene Classification

In certain applications, scene classification (at the image level) and object detection are combined into a joint task. 

For such a task, we can have two class domains, say ``SceneDom`` and ``ObjectDom``, respectively for scene classes and object classes. 

**Sample class definition:**

```yaml
SceneAndObjectSample:
    # Each samples contains an image, a scene label (optional)
    # together with a list of local objects.
    $def: struct
    $params: ['scenedom', 'objectdom']
    $fields:
        image: Image 
        sclabel: Label[dom=$scenedom]
        objects: List[LocalObjectEntry[cdom=$objectdom]]
    $optional: ['sclabel']
```

**Data samples:**

```yaml
data:
    sample-type: SceneAndObjectSample[scenedom=SceneDom, objectdom=ObjectDom]
    samples:
        - image: "xyz/0001.jpg"
            sclabel: "street"
            objects: 
            - { bbox: [x1, y1, w1, h1], label: 1 }
            - { bbox: [x2, y2, w2, h2], label: 2 }
            - { bbox: [x3, y3, w3, h3], label: 2 }
        - image: "xyz/0002.jpg"
            sclabel: "river"
            objects: 
            - { bbox: [x4, y4, w4, h4], label: 3 }
            - { bbox: [x5, y5, w5, h5], label: 4 }
```

## Image Segmentation

The image segmentation task is to assign pixel-wise labels to an image. 
A common practice is to use a labelmap, which is stored as an unstructured object in an external file. 

**Sample class definition:**

```yaml
ImageSegmentationSample:
    # Each sample contains an image together with a label map.
    $def: struct
    $params: ['cdom']
    $fields:
        image: Image
        labelmap: LabelMap[dom=$cdom]
```
        
**Data samples:**

```yaml
data:
    sample-type: ImageSegmentationSample[cdom=MyClassDom]
    samples:
        - { image: "imgs/0001.jpg", labelmap: "maps/0001.ppm" }
        - { image: "imgs/0002.jpg", labelmap: "maps/0002.ppm" }
        - { image: "imgs/0003.jpg", labelmap: "maps/0003.ppm" }
```