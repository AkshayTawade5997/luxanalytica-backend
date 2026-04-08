import asyncio
import logging
import psutil
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SentinelMonitor:
    def __init__(self):
        self.monitoring = False
        self.metrics_history = []
        self.alert_thresholds = {"cpu": 80, "memory": 85, "disk": 90}

    async def monitoring_loop(self):
        self.monitoring = True
        logger.info("👁️ Sentinel monitoring started (24/7)")

        while self.monitoring:
            try:
                metrics = await self._collect_metrics()
                self.metrics_history.append(metrics)

                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-1000:]

                await self._check_alerts(metrics)

                if len(self.metrics_history) % 5 == 0:
                    logger.info(f"📊 System status - CPU: {metrics['cpu']}%, Memory: {metrics['memory']}%")

                await asyncio.sleep(60)

            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(60)

    async def _collect_metrics(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "connections": len(psutil.net_connections()),
            "boot_time": psutil.boot_time()
        }

    async def _check_alerts(self, metrics: Dict[str, Any]):
        alerts = []

        if metrics["cpu"] > self.alert_thresholds["cpu"]:
            alerts.append(f"High CPU usage: {metrics['cpu']}%")

        if metrics["memory"] > self.alert_thresholds["memory"]:
            alerts.append(f"High memory usage: {metrics['memory']}%")

        if metrics["disk"] > self.alert_thresholds["disk"]:
            alerts.append(f"High disk usage: {metrics['disk']}%")

        for alert in alerts:
            logger.warning(f"🚨 ALERT: {alert}")

    def stop(self):
        self.monitoring = False
        logger.info("👁️ Sentinel monitoring stopped")
