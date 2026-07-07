import argparse
import json
from pathlib import Path
from ultralytics import YOLO
from utils.config_loader import load_yaml


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate YOLOv8n and save metrics.")
    parser.add_argument("--config", default="configs/model_config.yaml")
    parser.add_argument("--weights", default=None)
    parser.add_argument("--data", default=None)
    parser.add_argument("--out", default="results/evaluation_metrics.json")
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    weights = args.weights or cfg["model"]["trained_model"]
    data_yaml = args.data or cfg["paths"]["dataset_yaml"]

    model = YOLO(weights)
    metrics = model.val(data=data_yaml, plots=True)

    result = {
        "precision": float(metrics.box.mp),
        "recall": float(metrics.box.mr),
        "mAP_0.5": float(metrics.box.map50),
        "mAP_0.5_0.95": float(metrics.box.map),
        "mAP_0.75": float(metrics.box.map75),
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=4), encoding="utf-8")

    print(json.dumps(result, indent=4))
    print(f"Saved metrics to: {out}")


if __name__ == "__main__":
    main()
