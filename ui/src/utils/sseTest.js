// SSE数据解析测试
const testSSEParsing = () => {
  console.log('测试SSE数据解析...')
  
  // 模拟SSE数据
  const mockSSEData = `event: start
data: {"task_id": "test_123", "user_id": "user_456", "message": "开始生成图像..."}

event: process
data: {"task_id": "test_123", "message": "正在处理..."}

event: done
data: {"task_id": "test_123", "generated_images": [{"url": "http://example.com/image1.jpg", "size": "2K"}]}

`
  
  // 测试解析逻辑
  const events = mockSSEData.split('\n\n')
  events.forEach(eventText => {
    if (eventText.trim()) {
      const lines = eventText.split('\n')
      let eventType = ''
      let eventData = ''
      
      lines.forEach(line => {
        if (line.startsWith('event:')) {
          eventType = line.split(':')[1].trim()
        } else if (line.startsWith('data:')) {
          eventData = line.split(':')[1].trim()
        }
      })
      
      if (eventType && eventData) {
        console.log('解析事件:', eventType, eventData)
        try {
          const parsedData = JSON.parse(eventData)
          console.log('解析成功:', parsedData)
        } catch (e) {
          console.error('解析失败:', eventData, e)
        }
      }
    }
  })
}

// 在浏览器控制台中运行测试
if (typeof window !== 'undefined') {
  window.testSSEParsing = testSSEParsing
  console.log('SSE解析测试函数已加载，运行 testSSEParsing() 进行测试')
}
