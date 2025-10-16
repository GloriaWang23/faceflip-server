"""Dependency injection functions"""

import logging
from typing import Annotated, Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client, create_client
from starlette.exceptions import HTTPException

from app.core.config import settings
from app.core.response_code import ResponseCode

# 配置日志
logger = logging.getLogger(__name__)


# Security
security = HTTPBearer()


def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    if not settings.supabase_url or not settings.supabase_service_role_key:
        logger.error("❌ Supabase configuration missing - URL or service role key not set")
        raise HTTPException(
            status_code=500,
            detail=f"{ResponseCode.E_SYSTEM_BUSY.code}|Supabase configuration missing"
        )
    
    try:
        client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        logger.debug("✅ Supabase client created successfully")
        return client
    except Exception as e:
        logger.error(f"❌ Failed to create Supabase client: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"{ResponseCode.E_SYSTEM_BUSY.code}|Failed to initialize Supabase client"
        )


async def verify_jwt_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    supabase: Annotated[Client, Depends(get_supabase_client)]
) -> dict:
    """
    验证前端传来的 JWT token（由 Supabase JS SDK 生成）
    
    前端流程：
    1. 前端使用 Supabase JS SDK 进行登录/注册
    2. 获得 access_token
    3. 在请求头中携带：Authorization: Bearer <access_token>
    4. 后端验证 token 并返回用户信息
    """
    try:
        token = credentials.credentials
        logger.debug(f"🔍 Verifying JWT token (length: {len(token)})")
        
        # 使用 Supabase 验证 JWT token
        response = supabase.auth.get_user(token)
        
        if not response or not response.user:
            logger.warning("⚠️  Token verification failed: invalid response from Supabase")
            raise HTTPException(
                status_code=401,
                detail=f"{ResponseCode.E_TOKEN_NOT_VALID.code}|token not valid or expired"
            )
        
        logger.info(f"✅ Token verified for user: {response.user.email}")
        
        # 返回用户信息
        return {
            "id": response.user.id,
            "email": response.user.email,
            "user_metadata": response.user.user_metadata or {},
            "created_at": str(response.user.created_at) if response.user.created_at else None,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"❌ Token verification exception: {type(e).__name__}: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=401,
            detail=f"{ResponseCode.AUTH_FAILED.code}|authentication failed: {str(e)}"
        )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    supabase: Client = Depends(get_supabase_client)
) -> Optional[dict]:
    """可选的用户认证 - 允许匿名访问"""
    if not credentials:
        logger.debug("🔓 Optional auth: no credentials provided, returning None")
        return None
    
    try:
        token = credentials.credentials
        logger.debug(f"🔍 Optional auth: verifying token (length: {len(token)})")
        response = supabase.auth.get_user(token)
        
        if response and response.user:
            logger.info(f"✅ Optional auth: token verified for user {response.user.email}")
            return {
                "id": response.user.id,
                "email": response.user.email,
                "user_metadata": response.user.user_metadata or {},
                "created_at": str(response.user.created_at) if response.user.created_at else None,
            }
        else:
            logger.warning("⚠️  Optional auth: invalid token response")
    except Exception as e:
        logger.warning(f"⚠️  Optional auth: token verification failed - {type(e).__name__}: {str(e)}")
    
    return None


# Type aliases for common dependencies
SupabaseClient = Annotated[Client, Depends(get_supabase_client)]
CurrentUser = Annotated[dict, Depends(verify_jwt_token)]
OptionalUser = Annotated[Optional[dict], Depends(get_optional_user)]

