from pathlib import Path
from typing import Dict
from utils.common import load_yaml


def load_class_names(classes_yaml: str | Path = "configs/classes.yaml") -> Dict[int, str]:
    data = load_yaml(classes_yaml)
    return {int(k): v for k, v in data["classes"].items()}


def load_dangerous_classes(classes_yaml: str | Path = "configs/classes.yaml") -> set[str]:
    data = load_yaml(classes_yaml)
    return set(data.get("dangerous_classes", []))
