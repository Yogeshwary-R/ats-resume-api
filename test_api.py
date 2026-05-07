from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "running"
    print("✅ Health check passed!")

def test_register_invalid_email():
    response = client.post("/auth/register", json={
        "email": "notanemail",
        "password": "test123"
    })
    assert response.status_code == 422
    print("✅ Invalid email rejected!")

def test_register_short_password():
    response = client.post("/auth/register", json={
        "email": "test2@gmail.com",
        "password": "123"
    })
    assert response.status_code == 422
    print("✅ Short password rejected!")

def test_login_wrong_password():
    response = client.post("/auth/login", json={
        "email": "test@gmail.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    print("✅ Wrong password rejected!")

def test_analyze_without_token():
    response = client.post("/resume/analyze")
    assert response.status_code == 401
    print("✅ Unauthorized access blocked!")