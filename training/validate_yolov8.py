import argparse
from ultralytics import YOLO
from utils.common import load_yaml
from utils.logger import get_logger

logger = get_logger("validate")


def validate(config_path: str):
    cfg = load_yaml(config_path)
    model_path = cfg["paths"]["best_model"]
    dataset_yaml = cfg["paths"]["dataset_yaml"]
    image_size = cfg["training"]["image_size"]

    model = YOLO(model_path)
    logger.info("Validating model: %s", model_path)
    metrics = model.val(data=dataset_yaml, imgsz=image_size)

    logger.info("mAP@0.5: %.4f", metrics.box.map50)
    logger.info("mAP@0.5:0.95: %.4f", metrics.box.map)
    logger.info("Precision: %.4f", metrics.box.mp)
    logger.info("Recall: %.4f", metrics.box.mr)
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate trained YOLOv8 model")
    parser.add_argument("--config", default="configs/config.yaml")
    args = parser.parse_args()
    validate(args.config)
