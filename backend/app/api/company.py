from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


# ==========================
# GET ALL COMPANIES
# ==========================
@router.get("/")
def get_companies(db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    return companies


# ==========================
# GET COMPANY BY ID
# ==========================
@router.get("/{company_id}")
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()

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
    db_company = Company(
        company_name=company.company_name,
        industry=company.industry,
        email=company.email
    )

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

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
    db_company = db.query(Company).filter(Company.id == company_id).first()

    if db_company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    db_company.company_name = company.company_name
    db_company.industry = company.industry
    db_company.email = company.email

    db.commit()
    db.refresh(db_company)

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
    db_company = db.query(Company).filter(Company.id == company_id).first()

    if db_company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    db.delete(db_company)
    db.commit()

    return {
        "message": "Company deleted successfully!"
    }