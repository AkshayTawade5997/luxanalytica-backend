"""
Nexus-Prime: Central Orchestrator for Multi-Agent System
Manages task routing, agent coordination, and system-wide operations
"""

import asyncio
import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class NexusOrchestrator:
    """Central orchestrator managing all AI agents"""

    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.active_agents: set = set()
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.tasks: Dict[str, Dict] = {}
        self.running = False

    async def initialize_agents(self):
        """Initialize all specialized agents"""
        logger.info("🔄 Initializing agent fleet...")

        # Import agents here to avoid circular imports
        from agents.astra import AstraProjectManager
        from agents.pyra import PyraPythonAgent
        from agents.rhea import RheaRStatsAgent
        from agents.terra import TerraGISAgent
        from agents.geno import GenoExperimentalAgent
        from agents.luma import LumaReportAgent

        # Initialize all agents
        self.agents = {
            "astra": AstraProjectManager(),
            "pyra": PyraPythonAgent(),
            "rhea": RheaRStatsAgent(),
            "terra": TerraGISAgent(),
            "geno": GenoExperimentalAgent(),
            "luma": LumaReportAgent(),
        }

        # Activate all agents
        for name, agent in self.agents.items():
            await agent.initialize()
            self.active_agents.add(name)
            logger.info(f"  ✅ {name.upper()} agent activated")

        self.running = True

        # Start task processor
        asyncio.create_task(self._task_processor())

        logger.info(f"🎯 All {len(self.agents)} agents ready for 24/7 operations")

    async def _task_processor(self):
        """Background task processor"""
        while self.running:
            try:
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                asyncio.create_task(self._execute_task(task))
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Task processor error: {e}")

    async def _execute_task(self, task: Dict):
        """Execute a task with the appropriate agent"""
        task_id = task["id"]
        agent_name = task.get("agent", "astra")  # Default to Astra for routing

        try:
            self.tasks[task_id]["status"] = TaskStatus.PROCESSING.value
            self.tasks[task_id]["started_at"] = datetime.utcnow().isoformat()

            # Get the appropriate agent
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                result = await agent.process(task["data"])

                self.tasks[task_id]["status"] = TaskStatus.COMPLETED.value
                self.tasks[task_id]["result"] = result
                self.tasks[task_id]["completed_at"] = datetime.utcnow().isoformat()
            else:
                raise ValueError(f"Unknown agent: {agent_name}")

        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")
            self.tasks[task_id]["status"] = TaskStatus.FAILED.value
            self.tasks[task_id]["error"] = str(e)

    async def submit_task(self, task_data: Dict[str, Any]) -> str:
        """Submit a new task to the system"""
        task_id = str(uuid.uuid4())

        # Determine best agent for task
        agent_name = await self._route_task(task_data)

        task = {
            "id": task_id,
            "agent": agent_name,
            "data": task_data,
            "submitted_at": datetime.utcnow().isoformat()
        }

        self.tasks[task_id] = {
            "status": TaskStatus.PENDING.value,
            "agent": agent_name,
            "submitted_at": task["submitted_at"]
        }

        await self.task_queue.put(task)
        logger.info(f"📥 Task {task_id} submitted to {agent_name}")

        return task_id

    async def _route_task(self, task_data: Dict) -> str:
        """Intelligent task routing to appropriate agent"""
        task_type = task_data.get("type", "").lower()

        routing_map = {
            "python": "pyra",
            "data_analysis": "pyra",
            "r": "rhea",
            "statistics": "rhea",
            "gis": "terra",
            "spatial": "terra",
            "experimental": "geno",
            "design": "geno",
            "report": "luma",
            "visualization": "luma",
        }

        return routing_map.get(task_type, "astra")  # Default to Astra

    async def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Get status of a specific task"""
        return self.tasks.get(task_id)

    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {}
        for name, agent in self.agents.items():
            status[name] = {
                "active": name in self.active_agents,
                "status": await agent.get_status() if hasattr(agent, 'get_status') else "unknown"
            }
        return status

    async def get_agent_metrics(self) -> Dict[str, Any]:
        """Get metrics from all agents"""
        metrics = {}
        for name, agent in self.agents.items():
            if hasattr(agent, 'get_metrics'):
                metrics[name] = await agent.get_metrics()
        return metrics

    async def direct_agent_call(self, agent_name: str, data: Dict) -> Dict:
        """Direct call to a specific agent"""
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not found")

        agent = self.agents[agent_name]
        return await agent.process(data)

    async def check_agent_health(self):
        """Check health of all agents and restart if needed"""
        for name, agent in self.agents.items():
            try:
                if hasattr(agent, 'health_check'):
                    healthy = await agent.health_check()
                    if not healthy:
                        logger.warning(f"⚠️ Agent {name} unhealthy - restarting...")
                        await agent.initialize()
                        self.active_agents.add(name)
            except Exception as e:
                logger.error(f"Health check failed for {name}: {e}")

    async def shutdown(self):
        """Graceful shutdown of all agents"""
        self.running = False
        logger.info("🛑 Shutting down all agents...")

        for name, agent in self.agents.items():
            try:
                if hasattr(agent, 'shutdown'):
                    await agent.shutdown()
                logger.info(f"  ✅ {name} shutdown complete")
            except Exception as e:
                logger.error(f"Error shutting down {name}: {e}")

        self.active_agents.clear()
