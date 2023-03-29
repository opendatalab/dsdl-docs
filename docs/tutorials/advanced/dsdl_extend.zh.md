# DSDL类型扩展

DSDL已经支持很多基础类型Field（Bool、Int、Num、Str、Dict、Date、Time），标注类型Field（Coord、Coord3D、Interval、BBox、RotatedBBox、Polygon、Label、Keypoint、Text、ImageShape、UniqueID、InstanceID）以及媒体类型Field（Image、LabelMap、InstanceMap）。但在一些特殊情况下，这些预设的Field无法满足用户的开发需求，因此本章节会详解在DSDL中Field是如何定义的，从而方便用户自己拓展