from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.database import db_client
from src.api import vehicles, health, drivers, assignments, stats

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db_client.connect()
    yield
    # Shutdown
    db_client.close()

app = FastAPI(
    title="Fleet Management API",
    description="API for managing vehicle fleet inventory",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(assignments.router)
app.include_router(stats.router)
app.include_router(health.router)

@app.get("/api")
def api_root():
    return {"message": "Fleet Management API 2026 is running"}

# Mount static files (frontend) - must be last
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
