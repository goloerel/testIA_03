from fastapi.testclient import TestClient
from src.main import app
from src.services.vehicle_service import vehicle_service
from unittest.mock import patch, MagicMock

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

def test_create_vehicle_success():
    with patch("src.services.vehicle_service.vehicle_repository") as mock_repo:
        # Mock no duplicates
        mock_repo.get_by_placa.return_value = None
        mock_repo.get_by_numero_economico.return_value = None
        
        # Mock creation
        mock_repo.create.side_effect = lambda x: {**x, "_id": "507f1f77bcf86cd799439011"}

        response = client.post("/api/v1/vehicles/", json=valid_vehicle_payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["placa"] == valid_vehicle_payload["placa"]
        assert "_id" in data

def test_create_vehicle_duplicate_plate():
    with patch("src.services.vehicle_service.vehicle_repository") as mock_repo:
        # Mock duplicate plate
        mock_repo.get_by_placa.return_value = {"_id": "exists"}

        response = client.post("/api/v1/vehicles/", json=valid_vehicle_payload)
        
        assert response.status_code == 409
        assert "license plate" in response.json()["detail"]

def test_create_vehicle_duplicate_economic():
    with patch("src.services.vehicle_service.vehicle_repository") as mock_repo:
        # Mock no duplicate plate but duplicate economic
        mock_repo.get_by_placa.return_value = None
        mock_repo.get_by_numero_economico.return_value = {"_id": "exists"}

        response = client.post("/api/v1/vehicles/", json=valid_vehicle_payload)
        
        assert response.status_code == 409
        assert "economic number" in response.json()["detail"]
