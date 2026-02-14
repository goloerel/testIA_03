from fastapi import FastAPI
from src.routers import vehicles, drivers, assignments
from src.database import db_client

app = FastAPI(
    title="Fleet Management API (2026)",
    description="API for managing a vehicle fleet, drivers, and assignments.",
    version="1.0.0"
)

@app.on_event("startup")
def startup_db_client():
    db_client.connect()

@app.on_event("shutdown")
def shutdown_db_client():
    db_client.close()

app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(assignments.router)

@app.get("/")
def read_root():
    return {"message": "Fleet Management API 2026 is running"}
