from pathlib import Path
from typing import Dict, Any
from uuid import uuid4
import cv2
from utils.common import now_iso, now_for_filename, ensure_dir


class DetectionRecordBuilder:
    def __init__(self, image_dir: str, device_id: str, device_type: str, source_name: str, gps_provider):
        self.image_dir = ensure_dir(image_dir)
        self.device_id = device_id
        self.device_type = device_type
        self.source_name = source_name
        self.gps_provider = gps_provider

    def save_frame(self, frame, species: str) -> str:
        safe_species = species.replace(" ", "_").replace("/", "_")
        filename = f"{now_for_filename()}_{safe_species}.jpg"
        path = Path(self.image_dir) / filename
        if not cv2.imwrite(str(path), frame):
            raise RuntimeError(f"Failed to save detection image: {path}")
        return str(path)

    def build(self, frame, detection: Dict[str, Any]) -> Dict[str, Any]:
        species = detection["species"]
        image_path = self.save_frame(frame, species)
        location = self.gps_provider.get_location()
        return {
            "detection_id": str(uuid4()),
            "species": species,
            "class_id": int(detection["class_id"]),
            "confidence": round(float(detection["confidence"]), 4),
            "bbox_xyxy": detection.get("bbox_xyxy", []),
            "timestamp": now_iso(),
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "image_path": image_path,
            "image_url": None,
            "device_id": self.device_id,
            "device_type": self.device_type,
            "source": self.source_name,
            "sync_status": "pending",
        }
