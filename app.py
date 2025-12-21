import os
from flask import Flask
import redis

app = Flask(__name__)

_redis_client = None

def get_redis():
    global _redis_client
    if _redis_client is not None:
        return _redis_client

    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        _redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
        return _redis_client

    # fallback：給本機/舊寫法用
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    _redis_client = redis.Redis(host=host, port=port, decode_responses=True)
    return _redis_client


@app.get("/")
def hello():
    return "ok: web is running\n"


@app.get("/count")
def count():
    r = get_redis()
    n = r.incr("hits")
    return f"hits={n}\n"
