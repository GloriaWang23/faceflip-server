# 认证流程说明

## 📋 架构概述

本系统采用 **前后端分离的认证架构**：

- **前端**: 使用 Supabase JS SDK 进行用户登录/注册
- **后端**: 仅负责验证前端传来的 JWT token

## 🔐 认证流程

### 1. 前端认证流程

#### 1.1 用户注册

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

// 注册新用户
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123',
  options: {
    data: {
      full_name: 'John Doe'
    }
  }
})

if (data.session) {
  const accessToken = data.session.access_token
  // 将 token 保存到本地存储或状态管理
}
```

#### 1.2 用户登录

```javascript
// 登录
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password123'
})

if (data.session) {
  const accessToken = data.session.access_token
  const refreshToken = data.session.refresh_token
  
  // 保存 token
  localStorage.setItem('access_token', accessToken)
  localStorage.setItem('refresh_token', refreshToken)
}
```

#### 1.3 Token 刷新

```javascript
// 当 access_token 过期时，使用 refresh_token 刷新
const { data, error } = await supabase.auth.refreshSession({
  refresh_token: localStorage.getItem('refresh_token')
})

if (data.session) {
  const newAccessToken = data.session.access_token
  localStorage.setItem('access_token', newAccessToken)
}
```

### 2. 后端验证流程

#### 2.1 发送认证请求

前端在调用后端 API 时，需要在请求头中携带 token：

```javascript
// 使用 fetch
fetch('http://localhost:8000/api/users/me', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
})

// 使用 axios
axios.get('http://localhost:8000/api/users/me', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
})
```

#### 2.2 后端自动验证

后端使用依赖注入自动验证 token：

```python
from app.core.dependencies import CurrentUser

@router.get("/protected-route")
async def protected_route(current_user: CurrentUser):
    # current_user 会自动包含验证后的用户信息
    return {"user_id": current_user["id"]}
```

## 🔌 API 端点

### 认证相关

#### `GET /api/auth/verify`
验证 token 是否有效

**请求头:**
```
Authorization: Bearer <access_token>
```

**响应:**
```json
{
  "success": true,
  "message": "Token is valid",
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "user_metadata": {...},
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

#### `GET /api/auth/me`
获取当前用户信息

**请求头:**
```
Authorization: Bearer <access_token>
```

**响应:**
```json
{
  "success": true,
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "user_metadata": {...}
  }
}
```

#### `GET /api/auth/status`
检查认证状态（可选认证）

**请求头（可选）:**
```
Authorization: Bearer <access_token>
```

**响应（已认证）:**
```json
{
  "authenticated": true,
  "user": {...}
}
```

**响应（未认证）:**
```json
{
  "authenticated": false,
  "user": null
}
```

### 用户相关

#### `GET /api/users/me`
获取当前用户信息

**需要认证**: ✅

#### `GET /api/users/profile`
获取用户详细资料

**需要认证**: ✅

## 💻 实现细节

### 依赖注入方式

#### 必需认证

```python
from app.core.dependencies import CurrentUser

@router.get("/endpoint")
async def endpoint(current_user: CurrentUser):
    # 如果 token 无效，会自动返回 401 错误
    # current_user 包含用户信息
    pass
```

#### 可选认证

```python
from app.core.dependencies import OptionalUser

@router.get("/endpoint")
async def endpoint(user: OptionalUser):
    if user:
        # 用户已登录
        pass
    else:
        # 匿名用户
        pass
```

### 用户信息结构

验证成功后，`CurrentUser` 包含以下信息：

```python
{
    "id": "user-uuid",
    "email": "user@example.com",
    "user_metadata": {
        "full_name": "John Doe",
        "avatar_url": "https://...",
        # 其他自定义字段
    },
    "created_at": "2024-01-01T00:00:00Z"
}
```

## 🔒 安全考虑

### 1. Token 存储

**推荐方式:**
- 使用 `httpOnly` cookie（最安全）
- 或使用内存存储（适合 SPA）

**不推荐:**
- ❌ LocalStorage（易受 XSS 攻击）
- ❌ SessionStorage（易受 XSS 攻击）

### 2. Token 过期处理

```javascript
// 前端示例：自动刷新 token
async function fetchWithAuth(url, options = {}) {
  let token = getAccessToken()
  
  let response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`
    }
  })
  
  // 如果 token 过期
  if (response.status === 401) {
    // 尝试刷新 token
    const newToken = await refreshAccessToken()
    
    if (newToken) {
      // 重试请求
      response = await fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          'Authorization': `Bearer ${newToken}`
        }
      })
    } else {
      // 跳转到登录页
      redirectToLogin()
    }
  }
  
  return response
}
```

### 3. CORS 配置

确保在 `.env` 文件中正确配置 CORS：

```env
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

## 🧪 测试认证流程

### 1. 获取 Token

首先在前端使用 Supabase SDK 登录获取 token，或使用 Supabase Dashboard 获取测试 token。

### 2. 测试 API

```bash
# 验证 token
curl -X GET "http://localhost:8000/api/auth/verify" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 获取用户信息
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 检查认证状态（不带 token）
curl -X GET "http://localhost:8000/api/auth/status"

# 检查认证状态（带 token）
curl -X GET "http://localhost:8000/api/auth/status" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📝 常见问题

### Q: 如何处理 token 过期？

A: 前端需要实现自动刷新机制：
1. 检测到 401 错误
2. 使用 refresh_token 调用 Supabase 的 refreshSession
3. 更新 access_token
4. 重试原请求

### Q: 后端如何主动验证 token？

A: 使用 `AuthService`:

```python
from app.services.auth_service import AuthService
from app.core.dependencies import get_supabase_client

supabase = get_supabase_client()
auth_service = AuthService(supabase)
user = await auth_service.verify_token(token)
```

### Q: 如何获取其他用户的信息？

A: 需要使用 service_role_key：

```python
# 在 dependencies.py 中创建 admin client
def get_supabase_admin_client():
    return create_client(
        settings.supabase_url, 
        settings.supabase_service_role_key
    )
```

### Q: 前端登出后如何处理？

A: 前端调用 Supabase 登出并清除 token：

```javascript
await supabase.auth.signOut()
localStorage.removeItem('access_token')
localStorage.removeItem('refresh_token')
```

## 🔗 相关资源

- [Supabase Auth 文档](https://supabase.com/docs/guides/auth)
- [JWT 介绍](https://jwt.io/introduction)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

