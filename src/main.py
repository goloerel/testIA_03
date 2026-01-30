from fastapi import FastAPI
from src.routes import health, vehicles

app = FastAPI(
    title="Vehicle Inventory API",
    description="API for managing the vehicle fleet inventory.",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(vehicles.router)

@app.get("/")
def read_root():
    return {"message": "Fleet Management API"}
