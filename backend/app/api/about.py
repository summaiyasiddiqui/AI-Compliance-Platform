from fastapi import APIRouter

router = APIRouter(
    prefix="/about",
    tags=["About"]
)

@router.get("/")
def about():
    return {
        "project": "ComplianceAI",
        "developer": "Summaiya Nadeem",
        "version": "1.0.0",
        "description": "AI-powered Compliance Management Platform"
    }