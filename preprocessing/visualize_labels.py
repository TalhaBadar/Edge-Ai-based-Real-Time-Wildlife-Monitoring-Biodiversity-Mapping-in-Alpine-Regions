import argparse
import random
from pathlib import Path
import cv2
from utils.common import load_yaml, ensure_dir

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def yolo_to_xyxy(line: str, width: int, height: int):
    cls, x, y, w, h = line.split()
    x, y, w, h = float(x), float(y), float(w), float(h)
    x1 = int((x - w / 2) * width)
    y1 = int((y - h / 2) * height)
    x2 = int((x + w / 2) * width)
    y2 = int((y + h / 2) * height)
    return int(cls), x1, y1, x2, y2


def visualize(dataset_yaml: str, split: str, output_dir: str, count: int):
    data = load_yaml(dataset_yaml)
    base = Path(data.get("path", "."))
    if not base.is_absolute():
        base = Path(dataset_yaml).parent.parent / base
    image_dir = (base / data[split]).resolve()
    label_dir = Path(str(image_dir).replace("images", "labels"))
    names = {int(k): v for k, v in data["names"].items()}
    output_dir = ensure_dir(output_dir)
    images = [p for p in image_dir.iterdir() if p.suffix.lower() in IMAGE_EXTS]
    samples = random.sample(images, min(count, len(images)))
    for img_path in samples:
        img = cv2.imread(str(img_path))
        if img is None:
            continue
        h, w = img.shape[:2]
        label_path = label_dir / f"{img_path.stem}.txt"
        if label_path.exists():
            for line in label_path.read_text().splitlines():
                if not line.strip():
                    continue
                cls, x1, y1, x2, y2 = yolo_to_xyxy(line, w, h)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, names.get(cls, str(cls)), (x1, max(20, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        out = output_dir / img_path.name
        cv2.imwrite(str(out), img)
    print(f"Saved visualized samples to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize YOLO labels on random images")
    parser.add_argument("--data", default="data/dataset.yaml")
    parser.add_argument("--split", default="train", choices=["train", "val", "test"])
    parser.add_argument("--out", default="outputs/label_visualization")
    parser.add_argument("--count", type=int, default=20)
    args = parser.parse_args()
    visualize(args.data, args.split, args.out, args.count)
