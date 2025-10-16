# Vercel 部署指南

## 部署步骤

### 1. 推送代码到 GitHub

确保所有更改已提交并推送到 GitHub：

```bash
git add .
git commit -m "配置 Vercel 部署"
git push origin master
```

### 2. Vercel 项目配置

在 Vercel 控制台中配置项目时，使用以下设置：

#### 构建设置
- **Framework Preset**: `FastAPI`
- **Root Directory**: `./`
- **Build Command**: 留空（None）
- **Output Directory**: `N/A`
- **Install Command**: `pip install -r requirements.txt`

#### 环境变量

在 Vercel 项目的 **Settings** → **Environment Variables** 中添加以下环境变量：

```
APP_NAME=Face Flip Server
APP_VERSION=0.1.0
DEBUG=False
HOST=0.0.0.0
PORT=8000

# CORS - 根据你的前端域名修改
CORS_ORIGINS=["https://your-frontend-domain.vercel.app", "http://localhost:3000"]

# Supabase 配置
SUPABASE_URL=https://ynjlmthakbamarannuxe.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluamxtdGhha2JhbWFyYW5udXhlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyOTA2MjgsImV4cCI6MjA3NTg2NjYyOH0.PpjxgiUmrHVvkyPImS6NmoccT-SUpa5uLtSzIkonFYQ
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluamxtdGhha2JhbWFyYW5udXhlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDI5MDYyOCwiZXhwIjoyMDc1ODY2NjI4fQ.q4rgmSfeakidr44TMF3jY1tRksWJ_Ma7vgbZsoDp2K0

# JWT 配置
SECRET_KEY=m5lUYxOjBqabbhoJ7Bofm/Lauaii8RzqD1goG5+47uDvdlob7LuQKhG8Gz5NxRiw/e7GTnLGCY57LdScK5KtOw==
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 文件上传配置
MAX_UPLOAD_SIZE=10485760
UPLOAD_FOLDER=uploads

# 日志配置
LOG_LEVEL=INFO
```

### 3. 部署

1. 在 Vercel 控制台点击 **Deploy**
2. 等待构建完成
3. 部署成功后，访问生成的 URL 测试 API

### 4. 测试部署

部署成功后，访问以下端点测试：

- **根路径**: `https://your-project.vercel.app/`
- **健康检查**: `https://your-project.vercel.app/health`
- **API 文档**: `https://your-project.vercel.app/docs` （仅在 DEBUG=True 时可用）

## 重要说明

### Python 版本
- Vercel 支持 Python 3.12
- 项目已配置为使用 Python 3.12

### 文件上传限制
- Vercel Serverless Functions 有 4.5MB 的请求体限制
- 如果需要上传大文件，建议使用外部存储服务（如 Supabase Storage、AWS S3 等）

### Serverless 函数超时
- Vercel Hobby 计划：10秒超时
- Vercel Pro 计划：60秒超时
- 确保 API 响应时间在限制范围内

### CORS 配置
- 在生产环境中，请将 `CORS_ORIGINS` 设置为具体的前端域名
- 不要在生产环境中使用 `["*"]`

### 环境变量
- 确保所有敏感信息（如 SECRET_KEY、SUPABASE_KEY）都通过 Vercel 环境变量设置
- 不要将敏感信息提交到代码仓库

## 常见问题

### 1. 构建失败：找不到模块

确保 `requirements.txt` 包含所有依赖项。

### 2. 运行时错误：找不到 app 模块

确保项目结构正确，`api/index.py` 正确导入了 `app.main.app`。

### 3. CORS 错误

检查 `CORS_ORIGINS` 环境变量是否包含前端域名。

### 4. 环境变量未生效

- 确保在 Vercel 控制台中正确设置了环境变量
- 重新部署项目以应用新的环境变量

## 本地测试

在部署到 Vercel 之前，可以在本地测试：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行服务器
python run.py

# 或使用 uvicorn
uvicorn app.main:app --reload
```

## 监控和日志

在 Vercel 控制台的 **Deployments** 页面可以查看：
- 部署状态
- 构建日志
- 运行时日志
- 错误信息

## 自定义域名

在 Vercel 控制台的 **Settings** → **Domains** 中可以添加自定义域名。

