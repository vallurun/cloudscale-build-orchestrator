from src.scheduler import Scheduler
from src.models import BuildRequest, Step
import asyncio, uuid

def test_simple_run():
    async def _run():
        s = Scheduler(concurrency=1)
        await s.start()
        rid = str(uuid.uuid4())
        await s.submit(rid, BuildRequest(name="echo", steps=[Step(cmd="echo hello", timeout_sec=5, retries=0)]))
        await asyncio.sleep(0.5)
        # wait for queue to drain
        await s.q.join()
        st = s.runs[rid]
        assert st.status == "succeeded"
        await s.stop()
    asyncio.run(_run())
