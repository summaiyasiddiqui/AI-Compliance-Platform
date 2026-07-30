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

    model_config = {
        "json_schema_extra": {
            "example": {
                "company_name": "Tech Solutions Ltd",
                "industry": "Information Technology",
                "email": "contact@techsolutions.com"
            }
        }
    }


class CompanyResponse(BaseModel):
    id: int
    company_name: str
    industry: str
    email: EmailStr
    owner_id: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "company_name": "Tech Solutions Ltd",
                "industry": "Information Technology",
                "email": "contact@techsolutions.com",
                "owner_id": 5
            }
        }
    }