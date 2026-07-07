import argparse
from ultralytics import YOLO
from utils.common import ensure_dir


def detect_video(weights: str, source: str, conf: float, output: str):
    model = YOLO(weights)
    ensure_dir(output)
    model.predict(source=source, conf=conf, save=True, project=output, name="video_detection")
    print(f"Video detection completed. Results saved to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect animals in video")
    parser.add_argument("--weights", default="models/best.pt")
    parser.add_argument("--source", required=True)
    parser.add_argument("--conf", type=float, default=0.5)
    parser.add_argument("--out", default="outputs")
    args = parser.parse_args()
    detect_video(args.weights, args.source, args.conf, args.out)
