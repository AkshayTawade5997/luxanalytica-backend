"""
LuxAnalytica 24/7 AI Backend System
Multi-Agent Orchestration Platform with Self-Healing Capabilities
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Core components
from core.nexus import NexusOrchestrator
from core.sentinel import SentinelMonitor
from core.vault import VaultStorage
from core.pulse import PulseHealthCheck

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
nexus: Optional[NexusOrchestrator] = None
sentinel: Optional[SentinelMonitor] = None
vault: Optional[VaultStorage] = None
pulse: Optional[PulseHealthCheck] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle with 24/7 monitoring"""
    global nexus, sentinel, vault, pulse

    logger.info("🚀 Initializing LuxAnalytica 24/7 AI Backend...")

    # Initialize core systems
    vault = VaultStorage()
    pulse = PulseHealthCheck()
    sentinel = SentinelMonitor()

    # Initialize Nexus with all agents
    nexus = NexusOrchestrator()
    await nexus.initialize_agents()

    # Start 24/7 monitoring loops
    asyncio.create_task(sentinel.monitoring_loop())
    asyncio.create_task(pulse.health_check_loop())
    asyncio.create_task(self_healing_loop())

    logger.info("✅ All systems operational - 24/7 mode activated")

    yield

    # Shutdown
    logger.info("🛑 Shutting down systems...")
    await nexus.shutdown()
    logger.info("✅ Shutdown complete")

app = FastAPI(
    title="LuxAnalytica AI Backend",
    description="24/7 Autonomous Multi-Agent System for Data Analysis",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def self_healing_loop():
    """24/7 self-healing and optimization loop"""
    while True:
        try:
            await asyncio.sleep(60)

            # Memory optimization
            import psutil
            memory = psutil.virtual_memory()
            if memory.percent > 85:
                logger.warning(f"High memory usage: {memory.percent}% - triggering cleanup")
                await vault.cleanup_old_data()

            # Agent health check
            if nexus:
                await nexus.check_agent_health()

        except Exception as e:
            logger.error(f"Self-healing error: {e}")

@app.get("/")
async def root():
    """Root endpoint - system status"""
    return {
        "service": "LuxAnalytica AI Backend",
        "status": "operational",
        "mode": "24/7 autonomous",
        "timestamp": datetime.utcnow().isoformat(),
        "agents": await nexus.get_agent_status() if nexus else {}
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring services"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": pulse.get_uptime() if pulse else "unknown",
        "agents_active": len(nexus.active_agents) if nexus else 0
    }

@app.get("/agents")
async def list_agents():
    """List all available agents and their status"""
    if not nexus:
        raise HTTPException(status_code=503, detail="System initializing")
    return await nexus.get_agent_status()

@app.post("/task")
async def submit_task(task: Dict[str, Any], background_tasks: BackgroundTasks):
    """Submit a task to the agent system"""
    if not nexus:
        raise HTTPException(status_code=503, detail="System initializing")

    task_id = await nexus.submit_task(task)

    return {
        "task_id": task_id,
        "status": "submitted",
        "message": "Task queued for processing"
    }

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """Get task status and results"""
    if not nexus:
        raise HTTPException(status_code=503, detail="System initializing")

    status = await nexus.get_task_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")

    return status

@app.post("/analyze/python")
async def python_analysis(request: Dict[str, Any]):
    """Direct access to Pyra (Python analysis agent)"""
    if not nexus:
        raise HTTPException(status_code=503, detail="System initializing")

    result = await nexus.direct_agent_call("pyra", request)
    return result

@app.post("/analyze/r")
async def r_analysis(request: Dict[str, Any]):
    """Direct access to Rhea (R statistics agent)"""
    if not nexus:
        raise HTTPException(status_code=503, detail="System initializing")

    result = await nexus.direct_agent_call("rhea", request)
    return result

@app.post("/analyze/gis")
async def gis_analysis(request: Dict[str, Any]):
    """Direct access to Terra (GIS agent)"""
    if not nexus:
        raise HTTPException(status_code=503, detail="System initializing")

    result = await nexus.direct_agent_call("terra", request)
    return result

@app.post("/report/generate")
async def generate_report(request: Dict[str, Any]):
    """Direct access to Luma (Report generation agent)"""
    if not nexus:
        raise HTTPException(status_code=503, detail="System initializing")

    result = await nexus.direct_agent_call("luma", request)
    return result

@app.get("/monitoring/metrics")
async def get_metrics():
    """Get system metrics for monitoring"""
    import psutil

    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory": dict(psutil.virtual_memory()._asdict()),
        "disk": dict(psutil.disk_usage('/')._asdict()),
        "timestamp": datetime.utcnow().isoformat(),
        "agents": await nexus.get_agent_metrics() if nexus else {}
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
