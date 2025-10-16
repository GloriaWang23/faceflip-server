<template>
  <div class="image-upload-container">
    <div class="upload-header">
      <h2>图片上传</h2>
      <div v-if="user" class="user-info">
        <span class="user-badge">
          👤 {{ user.email?.split('@')[0] || '用户' }}
        </span>
      </div>
    </div>
    
    <!-- 文件选择区域 -->
    <div class="upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
      <input 
        ref="fileInput" 
        type="file" 
        accept="image/*" 
        @change="handleFileSelect" 
        style="display: none"
      />
      
      <div v-if="!selectedFile" class="upload-placeholder">
        <div class="upload-icon">📁</div>
        <p>点击选择图片或拖拽图片到此处</p>
        <p class="upload-hint">支持 JPG、PNG、GIF 格式</p>
      </div>
      
      <div v-else class="file-preview">
        <img :src="previewUrl" alt="预览图片" class="preview-image" />
        <div class="file-info">
          <p><strong>文件名:</strong> {{ selectedFile.name }}</p>
          <p><strong>大小:</strong> {{ formatFileSize(selectedFile.size) }}</p>
          <p><strong>类型:</strong> {{ selectedFile.type }}</p>
        </div>
      </div>
    </div>
    
    <!-- 上传按钮 -->
    <div class="upload-actions">
      <button 
        @click="uploadImage" 
        :disabled="!selectedFile || uploading"
        class="upload-btn"
      >
        {{ uploading ? '上传中...' : '上传图片' }}
      </button>
      
      <button 
        @click="clearFile" 
        :disabled="uploading"
        class="clear-btn"
      >
        清除
      </button>
    </div>
    
    <!-- 上传结果 -->
    <div v-if="uploadResult" class="upload-result">
      <div v-if="uploadResult.success" class="success-message">
        <h3>✅ 上传成功!</h3>
        <p><strong>图片链接:</strong></p>
        <a :href="uploadResult.publicUrl" target="_blank" class="image-link">
          {{ uploadResult.publicUrl }}
        </a>
        <div class="uploaded-image">
          <img :src="uploadResult.publicUrl" alt="上传的图片" />
        </div>
        
        <!-- 图像生成按钮 -->
        <div class="generate-section">
          <button 
            @click="generateImages" 
            :disabled="generating || !uploadResult.publicUrl"
            class="generate-btn"
          >
            {{ generating ? '生成中...' : '生成新图像' }}
          </button>
        </div>
      </div>
      
      <div v-else class="error-message">
        <h3>❌ 上传失败</h3>
        <p>{{ uploadResult.error }}</p>
      </div>
    </div>
    
    <!-- 图像生成状态 -->
    <div v-if="generationStatus" class="generation-status">
      <div class="status-message" :class="generationStatus.type">
        <h3>{{ generationStatus.title }}</h3>
        <p>{{ generationStatus.message }}</p>
        <div v-if="generationStatus.details" class="error-details">
          <p>{{ generationStatus.details }}</p>
        </div>
        <div v-if="generationStatus.type === 'process'" class="loading-spinner"></div>
        
        <!-- 错误处理建议 -->
        <div v-if="generationStatus.type === 'error'" class="error-suggestions">
          <h4>💡 建议操作：</h4>
          <ul>
            <li v-if="generationStatus.title.includes('API密钥')">
              请联系系统管理员配置ARK API密钥
            </li>
            <li v-if="generationStatus.title.includes('认证')">
              <button @click="clearFile" class="retry-btn">重新登录</button>
            </li>
            <li v-if="generationStatus.title.includes('网络')">
              <button @click="generateImages" class="retry-btn">重试</button>
            </li>
            <li v-if="generationStatus.title.includes('权限')">
              请联系管理员获取使用权限
            </li>
            <li v-if="generationStatus.title.includes('API限制')">
              请稍后再试，或联系管理员
            </li>
          </ul>
        </div>
      </div>
    </div>
    
    <!-- 生成的图像结果 -->
    <div v-if="generatedImages.length > 0" class="generated-images">
      <h3>🎨 生成的图像</h3>
      <p class="generated-count">共生成 {{ generatedImages.length }} 张图像</p>
      <div class="images-grid">
        <div v-for="(image, index) in generatedImages" :key="index" class="generated-image-item">
          <div class="image-container">
            <img 
              :src="image.url" 
              :alt="`生成的图像 ${index + 1}`"
              @load="onImageLoad(index)"
              @error="onImageError(index)"
              class="generated-image"
            />
            <div v-if="imageLoading[index]" class="image-loading">
              <div class="loading-spinner"></div>
            </div>
          </div>
          <div class="image-info">
            <p class="image-size">尺寸: {{ image.size || '未知' }}</p>
            <div class="image-actions">
              <a :href="image.url" target="_blank" class="action-btn view-btn">查看原图</a>
              <button @click="downloadImage(image.url, index)" class="action-btn download-btn">下载</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { uploadImage as uploadToSupabase } from '../supabase.js'
