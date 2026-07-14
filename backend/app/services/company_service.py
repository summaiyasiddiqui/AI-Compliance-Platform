from sqlalchemy.orm import Session
from app.models.company import Company
from app.models.user import User


# ==========================
# GET ALL COMPANIES
# ==========================
def get_all_companies(
    db: Session,
    current_user: User
):
    return (
        db.query(Company)
        .filter(Company.owner_id == current_user.id)
        .all()
    )


# ==========================
# GET COMPANY BY ID
# ==========================
def get_company_by_id(company_id: int, db: Session):
    return db.query(Company).filter(
        Company.id == company_id
    ).first()


# ==========================
# CREATE COMPANY
# ==========================
def create_company(
    company,
    db: Session,
    current_user: User
):
    print("Current user:", current_user)
    print("Current user ID:", current_user.id)

    db_company = Company(
        company_name=company.company_name,
        industry=company.industry,
        email=company.email,
        owner_id=current_user.id
    )

    print("Owner ID being saved:", db_company.owner_id)

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


# ==========================
# UPDATE COMPANY
# ==========================
def update_company(company_id: int, company, db: Session):
    db_company = get_company_by_id(company_id, db)

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
def delete_company(company_id: int, db: Session):
    db_company = get_company_by_id(company_id, db)

    if db_company is None:
        return None

    db.delete(db_company)
    db.commit()

    return True