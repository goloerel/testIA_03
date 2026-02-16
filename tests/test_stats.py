from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.api.stats import get_stats_service
from src.services.stats_service import StatsService

client = TestClient(app)

def get_mock_service(mock_v, mock_d, mock_a):
    return StatsService(
        vehicle_repository=mock_v,
        driver_repository=mock_d,
        assignment_repository=mock_a
    )

def test_get_stats():
    # Mocks
    mock_v = MagicMock()
    mock_d = MagicMock()
    mock_a = MagicMock()

    # Define return values
    mock_v.count_vehicles.return_value = 100
    mock_v.count_by_status.side_effect = lambda s: 80 if s == "ACTIVE" else 10
    
    mock_d.count_drivers.return_value = 50
    mock_d.count_by_status.return_value = 45 # Active
    
    mock_a.count_by_status.return_value = 40 # Active

    app.dependency_overrides[get_stats_service] = lambda: get_mock_service(mock_v, mock_d, mock_a)

    try:
        response = client.get("/api/v1/stats/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["vehicles_total"] == 100
        assert data["vehicles_active"] == 80
        assert data["vehicles_maintenance"] == 10
        assert data["drivers_total"] == 50
        assert data["drivers_active"] == 45
        assert data["assignments_active"] == 40
    finally:
        app.dependency_overrides = {}
