from fastapi import APIRouter, status, Response
from src.database import db_client

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
def perform_healthcheck(response: Response):
    try:
        # Check database connection
        db_client.connect()
        db_client.client.admin.command('ping')
        return {
            "status": "ok",
            "database": "connected"
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "detail": str(e)
        }
