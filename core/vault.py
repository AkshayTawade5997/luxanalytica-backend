import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class VaultStorage:
    def __init__(self, storage_path: str = "./data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)

        self.tasks_path = self.storage_path / "tasks"
        self.cache_path = self.storage_path / "cache"
        self.uploads_path = self.storage_path / "uploads"

        for path in [self.tasks_path, self.cache_path, self.uploads_path]:
            path.mkdir(exist_ok=True)

        logger.info(f"🗄️ Vault initialized at {storage_path}")

    async def store_task(self, task_id: str, data: Dict[str, Any]):
        file_path = self.tasks_path / f"{task_id}.json"
        with open(file_path, 'w') as f:
            json.dump(data, f)

    async def retrieve_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        file_path = self.tasks_path / f"{task_id}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return None

    async def cleanup_old_data(self, max_age_days: int = 7):
        cutoff = datetime.utcnow() - timedelta(days=max_age_days)
        cleaned = 0

        for file_path in self.tasks_path.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                task_time = datetime.fromisoformat(data.get("completed_at", data.get("submitted_at", datetime.utcnow().isoformat())))

                if task_time < cutoff:
                    file_path.unlink()
                    cleaned += 1
            except Exception as e:
                logger.error(f"Error cleaning {file_path}: {e}")

        logger.info(f"🧹 Cleaned up {cleaned} old task files")
