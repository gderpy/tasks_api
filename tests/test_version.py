from fastapi.testclient import TestClient
from app.main import app 


client = TestClient(app)

def test_version_ok():
    r = client.get("/version")
    assert r.status_code == 200
    body = r.json()
    assert body["app"] == "tasks-api"
    assert "version" in body