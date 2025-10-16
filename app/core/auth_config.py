"""
全局认证配置
类似于 Java Spring Security 的配置类

使用方式：
1. 在这里配置白名单路径（不需要认证的路径）
2. 支持精确匹配和正则表达式模式匹配
3. 默认所有路径都需要认证，白名单中的路径除外
"""

from typing import Set, List

# 白名单：这些路径不需要认证（精确匹配）
# 类似于 Spring Security 的 .antMatchers("/path").permitAll()
PUBLIC_PATHS: Set[str] = {
    # 根路径和健康检查
    "/",
    "/health",
    "/health/check", 
    "/health/ping",
    
    # API 文档
    "/docs",
    "/redoc",
    "/openapi.json",
    
    # 静态资源
    "/favicon.ico",
    
    # 认证相关接口（登录、注册不需要认证）
    "/api/auth/login",
    "/api/auth/register",
    "/api/auth/refresh",
    
    # API 健康检查
    "/api/health",
    "/api/health/check",
    "/api/health/ping",
    
    # 调试接口（临时）
    "/api/faceflip/debug/auth",
    "/api/faceflip/debug/env",
}

# 白名单路径模式（正则表达式）
# 类似于 Spring Security 的 .antMatchers("/path/**").permitAll()
PUBLIC_PATH_PATTERNS: List[str] = [
    r"^/docs.*",      # Swagger 文档相关，匹配 /docs, /docs/, /docs/xxx
    r"^/redoc.*",     # ReDoc 文档相关，匹配 /redoc, /redoc/, /redoc/xxx
    r"^/static/.*",   # 静态文件，匹配 /static/xxx
]


# 示例：如何添加新的公开路径
# 1. 精确匹配：PUBLIC_PATHS.add("/api/public/endpoint")
# 2. 模式匹配：PUBLIC_PATH_PATTERNS.append(r"^/api/public/.*")


"""
使用示例：

方式一：全局认证（推荐）
--------------------------
在 main.py 中启用全局认证中间件：
    app.add_middleware(AuthMiddleware, enable=True)

所有不在白名单中的路径都需要认证。
在路由处理函数中获取当前用户：

    from fastapi import Request
    from app.middleware.auth import get_current_user_from_request
    
    @router.get("/profile")
    async def get_profile(request: Request):
        user = get_current_user_from_request(request)
        return success(data=user)


方式二：路由级认证（原有方式）
--------------------------
在需要认证的路由中使用 CurrentUser 依赖：

    from app.core.dependencies import CurrentUser
    
    @router.get("/profile")
    async def get_profile(current_user: CurrentUser):
        return success(data=current_user)


两种方式对比：
--------------------------
| 特性         | 全局认证（方式一）      | 路由级认证（方式二）   |
|------------|-------------------|----------------|
| 默认行为     | 所有路径需要认证      | 只有标记的路由需要认证 |
| 配置方式     | 配置白名单          | 每个路由单独配置     |
| 类似于       | Spring Security   | 手动添加拦截器      |
| 适用场景     | 大部分接口需要认证    | 少数接口需要认证     |
| 代码侵入性   | 低（中心化配置）     | 高（分散在各个路由）   |


推荐做法：
--------------------------
1. 使用全局认证中间件（方式一）
2. 在 auth_config.py 中维护白名单
3. 在路由中使用 get_current_user_from_request() 获取用户信息
4. 这样最接近 Java Spring 的使用习惯
"""

