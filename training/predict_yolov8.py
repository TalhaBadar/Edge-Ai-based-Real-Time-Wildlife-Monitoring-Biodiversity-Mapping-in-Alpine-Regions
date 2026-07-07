import argparse
from ultralytics import YOLO
from utils.common import load_yaml


def predict(config_path: str, source: str):
    cfg = load_yaml(config_path)
    model = YOLO(cfg["paths"]["best_model"])
    infer_cfg = cfg["inference"]
    model.predict(
        source=source,
        imgsz=infer_cfg["image_size"],
        conf=infer_cfg["confidence"],
        iou=infer_cfg["iou"],
        save=True,
        project=cfg["paths"]["outputs_dir"],
        name="predictions",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run YOLOv8 prediction on image/video/folder")
    parser.add_argument("--config", default="configs/config.yaml")
    parser.add_argument("--source", required=True)
    args = parser.parse_args()
    predict(args.config, args.source)
