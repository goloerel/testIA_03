from fastapi.testclient import TestClient
from src.main import app
from src.services.vehicle_service import vehicle_service
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_list_vehicles_pagination():
    with patch("src.services.vehicle_service.vehicle_repository") as mock_repo:
        # Mock total count
        mock_repo.count_vehicles.return_value = 50
        
        # Mock list return
        mock_cursor = MagicMock()
        mock_cursor.__iter__.return_value = [
            {
                "_id": f"id_{i}",
                "placa": f"ABC-10{i}",
                "numero_economico": f"ECON-{i}",
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
            } for i in range(10)
        ]
        mock_repo.list_vehicles.return_value = mock_cursor

        response = client.get("/api/v1/vehicles?limit=10&offset=0")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 50
        assert len(data["items"]) == 10
        assert data["items"][0]["placa"] == "ABC-100"

        # Verify call args
        mock_repo.list_vehicles.assert_called_with(10, 0)
