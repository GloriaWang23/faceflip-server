# 统一响应格式说明

## 📋 响应格式

所有 API 接口**统一返回 HTTP 状态码 200**，通过响应体中的 `code` 字段来标识成功或失败。

### 响应结构

```json
{
  "code": 200,
  "msg": "成功",
  "data": {}
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | int | 业务状态码，200 表示成功，其他表示失败 |
| `msg` | string | 响应消息 |
| `data` | any | 响应数据，可以是对象、数组或 null |

## ✅ 成功响应

### 示例 1：返回对象数据

```json
{
  "code": 200,
  "msg": "成功",
  "data": {
    "user": {
      "id": "123456",
      "email": "user@example.com",
      "user_metadata": {
        "full_name": "张三"
      }
    }
  }
}
```

### 示例 2：返回数组数据

```json
{
  "code": 200,
  "msg": "成功",
  "data": {
    "list": [
      {"id": 1, "name": "项目1"},
      {"id": 2, "name": "项目2"}
    ],
    "total": 2
  }
}
```

### 示例 3：无返回数据

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": null
}
```

## ❌ 错误响应

### 客户端错误 (400-499)

```json
{
  "code": 400,
  "msg": "请求参数错误",
  "data": null
}
```

### 认证错误 (1000-1099)

```json
{
  "code": 1001,
  "msg": "Token 无效或已过期",
  "data": null
}
```

### 数据验证错误

```json
{
  "code": 422,
  "msg": "数据验证失败",
  "data": {
    "errors": [
      {
        "loc": ["body", "email"],
        "msg": "value is not a valid email address",
        "type": "value_error.email"
      }
    ],
    "messages": [
      "body.email: value is not a valid email address"
    ]
  }
}
```

### 服务器错误 (9000-9999)

```json
{
  "code": 9000,
  "msg": "服务器内部错误: division by zero",
  "data": null
}
```

## 🔢 错误码定义

### 成功码

| Code | 说明 |
|------|------|
| 200 | 成功 |

### 客户端错误 (400-499)

| Code | 说明 |
|------|------|
| 400 | 请求参数错误 |
| 401 | 未授权，请先登录 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 405 | 请求方法不允许 |
| 422 | 数据验证失败 |

### 认证相关错误 (1000-1099)

| Code | 说明 |
|------|------|
| 1001 | Token 无效 |
| 1002 | Token 已过期 |
| 1003 | 缺少 Token |
| 1004 | 认证失败 |

### 用户相关错误 (2000-2099)

| Code | 说明 |
|------|------|
| 2001 | 用户不存在 |
| 2002 | 用户已存在 |
| 2003 | 用户已被禁用 |

### 业务错误 (3000-3099)

| Code | 说明 |
|------|------|
| 3000 | 业务处理失败 |

### 文件相关错误 (4000-4099)

| Code | 说明 |
|------|------|
| 4001 | 文件大小超出限制 |
| 4002 | 文件类型不允许 |
| 4003 | 文件上传失败 |

### 数据库错误 (5000-5099)

| Code | 说明 |
|------|------|
| 5001 | 数据库操作失败 |

### 服务器错误 (9000-9999)

| Code | 说明 |
|------|------|
| 9000 | 服务器内部错误 |
| 9001 | 服务暂时不可用 |
| 9002 | 第三方服务错误 |

## 💻 后端使用

### 成功响应

```python
from app.core.response import success

@router.get("/example")
async def example():
    return success(
        data={"message": "Hello World"},
        msg="查询成功"  # 可选，默认为"成功"
    )
```

### 错误响应

```python
from app.core.response import error
from app.core.response_code import ResponseCode

@router.get("/example")
async def example():
    # 使用预定义的错误码
    return error(
        code=ResponseCode.USER_NOT_FOUND,
        msg="用户不存在"  # 可选，会覆盖默认消息
    )
```

### 抛出异常（会被全局异常处理器捕获）

```python
from starlette.exceptions import HTTPException
from app.core.response_code import ResponseCode

@router.get("/example")
async def example():
    # 方式1: 使用自定义错误码
    raise HTTPException(
        status_code=400,
        detail=f"{ResponseCode.USER_NOT_FOUND.code}|用户不存在"
    )
    
    # 方式2: 使用标准 HTTP 状态码（会自动映射）
    raise HTTPException(
        status_code=404,
        detail="资源未找到"
    )
```

