# 日志系统使用指南

## 概述

本项目已经为所有异常处理和关键操作添加了完整的日志记录，使用 Python 标准的 `logging` 模块。

## 日志级别

系统使用以下日志级别：

| 级别 | 用途 | 示例 |
|------|------|------|
| **DEBUG** | 调试信息，详细的执行流程 | 函数调用、参数值 |
| **INFO** | 一般信息，重要的业务操作 | 用户登录、数据更新 |
| **WARNING** | 警告信息，可能的问题 | Token 验证失败、资源未找到 |
| **ERROR** | 错误信息，需要关注 | 异常捕获、系统错误 |
| **CRITICAL** | 严重错误，系统级问题 | 数据库连接失败、服务崩溃 |

## 日志配置

### 1. 基础配置

在 `app/main.py` 中已经初始化了日志系统：

```python
from app.core.logging_config import setup_logging

# 初始化日志系统
setup_logging(
    log_level="DEBUG" if settings.debug else "INFO",
    enable_file_logging=False  # 设置为 True 启用文件日志
)
```

### 2. 配置选项

在 `app/core/logging_config.py` 中可以配置：

- **log_level**: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **log_file**: 日志文件路径（可选）
- **enable_file_logging**: 是否启用文件日志

### 3. 启用文件日志

修改 `app/main.py`：

```python
setup_logging(
    log_level="INFO",
    enable_file_logging=True,  # 启用文件日志
    log_file="logs/app.log"     # 可选，默认为 logs/app.log
)
```

启用后会生成：
- `logs/app.log` - 所有日志
- `logs/error.log` - 仅错误日志

## 日志使用示例

### 1. 在模块中使用日志

```python
import logging

# 在文件顶部获取 logger
logger = logging.getLogger(__name__)

class MyService:
    def my_function(self, param: str):
        try:
            logger.debug(f"🔍 Starting my_function with param: {param}")
            
            # 业务逻辑
            result = do_something(param)
            
            logger.info(f"✅ Operation completed successfully")
            return result
            
        except ValueError as e:
            logger.warning(f"⚠️  Invalid parameter: {str(e)}")
            return None
            
        except Exception as e:
            logger.error(
                f"❌ Unexpected error: {type(e).__name__}: {str(e)}",
                exc_info=True  # 包含完整的堆栈跟踪
            )
            raise
```

### 2. 日志格式规范

使用表情符号前缀来快速识别日志类型：

- 🔍 **DEBUG** - 调试、查询
- ✅ **SUCCESS** - 操作成功
- ⚠️ **WARNING** - 警告、问题
- ❌ **ERROR** - 错误、失败
- 🔐 **AUTH** - 认证相关
- 🔓 **PUBLIC** - 公开访问
- 🗑️ **DELETE** - 删除操作
- 🔄 **UPDATE** - 更新操作
- 📋 **CONFIG** - 配置相关
- 🚀 **STARTUP** - 启动相关

### 3. 异常日志

记录异常时使用 `exc_info=True` 来包含完整的堆栈跟踪：

```python
try:
    risky_operation()
except Exception as e:
    logger.error(
        f"❌ Operation failed: {type(e).__name__}: {str(e)}",
        exc_info=True  # 这会包含完整的堆栈跟踪
    )
```

### 4. 包含上下文信息

使用 `extra` 参数添加结构化的上下文信息：

```python
logger.error(
    f"❌ Request failed",
    exc_info=True,
    extra={
        "user_id": user_id,
        "path": request.url.path,
        "method": request.method,
        "client_ip": request.client.host
    }
)
```

## 已添加日志的模块

### 1. 认证中间件 (`app/middleware/auth.py`)

**日志内容**：
- Supabase 客户端初始化
- Token 验证过程
- 认证成功/失败
- 公开路径访问
- 认证错误详情

**示例日志**：
```
INFO - ✅ Token verified successfully for user: user@example.com
WARNING - ⚠️  Missing authorization header - GET /api/users/profile
ERROR - ❌ Token verification exception: HTTPError: 401 Unauthorized
```

### 2. 错误处理中间件 (`app/middleware/error_handler.py`)

**日志内容**：
- 未处理的异常
- 数据验证错误
- HTTP 异常
- 完整的堆栈跟踪

**示例日志**：
```
ERROR - ❌ Unhandled exception in GET /api/orders
Exception type: ValueError
Exception message: Invalid order ID
Traceback: ...
```

### 3. 依赖注入 (`app/core/dependencies.py`)

**日志内容**：
- Supabase 客户端创建
- JWT Token 验证
- 可选认证处理

**示例日志**：
```
DEBUG - 🔍 Verifying JWT token (length: 156)
INFO - ✅ Token verified for user: user@example.com
WARNING - ⚠️  Token verification failed: invalid response from Supabase
```

### 4. 认证服务 (`app/services/auth_service.py`)

**日志内容**：
- Token 验证
- 用户查询
- 认证错误

**示例日志**：
```
DEBUG - 🔍 [AuthService] Verifying token (length: 156)
INFO - ✅ [AuthService] Token verified successfully for user: user@example.com
ERROR - ❌ [AuthService] Token verification error: HTTPError: ...
```

