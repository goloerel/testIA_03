from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.api.drivers import get_driver_service
from src.services.driver_service import DriverService

client = TestClient(app)

valid_driver_payload = {
    "nombre": "Juan Perez",
    "licencia": "MX-DL-12345",
    "estado": "ACTIVE",
    "fecha_contratacion": "2024-01-15"
}

def get_mock_service(mock_repo):
    return DriverService(repository=mock_repo)

def test_create_driver_success():
    mock_repo = MagicMock()
    # Mock no duplicates
    mock_repo.get_by_license.return_value = None
    # Mock creation
    mock_repo.create.side_effect = lambda x: {**x, "_id": "507f1f77bcf86cd799439011"}
    
    app.dependency_overrides[get_driver_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.post("/api/v1/drivers/", json=valid_driver_payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == valid_driver_payload["nombre"]
        assert "_id" in data
        assert "fecha_creacion" in data
    finally:
        app.dependency_overrides = {}

def test_create_driver_duplicate():
    mock_repo = MagicMock()
    # Mock duplicate
    mock_repo.get_by_license.return_value = {"_id": "exists"}
    
    app.dependency_overrides[get_driver_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.post("/api/v1/drivers/", json=valid_driver_payload)
        
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]
    finally:
        app.dependency_overrides = {}
