from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.api.drivers import get_driver_service
from src.services.driver_service import DriverService

client = TestClient(app)

def get_mock_service(mock_repo):
    return DriverService(repository=mock_repo)

def test_list_drivers():
    mock_repo = MagicMock()
    
    drivers_data = [
        {
            "_id": f"507f1f77bcf86cd79943901{i}",
            "nombre": f"Driver {i}",
            "licencia": f"MX-DL-{i}",
            "estado": "ACTIVE",
            "fecha_contratacion": "2024-01-15",
            "fecha_creacion": "2024-01-15T10:00:00"
        } for i in range(5)
    ]
    mock_repo.list_drivers.return_value = drivers_data

    app.dependency_overrides[get_driver_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.get("/api/v1/drivers?limit=5&offset=0")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        assert data[0]["nombre"] == "Driver 0"
    finally:
        app.dependency_overrides = {}
