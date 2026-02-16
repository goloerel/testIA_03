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

mock_driver_data = {
    "_id": "507f1f77bcf86cd799439011",
    **valid_driver_payload,
    "fecha_creacion": "2024-01-15T10:00:00"
}

def get_mock_service(mock_repo):
    return DriverService(repository=mock_repo)

def test_update_driver_success():
    mock_repo = MagicMock()
    # 1. Get existing
    mock_repo.get_by_id.return_value = mock_driver_data
    # 2. Check duplicate (same license, same ID - no conflict)
    # Service logic: get_by_license returns doc. if doc._id != id -> conflict.
    mock_repo.get_by_license.return_value = {"_id": "507f1f77bcf86cd799439011"} 
    
    # 3. Mock update return
    updated_data = {**mock_driver_data, "nombre": "Juan Updated"}
    mock_repo.update.return_value = updated_data
    
    app.dependency_overrides[get_driver_service] = lambda: get_mock_service(mock_repo)

    try:
        # Request to update name
        payload = {**valid_driver_payload, "nombre": "Juan Updated"}
        
        response = client.put("/api/v1/drivers/507f1f77bcf86cd799439011", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Juan Updated"
    finally:
        app.dependency_overrides = {}

def test_update_driver_conflict():
    mock_repo = MagicMock()
    # Exists
    mock_repo.get_by_id.return_value = mock_driver_data
    # Conflict: license belongs to another ID
    mock_repo.get_by_license.return_value = {"_id": "other_id"}
    
    app.dependency_overrides[get_driver_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.put("/api/v1/drivers/507f1f77bcf86cd799439011", json=valid_driver_payload)
        
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]
    finally:
        app.dependency_overrides = {}
