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

def get_mock_service(mock_repo):
    return VehicleService(repository=mock_repo)

def test_create_vehicle_success():
    mock_repo = MagicMock()
    # Mock no duplicates
    mock_repo.get_by_placa.return_value = None
    mock_repo.get_by_numero_economico.return_value = None
    # Mock creation
    mock_repo.create.side_effect = lambda x: {**x, "_id": "507f1f77bcf86cd799439011"}
    
    app.dependency_overrides[get_vehicle_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.post("/api/v1/vehicles/", json=valid_vehicle_payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["placa"] == valid_vehicle_payload["placa"]
        assert "_id" in data
    finally:
        app.dependency_overrides = {}

def test_create_vehicle_duplicate_plate():
    mock_repo = MagicMock()
    # Mock duplicate plate
    mock_repo.get_by_placa.return_value = {"_id": "exists"}
    
    app.dependency_overrides[get_vehicle_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.post("/api/v1/vehicles/", json=valid_vehicle_payload)
        
        assert response.status_code == 409
        assert "license plate" in response.json()["detail"]
    finally:
        app.dependency_overrides = {}

def test_create_vehicle_duplicate_economic():
    mock_repo = MagicMock()
    # Mock no duplicate plate but duplicate economic
    mock_repo.get_by_placa.return_value = None
    mock_repo.get_by_numero_economico.return_value = {"_id": "exists"}
    
    app.dependency_overrides[get_vehicle_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.post("/api/v1/vehicles/", json=valid_vehicle_payload)
        
        assert response.status_code == 409
        assert "economic number" in response.json()["detail"]
    finally:
        app.dependency_overrides = {}
