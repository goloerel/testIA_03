from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

valid_vehicle_data = {
    "_id": "507f1f77bcf86cd799439011",
    "placa": "ABC-123",
    "numero_economico": "MTY-105",
    "marca": "Kenworth",
    "modelo": "T680",
    "anno": 2024,
    "tipo_vehiculo": "TRACTOR_TRUCK",
    "capacidad_carga_kg": 35000.0,
    "numero_serie": "1NKDL4XDXMP123456",
    "estado_vehiculo": "ACTIVE",
    "poliza_seguro": "QUALITAS-998877",
    "vigencia_seguro": "2027-01-29",
    "kilometraje_actual": 15000,
    "tipo_combustible": "DIESEL",
    "fecha_alta": "2024-01-01T00:00:00",
    "ultima_verificacion": None
}

def test_get_vehicle_success():
    with patch("src.services.vehicle_service.vehicle_repository") as mock_repo:
        mock_repo.get_by_id.return_value = valid_vehicle_data
        
        response = client.get("/api/v1/vehicles/507f1f77bcf86cd799439011")
        
        assert response.status_code == 200
        data = response.json()
        assert data["_id"] == "507f1f77bcf86cd799439011"
        assert data["placa"] == "ABC-123"

def test_get_vehicle_not_found():
    with patch("src.services.vehicle_service.vehicle_repository") as mock_repo:
        mock_repo.get_by_id.return_value = None
        
        response = client.get("/api/v1/vehicles/507f1f77bcf86cd799439011")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

def test_get_vehicle_invalid_id():
    response = client.get("/api/v1/vehicles/invalid-id-format")
    
    # Expect 400 Bad Request as per service logic
    assert response.status_code == 400
    assert "Invalid ID format" in response.json()["detail"]
