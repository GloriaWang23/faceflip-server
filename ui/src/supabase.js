import { createClient } from '@supabase/supabase-js'

// Supabase 配置 - 从环境变量读取
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://ynjlmthakbamarannuxe.supabase.co'
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluamxtdGhha2JhbWFyYW5udXhlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyOTA2MjgsImV4cCI6MjA3NTg2NjYyOH0.PpjxgiUmrHVvkyPImS6NmoccT-SUpa5uLtSzIkonFYQ'

// 检查配置
if (!supabaseUrl || !supabaseKey) {
  console.error('❌ Supabase 配置缺失，请检查环境变量设置')
} else {
  console.log('✅ Supabase 配置已加载')
}

// 创建 Supabase 客户端
export const supabase = createClient(supabaseUrl, supabaseKey)

// 存储桶名称
export const STORAGE_BUCKET = import.meta.env.VITE_STORAGE_BUCKET || 'images'

// 图片上传函数
export const uploadImage = async (file, fileName) => {
  try {
    console.log('开始上传图片:', fileName)
    console.log('使用存储桶:', STORAGE_BUCKET)
    
    const { data, error } = await supabase.storage
      .from(STORAGE_BUCKET)
      .upload(fileName, file, {
        contentType: file.type,
        upsert: true // 允许覆盖同名文件
      })

    if (error) {
      console.error('Supabase 上传错误:', error)
      throw error
    }

    // 获取公开 URL
    const { data: urlData } = supabase.storage
      .from(STORAGE_BUCKET)
      .getPublicUrl(fileName)

    console.log('上传成功:', urlData.publicUrl)

    return {
      success: true,
      data: data,
      publicUrl: urlData.publicUrl
    }
  } catch (error) {
    console.error('上传图片失败:', error)
    return {
      success: false,
      error: error.message
    }
  }
}
