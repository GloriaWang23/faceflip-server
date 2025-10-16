# Supabase用户认证集成使用说明

## 功能概述

前端已完全集成Supabase用户认证系统，提供完整的登录、注册、用户管理功能，并与图像上传和生成功能无缝结合。

## 新增功能

### 1. 用户认证组件

#### AuthForm.vue - 登录/注册表单
- **邮箱密码登录**: 支持邮箱和密码登录
- **用户注册**: 新用户注册功能
- **Google OAuth**: 一键Google登录
- **密码确认**: 注册时密码确认验证
- **错误处理**: 友好的错误提示
- **响应式设计**: 移动端适配

#### UserProfile.vue - 用户信息展示
- **头像显示**: 支持Google头像或默认头像
- **用户信息**: 显示用户名、邮箱、ID
- **统计信息**: 注册时间、最后登录时间
- **退出登录**: 一键退出功能

### 2. 认证状态管理

#### useAuth.js - 认证Composable
```javascript
const { 
  user,           // 当前用户信息
  loading,        // 加载状态
  error,          // 错误信息
  signIn,         // 登录方法
  signUp,         // 注册方法
  signOut,        // 退出方法
  isAuthenticated // 认证状态检查
} = useAuth()
```

**功能特性**:
- 自动初始化认证状态
- 监听认证状态变化
- 提供完整的认证方法
- 错误处理和状态管理
- 用户信息获取工具

### 3. 应用布局更新

#### App.vue - 主应用组件
- **条件渲染**: 根据认证状态显示不同内容
- **加载状态**: 优雅的加载动画
- **错误处理**: 错误状态显示和重试
- **响应式布局**: 桌面端和移动端适配
- **用户欢迎**: 头部显示用户信息

**布局结构**:
```
未登录: 显示登录表单
已登录: 显示用户信息 + 图片上传
```

### 4. 权限控制

#### ImageUpload.vue - 图片上传权限
- **用户验证**: 只有登录用户才能上传
- **文件命名**: 按用户ID组织文件结构
- **权限检查**: 上传前验证用户状态
- **用户标识**: 显示当前操作用户

**文件命名规则**:
```
{用户ID}/{日期}/{UUID}.{扩展名}
例如: abc123/2024-01-15/uuid.jpg
```

## 使用流程

### 1. 用户注册/登录
1. 访问应用首页
2. 选择"立即注册"或"立即登录"
3. 填写邮箱和密码
4. 或使用Google一键登录

### 2. 图片上传和生成
1. 登录后自动显示用户信息
2. 选择图片文件
3. 点击"上传图片"
4. 上传成功后点击"生成新图像"
5. 实时查看生成进度和结果

### 3. 用户管理
1. 查看个人信息
2. 查看注册和登录时间
3. 一键退出登录

## 技术实现

### 1. Supabase集成
```javascript
// 自动监听认证状态变化
supabase.auth.onAuthStateChange((event, session) => {
  user.value = session?.user || null
})
```

### 2. 状态管理
```javascript
// 全局认证状态
const user = ref(null)
const loading = ref(true)
const error = ref(null)
```

### 3. 权限控制
```javascript
// 检查用户权限
const canUpload = computed(() => {
  return isAuthenticated.value && !!user.value
})
```

### 4. 文件组织
```javascript
// 按用户ID组织文件
const generateFileName = (file) => {
  const userId = user.value?.id
  return `${userId}/${date}/${uuid}.${ext}`
}
```

## 配置要求

### 1. Supabase配置
确保在 `.env` 文件中配置：
```bash
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 2. Google OAuth配置
在Supabase Dashboard中配置Google OAuth：
1. 进入Authentication > Providers
2. 启用Google Provider
3. 配置Client ID和Client Secret
4. 设置重定向URL

### 3. 存储桶权限
确保Supabase存储桶配置正确：
- 创建 `images` 存储桶
- 设置适当的访问权限
- 配置文件上传策略

## 安全特性

### 1. 认证保护
- 所有敏感操作需要登录
- 自动验证用户状态
- 会话管理和刷新

### 2. 文件隔离
- 按用户ID组织文件
- 防止跨用户访问
- 安全的文件命名

### 3. 错误处理
- 友好的错误提示
- 网络错误处理
- 认证失败处理

## 响应式设计

### 1. 桌面端
- 双栏布局（用户信息 + 上传区域）
- 粘性用户信息卡片
- 大屏幕优化

### 2. 移动端
- 单栏布局
- 触摸友好的按钮
- 优化的表单输入

## 测试步骤

### 1. 启动应用
```bash
cd ui
npm run dev
```

### 2. 测试注册
1. 访问应用
2. 点击"立即注册"
3. 填写邮箱和密码
4. 检查邮箱确认链接

### 3. 测试登录
1. 使用注册的账户登录
2. 验证用户信息显示
3. 测试图片上传功能

### 4. 测试Google登录
1. 点击"使用Google登录"
2. 完成Google授权
3. 验证自动登录

## 故障排除

### 1. 认证失败
- 检查Supabase配置
- 验证环境变量
- 查看浏览器控制台

### 2. Google登录失败
- 检查OAuth配置
- 验证重定向URL
- 确认Client ID正确

### 3. 文件上传失败
- 检查存储桶权限
- 验证文件大小限制
- 确认用户已登录

### 4. 状态不同步
- 刷新页面
- 检查网络连接
- 清除浏览器缓存

## 下一步功能

1. **用户设置**: 个人资料编辑
2. **文件管理**: 查看和管理上传的文件
3. **生成历史**: 查看图像生成记录
4. **社交功能**: 分享和评论
5. **付费功能**: 高级用户权限
