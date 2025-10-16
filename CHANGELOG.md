# 更新日志

## [0.1.0] - 2024-10-13

### ✨ 新增功能

#### 认证架构调整
- **前后端分离的认证流程**: 前端使用 Supabase JS SDK 进行登录/注册，后端只负责 JWT 验证
- **简化的 API 端点**: 移除了后端的 signup/signin 端点，只保留 token 验证相关接口
- **灵活的依赖注入**: 
  - `CurrentUser` - 必需认证的依赖
  - `OptionalUser` - 可选认证的依赖

#### API 端点

**认证相关** (`/api/auth/`):
- `GET /verify` - 验证 JWT token 是否有效
- `GET /me` - 获取当前认证用户信息
- `GET /status` - 检查认证状态（支持可选认证）

**用户相关** (`/api/users/`):
- `GET /me` - 获取当前用户基本信息
- `GET /profile` - 获取用户详细资料

**健康检查** (`/api/health/`):
- `GET /` - 综合健康检查
- `GET /ping` - 简单 ping 检查

### 📝 文档

新增以下文档：

1. **AUTHENTICATION.md** - 详细的认证流程说明
   - 前后端认证架构
   - JWT 验证机制
   - API 端点使用说明
   - 安全考虑和最佳实践

2. **FRONTEND_EXAMPLE.md** - 前端集成示例
   - Supabase Client 配置
   - React 完整示例（Context, Hooks）
   - API 客户端封装
   - Token 自动刷新

3. **更新 README.md** - 反映新的认证流程
4. **更新 QUICKSTART.md** - 添加前端认证示例

### 🔧 核心变更

#### `app/core/dependencies.py`
- ✅ 新增 `verify_jwt_token` - JWT 验证函数
- ✅ 新增 `get_optional_user` - 可选认证函数
- ✅ 更新类型别名 `CurrentUser` 和 `OptionalUser`

#### `app/api/endpoints/auth.py`
- ❌ 移除 `POST /signup` 端点
- ❌ 移除 `POST /signin` 端点
- ❌ 移除 `POST /signout` 端点
- ❌ 移除 `POST /refresh` 端点
- ✅ 新增 `GET /verify` 端点
- ✅ 新增 `GET /me` 端点
- ✅ 新增 `GET /status` 端点

#### `app/api/endpoints/users.py`
- 🔄 简化 `GET /me` - 直接返回用户信息
- ✅ 新增 `GET /profile` - 返回详细资料

#### `app/services/auth_service.py`
- ❌ 移除 `sign_up` 方法
- ❌ 移除 `sign_in` 方法
- ❌ 移除 `sign_out` 方法
- ❌ 移除 `refresh_token` 方法
- ✅ 保留并优化 `verify_token` 方法
- ✅ 新增 `get_user_by_id` 方法（管理员功能）

### 🏗️ 项目结构

```
face-flip-server/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py      # ✅ 只包含验证端点
│   │   │   ├── users.py     # 🔄 简化用户端点
│   │   │   └── health.py
│   │   └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   ├── dependencies.py  # ✅ 新增 JWT 验证依赖
│   │   └── security.py
│   ├── services/
│   │   ├── auth_service.py  # 🔄 只保留验证功能
│   │   └── user_service.py
│   └── ...
├── docs/
│   ├── AUTHENTICATION.md    # ✅ 新增
│   └── FRONTEND_EXAMPLE.md  # ✅ 新增
└── ...
```

### 💡 使用方式

#### 前端登录

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

// 登录
const { data } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password123'
})

const accessToken = data.session.access_token
```

#### 调用后端 API

```javascript
// 携带 token 请求
fetch('http://localhost:8000/api/users/me', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
})
```

#### 后端端点实现

```python
from app.core.dependencies import CurrentUser

@router.get("/protected")
async def protected_route(current_user: CurrentUser):
    # current_user 自动包含验证后的用户信息
    return {"user_id": current_user["id"]}
```

### 🔒 安全改进

- ✅ JWT 验证由 Supabase 官方 SDK 处理，更安全可靠
- ✅ 前端直接与 Supabase 通信，减少后端密码处理风险
- ✅ 支持可选认证，灵活控制访问权限
- ✅ Token 过期自动处理机制

### 📦 依赖项

无新增依赖，使用现有包：
- `fastapi` - Web 框架
- `supabase` - Supabase 客户端（用于 token 验证）
- `pydantic` - 数据验证

### ⚠️ 破坏性变更

如果您正在使用旧版本的 API，请注意以下变更：

1. **移除的端点** - 以下端点已被移除：
   - `POST /api/auth/signup`
   - `POST /api/auth/signin`
   - `POST /api/auth/signout`
   - `POST /api/auth/refresh`

2. **迁移指南**:
   - 前端应改用 Supabase JS SDK 进行认证
   - 后端 API 调用时需携带 JWT token
   - 使用新的验证端点检查 token 状态

### 🔮 未来计划

- [ ] 添加 OAuth 第三方登录支持（Google, GitHub 等）
- [ ] 实现 Webhook 处理 Supabase 事件
- [ ] 添加用户角色和权限系统
- [ ] 实现 API 速率限制
- [ ] 添加更多示例（Vue, Angular）

---

**完整文档**: 查看 [AUTHENTICATION.md](docs/AUTHENTICATION.md) 了解详细的认证流程