import { useAuth } from '../composables/useAuth.js'
import { v4 as uuidv4 } from 'uuid'

// 使用认证状态
const { user, isAuthenticated, getAccessToken } = useAuth()

// 响应式数据
const fileInput = ref(null)
const selectedFile = ref(null)
const previewUrl = ref('')
const uploading = ref(false)
const uploadResult = ref(null)

// 图像生成相关
const generating = ref(false)
const generationStatus = ref(null)
const generatedImages = ref([])
const imageLoading = ref({}) // 跟踪每张图像的加载状态

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value.click()
}

// 处理文件选择
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    processFile(file)
  }
}

// 处理拖拽上传
const handleDrop = (event) => {
  const files = event.dataTransfer.files
  if (files.length > 0) {
    processFile(files[0])
  }
}

// 处理文件
const processFile = (file) => {
  // 检查文件类型
  if (!file.type.startsWith('image/')) {
    alert('请选择图片文件!')
    return
  }
  
  // 检查文件大小 (限制为 10MB)
  if (file.size > 10 * 1024 * 1024) {
    alert('图片大小不能超过 10MB!')
    return
  }
  
  selectedFile.value = file
  
  // 创建预览 URL
  const reader = new FileReader()
  reader.onload = (e) => {
    previewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)
  
  // 清除之前的上传结果
  uploadResult.value = null
}

// 生成文件名：用户ID/UTC日期/UUID.扩展名
const generateFileName = (originalFile) => {
  const userId = user.value?.id || 'anonymous'
  const now = new Date()
  const utcDate = now.toISOString().split('T')[0] // YYYY-MM-DD 格式
  const uuid = uuidv4()
  const fileExtension = originalFile.name.split('.').pop().toLowerCase()
  
  return `${userId}/${utcDate}/${uuid}.${fileExtension}`
}

// 检查用户权限
const canUpload = computed(() => {
  return isAuthenticated.value && !!user.value
})

// 上传图片
const uploadImage = async () => {
  if (!selectedFile.value) return
  
  // // 检查用户权限
  // if (!canUpload.value) {
  //   alert('请先登录后再上传图片')
  //   return
  // }
  
  uploading.value = true
  uploadResult.value = null
  
  try {
    // 生成文件名：用户ID/UTC日期/UUID.扩展名
    const fileName = generateFileName(selectedFile.value)
    console.log('生成的文件名:', fileName)
    console.log('用户ID:', user.value?.id)
    
    // 上传到 Supabase
    const result = await uploadToSupabase(selectedFile.value, fileName)
    uploadResult.value = result
    
  } catch (error) {
    uploadResult.value = {
      success: false,
      error: error.message || '上传失败'
    }
  } finally {
    uploading.value = false
  }
}

