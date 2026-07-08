from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("/")
def health_check():
    return {
        "status": "Running ✅",
        "message": "ComplianceAI API is running successfully"
    }