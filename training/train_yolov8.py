import argparse
from ultralytics import YOLO
from utils.common import load_yaml
from utils.logger import get_logger

logger = get_logger("train")


def train(config_path: str):
    cfg = load_yaml(config_path)
    train_cfg = cfg["training"]
    dataset_yaml = cfg["paths"]["dataset_yaml"]

    logger.info("Loading base model: %s", train_cfg["base_model"])
    model = YOLO(train_cfg["base_model"])

    logger.info("Starting YOLOv8 training")
    model.train(
        data=dataset_yaml,
        epochs=train_cfg["epochs"],
        imgsz=train_cfg["image_size"],
        batch=train_cfg["batch"],
        device=train_cfg["device"],
        patience=train_cfg["patience"],
        workers=train_cfg["workers"],
        cache=train_cfg["cache"],
        project=train_cfg["project"],
        name=train_cfg["run_name"],
    )
    logger.info("Training completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train YOLOv8n wildlife detector")
    parser.add_argument("--config", default="configs/config.yaml")
    args = parser.parse_args()
    train(args.config)
