from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.api.vehicles import get_vehicle_service
from src.services.vehicle_service import VehicleService

client = TestClient(app)

valid_vehicle_payload = {
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
    "tipo_combustible": "DIESEL"
}

existing_vehicle_data = {
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
    "poliza_seguro": "qualitas-old",
    "vigencia_seguro": "2027-01-29",
    "kilometraje_actual": 10000,
    "tipo_combustible": "DIESEL",
    "fecha_alta": "2024-01-01T00:00:00",
    "ultima_verificacion": None
}

def get_mock_service(mock_repo):
    return VehicleService(repository=mock_repo)

def test_update_vehicle_success():
    mock_repo = MagicMock()
    # 1. Get existing
    mock_repo.get_by_id.return_value = existing_vehicle_data
    # 2. Mock update return
    updated_data = {**existing_vehicle_data, "kilometraje_actual": 20000}
    mock_repo.update.return_value = updated_data
    
    app.dependency_overrides[get_vehicle_service] = lambda: get_mock_service(mock_repo)

    try:
        # Request to update mileage
        payload = {**valid_vehicle_payload, "kilometraje_actual": 20000}
        
        response = client.put("/api/v1/vehicles/507f1f77bcf86cd799439011", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["kilometraje_actual"] == 20000
    finally:
        app.dependency_overrides = {}

def test_update_vehicle_not_found():
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = None
    
    app.dependency_overrides[get_vehicle_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.put("/api/v1/vehicles/507f1f77bcf86cd799439011", json=valid_vehicle_payload)
        
        assert response.status_code == 404
    finally:
        app.dependency_overrides = {}
