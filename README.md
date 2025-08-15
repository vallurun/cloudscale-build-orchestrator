# CloudScale Build Orchestrator

A minimal, local-first prototype of a **distributed build & test orchestrator** inspired by Microsoft 1ES.
It parallelizes "build jobs" (simulated shell commands) using `asyncio`, caches artifacts, and exposes a small API
to submit builds, check status, and fetch logs. Designed to be extended with Azure (AKS, Blob Storage, Azure DevOps).

## Highlights
- **Async job scheduling:** FIFO queue, concurrency limits, backoff & retries
- **Artifact caching:** content-addressed cache with local FS backend (swap-in Azure Blob)
- **API:** FastAPI endpoints to submit jobs and query runs
- **Observability:** simple in-memory metrics + structured logs
- **CI ready:** pytest, lint hooks, GitHub Actions workflow

## Quick Start

### 1) Python (no Docker)
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Start the API (scheduler runs inside the same process)
uvicorn src.api:app --reload --port 8000
```

Submit a build:
```bash
curl -X POST http://localhost:8000/builds -H "Content-Type: application/json" -d '{
  "name": "unit-tests",
  "steps": [
    {"cmd": "echo compiling && python -V"},
    {"cmd": "pytest -q"}
  ]
}'
```

Check status:
```bash
curl http://localhost:8000/builds/<run_id>
```

### 2) Docker Compose
```bash
docker compose up --build
```

## Project Structure
```
1es-distributed-build-accelerator/
├─ src/
│  ├─ api.py            # FastAPI app (submit/query builds)
│  ├─ scheduler.py      # Async scheduler & job runner
│  ├─ worker.py         # Worker utilities (exec, retries)
│  ├─ cache.py          # Content-addressed artifact cache
│  └─ models.py         # Pydantic models
├─ tests/
│  └─ test_scheduler.py
├─ scripts/
│  └─ run_local.sh
├─ .github/workflows/
│  └─ ci.yml
├─ docker-compose.yml
├─ requirements.txt
└─ README.md
```

## Azure Integration (next steps)
- Replace `LocalCache` with Azure Blob-backed cache
- Run `api.py` on AKS; horizontal autoscale using KEDA
- Wire to Azure DevOps via service connection; trigger on PR
- Push metrics to Application Insights; logs to Log Analytics

## License
MIT
