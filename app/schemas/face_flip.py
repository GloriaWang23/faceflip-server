from pydantic import BaseModel
from typing import List, Optional


class FaceFlipOrder(BaseModel):
    order_id: str
    user_id: str
    product_id: str
    quantity: int
    total_price: float
    status: str


class ImageGenerationRequest(BaseModel):
    """图像生成请求模型"""
    urls: List[str]  # 输入图片URL列表
    task_id: str     # 任务ID


class GeneratedImage(BaseModel):
    """生成的图片信息"""
    url: str
    size: str


class ImageGenerationResponse(BaseModel):
    """图像生成响应模型"""
    urls: List[str]              # 生成前URL列表
    generated_images: List[GeneratedImage]  # 生成后图片列表
    task_id: str                 # 任务ID


class SSEEvent(BaseModel):
    """SSE事件模型"""
    event: str  # start, process, error, done
    data: Optional[dict] = None