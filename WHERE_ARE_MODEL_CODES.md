# Where Are the Model Codes?

For this FYP, the trained model files are different from the model code.

## Trained Model Files

These are generated after training:

```text
models/best.pt
models/best.tflite
models/best.onnx
```

These are not source code. They are trained weights/exports.

## Model Code Files

The model code is available in these folders:

### 1. Model Wrapper

```text
model/wildlife_yolov8n.py
```

This file loads YOLOv8n and provides reusable detection functions.

### 2. Training Code

```text
training/train_yolov8n.py
```

This file defines how YOLOv8n was trained on the custom wildlife dataset.

### 3. Validation and Evaluation Code

```text
training/validate_yolov8n.py
training/evaluate_metrics.py
```

These files calculate precision, recall, mAP@0.5, and mAP@0.5:0.95.

### 4. Export Code

```text
training/export_model.py
```

This file converts `best.pt` into TensorFlow Lite, ONNX, or TensorRT formats.

### 5. Inference Code

```text
inference/detect_image.py
inference/detect_video.py
inference/detect_camera.py
```

These files run the trained model on images, videos, and live camera feeds.

### 6. Edge Deployment Code

```text
edge_deployment/jetson_agx_detection.py
```

This file runs the trained model on Jetson Nano with AGX/USB camera input.

## Important Note for Instructor

The YOLOv8n architecture itself is provided by the Ultralytics library.  
Our contribution is the custom training pipeline, dataset configuration, evaluation, export, inference, and deployment code developed for the wildlife detection system.
