# FaceFlip 图片上传前端

这是一个基于 Vue 3 + Vite + Supabase 的图片上传应用。

## 功能特性

- 🖼️ 图片上传到 Supabase Storage
- 📱 响应式设计，支持移动端
- 🎨 现代化 UI 界面
- 📁 支持拖拽上传
- 🔍 图片预览功能
- 📊 文件信息显示
- 🔗 上传后获取公开链接
- 📅 智能文件命名：UTC日期/UUID.扩展名

## 技术栈

- **Vue 3** - 前端框架
- **Vite** - 构建工具
- **Supabase** - 后端服务和存储
- **pnpm** - 包管理器

## 快速开始

### 1. 安装依赖

```bash
pnpm install
```

### 2. 配置 Supabase

1. 在 [Supabase](https://supabase.com) 创建新项目
2. 在项目设置中获取以下信息：
   - Project URL
   - Anon public key
3. 创建存储桶：
   - 进入 Storage 页面
   - 创建名为 `images` 的存储桶
   - 设置为公开访问

### 3. 配置环境变量

创建 `.env.local` 文件：

```env
VITE_SUPABASE_URL=your_project_url_here
VITE_SUPABASE_ANON_KEY=your_anon_key_here
VITE_STORAGE_BUCKET=images
```

### 4. 启动开发服务器

```bash
pnpm dev
```

## Supabase 存储桶配置

### 创建存储桶

1. 登录 Supabase Dashboard
2. 选择您的项目
3. 进入 **Storage** 页面
4. 点击 **New bucket**
5. 输入桶名称：`images`
6. 设置为 **Public bucket**（公开访问）

### 设置存储策略

在 **Storage** > **Policies** 中创建以下策略：

```sql
-- 允许所有人上传文件
CREATE POLICY "Allow public uploads" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'images');

-- 允许所有人查看文件
CREATE POLICY "Allow public access" ON storage.objects
FOR SELECT USING (bucket_id = 'images');
```

## 项目结构

```
ui/
├── src/
│   ├── components/
│   │   └── ImageUpload.vue    # 图片上传组件
│   ├── supabase.js            # Supabase 配置
│   ├── App.vue               # 主应用组件
│   ├── main.js               # 应用入口
│   └── style.css             # 全局样式
├── package.json
└── vite.config.js
```

## 使用说明

1. **选择图片**：点击上传区域或拖拽图片文件
2. **预览图片**：选择后会自动显示图片预览和文件信息
3. **上传图片**：点击"上传图片"按钮开始上传
4. **获取链接**：上传成功后显示公开访问链接

## 文件命名规则

上传的图片将按照以下规则命名：
- **格式**: `UTC日期/UUID.扩展名`
- **示例**: `2024-01-15/a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg`
- **优势**: 
  - 按日期组织文件，便于管理
  - UUID 确保文件名唯一性
  - 避免文件名冲突

## 支持的图片格式

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

## 文件大小限制

- 最大文件大小：10MB
- Supabase 标准上传支持最大 6MB，超过建议使用分片上传

## 开发命令

```bash
# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev

# 构建生产版本
pnpm build

# 预览生产构建
pnpm preview
```

## 部署

### Vercel 部署

1. 将代码推送到 GitHub
2. 在 Vercel 中导入项目
3. 配置环境变量
4. 部署

### 其他平台

构建后的文件在 `dist/` 目录中，可以部署到任何静态文件服务器。

## 故障排除

### 常见问题

1. **上传失败**：检查 Supabase 配置和存储桶权限
2. **图片不显示**：确认存储桶设置为公开访问
3. **CORS 错误**：检查 Supabase 项目设置

### 调试

在浏览器开发者工具中查看控制台错误信息，检查网络请求状态。

## 许可证

MIT License