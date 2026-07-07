import argparse
from pathlib import Path
import cv2
from utils.common import load_yaml

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def find_corrupted(dataset_yaml: str):
    data = load_yaml(dataset_yaml)
    base = Path(data.get("path", "."))
    if not base.is_absolute():
        base = Path(dataset_yaml).parent.parent / base
    corrupted = []
    for split_key in ["train", "val", "test"]:
        rel = data.get(split_key)
        if not rel:
            continue
        image_dir = (base / rel).resolve()
        if not image_dir.exists():
            continue
        for img_path in image_dir.iterdir():
            if img_path.suffix.lower() not in IMAGE_EXTS:
                continue
            img = cv2.imread(str(img_path))
            if img is None:
                corrupted.append(str(img_path))
    print(f"Corrupted images found: {len(corrupted)}")
    for path in corrupted:
        print(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find corrupted images in YOLO dataset")
    parser.add_argument("--data", default="data/dataset.yaml")
    args = parser.parse_args()
    find_corrupted(args.data)
