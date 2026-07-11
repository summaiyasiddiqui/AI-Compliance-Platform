from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.company import CompanyCreate
from app.services import company_service

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


# ==========================
# GET ALL COMPANIES
# ==========================
@router.get("/")
def get_companies(db: Session = Depends(get_db)):
    return company_service.get_all_companies(db)


# ==========================
# GET COMPANY BY ID
# ==========================
@router.get("/{company_id}")
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = company_service.get_company_by_id(company_id, db)

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return company


# ==========================
# CREATE COMPANY
# ==========================
@router.post("/")
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):
    db_company = company_service.create_company(company, db)

    return {
        "message": "Company created successfully!",
        "company": db_company
    }


# ==========================
# UPDATE COMPANY
# ==========================
@router.put("/{company_id}")
def update_company(
    company_id: int,
    company: CompanyCreate,
    db: Session = Depends(get_db)
):
    db_company = company_service.update_company(
        company_id,
        company,
        db
    )

    if db_company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return {
        "message": "Company updated successfully!",
        "company": db_company
    }


# ==========================
# DELETE COMPANY
# ==========================
@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db)
):
    deleted = company_service.delete_company(
        company_id,
        db
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return {
        "message": "Company deleted successfully!"
    }