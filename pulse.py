"""
Pulse: Health Check and Uptime Monitor
Ensures 24/7 availability and external monitoring compatibility
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any
import time

logger = logging.getLogger(__name__)

class PulseHealthCheck:
    """Health check system for 24/7 monitoring"""

    def __init__(self):
        self.start_time = time.time()
        self.check_count = 0
        self.last_check = None
        self.healthy = True

    async def health_check_loop(self):
        """Continuous health check loop"""
        logger.info("💓 Pulse health monitoring started")

        while True:
            try:
                self.check_count += 1
                self.last_check = datetime.utcnow().isoformat()

                # Perform self-check
                self.healthy = await self._self_check()

                if not self.healthy:
                    logger.error("💔 Health check failed - system unhealthy")

                # Log every 10 checks
                if self.check_count % 10 == 0:
                    uptime = self.get_uptime()
                    logger.info(f"💓 Health check #{self.check_count} - Uptime: {uptime}")

                await asyncio.sleep(30)  # Check every 30 seconds

            except Exception as e:
                logger.error(f"Health check error: {e}")
                self.healthy = False
                await asyncio.sleep(30)

    async def _self_check(self) -> bool:
        """Perform internal health check"""
        try:
            # Check basic system functions
            import psutil

            # If CPU is critically high, mark unhealthy
            if psutil.cpu_percent() > 95:
                return False

            # If memory is critically high, mark unhealthy
            if psutil.virtual_memory().percent > 95:
                return False

            return True
        except Exception:
            return False

    def get_uptime(self) -> str:
        """Get system uptime as formatted string"""
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
        """Get current health status"""
        return {
            "healthy": self.healthy,
            "uptime": self.get_uptime(),
            "checks_performed": self.check_count,
            "last_check": self.last_check,
            "timestamp": datetime.utcnow().isoformat()
        }
