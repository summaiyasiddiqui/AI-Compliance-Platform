import requests

from app.config import settings
from app.logger import logger


def send_email(to_email: str, subject: str, body: str):

    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {settings.resend_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "from": settings.email_from,
        "to": [to_email],
        "subject": subject,
        "text": body,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=20,
        )

        response.raise_for_status()

        logger.info(
            f"Email sent successfully to {to_email}"
        )

    except Exception as e:
        logger.error(
            f"Failed to send email: {e}"
        )