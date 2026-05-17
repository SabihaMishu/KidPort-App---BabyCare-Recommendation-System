from fastapi import APIRouter, HTTPException, status, Depends
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.utils import timezone
import uuid

from app.api.schemas import InvitationCreate, InvitationResponse, AcceptInvitationRequest, Token
from app.models.invitation import Invitation
from app.core.security import get_current_user, require_role, create_access_token

router = APIRouter(prefix="/invitations", tags=["Invitations"])
User = get_user_model()

@router.post("/create", response_model=InvitationResponse, status_code=status.HTTP_201_CREATED)
def create_invitation(
    invite_data: InvitationCreate, 
    current_user: User = Depends(require_role(['PARENT']))
):
    try:
        invitation = Invitation.objects.create(
            invited_by=current_user,
            role_offered=invite_data.role_offered,
            email=invite_data.email.lower() if invite_data.email else None,
            status='PENDING'
        )
        
        return InvitationResponse(
            token=invitation.token,
            role_offered=invitation.role_offered,
            email=invitation.email,
            status=invitation.status,
            created_at=invitation.created_at,
            expires_at=invitation.expires_at,
            invited_by_name=current_user.full_name
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not create invitation: {str(e)}"
        )

@router.get("/validate/{token}", response_model=InvitationResponse)
def validate_invitation(token: uuid.UUID):
    try:
        invitation = Invitation.objects.get(token=token)
    except Invitation.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation link is invalid or has been deleted"
        )

    # Check status
    if invitation.status == 'ACCEPTED':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This invitation link has already been used"
        )
        
    if invitation.is_expired:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This invitation link has expired"
        )

    return InvitationResponse(
        token=invitation.token,
        role_offered=invitation.role_offered,
        email=invitation.email,
        status=invitation.status,
        created_at=invitation.created_at,
        expires_at=invitation.expires_at,
        invited_by_name=invitation.invited_by.full_name
    )

@router.post("/accept/{token}", response_model=Token)
def accept_invitation(token: uuid.UUID, accept_data: AcceptInvitationRequest):
    try:
        invitation = Invitation.objects.get(token=token)
    except Invitation.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation link is invalid"
        )

    if invitation.status == 'ACCEPTED':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This invitation has already been accepted"
        )

    if invitation.is_expired:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This invitation link has expired"
        )

    email = invitation.email
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation is missing an email address. Contact the sender."
        )

    # Use atomic transaction to make sure we create user AND mark invite accepted together
    try:
        with transaction.atomic():
            # 1. Create the new user with the invitation role
            user = User.objects.create_user(
                email=email,
                full_name=accept_data.full_name,
                password=accept_data.password,
                role=invitation.role_offered,
                terms_accepted=accept_data.terms_accepted
            )
            
            # 2. Mark invitation as accepted
            invitation.status = 'ACCEPTED'
            invitation.save()
            
            # 3. Create jwt token for user
            access_token = create_access_token(data={"sub": user.email})
            return Token(
                access_token=access_token,
                role=user.role,
                email=user.email,
                full_name=user.full_name
            )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during acceptance: {str(e)}"
        )
