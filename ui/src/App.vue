<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import ImageUpload from './components/ImageUpload.vue'
import AuthForm from './components/AuthForm.vue'
import UserProfile from './components/UserProfile.vue'
import DebugPage from './components/DebugPage.vue'
import { useAuth } from './composables/useAuth.js'

// 使用认证状态管理
const { user, loading, error, initAuth, signOut } = useAuth()

// 调试模式
const debugMode = computed(() => {
  return import.meta.env.VITE_DEBUG === 'true' || window.location.search.includes('debug=true')
})

// 计算属性
const isAuthenticated = computed(() => !!user.value)
const showAuthForm = computed(() => !isAuthenticated.value && !loading.value)
const showUserProfile = computed(() => isAuthenticated.value && !loading.value)
const showImageUpload = computed(() => isAuthenticated.value && !loading.value)

// 初始化认证状态
let cleanup = null

onMounted(async () => {
  try {
    cleanup = await initAuth()
  } catch (err) {
    console.error('初始化认证失败:', err)
  }
})

onUnmounted(() => {
  if (cleanup) {
    cleanup()
  }
})

// 处理退出登录
const handleSignOut = async () => {
  try {
    await signOut()
    console.log('用户已退出登录')
  } catch (err) {
    console.error('退出登录失败:', err)
  }
}
</script>

<template>
  <div class="app">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>正在加载...</p>
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="error" class="error-container">
      <div class="error-message">
        <h2>❌ 加载失败</h2>
        <p>{{ error }}</p>
        <button @click="window.location.reload()" class="retry-btn">
          重试
        </button>
      </div>
    </div>
    
    <!-- 主要内容 -->
    <div v-else class="app-content">
      <!-- 头部导航 -->
      <header class="app-header">
        <div class="header-content">
          <div class="logo">
            <h1>FaceFlip</h1>
            <p>AI图像生成平台</p>
          </div>
          
          <nav class="nav-menu">
            <div v-if="isAuthenticated" class="user-menu">
              <span class="welcome-text">
                欢迎，{{ user?.email?.split('@')[0] || '用户' }}！
              </span>
            </div>
          </nav>
        </div>
      </header>
      
      <!-- 主要内容区域 -->
      <main class="app-main">
        <!-- 调试模式 -->
        <div v-if="debugMode" class="debug-section">
          <DebugPage />
        </div>
        
        <!-- 未登录状态 - 显示登录表单 -->
        <div v-else-if="showAuthForm" class="auth-section">
          <AuthForm />
        </div>
        
        <!-- 已登录状态 - 显示用户信息和图片上传 -->
        <div v-else-if="showUserProfile" class="main-content">
          <div class="content-grid">
            <!-- 用户信息卡片 -->
            <div class="user-section">
              <UserProfile :user="user" @signout="handleSignOut" />
            </div>
            
            <!-- 图片上传和生成 -->
            <div class="upload-section">
              <ImageUpload />
            </div>
          </div>
        </div>
      </main>
      
      <!-- 页脚 -->
      <footer class="app-footer">
        <p>Powered by Vue 3 + Supabase + AI</p>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  color: white;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-container p {
  margin: 0;
  font-size: 1.1rem;
  opacity: 0.9;
}

/* 错误状态 */
.error-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
}

.error-message {
  background: white;
  padding: 40px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  max-width: 400px;
}

.error-message h2 {
  color: #dc3545;
  margin: 0 0 16px 0;
  font-size: 1.5rem;
}

.error-message p {
  color: #666;
  margin: 0 0 24px 0;
  line-height: 1.5;
}

.retry-btn {
  background-color: #667eea;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.retry-btn:hover {
  background-color: #5a6fd8;
}

/* 主要内容 */
.app-content {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* 头部导航 */
.app-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 20px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo h1 {
  font-size: 2rem;
  margin: 0 0 4px 0;
  font-weight: 600;
  color: white;
}

.logo p {
  font-size: 0.9rem;
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
}

.nav-menu {
  display: flex;
  align-items: center;
}

.user-menu {
  color: white;
}

.welcome-text {
  font-size: 0.9rem;
  opacity: 0.9;
}

/* 主要内容区域 */
.app-main {
  flex: 1;
  padding: 40px 20px;
}

.auth-section {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 200px);
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 40px;
  align-items: start;
}

.user-section {
  position: sticky;
  top: 20px;
}

.upload-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

/* 页脚 */
.app-footer {
  text-align: center;
  padding: 20px;
  color: white;
  opacity: 0.8;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.app-footer p {
  margin: 0;
  font-size: 0.9rem;
}

/* 调试模式 */
.debug-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .user-section {
    position: static;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .logo h1 {
    font-size: 1.8rem;
  }
  
  .app-main {
    padding: 20px 15px;
  }
  
  .upload-section {
    padding: 20px;
  }
  
  .content-grid {
    gap: 20px;
  }
}

@media (max-width: 480px) {
  .logo h1 {
    font-size: 1.5rem;
  }
  
  .logo p {
    font-size: 0.8rem;
  }
  
  .welcome-text {
    font-size: 0.8rem;
  }
  
  .upload-section {
    padding: 15px;
  }
}
</style>
