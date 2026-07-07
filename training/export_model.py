import argparse
from ultralytics import YOLO


def export(weights: str, fmt: str, imgsz: int = 640):
    """Export YOLO model to tflite, onnx, engine, torchscript, etc."""
    model = YOLO(weights)
    model.export(format=fmt, imgsz=imgsz)
    print(f"Export completed: {fmt}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export YOLOv8 model")
    parser.add_argument("--weights", default="models/best.pt")
    parser.add_argument("--format", default="tflite", choices=["tflite", "onnx", "engine", "torchscript", "openvino"])
    parser.add_argument("--imgsz", type=int, default=640)
    args = parser.parse_args()
    export(args.weights, args.format, args.imgsz)
