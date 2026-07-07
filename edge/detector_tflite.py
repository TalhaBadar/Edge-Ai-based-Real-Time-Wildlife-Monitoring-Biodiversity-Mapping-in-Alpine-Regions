from typing import List, Dict, Any
from ultralytics import YOLO


class TFLiteYOLODetector:
    """TFLite detector through Ultralytics wrapper.

    This class is useful for testing the exported .tflite model from Python.
    For Flutter deployment, the same .tflite model is placed inside the app assets.
    """

    def __init__(self, model_path: str, confidence: float = 0.5, image_size: int = 640):
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.image_size = image_size

    def detect(self, frame) -> List[Dict[str, Any]]:
        results = self.model.predict(frame, conf=self.confidence, imgsz=self.image_size, verbose=False)
        detections: List[Dict[str, Any]] = []
        if not results:
            return detections
        result = results[0]
        for box in result.boxes:
            cls_id = int(box.cls[0])
            detections.append({
                "class_id": cls_id,
                "species": result.names.get(cls_id, str(cls_id)),
                "confidence": float(box.conf[0]),
                "bbox_xyxy": [float(x) for x in box.xyxy[0].tolist()],
            })
        return detections
