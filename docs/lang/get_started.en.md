(get_started)=

# Get Started

In DSDL, a data set is described by a *data set description file*. 
Below is an example that illustrates a typical data set description file. 

The data set description file can be in either JSON or YAML format. 

**JSON Format:**

```json
    {
        "$dsdl-version": "0.5.0",
        "meta": {
            "name": "my-dataset",
            "creator": "my-team",
            "dataset-version": "1.0.0"
        },
        "defs": {
            "MyClassDom": {
                "$def": "class_domain",
                "classes": [
                    "dog",
                    "cat",
                    "fish",
                    "tiger"
                ]
            },
            "ImageClassificationSample" : {
                "$def": "struct",
                "$fields": {
                    "image": "Image",
                    "label": "Label[dom=MyClassDom]"
                }
            }
        },
        "data": {
            "sample-type": "ImageClassificationSample",
            "samples": [
                { "image": "xyz/0001.jpg", "label": "cat" },
                { "image": "xyz/0002.jpg", "label": "dog" }
            ]
        }
    }
```

**YAML format:**

```yaml

    $dsdl-version: "0.5.0"
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
        ImageClassificationSample:
            $def: struct
            $fields:
                image: Image
                label: Label[dom=MyClassDom]
    data:
        sample-type: ImageClassificationSample
        samples:
            - { image: "xyz/0001.jpg", label: "cat" }
            - { image: "xyz/0002.jpg", label: "dog" }
```

```{note}
Both JSON and YAML formats can express **exactly the same** data structure. 
Due to YAML's more concise form and that it allows comments, we will use YAML as the default format in later examples of this document, which can be easily translated into JSON format.
```

At the top level, the file consists of four parts:

- **header** specifies about how the description file should be interpreted;
- **meta section** provides meta information about the data set;
- **defs section** provides global definitions, *e.g.* user-defined types;
- **data section** describes the data contained in the data set.

```{note}
- The property names with a prefix ``$`` are reserved by DSDL for special meaning. 
- DSDL version (the property with name ``$dsdl-version`` in the header) must be explicitly specified. It is crucial for the DSDL interpreter to know the language version in order to interpret the description correctly.
- The definition for common types are often provided in standard or extended libraries. In most cases, users don't need to define their own types. In this example, we define ``ImageClassificationSample`` just for the purpose of illustration and being self-contained.
```
