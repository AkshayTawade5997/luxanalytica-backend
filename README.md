# LuxAnalytica AI Backend

**24/7 Autonomous Multi-Agent System for Data Analysis**

## 🚀 Quick Deploy to Render

1. Upload all files to GitHub (keep folder structure)
2. Connect to Render.com
3. Deploy automatically

## 📁 File Structure

```
luxanalytica-backend/
├── main.py                 # Main FastAPI app
├── requirements.txt        # Python dependencies
├── render.yaml            # Render config
├── Procfile               # Process file
├── .gitignore            # Git ignore
├── core/                 # Core systems
│   ├── __init__.py
│   ├── nexus.py         # Orchestrator
│   ├── sentinel.py      # Monitor
│   ├── vault.py         # Storage
│   └── pulse.py         # Health check
├── agents/               # AI agents
│   ├── __init__.py
│   ├── astra.py         # Project Manager
│   ├── pyra.py          # Python Analyst
│   ├── rhea.py          # R Statistics
│   ├── terra.py         # GIS Specialist
│   ├── geno.py          # Experimental Design
│   └── luma.py          # Report Generator
└── utils/                # Utilities
    └── __init__.py
```

## 🔗 API Endpoints

- `GET /` - System status
- `GET /health` - Health check
- `GET /agents` - List agents
- `POST /task` - Submit task
- `GET /task/{id}` - Check task status
- `POST /analyze/python` - Python analysis
- `POST /analyze/r` - R statistics
- `POST /analyze/gis` - GIS analysis
- `POST /report/generate` - Generate report

## 🤖 Agents

| Agent | Role |
|-------|------|
| Astra | Project Manager |
| Pyra | Python Analyst |
| Rhea | R Statistics |
| Terra | GIS Specialist |
| Geno | Experimental Design |
| Luma | Report Generator |

## 🌐 URL

Your backend will be at:
`https://luxanalytica-backend.onrender.com`
