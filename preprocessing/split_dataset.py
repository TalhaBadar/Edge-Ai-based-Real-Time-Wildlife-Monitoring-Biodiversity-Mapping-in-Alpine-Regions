import argparse
import random
import shutil
from pathlib import Path
from utils.common import ensure_dir

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def split_dataset(images_dir: str, labels_dir: str, output_dir: str, train_ratio: float = 0.8, val_ratio: float = 0.1, seed: int = 42):
    images_dir = Path(images_dir)
    labels_dir = Path(labels_dir)
    output_dir = Path(output_dir)
    images = [p for p in images_dir.iterdir() if p.suffix.lower() in IMAGE_EXTS]
    random.seed(seed)
    random.shuffle(images)
    n = len(images)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    splits = {
        "train": images[:n_train],
        "valid": images[n_train:n_train + n_val],
        "test": images[n_train + n_val:],
    }
    for split, split_images in splits.items():
        img_out = ensure_dir(output_dir / split / "images")
        lbl_out = ensure_dir(output_dir / split / "labels")
        for img in split_images:
            shutil.copy2(img, img_out / img.name)
            label = labels_dir / f"{img.stem}.txt"
            if label.exists():
                shutil.copy2(label, lbl_out / label.name)
    print(f"Dataset split completed at {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split unsplit YOLO dataset into train/valid/test")
    parser.add_argument("--images", required=True)
    parser.add_argument("--labels", required=True)
    parser.add_argument("--out", default="data")
    parser.add_argument("--train", type=float, default=0.8)
    parser.add_argument("--val", type=float, default=0.1)
    args = parser.parse_args()
    split_dataset(args.images, args.labels, args.out, args.train, args.val)
