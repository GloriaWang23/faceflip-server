# Vercel 部署指南

## 🚀 快速部署

### 1. 安装 Vercel CLI
```bash
npm install -g vercel
```

### 2. 登录 Vercel
```bash
vercel login
```

### 3. 一键部署
```bash
# 构建并部署到 Vercel
make vercel-deploy
```

## 📋 部署前准备

### 环境变量配置
在 Vercel Dashboard 的 Settings > Environment Variables 中设置以下变量：

#### 必需的环境变量
```bash
# Supabase 配置
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
ARK_API_KEY=your_ark_api_key
SECRET_KEY=your_jwt_secret_key_change_this_in_production
```

#### 可选的环境变量
```bash
# Supabase 服务角色密钥（用于服务端操作）
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# JWT 配置
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ARK 图像生成配置
ARK_DEFAULT_PROMPT=生成3张女孩和奶牛玩偶在游乐园开心地坐过山车的图片，涵盖早晨、中午、晚上
ARK_MODEL=doubao-seedream-4-0-250828
ARK_IMAGE_SIZE=2K
ARK_MAX_IMAGES=3

# Supabase 存储配置
SUPABASE_STORAGE_BUCKET=faceflip-images
```

## 🛠️ 构建命令

### 本地构建测试
```bash
# 构建前后端
make vercel-build

# 或者分别构建
make ui-install  # 安装前端依赖
make ui-build    # 构建前端
```

### Vercel 自动构建
Vercel 会自动执行以下构建步骤：

1. **后端构建**：
   - 使用 `@vercel/python` 构建器
   - 自动安装 Python 依赖
   - 部署 `api/index.py` 作为服务器端函数

2. **前端构建**：
   - 使用 `@vercel/static-build` 构建器
   - 执行 `npm install` 安装依赖
   - 执行 `npm run vercel-build` 构建静态文件
   - 输出到 `ui/dist` 目录

## 📁 项目结构

```
faceflip-server/
├── api/
│   └── index.py              # Vercel 服务器端入口
├── ui/
│   ├── package.json          # 前端依赖和构建脚本
│   ├── vite.config.js        # Vite 配置
│   └── dist/                 # 构建输出目录
├── vercel.json               # Vercel 配置文件
└── vercel-env.example       # 环境变量示例
```

## 🔧 Vercel 配置说明

### vercel.json 配置
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "ui/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "ui/$1"
    }
  ]
}
```

### 路由规则
- `/api/*` → 后端 API 路由
- `/*` → 前端静态文件

## 📦 依赖管理

### 后端依赖
- 使用 `pyproject.toml` 管理 Python 依赖
- Vercel 自动安装依赖

### 前端依赖
- 使用 `ui/package.json` 管理 Node.js 依赖
- 构建时自动安装依赖

## 🚀 部署流程

### 1. 自动部署（推荐）
```bash
# 推送代码到 GitHub
git push origin main

# Vercel 会自动检测并部署
```

### 2. 手动部署
```bash
# 本地构建
make vercel-build

# 部署到 Vercel
vercel --prod
```

### 3. 预览部署
```bash
# 部署预览版本
vercel
```

## 🔍 部署验证

### 检查部署状态
```bash
# 查看部署日志
vercel logs

# 查看项目信息
vercel ls
```

### 测试 API 端点
```bash
# 健康检查
curl https://your-domain.vercel.app/api/health

# 图像生成 API
curl -X POST https://your-domain.vercel.app/api/faceflip/generate \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com/image.jpg"], "task_id": "test123"}'
```

## 🐛 故障排除

### 常见问题

1. **构建失败**
   - 检查环境变量是否正确设置
   - 查看 Vercel 构建日志
   - 确保所有依赖都在 `pyproject.toml` 和 `package.json` 中

2. **API 路由不工作**
   - 检查 `vercel.json` 路由配置
   - 确保 `api/index.py` 文件存在
   - 验证环境变量设置

3. **前端资源加载失败**
   - 检查 `ui/dist` 目录是否存在
   - 验证 Vite 构建配置
   - 确保静态文件路径正确

### 调试命令
```bash
# 查看详细构建日志
vercel logs --follow

# 本地测试 Vercel 环境
vercel dev
```

## 📊 性能优化

### 前端优化
- 启用 Vite 的代码分割
- 使用 CDN 加速静态资源
- 压缩图片和资源

### 后端优化
- 使用 Vercel Edge Functions（如需要）
- 优化数据库查询
- 启用缓存策略

## 🔒 安全配置

### 环境变量安全
- 不要在代码中硬编码敏感信息
- 使用 Vercel 的环境变量管理
- 定期轮换 API 密钥

### CORS 配置
- 在生产环境中限制 CORS 源
- 使用具体的域名而不是通配符

## 📈 监控和日志

### Vercel Analytics
- 启用 Vercel Analytics 监控性能
- 设置错误追踪
- 监控 API 使用情况

### 日志管理
- 使用 Vercel 的内置日志功能
- 集成外部日志服务（如 Sentry）
- 设置日志告警

## 🔄 持续集成

### GitHub Actions（可选）
```yaml
name: Deploy to Vercel
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## 📞 支持

如果遇到部署问题，请：
1. 查看 Vercel 文档
2. 检查项目日志
3. 联系技术支持
