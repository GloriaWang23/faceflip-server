"""Authentication schemas"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class SignUpRequest(BaseModel):
    """Sign up request schema"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class SignInRequest(BaseModel):
    """Sign in request schema"""
    email: EmailStr
    password: str


class TokenRefreshRequest(BaseModel):
    """Token refresh request schema"""
    refresh_token: str


class AuthResponse(BaseModel):
    """Authentication response schema"""
    user: dict
    session: Optional[dict] = None
    message: str = "Success"
    
    class Config:
        from_attributes = True

