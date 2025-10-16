"""User schemas"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: Optional[str] = None


class UserProfile(UserBase):
    """User profile schema"""
    id: str
    created_at: str
    
    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    """User update request schema"""
    full_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response schema"""
    id: str
    email: str
    full_name: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

