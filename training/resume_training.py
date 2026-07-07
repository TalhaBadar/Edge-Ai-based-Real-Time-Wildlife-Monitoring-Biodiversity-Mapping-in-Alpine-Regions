import argparse
from ultralytics import YOLO


def resume(last_weights: str):
    model = YOLO(last_weights)
    model.train(resume=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resume interrupted YOLOv8 training")
    parser.add_argument("--last", default="runs/WildlifeDetector/weights/last.pt")
    args = parser.parse_args()
    resume(args.last)
