# Vercel 部署指南

## 前置条件

✅ 已更新以下文件以支持 Vercel 部署：
- `api/index.py` - 添加了 AuthMiddleware 和日志配置
- `.vercelignore` - 更新了忽略规则

## 部署步骤

### 1. 提交新文件到 Git

```bash
# 查看状态
git status

# 添加所有新文件
git add app/middleware/auth.py
git add app/core/auth_config.py
git add app/core/logging_config.py
git add api/index.py
git add .vercelignore

# 提交
git commit -m "feat: 添加全局认证中间件和日志系统

- 实现类似 Spring Security 的全局认证拦截器
- 添加完整的日志记录系统
- 更新 Vercel 部署配置
- 修复 Vercel 部署时的模块导入问题"

# 推送到远程仓库
git push origin master
```

### 2. Vercel 自动部署

如果你已经连接了 Vercel 和 GitHub，推送后 Vercel 会自动部署。

### 3. 手动触发部署

如果需要手动部署：

```bash
# 安装 Vercel CLI（如果还没安装）
npm i -g vercel

# 登录
vercel login

# 部署
vercel --prod
```

## 环境变量配置

确保在 Vercel 项目设置中配置了以下环境变量：

### 必需的环境变量

```bash
# Supabase 配置
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# JWT 配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 应用配置
DEBUG=False
APP_NAME=Face Flip Server
APP_VERSION=0.1.0
```

### 配置方法

1. 访问 Vercel Dashboard
2. 选择你的项目
3. 进入 Settings > Environment Variables
4. 添加上述环境变量
5. 选择环境：Production, Preview, Development

## 常见问题

### 问题 1：ModuleNotFoundError

**错误**：
```
ModuleNotFoundError: No module named 'app.middleware.auth'
```

**原因**：
- 新文件未提交到 git
- Vercel 从 git 部署时找不到文件

**解决**：
```bash
# 确保所有文件已提交
git add .
git commit -m "fix: add missing files"
git push
```

### 问题 2：Import Error

**错误**：
```
ImportError: cannot import name 'AuthMiddleware'
```

**原因**：
- Python 缓存问题
- 文件未正确部署

**解决**：
1. 清除 Vercel 缓存：在 Vercel Dashboard 中 Redeploy
2. 确认文件在 git 仓库中
3. 检查 `.vercelignore` 没有忽略重要文件

### 问题 3：日志文件问题

**错误**：
```
Permission denied: 'logs/app.log'
```

**原因**：
- Vercel 是 serverless 环境，不支持写文件

**解决**：
- `api/index.py` 中已设置 `enable_file_logging=False`
- 使用 `console.log` 查看日志，Vercel 会自动收集

## Vercel 环境特点

### 1. Serverless 环境

- ✅ 无状态
- ✅ 自动扩展
- ❌ 不支持文件系统写入
- ❌ 不支持长连接

### 2. 日志处理

- 日志输出到 stdout/stderr
- Vercel 自动收集日志
- 可在 Vercel Dashboard 查看

### 3. 冷启动

- 函数可能需要几秒钟初始化
- 第一次请求可能较慢
- 后续请求会更快

## 验证部署

部署成功后，测试以下接口：

### 1. 健康检查（公开接口）

```bash
curl https://your-app.vercel.app/health
```

预期响应：
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "status": "healthy",
    "app": "Face Flip Server",
    "version": "0.1.0"
  }
}
```

### 2. 需要认证的接口

```bash
# 没有 Token（应该返回 401）
curl https://your-app.vercel.app/api/users/profile

# 有 Token（应该返回用户信息）
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://your-app.vercel.app/api/users/profile
```

### 3. 查看日志

1. 访问 Vercel Dashboard
2. 选择你的项目
3. 进入 Deployments
4. 点击最新的部署
5. 查看 Function Logs

## 性能优化

### 1. 减少冷启动时间

- 减少依赖包大小
- 使用 Vercel 的预热功能
- 考虑使用 Edge Functions

### 2. 缓存策略

```python
# 在需要的地方添加缓存
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_data(key: str):
    return expensive_operation(key)
```

### 3. 数据库连接池

Supabase 自动管理连接池，无需额外配置。

## 监控和调试

### 1. Vercel Analytics

- 访问 Vercel Dashboard
- 查看 Analytics 标签
- 监控请求量、错误率等

### 2. 日志查询

```bash
# 使用 Vercel CLI 查看日志
vercel logs
```

### 3. 错误追踪

考虑集成第三方错误追踪服务：
- Sentry
- Rollbar
- Bugsnag

## 回滚

如果部署出现问题：

1. 访问 Vercel Dashboard
2. 进入 Deployments
3. 找到上一个正常的部署
4. 点击 "Promote to Production"

## 总结

完成以上步骤后：

1. ✅ 新文件已提交到 git
2. ✅ Vercel 配置已更新
3. ✅ 环境变量已配置
4. ✅ 部署成功并验证
5. ✅ 日志正常输出

现在你的应用应该可以在 Vercel 上正常运行了！🎉

