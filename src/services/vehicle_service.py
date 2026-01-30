from datetime import datetime, timezone
from typing import Dict
from fastapi import HTTPException, status
from src.repositories.vehicle_repository import vehicle_repository
from src.schemas.vehicle import VehicleInput, Vehicle

class VehicleService:
    def create_vehicle(self, vehicle_input: VehicleInput) -> Vehicle:
        # Business Logic: Check duplicates
        if vehicle_repository.get_by_placa(vehicle_input.placa):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Vehicle with license plate {vehicle_input.placa} already exists."
            )
        
        if vehicle_repository.get_by_numero_economico(vehicle_input.numero_economico):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Vehicle with economic number {vehicle_input.numero_economico} already exists."
            )

        # Prepare data for insertion
        vehicle_data = vehicle_input.model_dump()
        # Convert date to datetime for MongoDB BSON compatibility
        vehicle_data["vigencia_seguro"] = datetime.combine(vehicle_input.vigencia_seguro, datetime.min.time())
        
        vehicle_data["fecha_alta"] = datetime.now(timezone.utc)
        vehicle_data["ultima_verificacion"] = None

        # Persist
        created_vehicle = vehicle_repository.create(vehicle_data)
        
        return Vehicle(**created_vehicle)

    def list_vehicles(self, limit: int, offset: int) -> Dict:
        total = vehicle_repository.count_vehicles()
        cursor = vehicle_repository.list_vehicles(limit, offset)
        items = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            items.append(Vehicle(**doc))
            
        return {
            "total": total,
            "items": items
        }

    def get_vehicle(self, vehicle_id: str) -> Vehicle:
        # Validate ObjectId format? Pydantic/FastAPI might handle it if we type hint strict, 
        # but here we deal with string. Repository converts.
        # Check valid format first or let PyMongo fail? 
        # Ideally check valid ObjectId before calling DB to avoid server error 500 on bad ID.
        try:
            from bson import ObjectId
            if not ObjectId.is_valid(vehicle_id):
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
        except Exception:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

        vehicle_data = vehicle_repository.get_by_id(vehicle_id)
        if not vehicle_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with id {vehicle_id} not found"
            )
        vehicle_data["_id"] = str(vehicle_data["_id"])
        return Vehicle(**vehicle_data)

    def update_vehicle(self, vehicle_id: str, vehicle_input: VehicleInput) -> Vehicle:
        # 1. Check if vehicle exists
        # We can reuse get_vehicle logic or just call repo.get_by_id to avoid overhead of creating Vehicle object just to throw it away.
        # However, we need to handle invalid ID format too.
        existing_vehicle = self.get_vehicle(vehicle_id) # Raises 404/400 if needed

        # 2. Check duplicates if fields changed
        if vehicle_input.placa != existing_vehicle.placa:
             if vehicle_repository.get_by_placa(vehicle_input.placa):
                 raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Vehicle with license plate {vehicle_input.placa} already exists.")
        
        if vehicle_input.numero_economico != existing_vehicle.numero_economico:
             if vehicle_repository.get_by_numero_economico(vehicle_input.numero_economico):
                 raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Vehicle with economic number {vehicle_input.numero_economico} already exists.")

        # 3. Update
        vehicle_data = vehicle_input.model_dump()
        # Convert date to datetime for MongoDB BSON compatibility
        vehicle_data["vigencia_seguro"] = datetime.combine(vehicle_input.vigencia_seguro, datetime.min.time())
        
        # Keep original metadata that shouldn't change or handle it via logic
        # For now, we overwrite fields but preserve _id (handled by repo query)
        # Maybe we want to update ultima_verificacion? The spec said "allow updating fields".
        # Let's preserve fecha_alta from original.
        vehicle_data["fecha_alta"] = existing_vehicle.fecha_alta
        vehicle_data["ultima_verificacion"] = datetime.now(timezone.utc) # Update verification timestamp? Or just updated_at?
        # Spec says: "El sistema debe permitir actualizar solo el campo de estado y registrar la última fecha de verificación." -> History 3
        # But also "CRUD Completo". So general update. Let's update ultima_verificacion if status changes? or always? 
        # Let's just pass data for now.

        updated_doc = vehicle_repository.update(vehicle_id, vehicle_data)
        updated_doc["_id"] = str(updated_doc["_id"])
        return Vehicle(**updated_doc)

    def delete_vehicle(self, vehicle_id: str):
        # 1. Check ID format (optional but good practice)
        try:
            from bson import ObjectId
            if not ObjectId.is_valid(vehicle_id):
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
        except Exception:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

        # 2. Attempt delete
        if not vehicle_repository.delete(vehicle_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with id {vehicle_id} not found"
            )

vehicle_service = VehicleService()
