from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.organization import OrgCreate, OrgResponse, OrgInviteCreate
from app.db.session import get_db
from app.services.org_service import create_organization, create_invite, accept_invite
from app.api.deps import get_current_user, require_org_admin
from app.core.security import create_access_token

router = APIRouter(prefix="/api/v1/orgs", tags=["Organizations"])

@router.post("/", response_model=OrgResponse)
def create_org(payload: OrgCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    org = create_organization(db, payload.name, owner_user_id=current_user.id)
    return org

@router.post("/{org_id}/invite", response_model=dict)
def invite_user(org_id: str, payload: OrgInviteCreate, db: Session = Depends(get_db), admin = Depends(require_org_admin)):
    invite = create_invite(db, org_id, payload.invited_email, payload.role, creator_user_id=admin.user_id, expires_in_hours=payload.expires_in_hours)
    return {"invite_id": str(invite.id), "token": invite.token}

@router.post("/accept-invite")
def accept(payload: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    token = payload.get("token")
    member = accept_invite(db, token, current_user.id)
    return {"member_id": str(member.id), "org_id": str(member.org_id)}

@router.post("/auth/switch-org")
def switch_org(org_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    member = db.query(OrganizationMember).filter(
        OrganizationMember.user_id == current_user.id,
        OrganizationMember.org_id == org_id,
        OrganizationMember.is_active == True
    ).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")
    # roles for this member (single role per membership in our model)
    roles = [member.role.value] if hasattr(member.role, "value") else [member.role]
    token = create_access_token(subject=str(current_user.id), org_id=str(org_id), roles=roles)
    return {"access_token": token, "token_type": "bearer"}
