from pathlib import Path
from ultralytics import YOLO


class WildlifeTFLiteDetector:
    '''
    TFLite detector wrapper.

    Ultralytics allows exported YOLOv8 TFLite models to be loaded for prediction.
    This wrapper is useful for testing the same TFLite model that will be used in mobile deployment.
    '''

    def __init__(
        self,
        model_path: str | Path = "models/best.tflite",
        image_size: int = 640,
        confidence: float = 0.55,
    ) -> None:
        self.model_path = str(model_path)
        self.image_size = image_size
        self.confidence = confidence
        self.model = YOLO(self.model_path)

    def predict(self, source: str | int, save: bool = False):
        return self.model.predict(
            source=source,
            imgsz=self.image_size,
            conf=self.confidence,
            save=save,
        )
