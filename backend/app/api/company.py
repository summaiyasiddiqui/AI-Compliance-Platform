from fastapi import APIRouter
from app.schemas.company import CompanyCreate

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

@router.post("/")
def create_company(company: CompanyCreate):
    return {
        "message": "Company created successfully!",
        "company": company
    }