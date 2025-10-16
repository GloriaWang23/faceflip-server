# 图像生成流式接口使用说明

## 接口概述

`/generate/stream` 接口提供了基于ARK模型的图像生成功能，采用Server-Sent Events (SSE) 技术实现流式响应。

## 接口地址

```
POST /api/v1/faceflip/generate/stream
```

## 请求参数

### 请求体 (JSON)

```json
{
    "urls": [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ],
    "task_id": "unique_task_id_123"
}
```

### 参数说明

- `urls` (List[str]): 输入图片的URL列表
- `task_id` (str): 唯一的任务标识符

## 响应格式

接口返回SSE流式响应，包含以下事件类型：

### 1. start 事件
```json
{
    "event": "start",
    "data": {
        "task_id": "unique_task_id_123",
        "message": "开始生成图像..."
    }
}
```

### 2. process 事件
```json
{
    "event": "process", 
    "data": {
        "task_id": "unique_task_id_123",
        "message": "正在调用ARK模型生成图像..."
    }
}
```

### 3. done 事件
```json
{
    "event": "done",
    "data": {
        "urls": [
            "https://example.com/image1.jpg",
            "https://example.com/image2.jpg"
        ],
        "generated_images": [
            {
                "url": "https://generated-image1.jpg",
                "size": "2K"
            },
            {
                "url": "https://generated-image2.jpg", 
                "size": "2K"
            }
        ],
        "task_id": "unique_task_id_123"
    }
}
```

### 4. error 事件
```json
{
    "event": "error",
    "data": {
        "task_id": "unique_task_id_123",
        "error": "错误信息",
        "message": "图像生成失败"
    }
}
```

## 前端使用示例

### JavaScript (使用EventSource)

```javascript
const testData = {
    urls: [
        "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_1.png",
        "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_2.png"
    ],
    task_id: "task_" + Date.now()
};

// 发送POST请求获取SSE流
fetch('/api/v1/faceflip/generate/stream', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(testData)
})
.then(response => {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    function readStream() {
        return reader.read().then(({ done, value }) => {
            if (done) {
                console.log('流结束');
                return;
            }
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            lines.forEach(line => {
                if (line.startsWith('event:')) {
                    const eventType = line.split(':')[1].trim();
                    console.log('事件类型:', eventType);
                } else if (line.startsWith('data:')) {
                    const data = line.split(':')[1].trim();
                    try {
                        const parsedData = JSON.parse(data);
                        console.log('事件数据:', parsedData);
                        
                        // 处理不同事件类型
                        switch (parsedData.event) {
                            case 'start':
                                console.log('开始生成图像');
                                break;
                            case 'process':
                                console.log('正在处理...');
                                break;
                            case 'done':
                                console.log('生成完成:', parsedData.data);
                                break;
                            case 'error':
                                console.error('生成失败:', parsedData.data);
                                break;
                        }
                    } catch (e) {
                        console.log('原始数据:', data);
                    }
                }
            });
            
            return readStream();
        });
    }
    
    readStream();
})
.catch(error => {
    console.error('请求失败:', error);
});
```

### Vue.js 组件示例

```vue
<template>
  <div>
    <button @click="generateImages" :disabled="isGenerating">
      {{ isGenerating ? '生成中...' : '生成图像' }}
    </button>
    
    <div v-if="generatedImages.length > 0">
      <h3>生成的图像:</h3>
      <div v-for="image in generatedImages" :key="image.url">
        <img :src="image.url" :alt="'Generated image ' + image.size" />
        <p>尺寸: {{ image.size }}</p>
      </div>
    </div>
    
    <div v-if="errorMessage">
      <p style="color: red;">错误: {{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isGenerating: false,
      generatedImages: [],
      errorMessage: '',
      taskId: ''
    }
  },
  methods: {
    async generateImages() {
      this.isGenerating = true;
      this.generatedImages = [];
      this.errorMessage = '';
      this.taskId = 'task_' + Date.now();
      
      const requestData = {
        urls: [
          "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_1.png",
          "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_2.png"
        ],
        task_id: this.taskId
      };
      
      try {
        const response = await fetch('/api/v1/faceflip/generate/stream', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData)
        });
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        const readStream = () => {
          return reader.read().then(({ done, value }) => {
            if (done) {
              this.isGenerating = false;
              return;
            }
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            lines.forEach(line => {
              if (line.startsWith('data:')) {
                const data = line.split(':')[1].trim();
                try {
                  const parsedData = JSON.parse(data);
                  this.handleEvent(parsedData);
                } catch (e) {
                  console.log('解析数据失败:', data);
                }
              }
            });
            
            return readStream();
          });
        };
        
        await readStream();
        
      } catch (error) {
        this.errorMessage = error.message;
        this.isGenerating = false;
      }
    },
    
    handleEvent(data) {
      switch (data.event) {
        case 'start':
          console.log('开始生成图像');
          break;
        case 'process':
          console.log('正在处理...');
          break;
        case 'done':
          this.generatedImages = data.data.generated_images;
          this.isGenerating = false;
          break;
        case 'error':
          this.errorMessage = data.data.message;
          this.isGenerating = false;
          break;
      }
    }
  }
}
</script>
```

## 环境配置

### 方法1: 设置环境变量

```bash
export ARK_API_KEY="your_ark_api_key_here"
```

### 方法2: 创建 .env 文件

在项目根目录创建 `.env` 文件：

```bash
# .env
ARK_API_KEY=your_ark_api_key_here
```

### 方法3: 使用设置脚本

运行提供的设置脚本：

```bash
./setup_env.sh
```

### 验证配置

启动服务器前，确保环境变量已正确设置：

```bash
echo $ARK_API_KEY
```

如果输出为空，请重新设置环境变量。

## 测试

使用提供的测试脚本：

```bash
python test_generate_stream.py
```

确保服务器正在运行：

```bash
python run.py
```

## 注意事项

1. 确保ARK API Key已正确配置
2. 输入图片URL必须是可公开访问的
3. 生成的图片数量由ARK模型决定（通常为3张）
4. 接口支持CORS，可用于前端跨域请求
5. SSE连接会自动保持活跃状态
