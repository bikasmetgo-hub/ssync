import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.organization import Organization
from app.models.organization_member import OrganizationMember, OrgRole
from app.models.invite import Invite

INVITE_TOKEN_BYTES = 32

def create_organization(db: Session, name: str, owner_user_id):
    slug = name.lower().replace(" ", "-")
    org = Organization(name=name, slug=slug)
    db.add(org)
    db.commit()
    db.refresh(org)

    # add owner as admin
    member = OrganizationMember(org_id=org.id, user_id=owner_user_id, role=OrgRole.ADMIN)
    db.add(member)
    db.commit()
    return org

def create_invite(db: Session, org_id, invited_email: str, role: str, creator_user_id=None, expires_in_hours=72):
    # validate role
    if role not in {r.value for r in OrgRole}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")

    token = secrets.token_urlsafe(INVITE_TOKEN_BYTES)
    expires_at = datetime.now() + timedelta(hours=expires_in_hours)

    invite = Invite(
        org_id=org_id,
        invited_email=invited_email,
        token=token,
        role=role,
        created_by=creator_user_id,
        expires_at=expires_at
    )
    db.add(invite)
    db.commit()
    db.refresh(invite)
    # TODO: send email with invite link to accept (use email service)
    return invite

def accept_invite(db: Session, token: str, user_id):
    invite = db.query(Invite).filter(Invite.token == token).first()
    if not invite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
    if invite.accepted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invite already accepted")
    if invite.expires_at < datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invite expired")

    # add membership
    member = OrganizationMember(org_id=invite.org_id, user_id=user_id, role=invite.role)
    db.add(member)
    invite.accepted = True
    invite.accepted_by = user_id
    db.commit()
    db.refresh(member)
    return member
