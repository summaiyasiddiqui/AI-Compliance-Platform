from pydantic import BaseModel

class CompanyCreate(BaseModel):
    company_name: str
    industry: str
    email: str