<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h2>{{ isLogin ? '登录' : '注册' }}</h2>
        <p>{{ isLogin ? '欢迎回来！' : '创建新账户' }}</p>
      </div>
      
      <form @submit.prevent="handleSubmit" class="auth-form">
        <!-- 邮箱输入 -->
        <div class="form-group">
          <label for="email">邮箱</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="请输入邮箱地址"
            :disabled="loading"
          />
        </div>
        
        <!-- 密码输入 -->
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="请输入密码"
            :disabled="loading"
          />
        </div>
        
        <!-- 注册时显示确认密码 -->
        <div v-if="!isLogin" class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            required
            placeholder="请再次输入密码"
            :disabled="loading"
          />
        </div>
        
        <!-- 错误信息 -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <!-- 提交按钮 -->
        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? '处理中...' : (isLogin ? '登录' : '注册') }}
        </button>
      </form>
      
      <!-- 切换登录/注册 -->
      <div class="auth-switch">
        <p>
          {{ isLogin ? '还没有账户？' : '已有账户？' }}
          <button @click="toggleMode" class="switch-btn" :disabled="loading">
            {{ isLogin ? '立即注册' : '立即登录' }}
          </button>
        </p>
      </div>
      
      <!-- 第三方登录 -->
      <div class="social-auth">
        <div class="divider">
          <span>或</span>
        </div>
        
        <button @click="signInWithGoogle" class="social-btn google-btn" :disabled="loading">
          <svg viewBox="0 0 24 24" class="google-icon">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          使用 Google 登录
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { supabase } from '../supabase.js'

// 响应式数据
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const isLogin = ref(true)

// 切换登录/注册模式
const toggleMode = () => {
  isLogin.value = !isLogin.value
  error.value = ''
  password.value = ''
  confirmPassword.value = ''
}

// 处理表单提交
const handleSubmit = async () => {
  if (loading.value) return
  
  // 验证密码确认
  if (!isLogin.value && password.value !== confirmPassword.value) {
    error.value = '两次输入的密码不一致'
    return
  }
  
  loading.value = true
  error.value = ''
  
  try {
    if (isLogin.value) {
      await signIn()
    } else {
      await signUp()
    }
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// 邮箱密码登录
const signIn = async () => {
  const { error: signInError } = await supabase.auth.signInWithPassword({
    email: email.value,
    password: password.value
  })
  
  if (signInError) {
    throw new Error(signInError.message)
  }
}

// 邮箱密码注册
const signUp = async () => {
  const { error: signUpError } = await supabase.auth.signUp({
    email: email.value,
    password: password.value
  })
  
  if (signUpError) {
    throw new Error(signUpError.message)
  }
  
  // 注册成功后提示用户检查邮箱
  alert('注册成功！请检查您的邮箱并点击确认链接完成注册。')
}

// Google登录
const signInWithGoogle = async () => {
  if (loading.value) return
  
  loading.value = true
  error.value = ''
  
  try {
    const { error: googleError } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/`
      }
    })
    
    if (googleError) {
      throw new Error(googleError.message)
    }
  } catch (err) {
    error.value = err.message
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.auth-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-header h2 {
  color: #333;
  margin: 0 0 8px 0;
  font-size: 1.8rem;
}

.auth-header p {
  color: #666;
  margin: 0;
  font-size: 0.9rem;
}

.auth-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  color: #333;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.form-group input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 20px;
  font-size: 14px;
}

.submit-btn {
  width: 100%;
  background-color: #667eea;
  color: white;
  border: none;
  padding: 14px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
  background-color: #5a6fd8;
}

.submit-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.auth-switch {
  text-align: center;
  margin-bottom: 20px;
}

.auth-switch p {
  color: #666;
  margin: 0;
  font-size: 14px;
}

.switch-btn {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-weight: 500;
  text-decoration: underline;
}

.switch-btn:hover:not(:disabled) {
  color: #5a6fd8;
}

.switch-btn:disabled {
  color: #6c757d;
  cursor: not-allowed;
}

.social-auth {
  margin-top: 20px;
}

.divider {
  text-align: center;
  margin: 20px 0;
  position: relative;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background-color: #e1e5e9;
}

.divider span {
  background: white;
  padding: 0 15px;
  color: #666;
  font-size: 14px;
}

.social-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 12px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 500;
}

.social-btn:hover:not(:disabled) {
  border-color: #667eea;
  background-color: #f8f9fa;
}

.social-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.google-icon {
  width: 20px;
  height: 20px;
}

@media (max-width: 480px) {
  .auth-card {
    padding: 30px 20px;
  }
  
  .auth-header h2 {
    font-size: 1.5rem;
  }
}
</style>
