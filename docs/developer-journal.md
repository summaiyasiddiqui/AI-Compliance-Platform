# AI Compliance Platform

# 👩‍💻 Developer Journal

---

## Day 1 — July 6, 2026

### Goals

- [x] Create project folder
- [x] Install Python
- [x] Install Node.js
- [x] Install Git
- [x] Configure VS Code
- [ ] Create GitHub Repository
- [ ] Learn Git Basics

---

## What I Learned

Today I set up my development environment and created the project structure.

---

## Problems I Faced

- npm execution policy error
- Issue opening developer-journal.md

---

## How I Solved Them

(I deleted the file developer-journal.md from my docs and created it again in vs code.)

---

## Questions

Who are the users of ComplianceAI?
hospitals,schools,restaurants,universities


What problems does it solve?
it provides a dashboard which becomes the company's control room ,instead of reading files,management immediately knows where attention is needed

Why does it need AI?
Today, most companies manage compliance like this:

Excel Sheets

↓

Folders

↓

PDF Files

↓

WhatsApp

↓

Emails

Everything is scattered.

When an auditor visits, employees spend hours searching for documents.

Sometimes they can't even find them.

Our Solution

Instead of manually checking everything...

The company uploads documents into our platform.

Upload Documents

↓

AI Reads Everything

↓

AI Organizes Everything

↓

AI Finds Missing Documents

↓

AI Detects Risks

↓

Dashboard

↓

Reports

↓

Audit Ready

The company can see everything from one dashboard.

Describe ComplianceAI in one paragraph.
AI Compliance Management Platform is an AI-powered solution that helps organizations manage compliance documents, inspections, certifications, and audits from a single platform. Instead of manually tracking PDFs, Excel sheets, and reports, users upload their documents, and AI automatically extracts key information, identifies expired or missing certificates, detects compliance risks, sends reminders for upcoming deadlines, and generates audit-ready reports. The platform enables factories, hospitals, schools, universities, and other organizations to stay compliant, reduce manual work, avoid penalties, and make smarter, data-driven decisions through intelligent automation.

# Day 2 - Project Setup & Development Environment

**Date:** July 7, 2026

## Objective
Set up a professional development environment for the AI Compliance Platform and understand the project structure.
Learnt abt cmd and its commands 
reated the backend scaffold with:
  - app/
  - tests/
  - README.md
  - requirements.txt
- Created and activated a Python virtual environment (venv).
- Learned the purpose of virtual environments and why they isolate project dependencies.
- Created a `.gitignore` file to exclude unnecessary files like `venv`, cache files, and environment variables.
- Initialized Git locally using `git init`.
- Connected the local project to the GitHub repository.
- Successfully made and pushed the first commit to GitHub.
## New Concepts Learned
- Difference between Git and GitHub.
- Purpose of a virtual environment.
- Why every Python project should have a `requirements.txt`.
- Importance of `.gitignore`.
- Basic Git workflow:
  - git init
  - git status
  - git add
  - git commit
  - git push
## Challenges Faced
- Received the error:
  "fatal: not a git repository."
- Learned that creating a repository on GitHub does not automatically initialize Git locally.
- Solved the issue by initializing Git inside the project folder and connecting it to the remote repository.

## Key Takeaways
Today helped me understand how professional software projects are organized before any code is written. I learned that a clean project structure, version control, and isolated development environments are essential for building scalable applications.

## Reflection
Today's session made me feel much more comfortable with Git and project setup. Initially, Git seemed confusing, but after resolving the repository issue and successfully pushing my first commit, I gained confidence. I now understand why developers use virtual environments and how a well-organized project structure makes future development easier.

# Day 3

## What I learned
- Created my first FastAPI application.
- Understood what an API endpoint is.
- Ran a backend server using Uvicorn.
- Explored Swagger UI documentation.
- Learned that `--reload` automatically restarts the server.

## Biggest challenge
- Accidentally installed packages globally instead of in the virtual environment.
- Learned how to activate the virtual environment and use `python -m pip`.

## Reflection
Today was the first time I saw my own backend running in a browser. It made the project feel real.


# Day 4
## What I learned
Learned what APIRouter is and why it is used in FastAPI.
Understood how to organize API endpoints into separate router files instead of keeping everything in main.py.
Created my first router (health.py) and connected it to the application using app.include_router().
Learned the purpose of prefix and tags in routers.
Explored how Swagger UI automatically groups endpoints based on router tags.
## Biggest challenge
Encountered a ModuleNotFoundError while importing my router.
Discovered that the issue was caused by naming my file healthy.py instead of health.py and initially running the project from the wrong directory.
Fixed the file name, ran Uvicorn from the backend folder, and successfully started the application.
## Reflection
Today was my first experience building a modular FastAPI application instead of keeping everything in one file. Although I faced import errors, debugging them helped me better understand Python modules and project structure. Seeing both my Home and Health endpoints working in Swagger made me feel like I was building a real backend application.
# Day 5

## What I learned
- Learned what Pydantic schemas are and why they are used in FastAPI.
- Created my first schema (`CompanyCreate`) to validate incoming request data.
- Understood the difference between request schemas and response schemas.
- Built my first POST endpoint using `APIRouter`.
- Tested API requests and automatic validation using Swagger UI.

## Biggest challenge
- Initially struggled to understand the purpose of the `schemas` folder and why we use `CompanyCreate` instead of a simple `Company` class.
- After understanding request validation and how FastAPI uses schemas before executing the endpoint, the concept became much clearer.

## Reflection
Today my API became interactive. Instead of only returning data, it now accepts user input and validates it automatically using Pydantic. Seeing FastAPI return a `422 Unprocessable Entity` error when required data was missing helped me understand how request validation works behind the scenes. I feel much more confident about building structured APIs now.