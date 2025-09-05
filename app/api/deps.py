from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.models.organization_member import OrganizationMember, OrgRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    from app.models.user import User as UserModel
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise JWTError()
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def get_current_org(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # returns org_id or raises
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        org_id = payload.get("org_id")
        if not org_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active organization in token")
        return org_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

def get_current_member(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), org_id: str = Depends(get_current_org)) -> OrganizationMember:
    member = db.query(OrganizationMember).filter(
        OrganizationMember.user_id == current_user.id,
        OrganizationMember.org_id == org_id,
        OrganizationMember.is_active == True
    ).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not a member of this organization")
    return member

def require_role(*allowed_roles):
    def _require(member: OrganizationMember = Depends(get_current_member)):
        if member.role.value not in [r.value if hasattr(r, "value") else r for r in allowed_roles]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return member
    return _require

def require_org_admin(member: OrganizationMember = Depends(get_current_member)):
    if member.role != OrgRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin required")
    return member
