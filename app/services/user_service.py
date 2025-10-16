"""User service layer"""

import logging
from typing import Optional
from supabase import Client

from app.models.user import User
from app.schemas.user import UserUpdateRequest

# 配置日志
logger = logging.getLogger(__name__)


class UserService:
    """User service for business logic"""
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            logger.debug(f"🔍 [UserService] Getting user by ID: {user_id}")
            response = self.supabase.from_("users").select("*").eq("id", user_id).execute()
            
            if response.data and len(response.data) > 0:
                logger.info(f"✅ [UserService] User found: {user_id}")
                return User(**response.data[0])
            else:
                logger.warning(f"⚠️  [UserService] User not found: {user_id}")
            
            return None
        except Exception as e:
            logger.error(
                f"❌ [UserService] Error getting user {user_id}: {type(e).__name__}: {str(e)}",
                exc_info=True
            )
            return None
    
    async def update_user(self, user_id: str, update_data: UserUpdateRequest) -> Optional[User]:
        """Update user profile"""
        try:
            data_dict = update_data.model_dump(exclude_unset=True)
            logger.debug(f"🔄 [UserService] Updating user {user_id} with data: {list(data_dict.keys())}")
            
            response = self.supabase.from_("users").update(data_dict).eq("id", user_id).execute()
            
            if response.data and len(response.data) > 0:
                logger.info(f"✅ [UserService] User updated successfully: {user_id}")
                return User(**response.data[0])
            else:
                logger.warning(f"⚠️  [UserService] User update failed: {user_id}")
            
            return None
        except Exception as e:
            logger.error(
                f"❌ [UserService] Error updating user {user_id}: {type(e).__name__}: {str(e)}",
                exc_info=True
            )
            return None
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete user (soft delete)"""
        try:
            logger.info(f"🗑️  [UserService] Soft deleting user: {user_id}")
            self.supabase.from_("users").update({"is_active": False}).eq("id", user_id).execute()
            logger.info(f"✅ [UserService] User soft deleted successfully: {user_id}")
            return True
        except Exception as e:
            logger.error(
                f"❌ [UserService] Error deleting user {user_id}: {type(e).__name__}: {str(e)}",
                exc_info=True
            )
            return False

