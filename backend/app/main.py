from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from slowapi.errors import RateLimitExceeded

from app.api.about import router as about_router
from app.api.auth import router as auth_router
from app.api.company import router as company_router
from app.api.health import router as health_router
from app.api.ready import router as ready_router
from app.config import settings
from app.exceptions import (
    general_exception_handler,
    http_exception_handler,
    rate_limit_exception_handler,
    validation_exception_handler,
)
from app.limiter import limiter
from app.middleware import LoggingMiddleware, SecurityHeadersMiddleware

app = FastAPI(
    title="ComplianceAI API",
    description="""
## ComplianceAI Backend API

ComplianceAI is an AI-powered Compliance Management Platform designed to help organizations manage compliance requirements efficiently.

### Core Features

- Company management
- User authentication and authorization
- JWT access and refresh tokens
- Password reset
- Email notifications
- Rate limiting
- Health and readiness monitoring
- Secure error handling

### Authentication

Protected endpoints require a valid JWT access token.

Use the **Authorize** button in Swagger UI to provide your bearer token.

### API Reliability

The API provides consistent error responses for validation errors,
authentication failures, rate limiting, database failures, and unexpected
server exceptions.
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
allowed_hosts = [
    host.strip()
    for host in settings.allowed_hosts.split(",")
    if host.strip()
]

# TestClient uses "testserver" as the default Host header.
# Allow it only outside production.
if settings.environment.lower() != "production":
    allowed_hosts.append("testserver")

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=allowed_hosts,
)
app.state.limiter = limiter

app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

@app.get(
    "/",
    tags=["System"],
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
