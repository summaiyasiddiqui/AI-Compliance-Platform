from app.config import settings
from app.logger import logger
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def health_check():

    logger.info("Health endpoint accessed")

    return {
        "status": "healthy",
        "message": "ComplianceAI API is running successfully",
        "environment": settings.environment,
        "version": "1.0.0",
    }
