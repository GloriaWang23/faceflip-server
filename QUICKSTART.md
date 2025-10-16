# 快速开始指南

## 🚀 5 分钟快速启动

### 步骤 1: 安装依赖

```bash
# 运行自动设置脚本（推荐）
bash setup.sh

# 或手动安装
uv sync
```

### 步骤 2: 配置环境变量

编辑 `.env` 文件，填写必要的配置：

```env
# 必填项
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here

# 可选项（有默认值）
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
PORT=8000
```

### 步骤 3: 启动服务器

```bash
# 使用 make 命令
make run

# 或直接运行
uv run python run.py

# 或使用 uvicorn
uvicorn app.main:app --reload
```

### 步骤 4: 访问 API 文档

打开浏览器访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📝 常用命令

```bash
# 开发相关
make run          # 启动开发服务器
make test         # 运行测试
make format       # 格式化代码
make lint         # 代码检查

# Docker 相关
make docker-build # 构建 Docker 镜像
make docker-up    # 启动 Docker 容器
make docker-down  # 停止 Docker 容器

# 其他
make clean        # 清理缓存文件
make help         # 查看所有命令
```

## 🔌 API 使用示例

### 认证流程说明

**重要**: 本系统的登录/注册由前端使用 Supabase JS SDK 完成，后端只负责验证 JWT token。

### 1. 前端登录（使用 Supabase JS SDK）

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

### 2. 验证 Token

```bash
curl -X GET "http://localhost:8000/api/auth/verify" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. 获取用户信息

```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. 检查认证状态

```bash
# 不带 token - 返回未认证
curl -X GET "http://localhost:8000/api/auth/status"

# 带 token - 返回用户信息
curl -X GET "http://localhost:8000/api/auth/status" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🐳 使用 Docker

### Docker Compose（推荐）

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 手动 Docker

```bash
# 构建镜像
docker build -t face-flip-server .

# 运行容器
docker run -p 8000:8000 --env-file .env face-flip-server
```

## 🧪 运行测试

```bash
# 运行所有测试
make test

# 或使用 pytest
uv run pytest

# 运行特定测试文件
uv run pytest tests/test_main.py

# 查看测试覆盖率
uv run pytest --cov=app tests/
```

## 🔧 开发工作流

### 1. 创建新的 API 端点

在 `app/api/endpoints/` 创建新文件：

```python
# app/api/endpoints/posts.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_posts():
    return {"posts": []}
```

在 `app/api/routes.py` 中注册：

```python
from app.api.endpoints import posts

api_router.include_router(
    posts.router,
    prefix="/posts",
    tags=["posts"]
)
```

### 2. 添加新的 Schema

在 `app/schemas/` 创建：

```python
# app/schemas/post.py
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str
```

### 3. 创建服务层

在 `app/services/` 创建：

```python
# app/services/post_service.py
class PostService:
    def __init__(self, supabase_client):
        self.supabase = supabase_client
    
    async def create_post(self, data):
        # 业务逻辑
        pass
```

## 🐛 常见问题

### Q: 启动时提示 Supabase 配置缺失

**A:** 检查 `.env` 文件，确保 `SUPABASE_URL` 和 `SUPABASE_KEY` 已正确配置。

### Q: 如何启用/禁用调试模式？

**A:** 在 `.env` 文件中设置 `DEBUG=True` 或 `DEBUG=False`。

### Q: 端口被占用怎么办？

**A:** 在 `.env` 文件中修改 `PORT` 为其他可用端口。

### Q: 如何添加 CORS 白名单？

**A:** 在 `.env` 文件中修改 `CORS_ORIGINS`：
```env
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

## 📚 进一步学习

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Supabase 文档](https://supabase.com/docs)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [项目完整文档](README.md)

## 🤝 获取帮助

- 查看 [README.md](README.md) 了解详细信息
- 查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献
- 提交 Issue 报告问题或建议
- 查看项目 Wiki（如果有）

---

祝您开发愉快！🎉

