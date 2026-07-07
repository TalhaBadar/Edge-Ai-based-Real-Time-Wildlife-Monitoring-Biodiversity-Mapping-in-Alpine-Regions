from typing import List, Dict, Any
from ultralytics import YOLO


class YOLODetector:
    def __init__(self, model_path: str, confidence: float = 0.5, iou: float = 0.45, image_size: int = 640):
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.iou = iou
        self.image_size = image_size

    def detect(self, frame) -> List[Dict[str, Any]]:
        results = self.model.predict(
            frame,
            conf=self.confidence,
            iou=self.iou,
            imgsz=self.image_size,
            verbose=False,
        )
        detections: List[Dict[str, Any]] = []
        if not results:
            return detections
        result = results[0]
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()
            detections.append({
                "class_id": cls_id,
                "species": result.names.get(cls_id, str(cls_id)),
                "confidence": conf,
                "bbox_xyxy": [float(x) for x in xyxy],
            })
        return detections

    def annotate(self, frame):
        results = self.model.predict(frame, conf=self.confidence, iou=self.iou, imgsz=self.image_size, verbose=False)
        return results[0].plot() if results else frame
