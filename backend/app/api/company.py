from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.company import CompanyCreate, CompanyResponse
from app.services import company_service
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


# ==========================
# GET ALL COMPANIES
# ==========================
@router.get("/", response_model=list[CompanyResponse])
def get_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return company_service.get_all_companies(
        db,
        current_user
    )


# ==========================
# GET COMPANY BY ID
# ==========================
@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = company_service.get_company_by_id(
        company_id,
        db,
        current_user
    )

    if company is None:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this company."
        )

    return company


# ==========================
# CREATE COMPANY
# ==========================
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_company = company_service.create_company(
        company,
        db,
        current_user
    )

    if db_company is None:
        raise HTTPException(
            status_code=400,
            detail="You already have a company with this name."
        )

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_company = company_service.update_company(
        company_id,
        company,
        db,
        current_user
    )

    if db_company is None:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to update this company."
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = company_service.delete_company(
        company_id,
        db,
        current_user
    )

    if not deleted:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to delete this company."
        )

    return {
        "message": "Company deleted successfully!"
    }