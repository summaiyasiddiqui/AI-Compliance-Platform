import time
import uuid

from app.logger import logger
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()
        request_id = str(uuid.uuid4())[:8]

        client_ip = request.client.host if request.client else "Unknown"

        logger.info(
            f"[{request_id}] Incoming Request: "
            f"{request.method} {request.url.path} | "
            f"Client: {client_ip}"
        )

        response = await call_next(request)

        process_time = round((time.time() - start_time) * 1000, 2)

        logger.info(
            f"[{request_id}] "
            f"{request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time} ms | "
            f"Client: {client_ip}"
        )

        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response
