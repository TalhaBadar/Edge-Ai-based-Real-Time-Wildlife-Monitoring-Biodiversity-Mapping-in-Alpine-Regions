from pathlib import Path
from typing import Dict, Any, Optional
import firebase_admin
from firebase_admin import credentials, firestore, storage


class FirebaseClient:
    def __init__(self, service_account_json: str, storage_bucket: str, collection: str):
        self.service_account_json = Path(service_account_json)
        self.storage_bucket = storage_bucket
        self.collection = collection
        self.enabled = False
        self.db = None
        self.bucket = None
        self._init()

    def _init(self):
        if not self.service_account_json.exists():
            raise FileNotFoundError(
                f"Firebase service account not found: {self.service_account_json}. "
                "Place your real serviceAccount.json there or disable Firebase in config."
            )
        if not firebase_admin._apps:
            cred = credentials.Certificate(str(self.service_account_json))
            firebase_admin.initialize_app(cred, {"storageBucket": self.storage_bucket})
        self.db = firestore.client()
        self.bucket = storage.bucket()
        self.enabled = True

    def upload_image(self, image_path: str, remote_folder: str = "detections") -> str:
        path = Path(image_path)
        blob_path = f"{remote_folder}/{path.name}"
        blob = self.bucket.blob(blob_path)
        blob.upload_from_filename(str(path))
        blob.make_public()
        return blob.public_url

    def upload_record(self, record: Dict[str, Any]) -> str:
        doc_ref = self.db.collection(self.collection).document(record["detection_id"])
        doc_ref.set(record)
        return doc_ref.id

    def upload_detection(self, record: Dict[str, Any]) -> Optional[str]:
        image_url = None
        if record.get("image_path"):
            image_url = self.upload_image(record["image_path"])
            record["image_url"] = image_url
        record["sync_status"] = "synced"
        self.upload_record(record)
        return image_url
