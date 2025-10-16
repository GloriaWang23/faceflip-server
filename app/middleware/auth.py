"""全局认证中间件 - 类似 Java Spring 拦截器"""

import logging
import re
import traceback
from typing import List, Optional, Set
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from supabase import Client, create_client

from app.core.config import settings
from app.core.response_code import ResponseCode
from app.core.response import error
from app.core import auth_config

# 配置日志
logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """
    全局认证中间件
    
    类似于 Java Spring 的拦截器，支持配置白名单路径
    只有在白名单中的路径才不需要认证
    
    白名单配置在 app.core.auth_config 中维护
    """
    
    def __init__(self, app, enable: bool = True):
        """
        初始化认证中间件
        
        Args:
            app: FastAPI 应用实例
            enable: 是否启用全局认证（默认启用）
        """
        super().__init__(app)
        self.enable = enable
        self.supabase_client: Optional[Client] = None
        # 从配置文件加载白名单
        self.public_paths = auth_config.PUBLIC_PATHS
        self.public_path_patterns = auth_config.PUBLIC_PATH_PATTERNS
        self._compiled_patterns = [re.compile(pattern) for pattern in self.public_path_patterns]
    
    def _get_supabase_client(self) -> Client:
        """获取 Supabase 客户端（懒加载）"""
        if not self.supabase_client:
            if not settings.supabase_url or not settings.supabase_service_role_key:
                logger.error("❌ Supabase configuration missing - URL or service role key not set")
                raise Exception("Supabase configuration missing")
            try:
                self.supabase_client = create_client(
                    settings.supabase_url, 
                    settings.supabase_service_role_key
                )
                logger.info("✅ Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to create Supabase client: {e}", exc_info=True)
                raise
        return self.supabase_client
    
    def _is_public_path(self, path: str) -> bool:
        """
        判断路径是否在白名单中
        
        Args:
            path: 请求路径
            
        Returns:
            bool: True 表示是公开路径，不需要认证
        """
        # 精确匹配
        if path in self.public_paths:
            return True
        
        # 模式匹配
        for pattern in self._compiled_patterns:
            if pattern.match(path):
                return True
        
        return False
    
    async def _verify_token(self, token: str) -> Optional[dict]:
        """
        验证 JWT token
        
        Args:
            token: JWT token
            
        Returns:
            用户信息字典，验证失败返回 None
        """
        try:
            supabase = self._get_supabase_client()
            response = supabase.auth.get_user(token)
            
            if response and response.user:
                logger.info(f"✅ Token verified successfully for user: {response.user.email}")
                return {
                    "id": response.user.id,
                    "email": response.user.email,
                    "user_metadata": response.user.user_metadata or {},
                    "created_at": str(response.user.created_at) if response.user.created_at else None,
                }
            else:
                logger.warning(f"⚠️  Token verification failed: invalid response from Supabase")
        except Exception as e:
            logger.error(
                f"❌ Token verification exception: {type(e).__name__}: {str(e)}\n"
                f"Token preview: {token[:20]}...{token[-20:] if len(token) > 40 else ''}",
                exc_info=True
            )
        
        return None
    
    async def dispatch(self, request: Request, call_next):
        """
        中间件主逻辑 - 拦截所有请求进行认证检查
        
        类似于 Spring 的 HandlerInterceptor.preHandle()
        """
        path = request.url.path
        method = request.method
        
        try:
            # 如果未启用全局认证，直接放行
            if not self.enable:
                logger.debug(f"🔓 Global auth disabled - {method} {path}")
                return await call_next(request)
            
            # 检查是否是公开路径
            if self._is_public_path(path):
                logger.debug(f"🔓 Public path - {method} {path}")
                return await call_next(request)
            
            # 从请求头获取 token
            authorization = request.headers.get("Authorization")
            
            if not authorization:
                logger.warning(f"⚠️  Missing authorization header - {method} {path}")
                return error(
                    code=ResponseCode.UNAUTHORIZED,
                    msg="missing authorization header"
                )
            
            # 验证 Bearer token 格式
            parts = authorization.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                logger.warning(
                    f"⚠️  Invalid authorization header format - {method} {path}\n"
                    f"Header: {authorization[:50]}..."
                )
                return error(
                    code=ResponseCode.UNAUTHORIZED,
                    msg="invalid authorization header format"
                )
            
            token = parts[1]
            
            # 验证 token
            user = await self._verify_token(token)
            if not user:
                logger.warning(f"⚠️  Token verification failed - {method} {path}")
                return error(
                    code=ResponseCode.E_TOKEN_NOT_VALID,
                    msg="token not valid or expired"
                )
            
            # 将用户信息存储到 request.state 中，供后续使用
            request.state.current_user = user
            logger.info(f"🔐 Authenticated user {user['email']} - {method} {path}")
            
            # 放行请求
            return await call_next(request)
            
        except Exception as e:
            logger.error(
                f"❌ Auth middleware error for {method} {path}: {type(e).__name__}: {str(e)}",
                exc_info=True
            )
            return error(
                code=ResponseCode.E_SYSTEM_BUSY,
                msg=f"authentication error: {str(e)}"
            )


# 便捷函数：从 request.state 获取当前用户
def get_current_user_from_request(request: Request) -> Optional[dict]:
    """
    从 request.state 获取当前登录用户
    
    在中间件验证通过后，用户信息会存储在 request.state.current_user 中
    这样在路由处理函数中就可以直接获取，而不需要再次验证
    
    Usage:
        @router.get("/profile")
        async def get_profile(request: Request):
            user = get_current_user_from_request(request)
            return success(data=user)
    """
    return getattr(request.state, "current_user", None)

