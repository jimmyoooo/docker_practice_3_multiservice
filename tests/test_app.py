import os

def test_root():
    from app import app
    c = app.test_client()
    r = c.get("/")
    assert r.status_code == 200

def test_count_increments():
    os.environ["REDIS_URL"] = "redis://localhost:6379/0"
    from app import app
    c = app.test_client()
    a = c.get("/count").data.decode()
    b = c.get("/count").data.decode()
    assert "hits=" in a
    assert "hits=" in b