// 清除文件
const clearFile = () => {
  selectedFile.value = null
  previewUrl.value = ''
  uploadResult.value = null
  // 清除生成相关状态
  generating.value = false
  generationStatus.value = null
  generatedImages.value = []
  imageLoading.value = {}
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 生成图像
const generateImages = async () => {
  if (!uploadResult.value?.publicUrl) return
  
  // // 检查用户权限
  // if (!canUpload.value) {
  //   alert('请先登录后再生成图像')
  //   return
  // }
  
  generating.value = true
  generationStatus.value = null
  generatedImages.value = []
  imageLoading.value = {}
  
  const taskId = `task_${Date.now()}`
  const requestData = {
    urls: [uploadResult.value.publicUrl],
    task_id: taskId
  }
  
  try {
    // 获取JWT访问令牌
    const accessToken = await getAccessToken()
    if (!accessToken) {
      throw new Error('无法获取访问令牌，请重新登录')
    }
    
    console.log('使用JWT令牌请求SSE接口:', accessToken.substring(0, 20) + '...')
    
    const response = await fetch('/api/faceflip/generate/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(requestData)
    })
    
    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('认证失败，请重新登录')
      } else if (response.status === 403) {
        throw new Error('权限不足，无法访问此功能')
      } else {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
    }
    
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = '' // 用于缓存不完整的数据
    
    const readStream = () => {
      return reader.read().then(({ done, value }) => {
        if (done) {
          generating.value = false
          return
        }
        
        // 将新数据添加到缓冲区
        buffer += decoder.decode(value, { stream: true })
        
        // 按双换行符分割SSE事件
        const events = buffer.split('\n\n')
        
        // 保留最后一个可能不完整的事件
        buffer = events.pop() || ''
        
        // 处理完整的事件
        events.forEach(eventText => {
          if (eventText.trim()) {
            parseSSEEvent(eventText.trim())
          }
        })
        
        return readStream()
      })
    }
    
    // 解析单个SSE事件
    const parseSSEEvent = (eventText) => {
      const lines = eventText.split('\n')
      let eventType = ''
      let eventData = ''
      
      lines.forEach(line => {
        if (line.startsWith('event:')) {
          eventType = line.substring(6).trim() // 使用substring避免split问题
        } else if (line.startsWith('data:')) {
          // 处理data行，可能包含冒号
          const dataContent = line.substring(5).trim() // 移除'data:'前缀
          if (eventData) {
            eventData += '\n' + dataContent // 如果有多行data，合并
          } else {
            eventData = dataContent
          }
        }
      })
      
      if (eventType && eventData) {
        try {
          const parsedData = JSON.parse(eventData)
          
          // 构建正确的事件数据结构
          const eventPayload = {
            event: eventType,
            data: parsedData
          }
          
          handleGenerationEvent(eventPayload)
        } catch (e) {
          console.error('解析SSE数据失败:', eventData, e)
          // 尝试修复常见的JSON格式问题
          try {
            // 如果JSON解析失败，尝试修复格式
            let fixedData = eventData
            // 检查是否有未闭合的引号或括号
            if (!fixedData.includes('"task_id"')) {
              console.log('尝试修复JSON格式...')
              // 这里可以添加更多的修复逻辑
            }
            const parsedData = JSON.parse(fixedData)
            handleGenerationEvent(parsedData)
          } catch (e2) {
            console.error('修复JSON后仍然解析失败:', e2)
            // 发送一个通用的错误事件
            handleGenerationEvent({
              event: 'error',
              data: {
                message: '数据解析失败',
                error: e.message
              }
            })
          }
        }
      }
    }
    
    await readStream()
    
  } catch (error) {
    console.error('图像生成失败:', error)
    generationStatus.value = {
      type: 'error',
      title: '❌ 生成失败',
      message: error.message || '图像生成过程中发生错误'
    }
    generating.value = false
  }
}

// 处理生成事件
const handleGenerationEvent = (data) => {
  switch (data.event) {
    case 'start':
      generationStatus.value = {
        type: 'start',
        title: '🚀 开始生成',
        message: data.message || '正在准备生成图像...'
      }
      // 记录用户信息（如果存在）
      if (data.user_email) {
        console.log(`用户 ${data.user_email} 开始生成图像`)
      }
      break
      
    case 'process':
      generationStatus.value = {
        type: 'process',
        title: '⚙️ 处理中',
        message: data.message || '正在调用AI模型生成图像...'
      }
      break
      
    case 'done':
      generationStatus.value = {
        type: 'success',
        title: '✅ 生成完成',
        message: `成功生成了 ${data.data.generated_images.length} 张图像`
      }
      
      // 确保图像数据正确设置
      generatedImages.value = data.data.generated_images || []
      
      // 初始化图像加载状态
      generatedImages.value.forEach((_, index) => {
        imageLoading.value[index] = true
      })
      
      generating.value = false
      break
      
    case 'error':
      // 处理不同类型的错误
      let errorTitle = '❌ 生成失败'
      let errorMessage = data.data.message || '图像生成失败'
      let errorDetails = ''
      
      if (data.data.error) {
        const error = data.data.error
        
        // 处理特定错误类型
        if (error.includes('ARK_API_KEY')) {
          errorTitle = '🔑 API密钥未配置'
          errorMessage = 'ARK API密钥未设置，请联系管理员配置'
          errorDetails = '服务器需要配置火山引擎ARK API密钥才能生成图像'
        } else if (error.includes('认证') || error.includes('401')) {
          errorTitle = '🔐 认证失败'
          errorMessage = '认证失败，请重新登录'
          errorDetails = '您的登录状态已过期，请重新登录后重试'
        } else if (error.includes('权限') || error.includes('403')) {
          errorTitle = '🚫 权限不足'
          errorMessage = '权限不足，无法访问此功能'
          errorDetails = '您没有权限使用图像生成功能'
        } else if (error.includes('网络') || error.includes('timeout')) {
          errorTitle = '🌐 网络错误'
          errorMessage = '网络连接超时，请检查网络后重试'
          errorDetails = '无法连接到图像生成服务，请稍后重试'
        } else if (error.includes('API') || error.includes('quota')) {
          errorTitle = '📊 API限制'
          errorMessage = 'API调用次数已达上限'
          errorDetails = '图像生成服务暂时不可用，请稍后重试'
        } else {
          errorDetails = `技术错误: ${error}`
        }
      }
      
      generationStatus.value = {
        type: 'error',
        title: errorTitle,
        message: errorMessage,
        details: errorDetails
      }
      generating.value = false
      break
  }
}

