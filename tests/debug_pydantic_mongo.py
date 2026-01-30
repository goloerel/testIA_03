from bson import ObjectId
from datetime import datetime, date
from src.schemas.vehicle import Vehicle
import traceback

def check():
    print("Checking Pydantic validation with Mongo types...")
    try:
        # Simulate doc from Mongo
        doc = {
            "_id": ObjectId(), # ObjectId
            "placa": "ABC-1234",
            "numero_economico": "MTY-105",
            "marca": "Kenworth",
            "modelo": "T680",
            "anno": 2024,
            "tipo_vehiculo": "TRACTOR_TRUCK",
            "capacidad_carga_kg": 35000.0,
            "numero_serie": "1NKDL4XDXMP123456",
            "estado_vehiculo": "ACTIVE",
            "poliza_seguro": "QUALITAS-998877",
            "vigencia_seguro": datetime(2027, 1, 29, 0, 0), # Datetime from mongo
            "kilometraje_actual": 15000,
            "tipo_combustible": "DIESEL",
            "fecha_alta": datetime.now(),
            "ultima_verificacion": None
        }

        v = Vehicle(**doc)
        print("Success! Created Vehicle:", v.id)
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    check()
