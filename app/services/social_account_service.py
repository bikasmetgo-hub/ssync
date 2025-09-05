from sqlalchemy.orm import Session
from app.models.social_account import SocialAccount
from app.schemas.social_account import SocialAccountCreate
from fastapi import HTTPException, status

def create_or_update_social_account(db: Session, user_id: str, data: SocialAccountCreate):
    existing = db.query(SocialAccount).filter(
        SocialAccount.user_id == user_id,
        SocialAccount.provider == data.provider,
        SocialAccount.account_id == data.account_id
    ).first()

    if existing:
        # Update tokens
        existing.access_token = data.access_token
        existing.refresh_token = data.refresh_token
        existing.expires_at = data.expires_at
        existing.extra_data = data.extra_data
        db.commit()
        db.refresh(existing)
        return existing

    account = SocialAccount(user_id=user_id, **data.dict())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def list_user_accounts(db: Session, user_id: str):
    return db.query(SocialAccount).filter(SocialAccount.user_id == user_id).all()
