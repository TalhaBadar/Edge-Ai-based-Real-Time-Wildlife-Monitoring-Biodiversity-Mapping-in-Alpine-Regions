import argparse
import cv2
from ultralytics import YOLO


def detect_webcam(weights: str, camera: int, conf: float):
    model = YOLO(weights)
    cap = cv2.VideoCapture(camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera {camera}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model.predict(frame, conf=conf, verbose=False)
        annotated = results[0].plot()
        cv2.imshow("Wildlife Detection", annotated)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live webcam wildlife detection")
    parser.add_argument("--weights", default="models/best.pt")
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--conf", type=float, default=0.5)
    args = parser.parse_args()
    detect_webcam(args.weights, args.camera, args.conf)
