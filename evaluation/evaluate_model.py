import argparse
from ultralytics import YOLO
from utils.common import save_json


def evaluate(weights: str, data: str, imgsz: int, output_json: str):
    model = YOLO(weights)
    metrics = model.val(data=data, imgsz=imgsz)
    result = {
        "precision_mean": float(metrics.box.mp),
        "recall_mean": float(metrics.box.mr),
        "map_50": float(metrics.box.map50),
        "map_50_95": float(metrics.box.map),
        "map_75": float(metrics.box.map75),
    }
    save_json(result, output_json)
    print(result)
    print(f"Saved evaluation report to {output_json}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate YOLO model and export metrics")
    parser.add_argument("--weights", default="models/best.pt")
    parser.add_argument("--data", default="data/dataset.yaml")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--out", default="results/evaluation_metrics.json")
    args = parser.parse_args()
    evaluate(args.weights, args.data, args.imgsz, args.out)
