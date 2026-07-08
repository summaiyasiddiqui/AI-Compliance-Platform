from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.about import router as about_router
from app.api.company import router as company_router
app = FastAPI(
    title="ComplianceAI API",
    description="AI-powered Compliance Management Platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "project": "ComplianceAI",
        "version": "1.0.0",
        "developer": "Summaiya Nadeem",
        "message": "Welcome to ComplianceAI API!"
    }

app.include_router(health_router)
app.include_router(about_router)
app.include_router(company_router)