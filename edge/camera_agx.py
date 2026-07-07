import time
from threading import Thread, Lock
from typing import Any
import cv2


def _parse_camera_source(source: Any):
    if isinstance(source, int):
        return source
    if isinstance(source, str):
        if source.isdigit():
            return int(source)
        if source.lower() == "csi":
            return (
                "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, "
                "format=NV12, framerate=30/1 ! nvvidconv flip-method=0 ! "
                "video/x-raw, width=1280, height=720, format=BGRx ! videoconvert ! "
                "video/x-raw, format=BGR ! appsink"
            )
    return source


class CameraStream:
    """Threaded OpenCV camera stream for USB, AGX/CSI, RTSP, or HTTP camera sources."""

    def __init__(self, source=0, width=1280, height=720):
        self.source = _parse_camera_source(source)
        if isinstance(self.source, str) and "nvarguscamerasrc" in self.source:
            self.cap = cv2.VideoCapture(self.source, cv2.CAP_GSTREAMER)
        else:
            self.cap = cv2.VideoCapture(self.source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera source: {source}")
        self.lock = Lock()
        self.frame = None
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = Thread(target=self._update, daemon=True)
        self.thread.start()
        time.sleep(0.5)
        return self

    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.05)
                continue
            with self.lock:
                self.frame = frame

    def read(self):
        with self.lock:
            if self.frame is None:
                return None
            return self.frame.copy()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        self.cap.release()
