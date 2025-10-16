# Face Flip Server

一个基于 FastAPI 构建的现代化 Web 服务框架，集成了 Supabase 用户认证和数据库功能。

## ✨ 特性

- 🚀 **FastAPI** - 高性能异步 Web 框架
- 🔐 **认证系统** - 基于 Supabase 的用户认证
- 📦 **模块化架构** - 清晰的项目结构
- 🔒 **安全性** - JWT token、密码加密
- 📝 **API 文档** - 自动生成的 Swagger/ReDoc 文档
- 🛡️ **错误处理** - 全局错误处理中间件
- 📊 **日志记录** - 请求/响应日志中间件
- ⚙️ **配置管理** - 基于环境变量的配置

## 📋 项目结构

```
face-flip-server/
├── app/
│   ├── __init__.py
│   ├── main.py                 # 主应用入口
│   ├── api/                    # API 路由
│   │   ├── __init__.py
│   │   ├── routes.py          # 路由聚合
│   │   └── endpoints/         # API 端点
│   │       ├── auth.py        # 认证端点
│   │       ├── users.py       # 用户端点
│   │       └── health.py      # 健康检查
│   ├── core/                  # 核心功能
│   │   ├── config.py          # 配置管理
│   │   ├── dependencies.py    # 依赖注入
│   │   └── security.py        # 安全工具
│   ├── models/                # 数据模型
│   │   └── user.py
│   ├── schemas/               # Pydantic 模式
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── common.py
│   ├── services/              # 业务逻辑层
│   │   ├── auth_service.py
│   │   └── user_service.py
│   ├── middleware/            # 中间件
│   │   ├── logging.py
│   │   └── error_handler.py
│   └── utils/                 # 工具函数
│       ├── file_handler.py
│       ├── helpers.py
│       └── validators.py
├── pyproject.toml             # 项目依赖配置
├── run.py                     # 开发服务器启动脚本
├── .env.example              # 环境变量示例
└── README.md                 # 项目文档
```

## 🚀 快速开始

### 环境要求

- Python 3.12+
- UV 包管理器 (推荐) 或 pip
- Node.js 16+ (用于前端开发)

### 本地开发

#### 1. 安装依赖

使用 UV (推荐):

```bash
# 安装 UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装后端依赖
uv sync

# 安装前端依赖
cd ui && npm install && cd ..
```

#### 2. 配置环境变量

复制环境变量示例文件:

```bash
cp vercel-env.example .env
```

编辑 `.env` 文件，填写必要的配置：

```env
# Supabase 配置
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
ARK_API_KEY=your-ark-api-key

# JWT 密钥
SECRET_KEY=your-secret-key-change-this-in-production
```

#### 3. 运行服务器

后端开发模式:

```bash
# 使用 UV
uv run python run.py

# 或直接使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

前端开发模式:

```bash
cd ui && npm run dev
```

### 🚀 Vercel 部署

#### 一键部署

```bash
# 使用部署脚本
./deploy.sh

# 或使用 Makefile
make vercel-deploy
```

#### 手动部署

```bash
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 登录 Vercel
vercel login

# 3. 构建项目
make vercel-build

# 4. 部署
vercel --prod
```

#### 环境变量配置

在 Vercel Dashboard 的 Settings > Environment Variables 中设置：

- `SUPABASE_URL` - Supabase 项目 URL
- `SUPABASE_KEY` - Supabase 匿名密钥
- `ARK_API_KEY` - ARK API 密钥
- `SECRET_KEY` - JWT 密钥

详细配置请参考：[Vercel 部署文档](docs/VERCEL_DEPLOYMENT.md)

## 📚 API 文档

服务器启动后，访问以下地址查看 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔌 API 端点

### 认证 (Authentication)

**注意**: 登录/注册由前端直接调用 Supabase JS SDK 完成，后端只负责验证 JWT

- `GET /api/auth/verify` - 验证 token 是否有效
- `GET /api/auth/me` - 获取当前用户信息
- `GET /api/auth/status` - 检查认证状态（可选认证）

### 用户 (Users)

- `GET /api/users/me` - 获取当前用户信息
- `GET /api/users/profile` - 获取用户详细资料

### 健康检查 (Health)

- `GET /api/health` - 健康检查
- `GET /api/health/ping` - Ping 检查

## 🔐 认证流程

本系统采用前后端分离的认证架构：

1. **前端认证**: 使用 Supabase JS SDK 进行用户登录/注册
   ```javascript
   // 前端登录
   const { data } = await supabase.auth.signInWithPassword({
     email: 'user@example.com',
     password: 'password123'
   })
   const accessToken = data.session.access_token
   ```

2. **后端验证**: 在请求头中携带 token，后端自动验证
   ```
   Authorization: Bearer <access-token>
   ```

3. **自动验证**: 使用依赖注入自动完成 JWT 验证
   ```python
   @router.get("/api/endpoint")
   async def endpoint(current_user: CurrentUser):
       # current_user 自动包含验证后的用户信息
       return {"user_id": current_user["id"]}
   ```

详细说明请查看 [认证文档](docs/AUTHENTICATION.md)

## 🛠️ 开发工具

### 代码格式化

```bash
# 使用 Black 格式化代码
uv run black app/

# 使用 Ruff 检查代码
uv run ruff check app/
```

### 类型检查

```bash
uv run mypy app/
```

### 运行测试

```bash
uv run pytest
```

## 📦 依赖包

### 核心依赖

- `fastapi` - Web 框架
- `uvicorn` - ASGI 服务器
- `supabase` - Supabase 客户端
- `pydantic` - 数据验证
- `pydantic-settings` - 配置管理
- `python-jose` - JWT 处理
- `passlib` - 密码加密
- `python-multipart` - 文件上传

### 开发依赖

- `pytest` - 测试框架
- `black` - 代码格式化
- `ruff` - 代码检查
- `mypy` - 类型检查

## 🌍 环境变量

查看 `.env.example` 文件了解所有可用的环境变量配置。

主要配置项：

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `APP_NAME` | 应用名称 | Face Flip Server |
| `DEBUG` | 调试模式 | False |
| `HOST` | 服务器地址 | 0.0.0.0 |
| `PORT` | 服务器端口 | 8000 |
| `SUPABASE_URL` | Supabase 项目 URL | - |
| `SUPABASE_KEY` | Supabase API Key | - |
| `SECRET_KEY` | JWT 密钥 | - |
| `MAX_UPLOAD_SIZE` | 最大上传文件大小 | 10MB |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

如有问题，请提交 Issue 或联系维护者。

