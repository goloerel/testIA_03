from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.api.drivers import get_driver_service
from src.services.driver_service import DriverService

client = TestClient(app)

def get_mock_service(mock_repo):
    return DriverService(repository=mock_repo)

def test_delete_driver_success():
    mock_repo = MagicMock()
    # Exists
    mock_repo.get_by_id.return_value = {"_id": "507f1f77bcf86cd799439011"}
    # Delete success
    mock_repo.delete.return_value = True
    
    app.dependency_overrides[get_driver_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.delete("/api/v1/drivers/507f1f77bcf86cd799439011")
        assert response.status_code == 204
    finally:
        app.dependency_overrides = {}

def test_delete_driver_not_found():
    mock_repo = MagicMock()
    # Not found
    mock_repo.get_by_id.return_value = None
    
    app.dependency_overrides[get_driver_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.delete("/api/v1/drivers/507f1f77bcf86cd799439011")
        assert response.status_code == 404
    finally:
        app.dependency_overrides = {}
