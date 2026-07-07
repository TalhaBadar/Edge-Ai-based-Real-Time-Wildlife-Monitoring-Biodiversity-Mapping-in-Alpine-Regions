import argparse
from ultralytics import YOLO


def detect_tflite(model_path: str, source: str, conf: float):
    """Test exported TensorFlow Lite model using Ultralytics inference wrapper."""
    model = YOLO(model_path)
    model.predict(source=source, conf=conf, save=True, project="outputs", name="tflite_detection")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run inference with exported TFLite YOLO model")
    parser.add_argument("--model", default="models/best.tflite")
    parser.add_argument("--source", required=True)
    parser.add_argument("--conf", type=float, default=0.5)
    args = parser.parse_args()
    detect_tflite(args.model, args.source, args.conf)
