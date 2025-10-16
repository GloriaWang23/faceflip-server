# 图像生成服务修改说明

## 修改概述

根据用户需求，已将图像生成服务从返回ARK API的URL改为：
1. 从ARK API获取base64格式的图片数据
2. 将base64图片上传到Supabase存储
3. 返回Supabase存储的公开URL

## 主要修改

### 1. 依赖更新
- 添加了 `base64`, `uuid`, `datetime` 模块
- 集成了 `supabase` Python SDK

### 2. 服务类修改 (`app/services/image_generation_service.py`)

#### 新增属性
- `_ark_client`: ARK客户端实例
- `_supabase_client`: Supabase客户端实例

#### 新增方法
- `ark_client`: 延迟初始化ARK客户端
- `supabase_client`: 延迟初始化Supabase客户端
- `_upload_base64_to_supabase()`: 将base64图片上传到Supabase存储

#### 修改的方法
- `_call_ark_api()`: 将 `response_format` 从 `"url"` 改为 `"b64_json"`
- `generate_images_stream()`: 添加了上传到Supabase的逻辑

### 3. 配置更新 (`app/core/config.py`)
- 添加了 `supabase_storage_bucket` 配置项，默认值为 `"faceflip-images"`

## 工作流程

1. **接收请求**: 接收图片URL列表和任务ID
2. **调用ARK API**: 使用base64格式请求图片生成
3. **上传到Supabase**: 
   - 解码base64数据
   - 生成文件路径：`/UTC日期/UUID.png`
   - 上传到Supabase存储桶
   - 获取公开URL
4. **返回结果**: 返回Supabase存储的URL

## 环境变量要求

需要设置以下环境变量：
- `ARK_API_KEY`: ARK API密钥
- `SUPABASE_URL`: Supabase项目URL
- `SUPABASE_KEY`: Supabase API密钥

## 存储结构

图片将按以下结构存储在Supabase中：
```
faceflip-images/
├── 2024-01-15/
│   ├── uuid1.png
│   ├── uuid2.png
│   └── uuid3.png
└── 2024-01-16/
    └── ...
```

## 错误处理

- 如果上传到Supabase失败，会记录错误但继续处理其他图片
- 所有异常都会被捕获并作为SSE错误事件发送
- 修复了Supabase Python SDK响应对象处理问题（UploadResponse对象结构）

## 已知问题和修复

### 问题：'UploadResponse' object has no attribute 'get'
**原因**: Supabase Python SDK返回的是UploadResponse对象，不是字典
**修复**: 使用 `hasattr(result, 'error')` 和 `result.error` 来检查错误

## 测试

可以使用 `test_image_service.py` 脚本进行测试，需要先设置相应的环境变量。
