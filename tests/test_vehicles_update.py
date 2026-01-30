from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch, MagicMock
from src.schemas.vehicle import Vehicle

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
    "placa": "ABC-123", # Original plate
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

def test_update_vehicle_success():
    with patch("src.services.vehicle_service.vehicle_repository") as mock_repo:
        # 1. Get existing
        mock_repo.get_by_id.return_value = existing_vehicle_data
        
        # 2. Mock duplicate checks: Return None (no others found)
        mock_repo.get_by_placa.return_value = None
        mock_repo.get_by_numero_economico.return_value = None
        
        # 3. Mock update return
        updated_data = {**existing_vehicle_data, "kilometraje_actual": 20000}
        mock_repo.update.return_value = updated_data

        # Request to update mileage
        payload = {**valid_vehicle_payload, "kilometraje_actual": 20000}
        
        response = client.put("/api/v1/vehicles/507f1f77bcf86cd799439011", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["kilometraje_actual"] == 20000

def test_update_vehicle_not_found():
    with patch("src.services.vehicle_service.vehicle_repository") as mock_repo:
        mock_repo.get_by_id.return_value = None
        
        response = client.put("/api/v1/vehicles/507f1f77bcf86cd799439011", json=valid_vehicle_payload)
        
        assert response.status_code == 404

def test_update_vehicle_conflict_plate():
    with patch("src.services.vehicle_service.vehicle_repository") as mock_repo:
        # Existing vehicle has plate ABC-123
        mock_repo.get_by_id.return_value = existing_vehicle_data
        
        # We try to change plate to XYZ-999
        new_payload = {**valid_vehicle_payload, "placa": "XYZ-999"}
        
        # But XYZ-999 already exists!
        mock_repo.get_by_placa.return_value = {"_id": "507f1f77bcf86cd799439022"} # Different ID
        
        response = client.put("/api/v1/vehicles/507f1f77bcf86cd799439011", json=new_payload)
        
        assert response.status_code == 409
        assert "license plate" in response.json()["detail"]
