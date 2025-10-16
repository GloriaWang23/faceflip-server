"""User service layer"""

from typing import Optional
from supabase import Client

from app.models.user import User
from app.schemas.user import UserUpdateRequest


class UserService:
    """User service for business logic"""
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            response = self.supabase.from_("users").select("*").eq("id", user_id).execute()
            
            if response.data and len(response.data) > 0:
                return User(**response.data[0])
            
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    async def update_user(self, user_id: str, update_data: UserUpdateRequest) -> Optional[User]:
        """Update user profile"""
        try:
            data_dict = update_data.model_dump(exclude_unset=True)
            
            response = self.supabase.from_("users").update(data_dict).eq("id", user_id).execute()
            
            if response.data and len(response.data) > 0:
                return User(**response.data[0])
            
            return None
        except Exception as e:
            print(f"Error updating user: {e}")
            return None
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete user (soft delete)"""
        try:
            self.supabase.from_("users").update({"is_active": False}).eq("id", user_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

