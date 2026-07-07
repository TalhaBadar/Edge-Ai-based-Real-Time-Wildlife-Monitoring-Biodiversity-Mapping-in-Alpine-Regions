import argparse
import time
from utils.common import load_yaml
from utils.logger import get_logger
from edge.upload_cached import sync_once

logger = get_logger("sync_daemon")


def run(config_path: str):
    cfg = load_yaml(config_path)
    interval = int(cfg["edge"].get("sync_interval_seconds", 30))
    logger.info("Sync daemon started with interval=%s seconds", interval)
    while True:
        sync_once(config_path)
        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Continuous Firebase sync daemon")
    parser.add_argument("--config", default="configs/config.yaml")
    args = parser.parse_args()
    run(args.config)
