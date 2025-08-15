import asyncio, subprocess, shlex
from typing import Tuple

async def run_step(cmd: str, timeout: int) -> Tuple[int, str]:
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    try:
        stdout = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        output = (stdout[0] or b"").decode()
        return proc.returncode or 0, output
    except asyncio.TimeoutError:
        proc.kill()
        return 124, f"Timeout after {timeout}s for: {cmd}"
