from fastapi import APIRouter, HTTPException
from app.schemas.company import CompanyCreate

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

companies = []


@router.get("/")
def get_companies():
    return companies


@router.get("/{company_id}")
def get_company(company_id: int):

    if company_id >= len(companies):
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return companies[company_id]


@router.post("/")
def create_company(company: CompanyCreate):

    new_company = {
        "id": len(companies),
        "company_name": company.company_name,
        "industry": company.industry,
        "email": company.email
    }

    companies.append(new_company)

    return {
        "message": "Company created successfully!",
        "company": new_company
    }


@router.put("/{company_id}")
def update_company(company_id: int, company: CompanyCreate):

    if company_id >= len(companies):
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    updated_company = {
        "id": company_id,
        "company_name": company.company_name,
        "industry": company.industry,
        "email": company.email
    }

    companies[company_id] = updated_company

    return {
        "message": "Company updated successfully!",
        "company": updated_company
    }


@router.delete("/{company_id}")
def delete_company(company_id: int):

    if company_id >= len(companies):
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    deleted = companies.pop(company_id)

    return {
        "message": "Company deleted successfully!",
        "company": deleted
    }