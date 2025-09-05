from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class OrgCreate(BaseModel):
    name: str
    slug: Optional[str] = None

class OrgResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    created_at: datetime

    class Config:
        orm_mode = True

class OrgInviteCreate(BaseModel):
    invited_email: EmailStr
    role: str  # validate against OrgRole enum in service
    expires_in_hours: Optional[int] = 72
