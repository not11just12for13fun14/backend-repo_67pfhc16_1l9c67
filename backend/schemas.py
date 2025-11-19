from __future__ import annotations

from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field

# Each model defines a collection using the class name lowercased

class Lead(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    company: Optional[str] = None
    phone: Optional[str] = None
    screen_type: Literal[
        "Indoor LED",
        "Outdoor LED",
        "Interactive Touch",
        "Digital Advertising",
        "Transparent LED",
        "Custom"
    ]
    size_requirements: Optional[str] = None
    usage_type: Optional[str] = None
    message: Optional[str] = None

class TestMessage(BaseModel):
    message: str
