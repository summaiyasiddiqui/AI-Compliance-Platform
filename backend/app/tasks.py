from app.email_service import send_email
from app.logger import logger


def send_welcome_email(email: str, username: str):

    logger.info(f"Starting welcome email task for {email}")

    subject = "Welcome to ComplianceAI"

    body = f"""
Hello {username},

Welcome to ComplianceAI! 🎉

Your account has been created successfully.

We're excited to have you onboard.

Regards,
ComplianceAI Team
"""

    send_email(
        to_email=email,
        subject=subject,
        body=body
    )

    logger.info(f"Welcome email task completed for {email}")