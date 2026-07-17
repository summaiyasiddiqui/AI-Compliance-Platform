from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.models.company import Company
from app.models.user import User
from math import ceil

# ==========================
# GET ALL COMPANIES
# ==========================
def get_all_companies(
    db: Session,
    current_user: User,
    search: str = None,
    industry: str = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
):
    # Base query - only return companies owned by the logged-in user
    query = (
        db.query(Company)
        .filter(Company.owner_id == current_user.id)
    )

    # Search by company name
    if search:
        query = query.filter(
            Company.company_name.ilike(f"%{search}%")
        )

    # Filter by industry
    if industry:
        query = query.filter(
            Company.industry.ilike(industry)
        )
    # Count total records BEFORE pagination
    total_records = query.count()
    total_pages = ceil(total_records / limit) if total_records > 0 else 1

    # Allowed fields for sorting
    allowed_sort_fields = {
        "id": Company.id,
        "company_name": Company.company_name,
        "industry": Company.industry,
        "email": Company.email,
    }

    # Apply sorting
    if sort_by in allowed_sort_fields:
        column = allowed_sort_fields[sort_by]

        if order.lower() == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    # Pagination
    offset = (page - 1) * limit

    query = query.offset(offset).limit(limit)

    companies = query.all()

    return {
    "companies": companies,
    "total_records": total_records,
    "current_page": page,
    "page_size": limit,
    "total_pages": total_pages,
}


# ==========================
# GET COMPANY BY ID
# ==========================
from fastapi import HTTPException

def get_company_by_id(
    company_id: int,
    db: Session,
    current_user: User
):
    company = (
        db.query(Company)
        .filter(
            Company.id == company_id,
            Company.owner_id == current_user.id
        )
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "message": "Company not found",
                "data": None,
            },
        )

    return company


# ==========================
# CREATE COMPANY
# ==========================
def create_company(
    company,
    db: Session,
    current_user: User
):
    # Check if the current user already has a company
    # with the same name
    existing_company = (
        db.query(Company)
        .filter(
            Company.company_name == company.company_name,
            Company.owner_id == current_user.id
        )
        .first()
    )

    if existing_company:
        return None

    db_company = Company(
        company_name=company.company_name,
        industry=company.industry,
        email=company.email,
        owner_id=current_user.id
    )

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


# ==========================
# UPDATE COMPANY
# ==========================
def update_company(
    company_id: int,
    company,
    db: Session,
    current_user: User
):
    db_company = get_company_by_id(
        company_id,
        db,
        current_user
    )

    if db_company is None:
        return None

    db_company.company_name = company.company_name
    db_company.industry = company.industry
    db_company.email = company.email

    db.commit()
    db.refresh(db_company)

    return db_company


# ==========================
# DELETE COMPANY
# ==========================
def delete_company(
    company_id: int,
    db: Session,
    current_user: User
):
    db_company = get_company_by_id(
        company_id,
        db,
        current_user
    )

    if db_company is None:
        return None

    db.delete(db_company)
    db.commit()

    return True