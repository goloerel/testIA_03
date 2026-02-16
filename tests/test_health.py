from fastapi.testclient import TestClient
from src.main import app
from src.database import db_client
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_health_check_success():
    # We allow the real connection if it works, or we can mock it to always pass.
    # For integration testing, let's try to see if it really connects (integration test).
    # If using real DB, ensure it is up.
    response = client.get("/health")
    # If DB is not up during test, this might fail unless we mock.
    # To be safe and test logic:
    with patch("src.api.health.db_client") as mock_db:
        mock_db.client.admin.command.return_value = {"ok": 1}
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "database": "connected"}

def test_health_check_failure():
    # Mocking the database connection failure
    with patch("src.api.health.db_client") as mock_db:
        # Simulate exception when pinging
        mock_db.client.admin.command.side_effect = Exception("Connection refused")
        
        response = client.get("/health")
        assert response.status_code == 500
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["database"] == "disconnected"
