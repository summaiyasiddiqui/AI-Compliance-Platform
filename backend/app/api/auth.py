from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.security import hash_password, verify_password
from app.auth import create_access_token
from app.dependencies import get_current_user
from app.logger import logger
import secrets
from datetime import datetime, timedelta
from app.schemas.user import ForgotPasswordRequest, ResetPasswordRequest
from app.email_service import send_email

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# -----------------------------
# Register User
# -----------------------------
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    existing_email = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    background_tasks.add_task(
    send_welcome_email,
    new_user.email,
    new_user.username
)


    return new_user


# -----------------------------
# Login User
# -----------------------------

@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(
        f"Login attempt for username: {form_data.username}"
    )

    db_user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not db_user:
        logger.warning(
            f"Failed login attempt for username: {form_data.username}"
        )
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        db_user.hashed_password
    ):
        logger.warning(
            f"Failed login attempt for username: {form_data.username}"
        )
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": db_user.username}
    )

    logger.info(
        f"User logged in successfully: {db_user.username}"
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
   
# -----------------------------
# Current Logged-in User
# -----------------------------
@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    print("Received email:", repr(request.email))

    user = db.query(User).filter(User.email == request.email).first()

    print("User found:", user)

    if not user:
        return {
            "message": "If an account with that email exists, a password reset link has been sent."
        }

    token = secrets.token_urlsafe(32)

    user.reset_token = token
    user.reset_token_expires = datetime.utcnow() + timedelta(minutes=15)

    db.commit()

    reset_link = f"http://localhost:3000/reset-password?token={token}"

    subject = "Reset Your ComplianceAI Password"

    body = f"""
Hello {user.username},

We received a request to reset your password.

Click the link below:

{reset_link}

This link expires in 15 minutes.

If you didn't request this, simply ignore this email.

- ComplianceAI Team
"""

    send_email(
        to_email=user.email,
        subject=subject,
        body=body
    )

    return {
        "message": "If an account with that email exists, a password reset link has been sent."
    
    }
@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.reset_token == request.token
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token."
        )

    if user.reset_token_expires < datetime.utcnow():
        raise HTTPException(
        status_code=400,
        detail="Reset token has expired."
    )
   # Update the password
    user.hashed_password = hash_password(request.new_password)

    # Invalidate the token
    user.reset_token = None
    user.reset_token_expires = None

    # Save everything
    db.commit()

    return {
        "message": "Password has been reset successfully."
    }