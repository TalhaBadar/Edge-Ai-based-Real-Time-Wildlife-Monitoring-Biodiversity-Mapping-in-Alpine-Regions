# Wildlife Detection AI Module

This repository contains the AI and edge-device code for the FYP:

**Edge AI-based Wildlife Detection and Biodiversity Mapping in Alpine Regions**

The mobile application code is intentionally not included because it is maintained separately. This repository focuses on the AI pipeline, model training, model export, inference, Jetson Nano deployment, AGX/USB/CSI camera inference, offline caching, alert handling, and Firebase synchronization.

## Main Workflow

1. Dataset is prepared in YOLO format after annotation using CVAT and preprocessing/export through Roboflow.
2. YOLOv8n is trained on the custom wildlife dataset.
3. The trained model is validated and evaluated using precision, recall, and mAP.
4. The model is exported to TensorFlow Lite, ONNX, or TensorRT depending on deployment target.
5. On Jetson Nano, the camera captures frames and the model performs real-time detection.
6. Each detection record stores species name, confidence score, bounding box, timestamp, image path, location, device ID, and source.
7. If internet is available, the record and image are uploaded to Firebase.
8. If internet is unavailable, records are stored locally in SQLite and synchronized later.
9. Dangerous animal detections generate local alerts and can also trigger mobile notifications through Firebase.

## Dataset

The project dataset contains approximately 17,000 labeled images across 14 animal species:

- Boar
- Buffalo
- Cat
- Chicken
- Cow
- Dog
- Donkey
- Goat
- Horse
- KomodoDragon
- Lion
- Sheep
- Snake
- Tiger

## Important Notes

- Place your trained model at `models/best.pt`.
- Place your TensorFlow Lite model at `models/best.tflite` after export.
- Place your Firebase service account file at `firebase/serviceAccount.json`.
- Update `configs/config.yaml` before running on your machine or Jetson Nano.
- Do not commit real Firebase credentials to GitHub.

## Quick Start

Install requirements:

```bash
pip install -r requirements.txt
```

Train model:

```bash
python training/train_yolov8.py --config configs/config.yaml
```

Validate model:

```bash
python training/validate_yolov8.py --config configs/config.yaml
```

Export model:

```bash
python training/export_model.py --weights models/best.pt --format tflite
```

Run image inference:

```bash
python inference/detect_image.py --weights models/best.pt --source path/to/image.jpg
```

Run edge detection:

```bash
python edge/main_edge.py --config configs/config.yaml
```

Sync cached detections:

```bash
python edge/upload_cached.py --config configs/config.yaml
```
