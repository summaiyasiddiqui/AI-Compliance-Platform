import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.admin import require_admin
from app.auth import create_access_token, create_refresh_token, decode_refresh_token
from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.email_service import send_email, send_welcome_email
from app.limiter import limiter
from app.logger import logger
from app.models.user import User
from app.schemas.refresh_token import RefreshTokenRequest
from app.schemas.token import Token
from app.schemas.user import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    UserCreate,
    UserResponse,
)
from app.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])
LOGIN_RATE_LIMIT = "5/minute" if settings.environment == "production" else "1000/minute"


# -----------------------------
# Register User
# -----------------------------
@router.post(
    "/register",
    summary="Register a new user",
    description="Creates a new user account with a unique username and email address.",
    response_model=UserResponse,
    status_code=201,
    responses={
        201: {"description": "User registered successfully"},
        400: {"description": "Username or email already exists"},
        500: {"description": "Internal server error"},
    },
)
def register_user(
    user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = db.query(User).filter(User.email == user.email).first()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    background_tasks.add_task(send_welcome_email, new_user.email, new_user.username)

    return new_user


# -----------------------------
# Login User
# -----------------------------


@router.post(
    "/login",
    summary="Authenticate a user",
    description="Authenticates the user and returns an access token and refresh token.",
    response_model=Token,
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Invalid username or password"},
        429: {"description": "Too many login attempts"},
    },
)
@limiter.limit(LOGIN_RATE_LIMIT)
def login_user(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    logger.info(f"Login attempt for username: {form_data.username}")

    db_user = db.query(User).filter(User.username == form_data.username).first()

    if not db_user:
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(form_data.password, db_user.hashed_password):
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": db_user.username})

    refresh_token = create_refresh_token(data={"sub": db_user.username})
    db_user.refresh_token = refresh_token
    db.commit()

    logger.info(f"User logged in successfully: {db_user.username}")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# -----------------------------
# Refresh Access Token
# -----------------------------
@router.post(
    "/refresh",
    summary="Generate a new access token",
    description="Validates the refresh token and issues a new access token and refresh token.",
    response_model=Token,
    responses={
        200: {"description": "New access token generated"},
        401: {"description": "Invalid or revoked refresh token"},
    },
)
@limiter.limit("10/minute")
def refresh_access_token(
    request: Request,
    refresh_request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    payload = decode_refresh_token(refresh_request.refresh_token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    username = payload.get("sub")

    db_user = db.query(User).filter(User.username == username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")

    if db_user.refresh_token != refresh_request.refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token has been revoked")

    new_access_token = create_access_token(data={"sub": db_user.username})

    new_refresh_token = create_refresh_token(data={"sub": db_user.username})

    db_user.refresh_token = new_refresh_token
    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


# -----------------------------
# Refresh logout
# -----------------------------


@router.post(
    "/logout",
    summary="Logout the current user",
    description="Logs out the authenticated user by revoking the stored refresh token.",
    responses={
        200: {"description": "User logged out successfully"},
        401: {"description": "Authentication required"},
    },
)
def logout(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    current_user.refresh_token = None
    db.commit()

    logger.info(f"User logged out: {current_user.username}")

    return {"message": "Logged out successfully."}


# -----------------------------
# Current Logged-in User
# -----------------------------
@router.get(
    "/me",
    summary="Get the current user",
    description="Returns the profile information of the currently authenticated user.",
    response_model=UserResponse,
    responses={
        200: {"description": "Current user profile returned"},
        401: {"description": "Authentication required"},
    },
)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# -----------------------------
# forget password
# -----------------------------


@router.post(
    "/forgot-password",
    summary="Request a password reset",
    description="Sends a password reset link to the user's email if an account exists.",
    responses={
        200: {"description": "Password reset email processed"},
        429: {"description": "Too many password reset requests"},
    },
)
@limiter.limit("3/minute")
def forgot_password(
    request: Request,
    forgot_request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    print("Received email:", repr(forgot_request.email))

    user = db.query(User).filter(User.email == forgot_request.email).first()

    print("User found:", user)

    if not user:
        return {
            "message": "If an account with that email exists, a password reset link has been sent."
        }

    token = secrets.token_urlsafe(32)

    user.reset_token = token
    user.reset_token_expires = datetime.now(timezone.utc) + timedelta(minutes=15)

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

    send_email(to_email=user.email, subject=subject, body=body)

    return {
        "message": "If an account with that email exists, a password reset link has been sent."
    }


# -----------------------------
# reset password
# -----------------------------


@router.post(
    "/reset-password",
    summary="Reset user password",
    description="Resets the user's password using a valid password reset token.",
    responses={
        200: {"description": "Password reset successfully"},
        400: {"description": "Invalid or expired reset token"},
    },
)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == request.token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token.")

    expires_at = user.reset_token_expires

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Reset token has expired.")
    # Update the password
    user.hashed_password = hash_password(request.new_password)

    # Invalidate the token
    user.reset_token = None
    user.reset_token_expires = None

    # Save everything
    db.commit()

    return {"message": "Password has been reset successfully."}


# -----------------------------
# admin dashboard
# -----------------------------


@router.get(
    "/admin",
    summary="Access the admin dashboard",
    description="Allows administrators to access the protected admin dashboard.",
    responses={
        200: {"description": "Admin dashboard accessed successfully"},
        403: {"description": "Admin privileges required"},
    },
)
def admin_dashboard(
    current_user: User = Depends(require_admin),
):
    return {"message": f"Welcome Admin {current_user.username}!"}
