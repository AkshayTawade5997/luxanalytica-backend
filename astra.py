"""
Astra: Project Manager Agent
Coordinates complex projects and delegates tasks to other agents
"""

import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class AstraProjectManager:
    """Project management and task coordination agent"""

    def __init__(self):
        self.name = "Astra"
        self.role = "Project Manager"
        self.active_projects = {}
        self.task_history = []

    async def initialize(self):
        """Initialize Astra"""
        logger.info(f"🎯 {self.name} initialized - {self.role}")

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process project management tasks"""
        action = data.get("action", "plan")

        if action == "plan":
            return await self._create_project_plan(data)
        elif action == "delegate":
            return await self._delegate_tasks(data)
        elif action == "status":
            return await self._get_project_status(data)
        else:
            return await self._general_coordination(data)

    async def _create_project_plan(self, data: Dict) -> Dict:
        """Create a project execution plan"""
        project_name = data.get("project_name", "Unnamed Project")
        requirements = data.get("requirements", [])

        plan = {
            "project": project_name,
            "phases": [
                {"phase": 1, "name": "Analysis", "agent": "pyra/rhea", "duration": "2h"},
                {"phase": 2, "name": "Processing", "agent": "pyra", "duration": "4h"},
                {"phase": 3, "name": "Visualization", "agent": "luma", "duration": "2h"},
            ],
            "estimated_completion": "8 hours",
            "created_at": datetime.utcnow().isoformat()
        }

        self.active_projects[project_name] = plan

        return {
            "status": "success",
            "agent": self.name,
            "plan": plan,
            "message": f"Project '{project_name}' plan created with {len(plan['phases'])} phases"
        }

    async def _delegate_tasks(self, data: Dict) -> Dict:
        """Delegate tasks to appropriate agents"""
        tasks = data.get("tasks", [])

        delegations = []
        for task in tasks:
            task_type = task.get("type", "general")
            assigned_agent = self._determine_agent(task_type)

            delegations.append({
                "task": task,
                "assigned_to": assigned_agent,
                "status": "queued"
            })

        return {
            "status": "success",
            "agent": self.name,
            "delegations": delegations,
            "message": f"Delegated {len(tasks)} tasks"
        }

    def _determine_agent(self, task_type: str) -> str:
        """Determine best agent for task type"""
        mapping = {
            "python": "pyra",
            "data": "pyra",
            "statistics": "rhea",
            "r": "rhea",
            "gis": "terra",
            "spatial": "terra",
            "experiment": "geno",
            "report": "luma",
            "visualization": "luma"
        }
        return mapping.get(task_type.lower(), "pyra")

    async def _get_project_status(self, data: Dict) -> Dict:
        """Get status of active projects"""
        return {
            "status": "success",
            "agent": self.name,
            "active_projects": len(self.active_projects),
            "projects": list(self.active_projects.keys()),
            "total_tasks_managed": len(self.task_history)
        }

    async def _general_coordination(self, data: Dict) -> Dict:
        """General coordination tasks"""
        return {
            "status": "success",
            "agent": self.name,
            "message": "Coordination task completed",
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "name": self.name,
            "role": self.role,
            "active_projects": len(self.active_projects),
            "healthy": True
        }

    async def health_check(self) -> bool:
        """Health check"""
        return True

    async def shutdown(self):
        """Shutdown"""
        logger.info(f"🛑 {self.name} shutting down")
