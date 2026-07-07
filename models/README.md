# Models Folder

Place trained and exported models here:

```text
models/
├── best.pt        # YOLOv8n trained model
├── best.tflite    # TensorFlow Lite export for mobile app testing
├── best.onnx      # Optional ONNX export
└── best.engine    # Optional TensorRT engine for Jetson
```

This repository does not include your actual trained model weights. Copy your `best.pt` from YOLO training results into this folder.
