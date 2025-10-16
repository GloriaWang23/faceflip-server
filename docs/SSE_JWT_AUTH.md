# SSE接口JWT认证集成说明

## 功能概述

SSE（Server-Sent Events）图像生成接口现已集成JWT认证，确保只有经过认证的用户才能访问图像生成功能。

## 实现特性

### 1. 后端认证
- **移除白名单**: SSE接口从公开路径中移除，需要JWT认证
- **用户验证**: 通过认证中间件验证JWT令牌
- **用户信息**: 在SSE事件中包含用户信息
- **操作日志**: 记录用户操作日志

### 2. 前端认证
- **自动获取令牌**: 从Supabase会话中获取JWT访问令牌
- **请求头认证**: 在SSE请求中添加`Authorization: Bearer <token>`头
- **错误处理**: 处理认证失败和权限不足的情况
- **用户反馈**: 友好的错误提示信息

## 技术实现

### 后端实现

#### 1. 认证配置更新
```python
# app/core/auth_config.py
# 从白名单中移除SSE接口
PUBLIC_PATHS = {
    # ... 其他公开路径
    # "/api/faceflip/generate/stream",  # 已移除
}
```

#### 2. SSE接口更新
```python
@router.post("/generate/stream")
async def generate_images_stream(
    request: ImageGenerationRequest,
    http_request: Request
) -> StreamingResponse:
    # 获取当前用户（由认证中间件验证）
    current_user = get_current_user_from_request(http_request)
    if not current_user:
        raise HTTPException(status_code=401, detail="用户未认证或认证已过期")
    
    # 用户信息
    user_id = current_user.get("id")
    user_email = current_user.get("email")
    
    # 记录操作日志
    print(f"用户 {user_email} (ID: {user_id}) 开始生成图像")
```

#### 3. SSE事件增强
```python
# 开始事件包含用户信息
start_event = SSEEvent(
    event="start",
    data={
        "task_id": request.task_id,
        "user_id": user_id,
        "user_email": user_email,
        "message": "开始生成图像..."
    }
)
```

### 前端实现

#### 1. 认证状态管理
```javascript
// useAuth.js - 添加获取令牌方法
const getAccessToken = async () => {
  const { data: { session }, error } = await supabase.auth.getSession()
  if (error) return null
  return session?.access_token || null
}
```

#### 2. SSE请求认证
```javascript
// ImageUpload.vue - 添加JWT认证头
const accessToken = await getAccessToken()
if (!accessToken) {
  throw new Error('无法获取访问令牌，请重新登录')
}

const response = await fetch('/api/v1/faceflip/generate/stream', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`,
  },
  body: JSON.stringify(requestData)
})
```

#### 3. 错误处理
```javascript
if (!response.ok) {
  if (response.status === 401) {
    throw new Error('认证失败，请重新登录')
  } else if (response.status === 403) {
    throw new Error('权限不足，无法访问此功能')
  }
}
```

## 使用流程

### 1. 用户登录
1. 用户通过Supabase认证登录
2. 获取JWT访问令牌
3. 令牌存储在Supabase会话中

### 2. 图像生成请求
1. 前端检查用户认证状态
2. 获取JWT访问令牌
3. 在SSE请求头中添加认证信息
4. 发送请求到后端

### 3. 后端验证
1. 认证中间件验证JWT令牌
2. 提取用户信息
3. 记录操作日志
4. 处理图像生成请求

### 4. SSE事件流
1. 发送包含用户信息的开始事件
2. 处理图像生成过程
3. 发送进度和完成事件
4. 错误时发送包含用户信息的错误事件

## 安全特性

### 1. JWT令牌验证
- 使用Supabase JWT令牌
- 自动验证令牌有效性
- 处理令牌过期情况

### 2. 用户权限控制
- 只有登录用户才能访问
- 用户信息记录在操作日志中
- 防止未授权访问

### 3. 错误处理
- 认证失败时返回401状态码
- 权限不足时返回403状态码
- 友好的用户错误提示

## 配置要求

### 1. 后端配置
确保Supabase配置正确：
```python
# app/core/config.py
supabase_url: str = "your_supabase_url"
supabase_service_role_key: str = "your_service_role_key"
```

### 2. 前端配置
确保Supabase客户端配置正确：
```javascript
// supabase.js
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY
```

## 测试步骤

### 1. 未认证用户测试
1. 未登录状态下访问应用
2. 尝试生成图像
3. 应该显示"请先登录"提示

### 2. 认证用户测试
1. 登录用户账户
2. 上传图片
3. 点击"生成新图像"
4. 应该正常显示SSE事件流

### 3. 令牌过期测试
1. 等待JWT令牌过期
2. 尝试生成图像
3. 应该显示"认证失败，请重新登录"

## 故障排除

### 1. 认证失败
**症状**: 401 Unauthorized错误
**原因**: JWT令牌无效或过期
**解决**: 重新登录获取新令牌

### 2. 权限不足
**症状**: 403 Forbidden错误
**原因**: 用户权限不足
**解决**: 检查用户权限配置

### 3. 令牌获取失败
**症状**: "无法获取访问令牌"错误
**原因**: Supabase会话问题
**解决**: 检查Supabase配置和网络连接

## 监控和日志

### 1. 操作日志
后端会记录用户操作：
```
用户 user@example.com (ID: abc123) 开始生成图像，任务ID: task_1234567890
```

### 2. 认证日志
认证中间件会记录认证状态：
```
🔐 Authenticated user user@example.com - POST /api/v1/faceflip/generate/stream
```

### 3. 错误日志
认证失败时会记录错误信息：
```
⚠️ Token verification failed - POST /api/v1/faceflip/generate/stream
```

## 性能考虑

### 1. 令牌缓存
- JWT令牌在Supabase会话中缓存
- 避免频繁的令牌获取请求
- 自动处理令牌刷新

### 2. 连接复用
- SSE连接保持活跃
- 减少认证开销
- 提高响应速度

现在SSE接口已完全集成JWT认证，确保只有经过认证的用户才能访问图像生成功能！
