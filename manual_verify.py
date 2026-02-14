import sys
import os
from datetime import datetime, timedelta

# Ensure src is in path
sys.path.append(os.getcwd())

from src.models.vehicle import Vehicle, VehicleType
from src.models.driver import Driver, DriverStatus
from src.models.assignment import Assignment, AssignmentStatus
from src.services.vehicle_service import vehicle_service
from src.services.driver_service import driver_service
from src.services.assignment_service import assignment_service
from src.database import db_client

def run_tests():
    print("--- Starting Manual Verification ---")
    db_client.connect()
    
    # 1. Test Vehicle Creation & Duplicate Logic
    print("\n1. Testing Vehicles...")
    v1 = Vehicle(make="Toyota", model="Corolla", year=2024, vehicle_type=VehicleType.SEDAN, fuel_type="Gas")
    try:
        vehicle_service.create_vehicle(v1)
        print("Created vehicle 1")
    except Exception as e:
        print(f"Error creating vehicle 1: {e}")

    try:
        vehicle_service.create_vehicle(v1)
        print("Error: Duplicate vehicle allowed")
    except Exception as e:
        print(f"Success: Duplicate vehicle prevented (409)")

    # 2. Test Driver Creation & License Uniqueness
    print("\n2. Testing Drivers...")
    d1 = Driver(name="Erick", email="erick@example.com", phone="123", license="LIC-001")
    try:
        driver_service.create_driver(d1)
        print("Created driver 1")
    except Exception as e:
        print(f"Error creating driver 1: {e}")

    # 3. Test Assignment Logic
    print("\n3. Testing Assignments...")
    # Driver must be INACTIVE (they are by default)
    now = datetime.now()
    a1 = Assignment(
        driver_id=d1.id, 
        vehicle_id=v1.id, 
        start_date=now - timedelta(minutes=1), # Start in past to trigger ACTIVE
        end_date=now + timedelta(hours=1),
        origin="A",
        destination="B"
    )
    
    try:
        assignment_service.create_assignment(a1)
        print("Created assignment 1 (Triggered ACTIVE)")
        
        # Check driver status
        updated_driver = db_client.get_collection("drivers").find_one({"id": str(d1.id)})
        print(f"Driver status after assignment: {updated_driver['status']}")
    except Exception as e:
        print(f"Error creating assignment 1: {e}")

    # Test Overlap for same driver
    a2 = Assignment(
        driver_id=d1.id, 
        vehicle_id=v1.id, 
        start_date=now + timedelta(minutes=30),
        end_date=now + timedelta(hours=2),
        origin="C",
        destination="D"
    )
    try:
        assignment_service.create_assignment(a2)
        print("Error: Overlap allowed")
    except Exception as e:
        print(f"Success: Overlap prevented for driver ({e.detail})")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    run_tests()
