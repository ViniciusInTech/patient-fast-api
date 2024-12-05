from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_create_patient():
    response = client.post("/api/patients/", json={
        "name": "John Doe",
        "birth_date": "1980-01-01",
        "gender": "Male",
        "address": "123 Main St"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
