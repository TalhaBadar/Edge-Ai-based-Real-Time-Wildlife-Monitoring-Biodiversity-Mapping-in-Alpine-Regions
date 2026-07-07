import argparse
import time
import cv2
from utils.common import load_yaml
from utils.logger import get_logger
from edge.camera_agx import CameraStream
from edge.detector_yolo import YOLODetector
from edge.gps_provider import GPSProvider
from edge.record_builder import DetectionRecordBuilder
from edge.local_cache import LocalCache
from edge.internet import InternetMonitor
from edge.alert_manager import AlertManager
from edge.firebase_client import FirebaseClient

logger = get_logger("edge")


def run(config_path: str):
    cfg = load_yaml(config_path)
    edge_cfg = cfg["edge"]
    infer_cfg = cfg["inference"]
    loc_cfg = cfg["location"]
    firebase_cfg = cfg["firebase"]

    camera = CameraStream(
        source=edge_cfg["camera_source"],
        width=edge_cfg["frame_width"],
        height=edge_cfg["frame_height"],
    ).start()

    detector = YOLODetector(
        model_path=cfg["paths"]["best_model"],
        confidence=infer_cfg["confidence"],
        iou=infer_cfg["iou"],
        image_size=infer_cfg["image_size"],
    )

    gps = GPSProvider(
        mode=loc_cfg["mode"],
        fixed_latitude=loc_cfg["fixed_latitude"],
        fixed_longitude=loc_cfg["fixed_longitude"],
        serial_port=loc_cfg["serial_port"],
        baud_rate=loc_cfg["baud_rate"],
    )

    builder = DetectionRecordBuilder(
        image_dir=edge_cfg["local_image_dir"],
        device_id=edge_cfg["device_id"],
        device_type=edge_cfg["device_type"],
        source_name=edge_cfg["source_name"],
        gps_provider=gps,
    )

    cache = LocalCache(edge_cfg["local_cache_db"])
    alerts = AlertManager(
        enable_console=cfg["alerts"]["enable_console"],
        enable_gpio=cfg["alerts"]["enable_gpio"],
        gpio_pin=cfg["alerts"]["gpio_pin"],
    )

    firebase = None
    if firebase_cfg.get("enabled", False):
        try:
            firebase = FirebaseClient(
                service_account_json=firebase_cfg["service_account_json"],
                storage_bucket=firebase_cfg["storage_bucket"],
                collection=firebase_cfg["firestore_collection"],
            )
            logger.info("Firebase initialized")
        except Exception as e:
            logger.warning("Firebase disabled because initialization failed: %s", e)

    cooldown = float(edge_cfg.get("detection_cooldown_seconds", 5))
    last_seen = {}

    logger.info("Edge wildlife detection started")
    try:
        while True:
            frame = camera.read()
            if frame is None:
                time.sleep(0.05)
                continue

            detections = detector.detect(frame)
            now = time.time()
            for det in detections:
                species = det["species"]
                if now - last_seen.get(species, 0) < cooldown:
                    continue
                last_seen[species] = now

                record = builder.build(frame, det)
                cache.save(record)
                logger.info("Detection saved locally: %s %.2f", species, det["confidence"])

                if alerts.is_dangerous(species):
                    alerts.trigger(species, det["confidence"])

                if firebase and InternetMonitor.is_connected():
                    try:
                        image_url = firebase.upload_detection(record)
                        cache.mark_synced(record["detection_id"], image_url=image_url)
                        logger.info("Detection uploaded to Firebase: %s", record["detection_id"])
                    except Exception as e:
                        logger.warning("Upload failed; record kept in local cache: %s", e)

            if edge_cfg.get("display_window", False):
                annotated = detector.annotate(frame)
                cv2.imshow("Edge Wildlife Detection", annotated)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        alerts.cleanup()
        camera.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run edge wildlife detection on Jetson Nano")
    parser.add_argument("--config", default="configs/config.yaml")
    args = parser.parse_args()
    run(args.config)
