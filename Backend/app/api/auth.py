from fastapi import APIRouter, HTTPException, status, Depends
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
import requests
import os

from app.api.schemas import UserRegister, UserLogin, GoogleLoginRequest, Token
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
User = get_user_model()

# Google Client ID from Environment
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister):
    try:
        # Create user using custom UserManager
        user = User.objects.create_user(
            email=user_data.email.lower(),
            full_name=user_data.full_name,
            password=user_data.password,
            role=user_data.role,
            terms_accepted=user_data.terms_accepted
        )
        
        # Create Access Token
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
            detail="A user with this email already exists"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
def login(login_data: UserLogin):
    try:
        user = User.objects.get(email=login_data.email.lower())
    except User.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )

    # Use Django's check_password to check the hashed password
    if not check_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(data={"sub": user.email})
    return Token(
        access_token=access_token,
        role=user.role,
        email=user.email,
        full_name=user.full_name
    )

@router.post("/google", response_model=Token)
def google_signin(google_data: GoogleLoginRequest):
    token = google_data.token
    
    # 1. Verify the Google token
    email = None
    full_name = None
    
    # Check for mock token (convenient for local dev and testing)
    if token.startswith("mock-google-token"):
        # For mock, we parse email and name from string if it's like mock-google-token:email@test.com:Full Name
        parts = token.split(":")
        email = parts[1] if len(parts) > 1 else "mock_user@example.com"
        full_name = parts[2] if len(parts) > 2 else "Mock Google User"
    else:
        # Call Google API
        try:
            res = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}", timeout=5)
            if res.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Google OAuth token"
                )
            user_info = res.json()
            
            # Verify audience
            aud = user_info.get("aud")
            if GOOGLE_CLIENT_ID and aud != GOOGLE_CLIENT_ID:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token audience mismatch"
                )
                
            email = user_info.get("email")
            full_name = user_info.get("name", "Google User")
            
        except requests.RequestException:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Could not reach Google verification servers"
            )

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google token did not provide email address"
        )

    email = email.lower()

    # 2. Get or create the user in Django DB
    try:
        user = User.objects.get(email=email)
        # Existing user logs in, ensure terms are accepted
        if not user.terms_accepted:
            user.terms_accepted = True
            user.save()
    except User.DoesNotExist:
        # New user via Google, default role: PARENT
        user = User.objects.create_user(
            email=email,
            full_name=full_name,
            password=None,  # No password for OAuth users
            role='PARENT',
            terms_accepted=google_data.terms_accepted
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )

    # 3. Create and return JWT Access Token
    access_token = create_access_token(data={"sub": user.email})
    return Token(
        access_token=access_token,
        role=user.role,
        email=user.email,
        full_name=user.full_name
    )
