from fastapi import FastAPI, HTTPException
from .models import BuildRequest
from .scheduler import Scheduler
import asyncio, uuid

app = FastAPI(title="1ES Build Accelerator")
scheduler = Scheduler(concurrency=4)
loop = asyncio.get_event_loop()

@app.on_event("startup")
async def on_startup():
    await scheduler.start()

@app.on_event("shutdown")
async def on_shutdown():
    await scheduler.stop()

@app.post("/builds")
async def create_build(req: BuildRequest):
    run_id = str(uuid.uuid4())
    await scheduler.submit(run_id, req)
    return {"run_id": run_id}

@app.get("/builds/{run_id}")
async def get_build(run_id: str):
    status = scheduler.runs.get(run_id)
    if not status:
        raise HTTPException(404, "run not found")
    return status

@app.get("/healthz")
async def health():
    return {"ok": True}
