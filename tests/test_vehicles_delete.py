from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch

client = TestClient(app)

def test_delete_vehicle_success():
    with patch("src.services.vehicle_service.vehicle_repository") as mock_repo:
        # Mock successful delete (return True)
        mock_repo.delete.return_value = True
        
        response = client.delete("/api/v1/vehicles/507f1f77bcf86cd799439011")
        
        assert response.status_code == 204
        # 204 has no content

def test_delete_vehicle_not_found():
    with patch("src.services.vehicle_service.vehicle_repository") as mock_repo:
        # Mock failed delete (return False)
        mock_repo.delete.return_value = False
        
        response = client.delete("/api/v1/vehicles/507f1f77bcf86cd799439011")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

def test_delete_vehicle_invalid_id():
    response = client.delete("/api/v1/vehicles/invalid-id")
    assert response.status_code == 400
    assert "Invalid ID format" in response.json()["detail"]
