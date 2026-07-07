import argparse
from utils.common import load_yaml
from utils.logger import get_logger
from edge.local_cache import LocalCache
from edge.internet import InternetMonitor
from edge.firebase_client import FirebaseClient

logger = get_logger("sync")


def sync_once(config_path: str, limit: int | None = None):
    cfg = load_yaml(config_path)
    firebase_cfg = cfg["firebase"]
    if not firebase_cfg.get("enabled", False):
        logger.warning("Firebase is disabled in config.")
        return
    if not InternetMonitor.is_connected():
        logger.info("Internet unavailable. Sync skipped.")
        return

    cache = LocalCache(cfg["edge"]["local_cache_db"])
    firebase = FirebaseClient(
        service_account_json=firebase_cfg["service_account_json"],
        storage_bucket=firebase_cfg["storage_bucket"],
        collection=firebase_cfg["firestore_collection"],
    )
    records = cache.get_unsynced(limit=limit)
    logger.info("Unsynced records: %d", len(records))
    for record in records:
        try:
            image_url = firebase.upload_detection(record)
            cache.mark_synced(record["detection_id"], image_url=image_url)
            logger.info("Synced: %s", record["detection_id"])
        except Exception as e:
            logger.warning("Failed to sync %s: %s", record.get("detection_id"), e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload cached offline detections to Firebase")
    parser.add_argument("--config", default="configs/config.yaml")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    sync_once(args.config, args.limit)
