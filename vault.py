"""
Vault: Secure Data Storage and Management
Handles data persistence, caching, and cleanup
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class VaultStorage:
    """Secure storage system for LuxAnalytica"""

    def __init__(self, storage_path: str = "./data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)

        # Subdirectories
        self.tasks_path = self.storage_path / "tasks"
        self.cache_path = self.storage_path / "cache"
        self.uploads_path = self.storage_path / "uploads"

        for path in [self.tasks_path, self.cache_path, self.uploads_path]:
            path.mkdir(exist_ok=True)

        logger.info(f"🗄️ Vault initialized at {storage_path}")

    async def store_task(self, task_id: str, data: Dict[str, Any]):
        """Store task data"""
        file_path = self.tasks_path / f"{task_id}.json"
        with open(file_path, 'w') as f:
            json.dump(data, f)

    async def retrieve_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve task data"""
        file_path = self.tasks_path / f"{task_id}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return None

    async def cache_data(self, key: str, data: Dict[str, Any], ttl: int = 3600):
        """Cache data with TTL (seconds)"""
        cache_entry = {
            "data": data,
            "stored_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(seconds=ttl)).isoformat()
        }

        file_path = self.cache_path / f"{key}.json"
        with open(file_path, 'w') as f:
            json.dump(cache_entry, f)

    async def get_cached(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached data if not expired"""
        file_path = self.cache_path / f"{key}.json"

        if not file_path.exists():
            return None

        with open(file_path, 'r') as f:
            cache_entry = json.load(f)

        expires_at = datetime.fromisoformat(cache_entry["expires_at"])
        if datetime.utcnow() > expires_at:
            file_path.unlink()  # Delete expired cache
            return None

        return cache_entry["data"]

    async def cleanup_old_data(self, max_age_days: int = 7):
        """Clean up old task data"""
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

    async def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        def get_dir_size(path: Path) -> int:
            return sum(f.stat().st_size for f in path.glob('**/*') if f.is_file())

        return {
            "tasks_count": len(list(self.tasks_path.glob("*.json"))),
            "cache_count": len(list(self.cache_path.glob("*.json"))),
            "tasks_size_mb": get_dir_size(self.tasks_path) / (1024 * 1024),
            "cache_size_mb": get_dir_size(self.cache_path) / (1024 * 1024),
            "timestamp": datetime.utcnow().isoformat()
        }
