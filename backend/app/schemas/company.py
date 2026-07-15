from pydantic import BaseModel, EmailStr, Field


class CompanyCreate(BaseModel):
    company_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Company name"
    )

    industry: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Industry name"
    )

    email: EmailStr


class CompanyResponse(BaseModel):
    id: int
    company_name: str
    industry: str
    email: EmailStr
    owner_id: int

    class Config:
        from_attributes = True