# 前端集成示例

本文档提供前端如何与后端 API 集成的完整示例。

## 📦 安装 Supabase Client

```bash
npm install @supabase/supabase-js
# 或
yarn add @supabase/supabase-js
```

## 🔧 初始化 Supabase Client

```javascript
// lib/supabase.js
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

## 🔐 认证功能实现

### 1. 用户注册

```javascript
// services/auth.js
import { supabase } from '../lib/supabase'

export async function signUp(email, password, fullName) {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        full_name: fullName
      }
    }
  })

  if (error) {
    throw error
  }

  return data
}
```

### 2. 用户登录

```javascript
export async function signIn(email, password) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  })

  if (error) {
    throw error
  }

  // 返回 session 包含 access_token 和 refresh_token
  return {
    user: data.user,
    session: data.session,
    accessToken: data.session.access_token,
    refreshToken: data.session.refresh_token
  }
}
```

### 3. 用户登出

```javascript
export async function signOut() {
  const { error } = await supabase.auth.signOut()
  
  if (error) {
    throw error
  }
}
```

### 4. 获取当前 Session

```javascript
export async function getSession() {
  const { data: { session }, error } = await supabase.auth.getSession()
  
  if (error) {
    throw error
  }
  
  return session
}
```

## 🌐 API 请求封装

### 基础 HTTP 客户端

```javascript
// lib/api.js
import { supabase } from './supabase'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ApiClient {
  async getAccessToken() {
    const { data: { session } } = await supabase.auth.getSession()
    return session?.access_token
  }

  async request(endpoint, options = {}) {
    const token = await this.getAccessToken()
    
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    }

    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers
    })

    // 处理 token 过期
    if (response.status === 401) {
      // 尝试刷新 session
      const { data, error } = await supabase.auth.refreshSession()
      
      if (!error && data.session) {
        // 重试请求
        headers['Authorization'] = `Bearer ${data.session.access_token}`
        const retryResponse = await fetch(`${API_BASE_URL}${endpoint}`, {
          ...options,
          headers
        })
        return this.handleResponse(retryResponse)
      } else {
        // 跳转到登录页
        window.location.href = '/login'
        throw new Error('Session expired')
      }
    }

    return this.handleResponse(response)
  }

  async handleResponse(response) {
    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Request failed')
    }

    return data
  }

  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' })
  }

  async post(endpoint, body) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(body)
    })
  }

  async put(endpoint, body) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body)
    })
  }

  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' })
  }
}

export const api = new ApiClient()
```

## 📱 React 示例

### 认证上下文 (Context)

```javascript
// context/AuthContext.jsx
import { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from '../lib/supabase'
import { api } from '../lib/api'

const AuthContext = createContext({})

export const useAuth = () => useContext(AuthContext)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 获取初始 session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      setLoading(false)
    })

    // 监听认证状态变化
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => subscription.unsubscribe()
  }, [])

  const value = {
    user,
    loading,
    signUp: async (email, password, fullName) => {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: { full_name: fullName }
        }
      })
      if (error) throw error
      return data
    },
    signIn: async (email, password) => {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
      })
      if (error) throw error
      return data
    },
    signOut: async () => {
      const { error } = await supabase.auth.signOut()
      if (error) throw error
    },
    verifyToken: async () => {
      return api.get('/api/auth/verify')
    },
    getCurrentUser: async () => {
      return api.get('/api/users/me')
    }
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  )
}
```

### 登录组件

```javascript
// components/LoginForm.jsx
import { useState } from 'react'
import { useAuth } from '../context/AuthContext'

export function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { signIn } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await signIn(email, password)
      // 登录成功，跳转到首页
      window.location.href = '/'
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>登录</h2>
      
      {error && <div className="error">{error}</div>}
      
      <input
        type="email"
        placeholder="邮箱"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      
      <input
        type="password"
        placeholder="密码"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      
      <button type="submit" disabled={loading}>
        {loading ? '登录中...' : '登录'}
      </button>
    </form>
  )
}
```

### 受保护的路由

```javascript
// components/ProtectedRoute.jsx
import { useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { useRouter } from 'next/router'

export function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  if (loading || !user) {
    return <div>加载中...</div>
  }

  return children
}
```

### 使用 API 客户端

```javascript
// pages/profile.jsx
import { useEffect, useState } from 'react'
import { api } from '../lib/api'
import { ProtectedRoute } from '../components/ProtectedRoute'

export default function ProfilePage() {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadProfile() {
      try {
        const data = await api.get('/api/users/profile')
        setProfile(data.profile)
      } catch (err) {
        console.error('Failed to load profile:', err)
      } finally {
        setLoading(false)
      }
    }

    loadProfile()
  }, [])

  if (loading) return <div>加载中...</div>

  return (
    <ProtectedRoute>
      <div>
        <h1>个人资料</h1>
        <p>邮箱: {profile.email}</p>
        <p>姓名: {profile.full_name}</p>
      </div>
    </ProtectedRoute>
  )
}
```

## 🔄 Token 自动刷新

Supabase SDK 会自动处理 token 刷新，但如果需要手动刷新：

```javascript
// 手动刷新 session
async function refreshSession() {
  const { data, error } = await supabase.auth.refreshSession()
  
  if (error) {
    console.error('Failed to refresh session:', error)
    return null
  }
  
  return data.session
}

// 设置定时刷新（可选）
useEffect(() => {
  const interval = setInterval(async () => {
    const session = await refreshSession()
    if (!session) {
      // 跳转到登录页
      window.location.href = '/login'
    }
  }, 15 * 60 * 1000) // 每15分钟刷新一次

  return () => clearInterval(interval)
}, [])
```

## 🧪 测试工具

### 测试 Token 验证

```javascript
// utils/testAuth.js
import { api } from '../lib/api'

export async function testAuthentication() {
  try {
    // 验证 token
    const verifyResult = await api.get('/api/auth/verify')
    console.log('Token is valid:', verifyResult)

    // 获取用户信息
    const userInfo = await api.get('/api/users/me')
    console.log('User info:', userInfo)

    return true
  } catch (error) {
    console.error('Authentication test failed:', error)
    return false
  }
}
```

## 📝 环境变量配置

创建 `.env.local` 文件：

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🎯 完整流程示例

```javascript
// 完整的认证流程示例
async function completeAuthFlow() {
  try {
    // 1. 用户注册
    const { user, session } = await supabase.auth.signUp({
      email: 'user@example.com',
      password: 'password123',
      options: {
        data: {
          full_name: 'John Doe'
        }
      }
    })
    console.log('Signed up:', user)

    // 2. 用户登录
    const { data: signInData } = await supabase.auth.signInWithPassword({
      email: 'user@example.com',
      password: 'password123'
    })
    console.log('Signed in:', signInData.user)
    
    const accessToken = signInData.session.access_token

    // 3. 调用后端 API（验证 token）
    const verifyResponse = await fetch('http://localhost:8000/api/auth/verify', {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    })
    const verifyData = await verifyResponse.json()
    console.log('Token verified:', verifyData)

    // 4. 获取用户信息
    const userResponse = await fetch('http://localhost:8000/api/users/me', {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    })
    const userData = await userResponse.json()
    console.log('User data:', userData)

    // 5. 登出
    await supabase.auth.signOut()
    console.log('Signed out')

  } catch (error) {
    console.error('Error:', error)
  }
}
```

## 🔗 相关资源

- [Supabase Auth 文档](https://supabase.com/docs/guides/auth)
- [React Context API](https://react.dev/learn/passing-data-deeply-with-context)
- [Next.js 认证最佳实践](https://nextjs.org/docs/authentication)

