from pydantic import BaseModel, EmailStr

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john@example.com"
            }
        }
    }

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john123",
                "email": "john@example.com",
                "password": "StrongPassword123",
                "role": "user"
            }
        }
    }

class UserLogin(BaseModel):
    username: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john123",
                "password": "StrongPassword123"
            }
        }
    }


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = {
    "from_attributes": True,
    "json_schema_extra": {
        "example": {
            "id": 1,
            "username": "john123",
            "email": "john@example.com",
            "role": "user"
        }
    }
}

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "token": "your-reset-token",
                "new_password": "NewStrongPassword123"
            }
        }
    }