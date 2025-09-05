from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict

class SocialAccountBase(BaseModel):
    provider: str
    account_name: str
    account_id: str
    is_active: bool

class SocialAccountCreate(SocialAccountBase):
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    extra_data: Optional[Dict] = None

class SocialAccountResponse(SocialAccountBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
