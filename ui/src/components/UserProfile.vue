<template>
  <div class="user-profile">
    <div class="profile-header">
      <div class="avatar">
        <img v-if="user?.user_metadata?.avatar_url" :src="user.user_metadata.avatar_url" alt="头像" />
        <div v-else class="avatar-placeholder">
          {{ userInitials }}
        </div>
      </div>
      <div class="user-info">
        <h3>{{ userDisplayName }}</h3>
        <p class="user-email">{{ user?.email }}</p>
        <p class="user-id">ID: {{ user?.id?.slice(0, 8) }}...</p>
      </div>
    </div>
    
    <div class="profile-actions">
      <button @click="signOut" class="signout-btn">
        <svg viewBox="0 0 24 24" class="signout-icon">
          <path fill="currentColor" d="M16 17v-3H9v-4h7V7l5 5-5 5zM14 2a2 2 0 0 1 2 2v2h-2V4H5v16h9v-2h2v2a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9z"/>
        </svg>
        退出登录
      </button>
    </div>
    
    <div class="profile-stats">
      <div class="stat-item">
        <span class="stat-label">注册时间</span>
        <span class="stat-value">{{ formatDate(user?.created_at) }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">最后登录</span>
        <span class="stat-value">{{ formatDate(user?.last_sign_in_at) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { supabase } from '../supabase.js'

// Props
const props = defineProps({
  user: {
    type: Object,
    required: true
  }
})

// Emits
const emit = defineEmits(['signout'])

// 计算属性
const userDisplayName = computed(() => {
  if (props.user?.user_metadata?.full_name) {
    return props.user.user_metadata.full_name
  }
  if (props.user?.user_metadata?.name) {
    return props.user.user_metadata.name
  }
  return props.user?.email?.split('@')[0] || '用户'
})

const userInitials = computed(() => {
  const name = userDisplayName.value
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

// 方法
const signOut = async () => {
  try {
    const { error } = await supabase.auth.signOut()
    if (error) {
      console.error('退出登录失败:', error)
    } else {
      emit('signout')
    }
  } catch (err) {
    console.error('退出登录错误:', err)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '未知'
  
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.user-profile {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 0 auto;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 20px;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-info h3 {
  margin: 0 0 4px 0;
  color: #333;
  font-size: 1.2rem;
  font-weight: 600;
}

.user-email {
  margin: 0 0 4px 0;
  color: #666;
  font-size: 0.9rem;
  word-break: break-all;
}

.user-id {
  margin: 0;
  color: #999;
  font-size: 0.8rem;
  font-family: monospace;
}

.profile-actions {
  margin-bottom: 24px;
}

.signout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.signout-btn:hover {
  background-color: #c82333;
}

.signout-icon {
  width: 16px;
  height: 16px;
}

.profile-stats {
  border-top: 1px solid #e1e5e9;
  padding-top: 20px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.stat-item:last-child {
  margin-bottom: 0;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.stat-value {
  color: #333;
  font-size: 14px;
  font-weight: 500;
}

@media (max-width: 480px) {
  .user-profile {
    padding: 20px;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .avatar {
    width: 80px;
    height: 80px;
  }
  
  .user-info h3 {
    font-size: 1.1rem;
  }
}
</style>
