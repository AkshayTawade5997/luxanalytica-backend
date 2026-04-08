# LuxAnalytica AI Backend

**24/7 Autonomous Multi-Agent System for Data Analysis**

A production-ready AI backend featuring 10 specialized agents working in harmony to provide comprehensive data analysis, statistical computing, GIS processing, experimental design, and automated reporting.

## 🚀 Features

- **24/7 Operation**: Self-healing system with continuous monitoring
- **Multi-Agent Architecture**: 10 specialized AI agents orchestrated by Nexus-Prime
- **Auto-Scaling**: Efficient resource management and optimization
- **RESTful API**: FastAPI-based with automatic documentation
- **Free Tier Ready**: Optimized for Render.com free hosting

## 🤖 Agent Fleet

| Agent | Role | Specialization |
|-------|------|----------------|
| **Nexus-Prime** | Orchestrator | Central coordination and task routing |
| **Sentinel** | Monitor | 24/7 system monitoring and alerting |
| **Vault** | Storage | Secure data persistence and caching |
| **Pulse** | Health Check | Uptime monitoring and self-healing |
| **Astra** | Project Manager | Task coordination and delegation |
| **Pyra** | Python Analyst | Data processing, ML, pandas operations |
| **Rhea** | R Statistician | Statistical tests, regression, time series |
| **Terra** | GIS Specialist | Spatial analysis, mapping, geocoding |
| **Geno** | Experimentalist | Research design, power analysis |
| **Luma** | Report Specialist | Visualization, dashboards, reports |

## 📋 Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/AkshayTawade5997/luxanalytica-backend.git
cd luxanalytica-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload
```

### API Endpoints

- `GET /` - System status
- `GET /health` - Health check (for monitoring)
- `GET /agents` - List all agents and status
- `POST /task` - Submit a task
- `GET /task/{task_id}` - Check task status
- `POST /analyze/python` - Direct Python analysis
- `POST /analyze/r` - Direct R statistical analysis
- `POST /analyze/gis` - Direct GIS analysis
- `POST /report/generate` - Generate reports
- `GET /monitoring/metrics` - System metrics

### Example Usage

```python
import requests

# Submit analysis task
response = requests.post("http://localhost:8000/task", json={
    "type": "python",
    "operation": "statistical_analysis",
    "data": {...}
})
task_id = response.json()["task_id"]

# Check status
status = requests.get(f"http://localhost:8000/task/{task_id}")
print(status.json())
```

## 🌐 Deployment

### Render.com (Recommended - Free Tier)

1. Push code to GitHub
2. Connect repository to Render
3. Deploy automatically with `render.yaml`

### Environment Variables

- `PORT` - Server port (default: 8000)
- `PYTHON_VERSION` - Python version (3.11 recommended)

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LuxAnalytica Backend                      │
├─────────────────────────────────────────────────────────────┤
│  API Layer (FastAPI)                                         │
│  ├── REST Endpoints                                          │
│  ├── WebSocket (future)                                      │
│  └── Auto Documentation                                      │
├─────────────────────────────────────────────────────────────┤
│  Core Systems                                                │
│  ├── Nexus-Prime (Orchestrator)                             │
│  ├── Sentinel (24/7 Monitor)                                │
│  ├── Vault (Storage)                                        │
│  └── Pulse (Health Check)                                   │
├─────────────────────────────────────────────────────────────┤
│  Agent Fleet                                                 │
│  ├── Astra (Project Manager)                                │
│  ├── Pyra (Python)                                          │
│  ├── Rhea (R Statistics)                                    │
│  ├── Terra (GIS)                                            │
│  ├── Geno (Experimental Design)                             │
│  └── Luma (Reports)                                         │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Configuration

Edit `core/nexus.py` to customize:
- Agent behavior
- Task routing logic
- Resource limits

## 📈 Monitoring

The system includes built-in monitoring:
- CPU/Memory/Disk tracking
- Agent health checks
- Task queue monitoring
- Automatic cleanup

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 📄 License

MIT License - See LICENSE file

## 🔗 Connect

- Website: [LuxAnalytica](https://luxanalytica.com)
- Backend: [API Documentation](/docs)
- Status: 24/7 Operational

---

**Powered by LuxAnalytica AI** 🚀
