# Java 与 Python ResponseCode 映射

## 📋 完全兼容的错误码

这些错误码与 Java `ResultCode` 完全一致：

| Java 枚举 | Python 枚举 | Code | Message |
|-----------|-------------|------|---------|
| `SUCCESS` | `SUCCESS` | 200 | "success" |
| `E_SYSTEM_BUSY` | `E_SYSTEM_BUSY` | 500 | "system busy" |
| `E_SYSTEM_UNAVAILABLE` | `E_SYSTEM_UNAVAILABLE` | 11002 | "service is unavailable" |
| `E_INVALID_PARAM` | `E_INVALID_PARAM` | 12001 | "param invalid" |
| `E_USER_NOT_FOUND` | `E_USER_NOT_FOUND` | 13001 | "user not found" |
| `E_TOKEN_EXPIRED` | `E_TOKEN_EXPIRED` | 13002 | "token expired" |
| `E_TOKEN_NOT_VALID` | `E_TOKEN_NOT_VALID` | 13003 | "token not valid" |
| `E_ITEM_NOT_EXIST` | `E_ITEM_NOT_EXIST` | 14001 | "item not exist" |
| `E_ITEM_FORBIDDEN` | `E_ITEM_FORBIDDEN` | 14002 | "item forbidden" |

## 🔧 扩展的错误码

Python 额外扩展的错误码（不在 Java 中）：

### HTTP 标准错误 (400-499)

| Python 枚举 | Code | Message |
|-------------|------|---------|
| `BAD_REQUEST` | 400 | "bad request" |
| `UNAUTHORIZED` | 401 | "unauthorized" |
| `FORBIDDEN` | 403 | "forbidden" |
| `NOT_FOUND` | 404 | "not found" |
| `METHOD_NOT_ALLOWED` | 405 | "method not allowed" |
| `VALIDATION_ERROR` | 422 | "validation error" |

### 认证相关扩展 (13xxx)

| Python 枚举 | Code | Message |
|-------------|------|---------|
| `TOKEN_MISSING` | 13004 | "token missing" |
| `AUTH_FAILED` | 13005 | "authentication failed" |
| `USER_ALREADY_EXISTS` | 13006 | "user already exists" |
| `USER_DISABLED` | 13007 | "user disabled" |

### 业务错误 (15xxx)

| Python 枚举 | Code | Message |
|-------------|------|---------|
| `BUSINESS_ERROR` | 15000 | "business error" |

### 文件相关 (16xxx)

| Python 枚举 | Code | Message |
|-------------|------|---------|
| `FILE_TOO_LARGE` | 16001 | "file too large" |
| `FILE_TYPE_NOT_ALLOWED` | 16002 | "file type not allowed" |
| `FILE_UPLOAD_FAILED` | 16003 | "file upload failed" |

### 数据库错误 (17xxx)

| Python 枚举 | Code | Message |
|-------------|------|---------|
| `DATABASE_ERROR` | 17001 | "database error" |

### 第三方服务 (18xxx)

| Python 枚举 | Code | Message |
|-------------|------|---------|
| `THIRD_PARTY_ERROR` | 18001 | "third party service error" |

## 💻 使用示例

### Java 代码

```java
// 成功
return Result.success(data);

// 错误
return Result.error(ResultCode.E_USER_NOT_FOUND);

// 抛出异常
throw new BusinessException(ResultCode.E_TOKEN_EXPIRED);
```

### Python 代码

```python
from app.core.response import success, error
from app.core.response_code import ResponseCode

# 成功
return success(data=user_data)

# 错误
return error(code=ResponseCode.E_USER_NOT_FOUND)

# 抛出异常
from starlette.exceptions import HTTPException
raise HTTPException(
    status_code=401,
    detail=f"{ResponseCode.E_TOKEN_EXPIRED.code}|token expired"
)
```

## 🔄 错误码规划

### 当前分配

- **200**: 成功
- **400-499**: HTTP 标准错误
- **500**: 系统繁忙
- **11xxx**: 系统级错误
- **12xxx**: 参数错误
- **13xxx**: 认证/用户错误
- **14xxx**: 资源/项目错误
- **15xxx**: 业务错误
- **16xxx**: 文件错误
- **17xxx**: 数据库错误
- **18xxx**: 第三方服务错误

### 预留区间

- **19xxx**: 预留
- **20xxx+**: 自定义业务错误码

## 📝 方法兼容性

Python 的 `ResponseCode` 枚举提供了与 Java 兼容的方法：

```python
code = ResponseCode.E_TOKEN_EXPIRED

# Java 风格的 getter 方法
code.get_code()  # 返回 13002
code.get_msg()   # 返回 "token expired"

# Python 风格的属性访问
code.code        # 返回 13002
code.message     # 返回 "token expired"
code.msg         # 返回 "token expired" (兼容)
```

## 🎯 响应格式对比

### Java 响应格式

```json
{
  "code": 200,
  "msg": "success",
  "data": {}
}
```

### Python 响应格式

```json
{
  "code": 200,
  "msg": "success",
  "data": {}
}
```

**完全一致！** ✅

## 🔗 相关文档

- [ResponseCode 定义](../app/core/response_code.py)
- [响应格式文档](RESPONSE_FORMAT.md)
- [认证流程](AUTHENTICATION.md)

