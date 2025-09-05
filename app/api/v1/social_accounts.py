from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.social_account import SocialAccountResponse
from app.services.social_account_service import create_or_update_social_account, list_user_accounts
from app.core.security import create_access_token
from app.api.deps import get_current_user
from app.integrations.twitter import TwitterIntegration
import uuid

router = APIRouter()

@router.get("/twitter/connect")
def twitter_connect():
    twitter = TwitterIntegration()
    state = str(uuid.uuid4())  # random CSRF protection
    return {"auth_url": twitter.get_authorization_url(state)}

@router.get("/twitter/callback", response_model=SocialAccountResponse)
def twitter_callback(code: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    twitter = TwitterIntegration()
    token_data = twitter.exchange_code_for_token(code)
    profile = twitter.get_user_profile(token_data["access_token"])

    account_data = {
        "provider": "twitter",
        "account_name": profile["data"]["username"],
        "account_id": profile["data"]["id"],
        "access_token": token_data["access_token"],
        "refresh_token": token_data.get("refresh_token"),
        "extra_data": profile
    }
    return create_or_update_social_account(db, current_user.id, account_data)

@router.get("/me", response_model=list[SocialAccountResponse])
def get_my_accounts(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return list_user_accounts(db, current_user.id)
