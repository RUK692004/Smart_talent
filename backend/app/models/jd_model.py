from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JDCreate(BaseModel):
    job_role: Optional[str] = None
    description: str


class JDResponse(BaseModel):
    id: int
    job_role: Optional[str] = None
    description: str
    uploaded_at: datetime