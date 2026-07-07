import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from utils.common import load_yaml, ensure_dir


def convert_box(size, box):
    width, height = size
    xmin, ymin, xmax, ymax = box
    x = ((xmin + xmax) / 2.0) / width
    y = ((ymin + ymax) / 2.0) / height
    w = (xmax - xmin) / width
    h = (ymax - ymin) / height
    return x, y, w, h


def voc_to_yolo(xml_dir: str, output_dir: str, classes_yaml: str = "configs/classes.yaml"):
    class_data = load_yaml(classes_yaml)
    name_to_id = {v: int(k) for k, v in class_data["classes"].items()}
    xml_dir = Path(xml_dir)
    output_dir = ensure_dir(output_dir)
    for xml_file in xml_dir.glob("*.xml"):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        width = int(root.find("size/width").text)
        height = int(root.find("size/height").text)
        lines = []
        for obj in root.findall("object"):
            name = obj.find("name").text
            if name not in name_to_id:
                continue
            bbox = obj.find("bndbox")
            xmin = float(bbox.find("xmin").text)
            ymin = float(bbox.find("ymin").text)
            xmax = float(bbox.find("xmax").text)
            ymax = float(bbox.find("ymax").text)
            x, y, w, h = convert_box((width, height), (xmin, ymin, xmax, ymax))
            lines.append(f"{name_to_id[name]} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")
        (output_dir / f"{xml_file.stem}.txt").write_text("\n".join(lines))
    print(f"Converted VOC XML labels to YOLO format in {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Pascal VOC XML annotations to YOLO labels")
    parser.add_argument("--xml", required=True, help="Directory containing CVAT/Pascal VOC XML files")
    parser.add_argument("--out", required=True, help="Output directory for YOLO txt labels")
    parser.add_argument("--classes", default="configs/classes.yaml")
    args = parser.parse_args()
    voc_to_yolo(args.xml, args.out, args.classes)
