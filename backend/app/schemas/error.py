from typing import Any, Optional
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    data: Optional[Any] = None