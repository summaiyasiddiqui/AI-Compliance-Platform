from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.about import router as about_router
from app.api.ready import router as ready_router
from app.limiter import limiter
from slowapi.errors import RateLimitExceeded
from app.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    rate_limit_exception_handler,
)
from fastapi.middleware.cors import CORSMiddleware
from app.api.company import router as company_router
from app.api.auth import router as auth_router
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from app.middleware import (
    LoggingMiddleware,
    SecurityHeadersMiddleware,
)

app = FastAPI(
    title="ComplianceAI API",
    description="""
## ComplianceAI Backend API

ComplianceAI is an AI-powered Compliance Management Platform designed to help organizations manage compliance requirements efficiently.

### Features
- 🔐 JWT Authentication
- 🔄 Refresh Token Authentication
- 👤 Role-Based Access Control (RBAC)
- 🏢 Company Management
- 📧 Email Notifications
- 🔑 Password Reset
- 🚦 Rate Limiting
- 📝 Structured API Responses
- 📊 OpenAPI Documentation

Built using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Docker**.
""",
    version="1.0.0",
    contact={
        "name": "Summaiya Nadeem",
        "email": "summaiyanadeem002@gmail.com",
    },
    license_info={
        "name": "MIT License",
    },
    terms_of_service="https://example.com/terms",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React (Create React App)
        "http://localhost:5173",  # React (Vite)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter

app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)


@app.get(
    "/",
    summary="API Home",
    description="Returns basic information about the ComplianceAI API.",
)
def home():
    return {
        "project": "ComplianceAI",
        "version": "1.0.0",
        "developer": "Summaiya Nadeem",
        "message": "Welcome to ComplianceAI API!",
    }


app.include_router(health_router)
app.include_router(about_router)
app.include_router(company_router)
app.include_router(auth_router)
app.include_router(ready_router)
