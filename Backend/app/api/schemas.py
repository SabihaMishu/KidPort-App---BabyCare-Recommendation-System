from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Literal
from datetime import datetime
import uuid

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Literal['PARENT', 'NANNY', 'DAYCARE', 'DOCTOR']
    terms_accepted: bool

    @field_validator('terms_accepted')
    @classmethod
    def must_accept_terms(cls, v: bool) -> bool:
        if v is not True:
            raise ValueError('Terms & Conditions must be accepted')
        return v

    @field_validator('full_name')
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Full name cannot be empty')
        return v.strip()

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class GoogleLoginRequest(BaseModel):
    token: str
    terms_accepted: bool

    @field_validator('terms_accepted')
    @classmethod
    def must_accept_terms(cls, v: bool) -> bool:
        if v is not True:
            raise ValueError('Terms & Conditions must be accepted')
        return v

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    email: str
    full_name: str

class InvitationCreate(BaseModel):
    role_offered: Literal['NANNY', 'DAYCARE', 'DOCTOR']
    email: Optional[EmailStr] = None

class InvitationResponse(BaseModel):
    token: uuid.UUID
    role_offered: str
    email: Optional[str]
    status: str
    created_at: datetime
    expires_at: datetime
    invited_by_name: str

    class Config:
        from_attributes = True

class AcceptInvitationRequest(BaseModel):
    full_name: str
    password: str
    terms_accepted: bool

    @field_validator('terms_accepted')
    @classmethod
    def must_accept_terms(cls, v: bool) -> bool:
        if v is not True:
            raise ValueError('Terms & Conditions must be accepted')
        return v
