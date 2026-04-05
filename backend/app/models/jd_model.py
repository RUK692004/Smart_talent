from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class JDCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    skills: List[str] = []
    experience_required: float = 0
    keywords: List[str] = []


class JDResponse(BaseModel):
    id: int
    title: str
    parsed_data: Dict[str, Any]