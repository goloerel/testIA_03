from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.api.vehicles import get_vehicle_service
from src.services.vehicle_service import VehicleService

client = TestClient(app)

def get_mock_service(mock_repo):
    return VehicleService(repository=mock_repo)

def test_list_vehicles_pagination():
    mock_repo = MagicMock()
    
    # Mock list return
    vehicles_data = [
        {
            "_id": f"507f1f77bcf86cd79943901{i}",
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
    mock_repo.list_vehicles.return_value = vehicles_data

    app.dependency_overrides[get_vehicle_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.get("/api/v1/vehicles?limit=10&offset=0")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10
        assert data[0]["placa"] == "ABC-100"

        # Verify call args
        mock_repo.list_vehicles.assert_called_with(10, 0)
    finally:
        app.dependency_overrides = {}
