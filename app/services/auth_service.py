"""Authentication service layer

注意：用户登录/注册由前端直接调用 Supabase JS SDK 完成
此服务层仅用于后端需要的 token 验证等操作
"""

from typing import Optional
from supabase import Client


class AuthService:
    """
    认证服务
    
    主要功能：
    - 验证 JWT token
    - 获取用户信息
    """
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
    
    async def verify_token(self, token: str) -> Optional[dict]:
        """
        验证 JWT token 并返回用户信息
        
        Args:
            token: JWT access token
            
        Returns:
            用户信息字典，如果 token 无效则返回 None
        """
        try:
            response = self.supabase.auth.get_user(token)
            
            if response and response.user:
                return {
                    "id": response.user.id,
                    "email": response.user.email,
                    "user_metadata": response.user.user_metadata or {},
                    "created_at": str(response.user.created_at) if response.user.created_at else None,
                }
            
            return None
        except Exception as e:
            print(f"Token verification error: {e}")
            return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """
        根据用户 ID 获取用户信息（需要 service_role_key）
        
        Args:
            user_id: 用户 ID
            
        Returns:
            用户信息字典
        """
        try:
            # 这需要使用 service_role_key 的客户端
            response = self.supabase.auth.admin.get_user_by_id(user_id)
            
            if response and response.user:
                return {
                    "id": response.user.id,
                    "email": response.user.email,
                    "user_metadata": response.user.user_metadata or {},
                    "created_at": str(response.user.created_at) if response.user.created_at else None,
                }
            
            return None
        except Exception as e:
            print(f"Get user error: {e}")
            return None

