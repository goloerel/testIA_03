from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.api.drivers import get_driver_service
from src.services.driver_service import DriverService

client = TestClient(app)

mock_driver_data = {
    "_id": "507f1f77bcf86cd799439011",
    "nombre": "Juan Perez",
    "licencia": "MX-DL-12345",
    "estado": "ACTIVE",
    "fecha_contratacion": "2024-01-15",
    "fecha_creacion": "2024-01-15T10:00:00"
}

def get_mock_service(mock_repo):
    return DriverService(repository=mock_repo)

def test_get_driver_success():
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = mock_driver_data
    
    app.dependency_overrides[get_driver_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.get("/api/v1/drivers/507f1f77bcf86cd799439011")
        
        assert response.status_code == 200
        data = response.json()
        assert data["licencia"] == "MX-DL-12345"
    finally:
        app.dependency_overrides = {}

def test_get_driver_not_found():
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = None
    
    app.dependency_overrides[get_driver_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.get("/api/v1/drivers/507f1f77bcf86cd799439011")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    finally:
        app.dependency_overrides = {}
