from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, JSON, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    provider = Column(String, nullable=False)  # e.g., 'twitter', 'linkedin'
    account_name = Column(String, nullable=False)
    account_id = Column(String, nullable=False)  # Social platform's unique ID

    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    extra_data = Column(JSON, nullable=True)  # Store profile pic, etc.
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())