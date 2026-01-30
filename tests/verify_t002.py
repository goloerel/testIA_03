
from src.database import db_client
from src.schemas.vehicle import VehicleInput, VehicleType, VehicleStatus, FuelType
from pydantic import ValidationError
import datetime

def test_connection():
    try:
        db_client.connect()
        # Simple command to check connection
        db_client.client.admin.command('ping')
        print("PASS: MongoDB Connection Successful")
    except Exception as e:
        print(f"FAIL: MongoDB Connection Failed - {e}")

def test_valid_vehicle():
    try:
        v = VehicleInput(
            placa="ABC-1234",
            numero_economico="MTY-105",
            marca="Kenworth",
            modelo="T680",
            anno=2024,
            tipo_vehiculo=VehicleType.TRACTOR_TRUCK,
            capacidad_carga_kg=35000.0,
            numero_serie="1NKDL4XDXMP123456",
            estado_vehiculo=VehicleStatus.ACTIVE,
            poliza_seguro="QUALITAS-998877",
            vigencia_seguro=datetime.date(2027, 1, 29),
            kilometraje_actual=15000,
            tipo_combustible=FuelType.DIESEL
        )
        print("PASS: Valid Vehicle Schema")
    except ValidationError as e:
        print(f"FAIL: Valid Vehicle Schema Rejected - {e}")

def test_invalid_license_plate():
    try:
        VehicleInput(
            placa="INVALID-PLATE", # Too long
            numero_economico="MTY-105",
            marca="Kenworth",
            modelo="T680",
            anno=2024,
            tipo_vehiculo=VehicleType.TRACTOR_TRUCK,
            capacidad_carga_kg=35000.0,
            numero_serie="1NKDL4XDXMP123456",
            estado_vehiculo=VehicleStatus.ACTIVE,
            poliza_seguro="QUALITAS-998877",
            vigencia_seguro=datetime.date(2027, 1, 29),
            kilometraje_actual=15000,
            tipo_combustible=FuelType.DIESEL
        )
        print("FAIL: Invalid License Plate Accepted")
    except ValidationError:
        print("PASS: Invalid License Plate Rejected")

if __name__ == "__main__":
    test_connection()
    test_valid_vehicle()
    test_invalid_license_plate()
