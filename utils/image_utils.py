from pathlib import Path
from typing import Iterable, Dict, Any
import cv2


def save_image(image, output_path: str | Path) -> str:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), image):
        raise RuntimeError(f"Failed to save image: {output_path}")
    return str(output_path)


def draw_detections(frame, detections: Iterable[Dict[str, Any]]):
    """Draw bounding boxes on a copy of frame."""
    output = frame.copy()
    for det in detections:
        bbox = det.get("bbox_xyxy")
        if not bbox:
            continue
        x1, y1, x2, y2 = map(int, bbox)
        label = f"{det.get('species', 'unknown')} {det.get('confidence', 0):.2f}"
        cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(output, label, (x1, max(20, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return output
