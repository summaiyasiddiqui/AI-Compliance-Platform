from fastapi import FastAPI

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
        "status": "Running ✅",
        "developer": "Summaiya Nadeem",
        "message": "Welcome to ComplianceAI API!"
    }