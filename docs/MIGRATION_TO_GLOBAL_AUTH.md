# 迁移到全局认证中间件

## 更新说明

本次更新添加了类似 **Java Spring Security** 的全局认证中间件，实现了统一的权限拦截和管理。

## 新增文件

1. **`app/middleware/auth.py`**
   - 全局认证中间件实现
   - 支持白名单配置
   - 类似 Spring 的 HandlerInterceptor

2. **`app/core/auth_config.py`**
   - 认证配置文件
   - 白名单路径管理
   - 类似 Spring Security 的配置类

3. **`docs/GLOBAL_AUTH.md`**
   - 详细使用文档
   - 包含示例和最佳实践

4. **`docs/MIGRATION_TO_GLOBAL_AUTH.md`**（本文件）
   - 迁移指南

## 主要变更

### 1. 中间件注册 (`app/main.py`)

```python
# 新增
from app.middleware.auth import AuthMiddleware

# 注册全局认证中间件
app.add_middleware(AuthMiddleware, enable=True)
```

### 2. 中间件导出 (`app/middleware/__init__.py`)

```python
from app.middleware.auth import AuthMiddleware, get_current_user_from_request

__all__ = [
    "AuthMiddleware",
    "get_current_user_from_request",
    # ...
]
```

### 3. 示例更新 (`app/api/endpoints/users.py`)

添加了使用全局认证中间件的示例：

```python
from fastapi import Request
from app.middleware.auth import get_current_user_from_request

@router.get("/profile")
async def get_user_profile(request: Request):
    # 从 request.state 获取已验证的用户
    current_user = get_current_user_from_request(request)
    return success(data=current_user)
```

## 使用方式对比

### 旧方式（仍然支持）

```python
from app.core.dependencies import CurrentUser

@router.get("/profile")
async def get_profile(current_user: CurrentUser):
    return success(data=current_user)
```

**特点**：
- ❌ 需要在每个需要认证的路由中手动添加 `CurrentUser` 参数
- ❌ 容易遗漏，导致安全问题
- ✅ 灵活，可以选择性添加

### 新方式（推荐）

```python
from fastapi import Request
from app.middleware.auth import get_current_user_from_request

@router.get("/profile")
async def get_profile(request: Request):
    user = get_current_user_from_request(request)
    return success(data=user)
```

**特点**：
- ✅ 默认所有路径都需要认证（更安全）
- ✅ 统一管理白名单（中心化配置）
- ✅ 类似 Spring Security 的使用体验
- ✅ 减少重复代码

## 迁移步骤

如果你想将现有路由迁移到新方式：

### 步骤 1：确认路由是否需要认证

- 如果不需要认证 → 添加到白名单
- 如果需要认证 → 继续下一步

### 步骤 2：添加白名单（如果需要）

在 `app/core/auth_config.py` 中：

```python
# 精确匹配
PUBLIC_PATHS.add("/api/public/endpoint")

# 或模式匹配
PUBLIC_PATH_PATTERNS.append(r"^/api/public/.*")
```

### 步骤 3：修改路由参数

**之前：**
```python
async def my_route(current_user: CurrentUser):
    user_id = current_user["id"]
```

**之后：**
```python
from fastapi import Request
from app.middleware.auth import get_current_user_from_request

async def my_route(request: Request):
    current_user = get_current_user_from_request(request)
    user_id = current_user["id"]
```

### 步骤 4：测试

1. 启动服务器
2. 测试需要认证的接口（带 Token）
3. 测试白名单接口（不带 Token）
4. 确认所有接口正常工作

## 配置示例

### 常见白名单配置

```python
# app/core/auth_config.py

PUBLIC_PATHS = {
    # 首页和健康检查
    "/",
    "/health",
    "/health/check",
    "/health/ping",
    
    # 文档
    "/docs",
    "/redoc",
    "/openapi.json",
    
    # 认证接口
    "/api/auth/login",
    "/api/auth/register",
    "/api/auth/refresh",
    "/api/auth/reset-password",
    
    # 公开 API
    "/api/public/info",
    "/api/public/status",
}

PUBLIC_PATH_PATTERNS = [
    r"^/docs.*",           # 文档相关
    r"^/redoc.*",          # ReDoc
    r"^/static/.*",        # 静态文件
    r"^/api/public/.*",    # 所有公开 API
]
```

## 兼容性

### 向后兼容

- ✅ **完全兼容**：旧的 `CurrentUser` 依赖方式仍然可以使用
- ✅ **逐步迁移**：可以逐个接口迁移，不需要一次性修改所有代码
- ✅ **混合使用**：新旧方式可以在同一个项目中共存

### 禁用全局认证

如果需要临时禁用全局认证（例如在开发测试阶段）：

```python
# app/main.py
app.add_middleware(AuthMiddleware, enable=False)
```

这样就回到了原来的行为：只有使用 `CurrentUser` 的路由才会校验。

## 常见问题

### Q1: 为什么要使用全局认证？

**A:** 
- 更安全：默认需要认证，避免遗漏
- 更清晰：白名单配置一目了然
- 更统一：类似主流框架（Spring Security）的做法

### Q2: 如何判断哪些路径应该加入白名单？

**A:**
- 公开页面（首页、关于我们等）
- 认证接口（登录、注册等）
- 健康检查接口
- 公开 API
- 静态资源

### Q3: 全局认证会影响性能吗？

**A:**
- 白名单路径：不会验证 Token，性能无影响
- 需要认证的路径：与原来的 `CurrentUser` 方式性能相同
- 每次请求都会调用 Supabase 验证 Token（原来也是这样）
- 未来可以考虑添加 Token 缓存机制优化

### Q4: 我可以只迁移部分接口吗？

**A:**
- 可以！新旧方式可以共存
- 推荐逐步迁移，先迁移新功能
- 最终目标是全部使用新方式

### Q5: 如何调试认证问题？

**A:**
1. 检查日志：中间件会打印 Token 验证失败信息
2. 检查白名单：确认路径配置正确
3. 检查 Token：确认 Token 格式和有效性
4. 临时禁用：`enable=False` 快速排查

## 最佳实践

### ✅ 推荐做法

1. **使用全局认证中间件**
   ```python
   app.add_middleware(AuthMiddleware, enable=True)
   ```

2. **在配置文件中维护白名单**
   ```python
   # app/core/auth_config.py
   PUBLIC_PATHS.add("/api/public/new-endpoint")
   ```

3. **使用 get_current_user_from_request() 获取用户**
   ```python
   user = get_current_user_from_request(request)
   ```

4. **为公开接口添加注释说明**
   ```python
   # 这个接口在白名单中，不需要认证
   "/api/public/info"
   ```

### ❌ 不推荐做法

1. **混乱的认证方式**
   - 有些用 CurrentUser，有些用全局中间件
   - 建议统一使用全局中间件

2. **分散的白名单配置**
   - 不要在代码中硬编码白名单判断
   - 统一在 `auth_config.py` 中管理

3. **过度使用白名单**
   - 不要把所有接口都加入白名单
   - 遵循"默认需要认证"的原则

## 总结

全局认证中间件带来的好处：

- 🎯 **安全性更高**：默认需要认证
- 📝 **配置集中**：白名单统一管理
- 🚀 **易于维护**：不需要每个路由单独配置
- 🔧 **灵活控制**：可以启用/禁用
- 🎨 **代码简洁**：减少重复代码

开始使用全局认证中间件，让你的 API 更安全、更易维护！

详细使用说明请参考：[GLOBAL_AUTH.md](./GLOBAL_AUTH.md)

