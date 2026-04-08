"""
Sentinel: 24/7 System Monitor
Monitors system health, resource usage, and agent performance
"""

import asyncio
import logging
import psutil
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SentinelMonitor:
    """24/7 monitoring system for LuxAnalytica backend"""

    def __init__(self):
        self.monitoring = False
        self.metrics_history = []
        self.alert_thresholds = {
            "cpu": 80,
            "memory": 85,
            "disk": 90
        }

    async def monitoring_loop(self):
        """Continuous monitoring loop"""
        self.monitoring = True
        logger.info("👁️ Sentinel monitoring started (24/7)")

        while self.monitoring:
            try:
                metrics = await self._collect_metrics()
                self.metrics_history.append(metrics)

                # Keep only last 1000 metrics points
                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-1000:]

                # Check thresholds and alert
                await self._check_alerts(metrics)

                # Log status every 5 minutes
                if len(self.metrics_history) % 5 == 0:
                    logger.info(f"📊 System status - CPU: {metrics['cpu']}%, Memory: {metrics['memory']}%")

                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(60)

    async def _collect_metrics(self) -> Dict[str, Any]:
        """Collect system metrics"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "connections": len(psutil.net_connections()),
            "boot_time": psutil.boot_time()
        }

    async def _check_alerts(self, metrics: Dict[str, Any]):
        """Check for threshold violations"""
        alerts = []

        if metrics["cpu"] > self.alert_thresholds["cpu"]:
            alerts.append(f"High CPU usage: {metrics['cpu']}%")

        if metrics["memory"] > self.alert_thresholds["memory"]:
            alerts.append(f"High memory usage: {metrics['memory']}%")

        if metrics["disk"] > self.alert_thresholds["disk"]:
            alerts.append(f"High disk usage: {metrics['disk']}%")

        for alert in alerts:
            logger.warning(f"🚨 ALERT: {alert}")
            # Here you could send notifications (email, Slack, etc.)

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        return {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "timestamp": datetime.utcnow().isoformat()
        }

    def stop(self):
        """Stop monitoring"""
        self.monitoring = False
        logger.info("👁️ Sentinel monitoring stopped")
