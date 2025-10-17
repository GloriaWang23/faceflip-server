# 🚀 Vercel 部署完整指南

本指南将帮助你完成 FaceFlip Server 到 Vercel 的部署配置。

## 📋 目录
- [前期准备](#前期准备)
- [环境变量配置](#环境变量配置)
- [构建配置说明](#构建配置说明)
- [部署步骤](#部署步骤)
- [验证部署](#验证部署)
- [常见问题](#常见问题)

---

## 🎯 前期准备

### 1. 安装 Vercel CLI
```bash
npm install -g vercel
```

### 2. 登录 Vercel 账号
```bash
vercel login
```

### 3. 准备环境变量
复制 `vercel-env.example` 文件内容，准备配置到 Vercel Dashboard

---

## 🔐 环境变量配置

### 必需的环境变量（关键）
在 **Vercel Dashboard > Settings > Environment Variables** 中配置：

#### Supabase 配置
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
SUPABASE_STORAGE_BUCKET=images
```

#### 火山引擎 ARK API 配置
```bash
ARK_API_KEY=your_ark_api_key
```

#### JWT 安全配置
```bash
SECRET_KEY=your_very_long_random_secret_key_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 可选的环境变量

#### ARK 图像生成配置
```bash
ARK_DEFAULT_PROMPT=生成3张女孩和奶牛玩偶在游乐园开心地坐过山车的图片，涵盖早晨、中午、晚上
ARK_MODEL=doubao-seedream-4-0-250828
ARK_IMAGE_SIZE=2K
ARK_MAX_IMAGES=3
ARK_API_TIMEOUT_SECONDS=50
SSE_TIMEOUT_SECONDS=60
```

#### 应用配置
```bash
APP_NAME=Face Flip Server
APP_VERSION=0.1.0
DEBUG=false
LOG_LEVEL=INFO
```

#### CORS 配置
```bash
CORS_ORIGINS=["*"]
CORS_CREDENTIALS=true
CORS_METHODS=["*"]
CORS_HEADERS=["*"]
```

⚠️ **生产环境建议**：将 `CORS_ORIGINS` 改为具体的域名，如 `["https://your-domain.vercel.app"]`

---

## 📁 构建配置说明

### vercel.json 配置解析

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",          // 后端入口文件
      "use": "@vercel/python",         // Python 运行时
      "config": {
        "maxLambdaSize": "50mb"        // Lambda 函数大小限制（包含依赖）
      }
    },
    {
      "src": "ui/package.json",        // 前端构建配置
      "use": "@vercel/static-build",   // 静态构建器
      "config": {
        "distDir": "ui/dist"           // 构建输出目录
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",              // API 路由 → 后端函数
      "dest": "api/index.py"
    },
    {
      "src": "/assets/(.*)",           // 静态资源路由
      "dest": "ui/dist/assets/$1"
    },
    {
      "src": "/(.*\\.(js|css|png|jpg|jpeg|gif|svg|ico|json|woff|woff2|ttf|eot))",
      "dest": "ui/dist/$1"             // 其他静态文件
    },
    {
      "src": "/(.*)",                  // 所有其他路由 → 前端 SPA
      "dest": "ui/dist/index.html"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.12"           // Python 版本
  },
  "functions": {
    "api/index.py": {
      "maxDuration": 60                // 函数最大执行时间（秒）
    }
  }
}
```

### 关键配置说明

1. **maxLambdaSize**: `50mb`
   - 允许较大的 Lambda 函数（包含 volcengine SDK 等依赖）
   
2. **maxDuration**: `60` 秒
   - SSE 流式响应需要较长的执行时间
   - Vercel Hobby 计划限制为 10 秒，Pro 计划可达 60 秒
   
3. **distDir**: `ui/dist`
   - Vite 构建输出目录
   - 包含所有前端静态资源

---

## 🚀 部署步骤

### 方法一：通过 Vercel CLI 部署（推荐）

#### 1. 初始化项目
```bash
cd /Users/shareit/Documents/workspace/faceflip-server
vercel
```

首次运行会询问：
- **Set up and deploy?** → Yes
- **Which scope?** → 选择你的账号/团队
- **Link to existing project?** → No（首次部署）
- **Project name?** → faceflip-server（或自定义名称）
- **In which directory is your code located?** → `./`

#### 2. 配置环境变量
```bash
# 交互式添加环境变量
vercel env add SUPABASE_URL
vercel env add SUPABASE_KEY
vercel env add ARK_API_KEY
vercel env add SECRET_KEY
# ... 添加所有必需的环境变量
```

#### 3. 部署到生产环境
```bash
vercel --prod
```

### 方法二：通过 Vercel Dashboard 部署

#### 1. 导入 Git 仓库
1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 **New Project**
3. 导入你的 GitHub/GitLab/Bitbucket 仓库

#### 2. 配置构建设置
- **Framework Preset**: Other
- **Build Command**: 留空（使用 vercel.json 配置）
- **Output Directory**: 留空（使用 vercel.json 配置）
- **Install Command**: 留空（使用 vercel.json 配置）

#### 3. 配置环境变量
在 **Environment Variables** 部分添加所有必需的环境变量

#### 4. 部署
点击 **Deploy** 按钮开始部署

---

## ✅ 验证部署

### 1. 检查健康状态
```bash
curl https://your-project.vercel.app/health/check
```

预期响应：
```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "status": "healthy",
    "app": "Face Flip Server",
    "version": "0.1.0"
  }
}
```

### 2. 测试前端访问
访问: `https://your-project.vercel.app`

应该能看到 Vue 前端界面

### 3. 测试 API 认证
```bash
curl https://your-project.vercel.app/api/faceflip/debug/env
```

检查环境变量是否正确配置（敏感信息会被部分隐藏）

### 4. 测试图像生成（需要登录）
1. 在前端界面登录
2. 上传图片
3. 点击"生成新图像"
4. 观察 SSE 流式响应

---

## 📊 构建输出说明

### 后端构建
```
✓ Building Python serverless function...
✓ Installing dependencies from requirements.txt
✓ Function: api/index.py (50 MB)
```

### 前端构建
```
✓ Installing dependencies (pnpm install)
✓ Building frontend (pnpm run vercel-build)
✓ Output: ui/dist (静态文件)
  ├── index.html
  ├── assets/
  │   ├── index-xxx.js
  │   └── index-xxx.css
  └── vite.svg
```

---

## 🔧 本地测试 Vercel 环境

### 1. 安装前端依赖
```bash
cd ui
pnpm install
# 或
npm install
```

### 2. 本地构建测试
```bash
# 构建前端
cd ui
pnpm run build

# 构建后端（Python 依赖）
cd ..
pip install -r requirements.txt
```

### 3. 使用 Vercel Dev 测试
```bash
vercel dev
```

这会在本地启动类似 Vercel 环境的服务器：
- 前端：http://localhost:3000
- API：http://localhost:3000/api

---

## 🐛 常见问题

### 问题 1：构建失败 - Python 依赖安装错误
**原因**: Lambda 函数大小超限或依赖冲突

**解决方案**:
1. 检查 `requirements.txt` 中的依赖版本
2. 确保 `maxLambdaSize` 设置为 `50mb`
3. 移除不必要的依赖

### 问题 2：SSE 连接超时
**原因**: Vercel Hobby 计划限制函数执行时间为 10 秒

**解决方案**:
1. 升级到 Vercel Pro 计划（支持 60 秒）
2. 或修改代码，将长时间任务改为异步轮询模式

### 问题 3：前端资源 404
**原因**: 路由配置不正确或构建输出目录错误

**解决方案**:
1. 检查 `vercel.json` 中的 `distDir` 设置
2. 确认 `ui/dist` 目录存在且包含 `index.html`
3. 检查 routes 配置顺序（API 路由应在前）

### 问题 4：CORS 错误
**原因**: CORS 配置不正确

**解决方案**:
1. 检查 `CORS_ORIGINS` 环境变量
2. 确保包含你的 Vercel 域名
3. 生产环境避免使用 `["*"]`

### 问题 5：环境变量未生效
**原因**: 环境变量作用域设置错误

**解决方案**:
1. 在 Vercel Dashboard 中重新添加环境变量
2. 确保选择正确的环境（Production/Preview/Development）
3. 重新部署项目

### 问题 6：图片上传失败
**原因**: Supabase 存储桶配置错误

**解决方案**:
1. 检查 `SUPABASE_STORAGE_BUCKET` 环境变量
2. 确认存储桶名称与 Supabase 中的一致
3. 验证 Supabase 服务角色密钥权限

---

## 📈 性能优化建议

### 前端优化
1. **启用 Gzip/Brotli 压缩**（Vercel 自动启用）
2. **配置 CDN 缓存**: 静态资源自动使用 Vercel Edge Network
3. **代码分割**: Vite 自动处理

### 后端优化
1. **冷启动优化**: 
   - 减少依赖体积
   - 使用 Vercel Edge Functions（如适用）
   
2. **缓存策略**:
   - 对 Supabase 查询结果进行缓存
   - 使用 Redis 等外部缓存（需额外配置）

3. **并发控制**:
   - 限制同时处理的图像生成任务数量
   - 使用队列系统处理大量请求

---

## 🔒 安全最佳实践

1. **环境变量管理**
   - 定期轮换 API 密钥
   - 不在代码中硬编码敏感信息
   - 使用 Vercel 的加密存储

2. **CORS 配置**
   - 生产环境使用具体域名
   - 避免使用通配符 `*`

3. **认证保护**
   - 确保所有敏感 API 端点都需要 JWT 认证
   - 定期审查访问日志

4. **限流**
   - 配置 Vercel 的 Rate Limiting
   - 或在应用层实现限流逻辑

---

## 📞 获取帮助

- **Vercel 文档**: https://vercel.com/docs
- **FastAPI 文档**: https://fastapi.tiangolo.com
- **Supabase 文档**: https://supabase.com/docs
- **项目问题**: 查看 GitHub Issues

---

## 🎉 部署成功后

部署成功后，你会获得：
- ✅ 生产环境 URL: `https://your-project.vercel.app`
- ✅ 自动 HTTPS 证书
- ✅ 全球 CDN 加速
- ✅ 自动 CI/CD（Git 推送自动部署）

祝你部署顺利！🚀

