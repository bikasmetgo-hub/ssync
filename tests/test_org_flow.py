import pytest
from app.core.security import hash_password
from app.models.user import User
from app.models.organization import Organization
from app.models.organization_member import OrganizationMember, OrgRole
from app.services.org_service import create_organization, create_invite, accept_invite

def make_user(db, email="owner@example.com"):
    u = User(email=email, hashed_password=hash_password("password"))
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

def test_create_org_and_admin_membership(db_session):
    user = make_user(db_session)
    org = create_organization(db_session, "Acme Corp", owner_user_id=user.id)
    assert org.name == "Acme Corp"
    # admin membership exists
    m = db_session.query(OrganizationMember).filter_by(org_id=org.id, user_id=user.id).first()
    assert m is not None
    assert m.role == OrgRole.ADMIN

def test_invite_and_accept(db_session):
    owner = make_user(db_session, email="owner2@example.com")
    org = create_organization(db_session, "TestOrg", owner_user_id=owner.id)
    invite = create_invite(db_session, org.id, "invitee@example.com", role="member", creator_user_id=owner.id, expires_in_hours=1)
    assert invite.invited_email == "invitee@example.com"
    # create invitee user and accept
    invitee = make_user(db_session, email="invitee@example.com")
    member = accept_invite(db_session, invite.token, invitee.id)
    assert member.org_id == org.id
    assert member.user_id == invitee.id
    assert member.role.value == "member"
