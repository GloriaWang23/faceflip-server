<template>
  <div class="debug-container">
    <h1>调试信息</h1>
    
    <div class="debug-section">
      <h2>认证状态</h2>
      <p><strong>加载中:</strong> {{ loading }}</p>
      <p><strong>用户:</strong> {{ user ? user.email : '未登录' }}</p>
      <p><strong>错误:</strong> {{ error || '无' }}</p>
      <p><strong>认证状态:</strong> {{ isAuthenticated() ? '已认证' : '未认证' }}</p>
    </div>
    
    <div class="debug-section">
      <h2>Supabase配置</h2>
      <p><strong>URL:</strong> {{ supabaseUrl }}</p>
      <p><strong>Key:</strong> {{ supabaseKey ? '已配置' : '未配置' }}</p>
    </div>
    
    <div class="debug-section">
      <h2>操作</h2>
      <button @click="testConnection" :disabled="loading">
        测试Supabase连接
      </button>
      <button @click="reinitAuth" :disabled="loading">
        重新初始化认证
      </button>
    </div>
    
    <div v-if="testResult" class="debug-section">
      <h2>测试结果</h2>
      <pre>{{ testResult }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { supabase } from '../supabase.js'
import { useAuth } from '../composables/useAuth.js'

const { user, loading, error, initAuth, isAuthenticated } = useAuth()
const testResult = ref('')

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://ynjlmthakbamarannuxe.supabase.co'
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluamxtdGhha2JhbWFyYW5udXhlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyOTA2MjgsImV4cCI6MjA3NTg2NjYyOH0.PpjxgiUmrHVvkyPImS6NmoccT-SUpa5uLtSzIkonFYQ'

const testConnection = async () => {
  try {
    testResult.value = '测试连接中...'
    
    const { data, error } = await supabase.auth.getSession()
    
    if (error) {
      testResult.value = `连接失败: ${error.message}`
    } else {
      testResult.value = `连接成功!\n会话状态: ${data.session ? '已存在' : '不存在'}\n用户: ${data.session?.user?.email || '无'}`
    }
  } catch (err) {
    testResult.value = `测试失败: ${err.message}`
  }
}

const reinitAuth = async () => {
  try {
    testResult.value = '重新初始化认证中...'
    await initAuth()
    testResult.value = '重新初始化完成'
  } catch (err) {
    testResult.value = `重新初始化失败: ${err.message}`
  }
}
</script>

<style scoped>
.debug-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.debug-section {
  background: #f8f9fa;
  padding: 20px;
  margin: 20px 0;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

.debug-section h2 {
  margin-top: 0;
  color: #333;
}

.debug-section p {
  margin: 8px 0;
  color: #666;
}

.debug-section button {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

.debug-section button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.debug-section pre {
  background: #e9ecef;
  padding: 15px;
  border-radius: 4px;
  white-space: pre-wrap;
  font-family: monospace;
}
</style>
