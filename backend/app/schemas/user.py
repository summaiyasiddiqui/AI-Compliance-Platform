from pydantic import BaseModel, EmailStr, Field, field_validator


def validate_password_strength(password: str) -> str:
    if password != password.strip():
        raise ValueError("Password must not contain leading or trailing whitespace.")

    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters long.")

    if not any(char.isalpha() for char in password):
        raise ValueError("Password must contain at least one letter.")

    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one number.")

    return password


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    model_config = {"json_schema_extra": {"example": {"email": "john@example.com"}}}


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=12)
    role: str = "user"

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        return validate_password_strength(password)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john123",
                "email": "john@example.com",
                "password": "StrongPassword123",
                "role": "user",
            }
        }
    }


class UserLogin(BaseModel):
    username: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {"username": "john123", "password": "StrongPassword123"}
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
                "role": "user",
            }
        },
    }


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=12)

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, password: str) -> str:
        return validate_password_strength(password)

    model_config = {
        "json_schema_extra": {
            "example": {
                "token": "your-reset-token",
                "new_password": "NewStrongPassword123",
            }
        }
    }