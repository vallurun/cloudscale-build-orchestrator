import hashlib
import os
from typing import Optional

class LocalCache:
    def __init__(self, root: str = ".cache"):
        self.root = root
        os.makedirs(self.root, exist_ok=True)

    def key(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    def path_for(self, key: str) -> str:
        return os.path.join(self.root, key)

    def get(self, key: str) -> Optional[bytes]:
        p = self.path_for(key)
        if os.path.exists(p):
            with open(p, "rb") as f:
                return f.read()
        return None

    def put(self, content: bytes) -> str:
        k = self.key(content)
        p = self.path_for(k)
        if not os.path.exists(p):
            with open(p, "wb") as f:
                f.write(content)
        return k