// 图像加载处理
const onImageLoad = (index) => {
  imageLoading.value[index] = false
}

const onImageError = (index) => {
  imageLoading.value[index] = false
}

// 下载图像
const downloadImage = async (url, index) => {
  try {
    // 创建一个临时的a标签来触发下载
    const link = document.createElement('a')
    link.href = url
    link.download = `generated_image_${index + 1}.jpg`
    link.target = '_blank'
    
    // 添加到DOM，点击，然后移除
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (error) {
    alert('下载失败，请尝试右键保存图像')
  }
}
</script>

<style scoped>
.image-upload-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.upload-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.upload-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.upload-area {
  border: 2px dashed #ccc;
  border-radius: 10px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.upload-area:hover {
  border-color: #007bff;
  background-color: #f8f9fa;
}

.upload-placeholder {
  color: #666;
}

.upload-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.upload-hint {
  font-size: 14px;
  color: #999;
  margin-top: 5px;
}

.file-preview {
  display: flex;
  align-items: center;
  gap: 20px;
}

.preview-image {
  max-width: 150px;
  max-height: 150px;
  border-radius: 8px;
  object-fit: cover;
}

.file-info {
  text-align: left;
  flex: 1;
}

.file-info p {
  margin: 5px 0;
  color: #333;
}

.upload-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 20px;
}

.upload-btn, .clear-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
}

.upload-btn {
  background-color: #007bff;
  color: white;
}

.upload-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

.upload-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.clear-btn {
  background-color: #6c757d;
  color: white;
}

.clear-btn:hover:not(:disabled) {
  background-color: #545b62;
}

.upload-result {
  margin-top: 20px;
  padding: 20px;
  border-radius: 8px;
}

.success-message {
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  color: #155724;
}

.error-message {
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.image-link {
  color: #007bff;
  text-decoration: none;
  word-break: break-all;
  display: block;
  margin: 10px 0;
}

.image-link:hover {
  text-decoration: underline;
}

.uploaded-image {
  margin-top: 15px;
}

.uploaded-image img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* 生成按钮样式 */
.generate-section {
  margin-top: 20px;
  text-align: center;
}

.generate-btn {
  background-color: #28a745;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
}

.generate-btn:hover:not(:disabled) {
  background-color: #218838;
}

.generate-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

/* 生成状态样式 */
.generation-status {
  margin-top: 20px;
  padding: 20px;
  border-radius: 8px;
}

.status-message {
  text-align: center;
}

.status-message.start {
  background-color: #d1ecf1;
  border: 1px solid #bee5eb;
  color: #0c5460;
}

.status-message.process {
  background-color: #fff3cd;
  border: 1px solid #ffeaa7;
  color: #856404;
}

.status-message.success {
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  color: #155724;
}

.status-message.error {
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

/* 加载动画 */
.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #856404;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 10px auto;
}

/* 错误详情和建议样式 */
.error-details {
  margin-top: 10px;
  padding: 10px;
  background-color: rgba(0,0,0,0.05);
  border-radius: 4px;
  font-size: 14px;
  color: #666;
}

.error-suggestions {
  margin-top: 15px;
  padding: 15px;
  background-color: rgba(0,0,0,0.03);
  border-radius: 6px;
  border-left: 4px solid #007bff;
}

.error-suggestions h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 14px;
}

.error-suggestions ul {
  margin: 0;
  padding-left: 20px;
}

.error-suggestions li {
  margin: 8px 0;
  color: #555;
  font-size: 14px;
}

.retry-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  margin-left: 10px;
  transition: background-color 0.3s ease;
}

.retry-btn:hover {
  background-color: #0056b3;
}

/* 生成结果样式 */
.generated-images {
  margin-top: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.generated-images h3 {
  text-align: center;
  color: #333;
  margin-bottom: 10px;
}

.generated-count {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-bottom: 20px;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
  margin-top: 20px;
}

.generated-image-item {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.generated-image-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

.image-container {
  position: relative;
  width: 100%;
  height: 300px;
  overflow: hidden;
}

.generated-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.3s ease;
}

.image-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 255, 255, 0.9);
  padding: 10px;
  border-radius: 50%;
}

.image-info {
  padding: 15px;
}

.image-size {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 14px;
}

.image-actions {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.view-btn {
  background-color: #007bff;
  color: white;
}

.view-btn:hover {
  background-color: #0056b3;
}

.download-btn {
  background-color: #28a745;
  color: white;
}

.download-btn:hover {
  background-color: #218838;
}

@media (max-width: 768px) {
  .file-preview {
    flex-direction: column;
    text-align: center;
  }
  
  .file-info {
    text-align: center;
  }
  
  .upload-actions {
    flex-direction: column;
  }
  
  .images-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .image-container {
    height: 250px;
  }
}
</style>
