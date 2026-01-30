from src.services.vehicle_service import vehicle_service
from src.repositories.vehicle_repository import vehicle_repository
from datetime import datetime
import traceback

def reproduce():
    try:
        # Insert a dummy document directly to ensure we have data
        doc = {
            "placa": "TST-999",
            "numero_economico": "TST-01",
            "marca": "Test",
            "modelo": "Test",
            "anno": 2024,
            "tipo_vehiculo": "TRACTOR_TRUCK",
            "capacidad_carga_kg": 100.0,
            "numero_serie": "1NKDL4XDXMP123456",
            "estado_vehiculo": "ACTIVE",
            "poliza_seguro": "POL-1",
            "vigencia_seguro": datetime(2025, 1, 1),
            "kilometraje_actual": 100,
            "tipo_combustible": "DIESEL",
            "fecha_alta": datetime.now(),
            "ultima_verificacion": None
        }
        vehicle_repository.create(doc)
        print("Inserted test doc.")

        print("Listing vehicles...")
        result = vehicle_service.list_vehicles(10, 0)
        print("Success! Items:", len(result["items"]))
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    reproduce()
