# Firestore Schema

Collection: `detections`

Each document represents one detected animal instance.

```json
{
  "detection_id": "uuid",
  "species": "Tiger",
  "class_id": 13,
  "confidence": 0.93,
  "bbox_xyxy": [120.5, 80.1, 400.0, 360.0],
  "timestamp": "2026-07-07T10:15:30Z",
  "latitude": 34.1688,
  "longitude": 73.2215,
  "image_path": "edge_cache/images/...jpg",
  "image_url": "https://...",
  "device_id": "JETSON_NANO_01",
  "device_type": "NVIDIA Jetson Nano",
  "source": "AGX Camera",
  "sync_status": "synced"
}
```

Suggested indexes:

- `species ASC, timestamp DESC`
- `device_id ASC, timestamp DESC`
- `timestamp DESC`
