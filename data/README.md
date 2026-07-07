# Dataset Folder

Expected YOLOv8 structure:

```text
data/
├── dataset.yaml
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

Each image must have a matching `.txt` label file in YOLO format:

```text
class_id x_center y_center width height
```

All bounding box values must be normalized between 0 and 1.
