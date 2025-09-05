from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str, *, expires_minutes: int = None, org_id: str = None, roles: list = None, extra: dict = None):
    expires_minutes = expires_minutes or settings.jwt_expire_minutes
    to_encode = {"sub": str(subject)}
    if org_id:
        to_encode["org_id"] = str(org_id)
    if roles:
        to_encode["roles"] = roles
    if extra:
        to_encode.update(extra)
    expire = datetime.now() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)