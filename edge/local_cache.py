import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional


class LocalCache:
    """SQLite offline cache for detection records."""

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS detections (
                    detection_id TEXT PRIMARY KEY,
                    payload TEXT NOT NULL,
                    synced INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def save(self, record: Dict[str, Any]) -> None:
        payload = json.dumps(record)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO detections (detection_id, payload, synced) VALUES (?, ?, ?)",
                (record["detection_id"], payload, 0 if record.get("sync_status") != "synced" else 1),
            )
            conn.commit()

    def get_unsynced(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        query = "SELECT payload FROM detections WHERE synced = 0 ORDER BY created_at ASC"
        if limit:
            query += f" LIMIT {int(limit)}"
        with self._connect() as conn:
            rows = conn.execute(query).fetchall()
        return [json.loads(r[0]) for r in rows]

    def mark_synced(self, detection_id: str, image_url: str | None = None) -> None:
        with self._connect() as conn:
            row = conn.execute("SELECT payload FROM detections WHERE detection_id = ?", (detection_id,)).fetchone()
            if row:
                payload = json.loads(row[0])
                payload["sync_status"] = "synced"
                if image_url:
                    payload["image_url"] = image_url
                conn.execute(
                    "UPDATE detections SET payload = ?, synced = 1 WHERE detection_id = ?",
                    (json.dumps(payload), detection_id),
                )
            conn.commit()

    def count_unsynced(self) -> int:
        with self._connect() as conn:
            return int(conn.execute("SELECT COUNT(*) FROM detections WHERE synced = 0").fetchone()[0])
