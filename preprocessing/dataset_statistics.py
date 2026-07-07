import argparse
from pathlib import Path
from collections import Counter
import pandas as pd
from utils.common import load_yaml, ensure_dir


def statistics(dataset_yaml: str, output_csv: str = "outputs/dataset_statistics.csv"):
    data = load_yaml(dataset_yaml)
    base = Path(data.get("path", "."))
    if not base.is_absolute():
        base = Path(dataset_yaml).parent.parent / base
    names = {int(k): v for k, v in data["names"].items()}
    rows = []

    for split_key in ["train", "val", "test"]:
        rel = data.get(split_key)
        if not rel:
            continue
        image_dir = (base / rel).resolve()
        label_dir = Path(str(image_dir).replace("images", "labels"))
        object_counter = Counter()
        image_count = len([p for p in image_dir.glob("*.*") if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}]) if image_dir.exists() else 0
        if label_dir.exists():
            for label in label_dir.glob("*.txt"):
                for line in label.read_text().splitlines():
                    if line.strip():
                        object_counter[int(line.split()[0])] += 1
        for cls_id, class_name in names.items():
            rows.append({"split": split_key, "class_id": cls_id, "class_name": class_name, "object_count": object_counter[cls_id], "image_count_total_split": image_count})

    df = pd.DataFrame(rows)
    ensure_dir(Path(output_csv).parent)
    df.to_csv(output_csv, index=False)
    print(df)
    print(f"Saved statistics to {output_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate dataset statistics")
    parser.add_argument("--data", default="data/dataset.yaml")
    parser.add_argument("--out", default="outputs/dataset_statistics.csv")
    args = parser.parse_args()
    statistics(args.data, args.out)
