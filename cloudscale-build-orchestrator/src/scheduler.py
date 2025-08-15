import asyncio, time
from typing import Dict, Any
from .models import BuildRequest, BuildStatus
from .worker import run_step
from .cache import LocalCache

class Scheduler:
    def __init__(self, concurrency: int = 4):
        self.q: asyncio.Queue[tuple[str, BuildRequest]] = asyncio.Queue()
        self.concurrency = concurrency
        self.cache = LocalCache()
        self.runs: Dict[str, BuildStatus] = {}
        self._workers = []

    async def start(self):
        for _ in range(self.concurrency):
            self._workers.append(asyncio.create_task(self._worker()))

    async def stop(self):
        for w in self._workers:
            w.cancel()

    async def submit(self, run_id: str, req: BuildRequest):
        status = BuildStatus(run_id=run_id, name=req.name, status="queued", started_at=time.time(), logs=[])
        self.runs[run_id] = status
        await self.q.put((run_id, req))

    async def _worker(self):
        while True:
            run_id, req = await self.q.get()
            status = self.runs[run_id]
            status.status = "running"
            try:
                for step in req.steps:
                    rc, out = await run_step(step.cmd, step.timeout_sec)
                    status.logs.append(out)
                    if rc != 0:
                        # retry logic
                        for attempt in range(step.retries):
                            rc, out = await run_step(step.cmd, step.timeout_sec)
                            status.logs.append(f"[retry {attempt+1}]\n{out}")
                            if rc == 0:
                                break
                        if rc != 0:
                            status.status = f"failed ({rc})"
                            status.finished_at = time.time()
                            break
                else:
                    status.status = "succeeded"
                    status.finished_at = time.time()
            finally:
                self.q.task_done()
