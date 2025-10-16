"""User endpoints"""

from fastapi import APIRouter, Request

from app.core.dependencies import CurrentUser
from app.middleware.auth import get_current_user_from_request
from app.core.response import success


router = APIRouter()


@router.get("/me")
async def get_current_user_profile(current_user: CurrentUser):
    """
    获取当前用户信息
    
    需要在请求头中携带有效的 JWT token
    
    注意：这个接口使用了依赖注入方式（CurrentUser），
    这是原有方式，仍然支持。新的方式是使用全局认证中间件。
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
async def get_user_profile(request: Request):
    """
    获取用户详细资料（使用全局认证中间件）
    
    包含用户的元数据信息
    
    注意：这个接口使用了新的全局认证中间件方式，
    通过 get_current_user_from_request() 获取已验证的用户信息。
    这是推荐的使用方式。
    """
    # 从 request.state 获取当前用户（已通过全局认证中间件验证）
    current_user = get_current_user_from_request(request)
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

