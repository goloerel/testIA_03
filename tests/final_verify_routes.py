from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch, MagicMock
from bson import ObjectId
from datetime import datetime

client = TestClient(app)

def test_full_flow():
    # We will mock repo to return valid Docs with ObjectId and datetime
    with patch("src.services.vehicle_service.vehicle_repository") as mock_repo:
        
        # 1. Test LIST
        mock_repo.count_vehicles.return_value = 1
        mock_doc = {
            "_id": ObjectId("507f1f77bcf86cd799439011"),
            "placa": "ABC-123",
            "numero_economico": "N-1",
            "marca": "M",
            "modelo": "M",
            "anno": 2024,
            "tipo_vehiculo": "TRACTOR_TRUCK",
            "capacidad_carga_kg": 100.0,
            "numero_serie": "1NKDL4XDXMP123456",
            "estado_vehiculo": "ACTIVE",
            "poliza_seguro": "P",
            "vigencia_seguro": datetime(2025, 1, 1),
            "kilometraje_actual": 100,
            "tipo_combustible": "DIESEL",
            "fecha_alta": datetime.now(),
            "ultima_verificacion": None
        }
        mock_cursor = MagicMock()
        mock_cursor.__iter__.return_value = [mock_doc]
        mock_repo.list_vehicles.return_value = mock_cursor
        
        print("Testing List...")
        res = client.get("/api/v1/vehicles")
        print("Response JSON keys:", res.json()["items"][0].keys())
        assert res.status_code == 200
        assert res.json()["items"][0]["_id"] == "507f1f77bcf86cd799439011"
        print("List passed.")

        # 2. Test GET
        mock_repo.get_by_id.return_value = mock_doc
        print("Testing Get...")
        res = client.get("/api/v1/vehicles/507f1f77bcf86cd799439011")
        assert res.status_code == 200
        print("Get passed.")
        
        # 3. Test UPDATE
        mock_repo.get_by_placa.return_value = None
        mock_repo.get_by_numero_economico.return_value = None
        mock_repo.update.return_value = mock_doc
        
        print("Testing Update...")
        payload = {
            "placa": "ABC-123",
            "numero_economico": "N-1",
            "marca": "M",
            "modelo": "M",
            "anno": 2024,
            "tipo_vehiculo": "TRACTOR_TRUCK",
            "capacidad_carga_kg": 100.0,
            "numero_serie": "1NKDL4XDXMP123456",
            "estado_vehiculo": "ACTIVE",
            "poliza_seguro": "P",
            "vigencia_seguro": "2025-01-01",
            "kilometraje_actual": 100,
            "tipo_combustible": "DIESEL"
        }
        res = client.put("/api/v1/vehicles/507f1f77bcf86cd799439011", json=payload)
        assert res.status_code == 200
        print("Update passed.")

if __name__ == "__main__":
    test_full_flow()