### 自定义错误码

```python
from app.core.response import ResponseUtil

@router.get("/example")
async def example():
    return ResponseUtil.custom(
        code=5000,
        msg="自定义错误消息",
        data={"detail": "详细信息"}
    )
```

## 🌐 前端使用

### JavaScript/TypeScript

```typescript
// 响应接口定义
interface ApiResponse<T = any> {
  code: number
  msg: string
  data: T | null
}

// 请求封装
async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options)
  const result: ApiResponse<T> = await response.json()
  
  // 判断业务状态码
  if (result.code === 200) {
    return result.data as T
  } else {
    throw new Error(`[${result.code}] ${result.msg}`)
  }
}

// 使用示例
try {
  const data = await request<{user: User}>('/api/users/me', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  console.log('用户信息:', data.user)
} catch (error) {
  console.error('请求失败:', error.message)
  
  // 根据错误码进行处理
  if (error.message.includes('[1001]')) {
    // Token 无效，跳转登录页
    redirectToLogin()
  }
}
```

### Axios 拦截器

```typescript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000'
})

// 响应拦截器
api.interceptors.response.use(
  response => {
    const { code, msg, data } = response.data
    
    if (code === 200) {
      return data
    } else {
      // 业务错误
      const error = new Error(msg)
      error.code = code
      
      // 根据错误码处理
      if (code === 1001 || code === 1002) {
        // Token 无效或过期
        window.location.href = '/login'
      }
      
      return Promise.reject(error)
    }
  },
  error => {
    return Promise.reject(error)
  }
)

// 使用
api.get('/api/users/me')
  .then(data => {
    console.log('用户信息:', data.user)
  })
  .catch(error => {
    console.error('错误:', error.message)
  })
```

## 📝 测试示例

### cURL 测试

```bash
# 成功响应
curl http://localhost:8000/api/health/ping
# {"code":200,"msg":"成功","data":{"message":"pong"}}

# 认证失败
curl http://localhost:8000/api/users/me
# {"code":401,"msg":"未授权，请先登录","data":null}

# 带 Token 请求
curl http://localhost:8000/api/users/me \
  -H "Authorization: Bearer YOUR_TOKEN"
# {"code":200,"msg":"成功","data":{"user":{...}}}

# Token 无效
curl http://localhost:8000/api/users/me \
  -H "Authorization: Bearer invalid-token"
# {"code":1001,"msg":"Token 无效或已过期","data":null}
```

## 🎯 最佳实践

### 1. 统一错误处理

前端应该有统一的错误处理机制：

```typescript
// 错误处理映射
const errorHandlers = {
  1001: () => redirectToLogin(),  // Token 无效
  1002: () => refreshToken(),     // Token 过期
  2001: () => showNotFound(),     // 用户不存在
  9000: () => showError('服务器错误')
}

function handleError(code: number, msg: string) {
  const handler = errorHandlers[code]
  if (handler) {
    handler()
  } else {
    showToast(msg)
  }
}
```

### 2. TypeScript 类型定义

```typescript
// 错误码枚举
enum ResponseCode {
  SUCCESS = 200,
  BAD_REQUEST = 400,
  UNAUTHORIZED = 401,
  TOKEN_INVALID = 1001,
  TOKEN_EXPIRED = 1002,
  USER_NOT_FOUND = 2001,
  INTERNAL_ERROR = 9000
}

// 响应类型
interface ApiResponse<T = any> {
  code: ResponseCode
  msg: string
  data: T | null
}
```

### 3. 错误日志

后端所有异常都会打印详细的堆栈信息，便于调试：

```python
# 全局异常处理会自动打印
❌ Unhandled error: division by zero
Traceback (most recent call last):
  File "/app/api/endpoints/example.py", line 10, in example
    result = 1 / 0
ZeroDivisionError: division by zero
```

## 🔗 相关文档

- [认证流程](AUTHENTICATION.md)
- [API 接口文档](http://localhost:8000/docs)
- [错误码定义](../app/core/response_code.py)

