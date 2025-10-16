import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator

from app.core.config import settings
from app.core.response import success
from app.core.dependencies import CurrentUser
from app.schemas.face_flip import ImageGenerationRequest, SSEEvent
from app.services.image_generation_service import image_generation_service


router = APIRouter()


@router.get("/debug/auth")
async def debug_auth(current_user: CurrentUser):
    """
    调试认证状态接口
    """
    return {
        "authenticated": True,
        "user": current_user,
        "method": "dependency_injection",
        "message": "通过依赖注入认证成功"
    }


@router.get("/debug/env")
async def debug_env():
    """
    调试环境变量配置
    """
    from app.core.config import settings
    
    return {
        "supabase_url": settings.supabase_url[:20] + "..." if settings.supabase_url else None,
        "supabase_key": settings.supabase_key[:10] + "..." if settings.supabase_key else None,
        "supabase_service_role_key": "SET" if settings.supabase_service_role_key else "NOT_SET",
        "ark_api_key": "SET" if settings.ark_api_key else "NOT_SET",
        "secret_key": "SET" if settings.secret_key else "NOT_SET",
        "message": "环境变量检查完成"
    }


@router.post("/generate/stream")
async def generate_images_stream(
    request: ImageGenerationRequest,
    current_user: CurrentUser
) -> StreamingResponse:
    """
    流式生成图像接口（需要JWT认证）
    
    Args:
        request: 图像生成请求，包含urls和task_id
        current_user: 当前登录用户（通过依赖注入获取）
        
    Returns:
        StreamingResponse: SSE流式响应
    """
    
    # 验证用户权限（可选：添加更多权限检查）
    user_id = current_user.get("id")
    user_email = current_user.get("email")
    
    # 记录用户操作日志
    print(f"用户 {user_email} (ID: {user_id}) 开始生成图像，任务ID: {request.task_id}")
    
    async def event_generator() -> AsyncGenerator[str, None]:
        """生成SSE事件流"""
        try:
            # 发送开始事件，包含用户信息
            start_event = SSEEvent(
                event="start",
                data={
                    "task_id": request.task_id,
                    "user_id": user_id,
                    "user_email": user_email,
                    "message": "开始生成图像..."
                }
            )
            event_data = f"event: {start_event.event}\n"
            json_data = json.dumps(start_event.data, ensure_ascii=False)
            event_data += f"data: {json_data}\n\n"
            print(f"发送开始SSE事件: {start_event.event}, 数据: {json_data}")
            yield event_data
            
            # 调用图像生成服务
            async for event in image_generation_service.generate_images_stream(
                urls=request.urls,
                task_id=request.task_id,
                user_id=user_id
            ):
                # 格式化SSE事件
                event_data = f"event: {event.event}\n"
                json_data = json.dumps(event.data, ensure_ascii=False)
                event_data += f"data: {json_data}\n\n"
                print(f"发送SSE事件: {event.event}, 数据: {json_data}")
                yield event_data
                
        except Exception as e:
            # 发送错误事件
            error_event = SSEEvent(
                event="error",
                data={
                    "task_id": request.task_id,
                    "user_id": user_id,
                    "user_email": user_email,
                    "error": str(e),
                    "message": "图像生成过程中发生错误"
                }
            )
            event_data = f"event: {error_event.event}\n"
            json_data = json.dumps(error_event.data, ensure_ascii=False)
            event_data += f"data: {json_data}\n\n"
            print(f"发送错误SSE事件: {error_event.event}, 数据: {json_data}")
            yield event_data
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control, Authorization",
            "Access-Control-Allow-Methods": "POST, OPTIONS"
        }
    )
