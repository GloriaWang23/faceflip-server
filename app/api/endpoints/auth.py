"""Authentication endpoints

注意：用户登录/注册由前端直接调用 Supabase JS SDK 完成
后端只负责验证 JWT token 的有效性
"""

from fastapi import APIRouter

from app.core.dependencies import CurrentUser, OptionalUser
from app.core.response import success


router = APIRouter()


@router.get("/verify")
async def verify_token(current_user: CurrentUser):
    """
    验证 JWT token 是否有效
    
    前端使用 Supabase JS SDK 登录后，可以调用此接口验证 token 是否有效
    """
    return success(
        data={
            "user": {
                "id": current_user["id"],
                "email": current_user["email"],
                "user_metadata": current_user.get("user_metadata", {}),
                "created_at": current_user.get("created_at")
            }
        },
        msg="token verified"
    )


@router.get("/me")
async def get_authenticated_user(current_user: CurrentUser):
    """
    获取当前认证用户的信息
    
    需要在请求头中携带有效的 JWT token:
    Authorization: Bearer <your-access-token>
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


@router.get("/status")
async def auth_status(user: OptionalUser):
    """
    检查认证状态（可选认证）
    
    如果提供了有效的 token，返回用户信息
    如果没有 token 或 token 无效，返回未认证状态
    """
    if user:
        return success(
            data={
                "authenticated": True,
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "user_metadata": user.get("user_metadata", {}),
                    "created_at": user.get("created_at")
                }
            }
        )
    else:
        return success(
            data={
                "authenticated": False,
                "user": None
            }
        )

