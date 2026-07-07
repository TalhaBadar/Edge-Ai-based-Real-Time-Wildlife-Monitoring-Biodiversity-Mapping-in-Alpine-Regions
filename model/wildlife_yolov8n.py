from pathlib import Path
from typing import Any
import numpy as np
from ultralytics import YOLO


class WildlifeYOLOv8n:
    '''
    Reusable YOLOv8n wrapper for wildlife detection.

    This class represents the model code used in the project.
    It loads a trained YOLOv8n model and returns structured detections.
    '''

    def __init__(
        self,
        weights: str | Path = "models/best.pt",
        image_size: int = 640,
        confidence: float = 0.55,
        iou: float = 0.45,
    ) -> None:
        self.weights = str(weights)
        self.image_size = image_size
        self.confidence = confidence
        self.iou = iou
        self.model = YOLO(self.weights)

    def predict_raw(self, source: Any, save: bool = False):
        return self.model.predict(
            source=source,
            imgsz=self.image_size,
            conf=self.confidence,
            iou=self.iou,
            save=save,
            verbose=False,
        )

    def detect_frame(self, frame: np.ndarray) -> list[dict]:
        results = self.predict_raw(frame, save=False)
        detections: list[dict] = []

        for result in results:
            names = result.names
            if result.boxes is None:
                continue

            for box in result.boxes:
                class_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item())
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                detections.append(
                    {
                        "class_id": class_id,
                        "species": names[class_id],
                        "confidence": confidence,
                        "bbox": [float(x1), float(y1), float(x2), float(y2)],
                    }
                )

        return detections

    def detect_source(self, source: str | int, save: bool = False):
        return self.predict_raw(source=source, save=save)
