import asyncio
import logging
from datetime import datetime
from typing import Dict, Any
import time

logger = logging.getLogger(__name__)

class PulseHealthCheck:
    def __init__(self):
        self.start_time = time.time()
        self.check_count = 0
        self.last_check = None
        self.healthy = True

    async def health_check_loop(self):
        logger.info("💓 Pulse health monitoring started")

        while True:
            try:
                self.check_count += 1
                self.last_check = datetime.utcnow().isoformat()

                self.healthy = await self._self_check()

                if not self.healthy:
                    logger.error("💔 Health check failed - system unhealthy")

                if self.check_count % 10 == 0:
                    uptime = self.get_uptime()
                    logger.info(f"💓 Health check #{self.check_count} - Uptime: {uptime}")

                await asyncio.sleep(30)

            except Exception as e:
                logger.error(f"Health check error: {e}")
                self.healthy = False
                await asyncio.sleep(30)

    async def _self_check(self) -> bool:
        try:
            import psutil

            if psutil.cpu_percent() > 95:
                return False

            if psutil.virtual_memory().percent > 95:
                return False

            return True
        except Exception:
            return False

    def get_uptime(self) -> str:
        uptime_seconds = int(time.time() - self.start_time)

        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60

        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

    def get_status(self) -> Dict[str, Any]:
        return {
            "healthy": self.healthy,
            "uptime": self.get_uptime(),
            "checks_performed": self.check_count,
            "last_check": self.last_check,
            "timestamp": datetime.utcnow().isoformat()
        }
