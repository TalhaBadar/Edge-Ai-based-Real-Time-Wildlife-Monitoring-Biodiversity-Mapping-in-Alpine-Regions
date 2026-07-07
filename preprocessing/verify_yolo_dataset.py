import argparse
from pathlib import Path
from collections import defaultdict
from utils.common import load_yaml

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def verify(dataset_yaml: str):
    data = load_yaml(dataset_yaml)
    base = Path(data.get("path", "."))
    if not base.is_absolute():
        base = Path(dataset_yaml).parent.parent / base
    names = data["names"]
    nc = len(names)
    errors = []
    stats = defaultdict(lambda: {"images": 0, "labels": 0, "objects": 0})

    for split_key in ["train", "val", "test"]:
        rel = data.get(split_key)
        if not rel:
            continue
        image_dir = (base / rel).resolve()
        label_dir = Path(str(image_dir).replace("images", "labels"))
        if not image_dir.exists():
            errors.append(f"Missing image directory: {image_dir}")
            continue
        if not label_dir.exists():
            errors.append(f"Missing label directory: {label_dir}")
            continue

        for img in image_dir.iterdir():
            if img.suffix.lower() not in IMAGE_EXTS:
                continue
            stats[split_key]["images"] += 1
            label = label_dir / f"{img.stem}.txt"
            if not label.exists():
                errors.append(f"Missing label for image: {img}")
                continue
            stats[split_key]["labels"] += 1
            for line_no, line in enumerate(label.read_text().splitlines(), start=1):
                if not line.strip():
                    continue
                parts = line.split()
                if len(parts) != 5:
                    errors.append(f"Invalid label format: {label}:{line_no}")
                    continue
                try:
                    cls = int(parts[0])
                    vals = [float(v) for v in parts[1:]]
                except ValueError:
                    errors.append(f"Non-numeric label value: {label}:{line_no}")
                    continue
                if cls < 0 or cls >= nc:
                    errors.append(f"Class id out of range: {label}:{line_no} -> {cls}")
                if any(v < 0 or v > 1 for v in vals):
                    errors.append(f"Bounding box values not normalized: {label}:{line_no}")
                stats[split_key]["objects"] += 1

    print("Dataset verification summary")
    for split, s in stats.items():
        print(f"{split}: {s['images']} images, {s['labels']} labels, {s['objects']} objects")
    print(f"Errors found: {len(errors)}")
    for e in errors[:100]:
        print("-", e)
    if len(errors) > 100:
        print(f"...and {len(errors)-100} more errors")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify YOLO dataset labels and structure")
    parser.add_argument("--data", default="data/dataset.yaml")
    args = parser.parse_args()
    verify(args.data)
