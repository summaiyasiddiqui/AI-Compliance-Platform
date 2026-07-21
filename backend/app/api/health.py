from fastapi import APIRouter
from app.logger import logger 

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("/")
def health_check():

    logger.info("Health endpoint accessed")

    return {
        "status": "Running ✅",
        "message": "ComplianceAI API is running successfully"
    }