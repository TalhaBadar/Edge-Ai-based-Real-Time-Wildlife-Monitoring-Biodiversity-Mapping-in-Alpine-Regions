import argparse
from pathlib import Path
from ultralytics import YOLO
from utils.common import ensure_dir


def detect(weights: str, source: str, conf: float, output: str):
    model = YOLO(weights)
    ensure_dir(output)
    results = model.predict(source=source, conf=conf, save=True, project=output, name="image_detection")
    print(f"Detection completed. Results saved to {output}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect animals in image or folder")
    parser.add_argument("--weights", default="models/best.pt")
    parser.add_argument("--source", required=True)
    parser.add_argument("--conf", type=float, default=0.5)
    parser.add_argument("--out", default="outputs")
    args = parser.parse_args()
    detect(args.weights, args.source, args.conf, args.out)
