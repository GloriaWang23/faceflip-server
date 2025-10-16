import { ref, readonly, onMounted, onUnmounted } from 'vue'
import { supabase } from '../supabase.js'

// 全局状态
const user = ref(null)
const loading = ref(true)
const error = ref(null)

// 初始化认证状态
const initAuth = async () => {
  try {
    console.log('开始初始化认证状态...')
    
    // 获取当前会话
    const { data: { session }, error: sessionError } = await supabase.auth.getSession()
    
    if (sessionError) {
      console.error('获取会话失败:', sessionError)
      throw sessionError
    }
    
    console.log('当前会话:', session ? '已存在' : '不存在')
    user.value = session?.user || null
    
    // 监听认证状态变化
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        console.log('认证状态变化:', event, session?.user?.email)
        user.value = session?.user || null
        
        // 处理不同的事件
        switch (event) {
          case 'SIGNED_IN':
            console.log('用户已登录:', session.user.email)
            break
          case 'SIGNED_OUT':
            console.log('用户已退出')
            break
          case 'TOKEN_REFRESHED':
            console.log('令牌已刷新')
            break
          case 'PASSWORD_RECOVERY':
            console.log('密码恢复')
            break
        }
      }
    )
    
    console.log('认证状态初始化完成')
    
    // 返回清理函数
    return () => subscription.unsubscribe()
    
  } catch (err) {
    console.error('初始化认证失败:', err)
    error.value = err.message
  } finally {
    loading.value = false
    console.log('认证加载状态已设置为false')
  }
}

// 登录方法
const signIn = async (email, password) => {
  try {
    loading.value = true
    error.value = null
    
    const { data, error: signInError } = await supabase.auth.signInWithPassword({
      email,
      password
    })
    
    if (signInError) {
      throw signInError
    }
    
    return data
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    loading.value = false
  }
}

// 注册方法
const signUp = async (email, password) => {
  try {
    loading.value = true
    error.value = null
    
    const { data, error: signUpError } = await supabase.auth.signUp({
      email,
      password
    })
    
    if (signUpError) {
      throw signUpError
    }
    
    return data
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    loading.value = false
  }
}

// Google登录
const signInWithGoogle = async () => {
  try {
    loading.value = true
    error.value = null
    
    const { error: googleError } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/`
      }
    })
    
    if (googleError) {
      throw googleError
    }
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    loading.value = false
  }
}

// 退出登录
const signOut = async () => {
  try {
    loading.value = true
    error.value = null
    
    const { error: signOutError } = await supabase.auth.signOut()
    
    if (signOutError) {
      throw signOutError
    }
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    loading.value = false
  }
}

// 重置密码
const resetPassword = async (email) => {
  try {
    loading.value = true
    error.value = null
    
    const { error: resetError } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/reset-password`
    })
    
    if (resetError) {
      throw resetError
    }
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    loading.value = false
  }
}

// 更新密码
const updatePassword = async (newPassword) => {
  try {
    loading.value = true
    error.value = null
    
    const { error: updateError } = await supabase.auth.updateUser({
      password: newPassword
    })
    
    if (updateError) {
      throw updateError
    }
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    loading.value = false
  }
}

// 更新用户资料
const updateProfile = async (updates) => {
  try {
    loading.value = true
    error.value = null
    
    const { error: updateError } = await supabase.auth.updateUser({
      data: updates
    })
    
    if (updateError) {
      throw updateError
    }
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    loading.value = false
  }
}

// 清除错误
const clearError = () => {
  error.value = null
}

// 检查用户是否已登录
const isAuthenticated = () => {
  return !!user.value
}

// 获取用户ID
const getUserId = () => {
  return user.value?.id
}

// 获取用户邮箱
const getUserEmail = () => {
  return user.value?.email
}

// 获取用户元数据
const getUserMetadata = () => {
  return user.value?.user_metadata || {}
}

// 获取访问令牌
const getAccessToken = async () => {
  try {
    const { data: { session }, error } = await supabase.auth.getSession()
    if (error) {
      console.error('获取会话失败:', error)
      return null
    }
    return session?.access_token || null
  } catch (err) {
    console.error('获取访问令牌失败:', err)
    return null
  }
}

// 导出认证状态管理
export function useAuth() {
  return {
    // 状态
    user: readonly(user),
    loading: readonly(loading),
    error: readonly(error),
    
    // 方法
    initAuth,
    signIn,
    signUp,
    signInWithGoogle,
    signOut,
    resetPassword,
    updatePassword,
    updateProfile,
    clearError,
    
    // 工具方法
    isAuthenticated,
    getUserId,
    getUserEmail,
    getUserMetadata,
    getAccessToken
  }
}
