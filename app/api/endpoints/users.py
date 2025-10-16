"""User endpoints"""

from fastapi import APIRouter

from app.core.dependencies import CurrentUser
from app.core.response import success


router = APIRouter()


@router.get("/me")
async def get_current_user_profile(current_user: CurrentUser):
    """
    获取当前用户信息
    
    需要在请求头中携带有效的 JWT token
    """
    return success(
        data={
            "user": {
                "id": current_user["id"],
                "email": current_user["email"],
                "user_metadata": current_user.get("user_metadata", {}),
                "created_at": current_user.get("created_at")
            }
        }
    )


@router.get("/profile")
async def get_user_profile(current_user: CurrentUser):
    """
    获取用户详细资料
    
    包含用户的元数据信息
    """
    user_metadata = current_user.get("user_metadata", {})
    
    return success(
        data={
            "profile": {
                "id": current_user["id"],
                "email": current_user["email"],
                "full_name": user_metadata.get("full_name"),
                "avatar_url": user_metadata.get("avatar_url"),
                "created_at": current_user.get("created_at"),
                "metadata": user_metadata
            }
        }
    )

