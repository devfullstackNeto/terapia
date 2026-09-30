import os
import time
from pathlib import Path

from redis import Redis

redis = Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))
while True:
    try:
        redis.ping()
        Path("/tmp/worker-ready").touch()
        redis.set("terapia:worker:heartbeat", str(time.time()), ex=60)
    except Exception:
        Path("/tmp/worker-ready").unlink(missing_ok=True)
    time.sleep(15)
