import os
from flask import Flask
import redis

app = Flask(__name__)

# 用環境變數拿 redis 位置；在 compose 裡我們會設成 "redis"
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

@app.get("/")
def hello():
    return "ok: web is running\n"

@app.get("/count")
def count():
    n = r.incr("hits")
    return f"hits={n}\n"

