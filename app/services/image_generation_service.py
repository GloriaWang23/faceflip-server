"""图像生成服务"""

import os
import asyncio
import base64
import uuid
from datetime import datetime, timezone
from typing import List, AsyncGenerator, Optional
from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime.types.images.images import SequentialImageGenerationOptions
from supabase import create_client, Client

from app.core.config import settings
from app.schemas.face_flip import GeneratedImage, ImageGenerationResponse, SSEEvent


class ImageGenerationService:
    """图像生成服务类"""
    
    def __init__(self):
        """初始化服务"""
        self._ark_client = None
        self._supabase_client = None
    
    @property
    def ark_client(self):
        """延迟初始化ARK客户端"""
        if self._ark_client is None:
            api_key = settings.ark_api_key or os.environ.get("ARK_API_KEY")
            if not api_key:
                raise ValueError("ARK_API_KEY 环境变量未设置")
            
            self._ark_client = Ark(
                base_url="https://ark.cn-beijing.volces.com/api/v3",
                api_key=api_key,
            )
        return self._ark_client
    
    @property
    def supabase_client(self) -> Client:
        """延迟初始化Supabase客户端"""
        if self._supabase_client is None:
            supabase_url = settings.supabase_url or os.environ.get("SUPABASE_URL")
            supabase_key = settings.supabase_key or os.environ.get("SUPABASE_KEY")
            
            if not supabase_url or not supabase_key:
                raise ValueError("SUPABASE_URL 和 SUPABASE_KEY 环境变量未设置")
            
            self._supabase_client = create_client(supabase_url, supabase_key)
        return self._supabase_client
    
    async def _upload_base64_to_supabase(self, base64_data: str, filename: str, user_id: str) -> str:
        """
        将base64图片上传到Supabase存储
        
        Args:
            base64_data: base64编码的图片数据
            filename: 文件名
            user_id: 用户ID
            
        Returns:
            str: Supabase存储的公开URL
        """
        try:
            # 解码base64数据
            image_data = base64.b64decode(base64_data)
            
            # 生成存储路径：/userId/utc_date/uuid.png
            utc_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            file_path = f"{user_id}/{utc_date}/{filename}"
            
            # 上传到Supabase存储
            bucket_name = settings.supabase_storage_bucket
            result = self.supabase_client.storage.from_(bucket_name).upload(
                file_path,
                image_data,
                file_options={"content-type": "image/png"}
            )
            
            # 检查上传结果 - Supabase Python SDK返回的是UploadResponse对象
            if hasattr(result, 'error') and result.error:
                raise Exception(f"上传失败: {result.error}")
            
            # 验证上传是否成功
            if not hasattr(result, 'path') or not result.path:
                raise Exception("上传失败: 未返回文件路径")
            
            # 获取公开URL
            public_url = self.supabase_client.storage.from_(bucket_name).get_public_url(file_path)
            return public_url
            
        except Exception as e:
            raise Exception(f"上传到Supabase失败: {str(e)}")
    
    async def generate_images_stream(
        self, 
        urls: List[str], 
        task_id: str,
        user_id: str,
        prompt: Optional[str] = None
    ) -> AsyncGenerator[SSEEvent, None]:
        """
        流式生成图像
        
        Args:
            urls: 输入图片URL列表
            task_id: 任务ID
            user_id: 用户ID
            prompt: 生成提示词，如果为None则使用环境变量配置的默认值
            
        Yields:
            SSEEvent: SSE事件
        """
        try:
            # 使用环境变量配置的默认prompt（如果未提供）
            if prompt is None:
                prompt = settings.ark_default_prompt
            
            # 发送开始事件
            yield SSEEvent(
                event="start",
                data={"task_id": task_id, "message": "开始生成图像..."}
            )
            
            # 发送处理中事件
            yield SSEEvent(
                event="process",
                data={"task_id": task_id, "message": "正在调用ARK模型生成图像..."}
            )
            
            # 在线程池中执行同步的ARK API调用，带超时
            loop = asyncio.get_event_loop()
            images_response = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    self._call_ark_api,
                    urls,
                    prompt
                ),
                timeout=settings.ark_api_timeout_seconds
            )
            
            # 发送上传开始事件
            yield SSEEvent(
                event="upload_start",
                data={"task_id": task_id, "message": "开始上传生成的图片到存储..."}
            )
            
            # 处理响应并上传到Supabase
            generated_images = []
            for i, image in enumerate(images_response.data):
                try:
                    # 生成唯一文件名
                    filename = f"{uuid.uuid4()}.png"
                    
                    # 上传base64图片到Supabase
                    supabase_url = await self._upload_base64_to_supabase(
                        image.b64_json, 
                        filename,
                        user_id
                    )
                    
                    generated_images.append(GeneratedImage(
                        url=supabase_url,
                        size=image.size
                    ))
                    
                except Exception as e:
                    # 如果上传失败，记录错误但继续处理其他图片
                    print(f"上传图片 {i+1} 失败: {str(e)}")
                    # 可以选择跳过失败的图片或者使用原始URL
                    continue
            
            # 构建响应数据
            response_data = ImageGenerationResponse(
                urls=urls,
                generated_images=generated_images,
                task_id=task_id
            )
            
            # 发送完成事件
            yield SSEEvent(
                event="done",
                data=response_data.dict()
            )
            
        except Exception as e:
            # 发送错误事件
            yield SSEEvent(
                event="error",
                data={
                    "task_id": task_id,
                    "error": str(e),
                    "message": "图像生成失败"
                }
            )
    
    def _call_ark_api(self, urls: List[str], prompt: str):
        """
        调用ARK API生成图像
        
        Args:
            urls: 输入图片URL列表
            prompt: 生成提示词
            
        Returns:
            imagesResponse: ARK API响应
        """
        return self.ark_client.images.generate(
            model=settings.ark_model,
            prompt=prompt,
            image=urls,
            size=settings.ark_image_size,
            sequential_image_generation="auto",
            sequential_image_generation_options=SequentialImageGenerationOptions(max_images=settings.ark_max_images),
            response_format="b64_json",  # 改为返回base64格式
            watermark=True
        )


# 创建服务实例
image_generation_service = ImageGenerationService()