### 5. 用户服务 (`app/services/user_service.py`)

**日志内容**：
- 用户查询
- 用户更新
- 用户删除（软删除）
- 数据库操作错误

**示例日志**：
```
DEBUG - 🔍 [UserService] Getting user by ID: 123
INFO - ✅ [UserService] User updated successfully: 123
WARNING - ⚠️  [UserService] User not found: 456
```

## 日志输出格式

### DEBUG 模式（详细）

```
2024-10-16 10:30:45 - app.middleware.auth - INFO - [auth.py:100] - ✅ Token verified successfully for user: user@example.com
```

格式：`时间 - 模块名 - 级别 - [文件:行号] - 消息`

### PRODUCTION 模式（简洁）

```
2024-10-16 10:30:45 - app.middleware.auth - INFO - ✅ Token verified successfully for user: user@example.com
```

格式：`时间 - 模块名 - 级别 - 消息`

## 日志查看和分析

### 1. 实时查看日志

```bash
# 启动服务器，日志会输出到控制台
uv run python run.py

# 如果启用了文件日志，可以实时查看
tail -f logs/app.log
```

### 2. 过滤特定日志

```bash
# 只看错误日志
tail -f logs/error.log

# 或者过滤控制台输出
uv run python run.py 2>&1 | grep "ERROR"

# 查看特定模块的日志
uv run python run.py 2>&1 | grep "AuthService"
```

### 3. 搜索特定事件

```bash
# 查找特定用户的所有日志
grep "user@example.com" logs/app.log

# 查找所有认证失败
grep "Token verification failed" logs/app.log

# 查找特定时间段的日志
grep "2024-10-16 10:" logs/app.log
```

## 最佳实践

### ✅ 推荐做法

1. **使用合适的日志级别**
   ```python
   logger.debug("详细的调试信息")      # 仅在开发时
   logger.info("重要的业务操作")       # 生产环境
   logger.warning("可能的问题")        # 需要关注
   logger.error("错误信息")           # 需要处理
   ```

2. **包含足够的上下文**
   ```python
   logger.error(
       f"❌ Failed to process order {order_id} for user {user_id}",
       exc_info=True,
       extra={"order_id": order_id, "user_id": user_id}
   )
   ```

3. **使用 f-string 格式化**
   ```python
   logger.info(f"✅ User {user_id} completed action {action}")
   ```

4. **记录异常时使用 exc_info=True**
   ```python
   except Exception as e:
       logger.error("❌ Operation failed", exc_info=True)
   ```

5. **敏感信息脱敏**
   ```python
   # ❌ 不要记录完整的密码、Token
   logger.debug(f"Token: {token}")
   
   # ✅ 只记录前后几位
   logger.debug(f"Token: {token[:10]}...{token[-10:]}")
   ```

### ❌ 避免的做法

1. **不要使用 print()**
   ```python
   # ❌ 错误
   print(f"Error: {e}")
   
   # ✅ 正确
   logger.error(f"❌ Error: {e}", exc_info=True)
   ```

2. **不要记录过多的调试信息**
   ```python
   # ❌ 过度日志
   logger.debug("Starting function")
   logger.debug("Checking parameter")
   logger.debug("Validating input")
   
   # ✅ 合理日志
   logger.debug(f"Processing request with params: {params}")
   ```

3. **不要忽略异常**
   ```python
   # ❌ 静默失败
   try:
       risky_operation()
   except:
       pass
   
   # ✅ 记录异常
   try:
       risky_operation()
   except Exception as e:
       logger.error("❌ Operation failed", exc_info=True)
       raise
   ```

## 生产环境配置

### 1. 推荐配置

```python
setup_logging(
    log_level="INFO",           # 生产环境使用 INFO
    enable_file_logging=True,   # 启用文件日志
)
```

### 2. 日志轮转

可以使用 Python 的 `RotatingFileHandler` 或 `TimedRotatingFileHandler`：

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5                # 保留 5 个备份
)
```

### 3. 集中式日志管理

在生产环境中，建议使用集中式日志管理工具：

- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Grafana Loki**
- **CloudWatch** (AWS)
- **Stackdriver** (GCP)

## 故障排查

### 问题 1：日志没有输出

**检查项**：
1. 确认日志级别配置正确
2. 检查 logger 是否正确初始化
3. 验证日志配置是否在应用启动时执行

### 问题 2：日志输出太多

**解决方案**：
1. 提高日志级别（DEBUG → INFO → WARNING）
2. 为第三方库设置更高的日志级别
3. 使用日志过滤器

### 问题 3：日志文件过大

**解决方案**：
1. 启用日志轮转
2. 定期清理旧日志
3. 使用更高的日志级别

## 总结

现在系统已经为所有异常处理添加了完整的日志记录：

- ✅ **认证中间件** - 完整的认证流程日志
- ✅ **错误处理** - 所有异常都被记录
- ✅ **服务层** - 业务操作和错误日志
- ✅ **依赖注入** - Token 验证日志
- ✅ **结构化日志** - 统一的格式和上下文

使用这些日志可以：
- 🔍 快速定位问题
- 📊 分析用户行为
- 🛡️ 安全审计
- 📈 性能监控

