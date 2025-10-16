# 前端加载问题故障排除指南

## 问题描述
前端应用一直显示"正在加载..."状态，无法正常显示内容。

## 可能原因

### 1. Supabase连接问题
- Supabase URL或API Key配置错误
- 网络连接问题
- Supabase服务不可用

### 2. 认证状态初始化问题
- `useAuth` composable初始化失败
- 会话获取超时
- 认证状态监听器未正确设置

### 3. 环境变量问题
- 缺少必要的环境变量
- 环境变量值不正确
- 环境变量未正确加载

## 解决步骤

### 步骤1: 启用调试模式
在浏览器地址栏添加 `?debug=true` 参数：
```
http://localhost:5173/?debug=true
```

这将显示调试页面，包含：
- 认证状态信息
- Supabase配置信息
- 连接测试功能

### 步骤2: 检查控制台日志
打开浏览器开发者工具，查看控制台输出：
- 查找错误信息
- 检查Supabase连接状态
- 查看认证初始化日志

### 步骤3: 验证Supabase配置
确保在项目根目录创建 `.env.local` 文件：
```bash
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 步骤4: 测试Supabase连接
在调试页面点击"测试Supabase连接"按钮，检查：
- 连接是否成功
- 会话状态是否正确
- 用户信息是否获取

### 步骤5: 重新初始化认证
如果连接测试失败，点击"重新初始化认证"按钮。

## 常见错误和解决方案

### 错误1: "Supabase 配置缺失"
**原因**: 环境变量未设置
**解决**: 检查 `.env.local` 文件是否存在且配置正确

### 错误2: "获取会话失败"
**原因**: Supabase URL或Key错误
**解决**: 验证Supabase项目配置

### 错误3: "认证状态初始化失败"
**原因**: 网络问题或Supabase服务不可用
**解决**: 检查网络连接和Supabase服务状态

### 错误4: 无限加载
**原因**: `loading` 状态未正确设置为 `false`
**解决**: 检查 `initAuth` 函数的 `finally` 块

## 调试技巧

### 1. 添加更多日志
在 `useAuth.js` 中添加更多 `console.log` 语句：
```javascript
console.log('当前状态:', { user: user.value, loading: loading.value, error: error.value })
```

### 2. 检查网络请求
在开发者工具的Network标签页中查看：
- Supabase API请求
- 请求状态和响应
- 错误信息

### 3. 验证环境变量
在浏览器控制台中运行：
```javascript
console.log('Supabase URL:', import.meta.env.VITE_SUPABASE_URL)
console.log('Supabase Key:', import.meta.env.VITE_SUPABASE_ANON_KEY)
```

## 预防措施

### 1. 添加超时处理
```javascript
const initAuth = async () => {
  const timeout = new Promise((_, reject) => 
    setTimeout(() => reject(new Error('初始化超时')), 10000)
  )
  
  try {
    await Promise.race([initAuthInternal(), timeout])
  } catch (err) {
    console.error('初始化失败:', err)
    loading.value = false
  }
}
```

### 2. 添加重试机制
```javascript
const initAuthWithRetry = async (retries = 3) => {
  for (let i = 0; i < retries; i++) {
    try {
      return await initAuth()
    } catch (err) {
      if (i === retries - 1) throw err
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
  }
}
```

### 3. 添加降级方案
```javascript
const initAuth = async () => {
  try {
    // 正常初始化
    return await initAuthInternal()
  } catch (err) {
    console.warn('认证初始化失败，使用降级方案')
    // 设置默认状态
    user.value = null
    loading.value = false
    error.value = '认证服务暂时不可用'
  }
}
```

## 联系支持

如果问题仍然存在，请提供以下信息：
1. 浏览器控制台的完整错误日志
2. 调试页面的输出信息
3. 网络请求的详细信息
4. 环境变量配置（隐藏敏感信息）
5. 浏览器版本和操作系统信息
