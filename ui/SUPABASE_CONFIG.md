# Supabase 配置说明

## ✅ 配置已完成

您的 Supabase 配置已经完成！根目录的 `.env` 文件中的配置已经自动同步到前端项目。

### 当前配置信息

- **Supabase URL**: `https://ynjlmthakbamarannuxe.supabase.co`
- **存储桶**: `images`
- **配置文件**: `ui/.env.local` (已自动创建)

## 🗂️ 下一步：创建存储桶

您需要在 Supabase Dashboard 中创建存储桶：

### 1. 登录 Supabase Dashboard
访问 [https://supabase.com/dashboard](https://supabase.com/dashboard)

### 2. 选择项目
选择项目 ID: `ynjlmthakbamarannuxe`

### 3. 创建存储桶
1. 进入 **Storage** 页面
2. 点击 **New bucket**
3. 输入桶名称：`images`
4. ✅ 选择 **Public bucket**（公开访问）
5. 点击 **Create bucket**

### 4. 设置存储策略
在 **Storage** > **Policies** 中创建以下策略：

```sql
-- 允许所有人上传文件
CREATE POLICY "Allow public uploads" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'images');

-- 允许所有人查看文件
CREATE POLICY "Allow public access" ON storage.objects
FOR SELECT USING (bucket_id = 'images');
```

## 🚀 测试上传功能

1. 启动开发服务器：
   ```bash
   cd ui
   pnpm dev
   ```

2. 打开浏览器访问应用

3. 尝试上传一张图片

4. 检查浏览器控制台是否有 "✅ Supabase 配置已加载" 消息

## 🔧 故障排除

### 如果上传失败：
1. 确认存储桶 `images` 已创建
2. 确认存储桶设置为公开访问
3. 确认存储策略已正确设置
4. 检查浏览器控制台的错误信息

### 如果配置未加载：
1. 确认 `ui/.env.local` 文件存在
2. 重启开发服务器
3. 检查环境变量名称是否正确（必须以 `VITE_` 开头）
