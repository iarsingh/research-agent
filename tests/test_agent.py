from fastapi.testclient import TestClient
from research.main import app

client = TestClient(app)


def test_runs_and_refuses_a_write():
    payload = client.post("/agent/run", json={"goal": 'error budget notes', **{'payload': {'notes': ['error budget is 43 minutes', 'cafeteria menu']}}}).json()
    assert payload["refused"] is False
    assert payload["applied"] is False
    assert payload["hits"]
    refused = client.post("/agent/run", json={"goal": 'publish this to twitter'}).json()
    assert refused["refused"] is True
