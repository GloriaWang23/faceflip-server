"""Error handling middleware"""

import logging
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.response_code import ResponseCode
from app.core.response import error

# 配置日志
logger = logging.getLogger(__name__)


async def error_handler_middleware(request: Request, call_next):
    """全局错误处理中间件 - 捕获所有异常"""
    try:
        return await call_next(request)
    except Exception as exc:
        # 记录详细的错误日志
        logger.error(
            f"❌ Unhandled exception in {request.method} {request.url.path}\n"
            f"Exception type: {type(exc).__name__}\n"
            f"Exception message: {str(exc)}\n"
            f"Traceback:\n{''.join(traceback.format_tb(exc.__traceback__))}",
            exc_info=True,
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_host": request.client.host if request.client else "unknown"
            }
        )
        
        return error(
            code=ResponseCode.E_SYSTEM_BUSY,
            msg=f"system error: {str(exc)}"
        )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理数据验证错误"""
    errors = exc.errors()
    error_messages = []
    
    for error_item in errors:
        field = ".".join(str(x) for x in error_item["loc"])
        message = error_item["msg"]
        error_messages.append(f"{field}: {message}")
    
    # 记录验证错误日志
    logger.warning(
        f"⚠️  Validation error in {request.method} {request.url.path}\n"
        f"Errors: {error_messages}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "validation_errors": errors
        }
    )
    
    return error(
        code=ResponseCode.E_INVALID_PARAM,
        msg="param invalid",
        data={"errors": errors, "messages": error_messages}
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """处理 HTTP 异常"""
    detail = str(exc.detail)
    
    # 记录 HTTP 异常日志
    log_level = logging.WARNING if exc.status_code < 500 else logging.ERROR
    logger.log(
        log_level,
        f"{'⚠️ ' if exc.status_code < 500 else '❌'} HTTP {exc.status_code} in {request.method} {request.url.path}\n"
        f"Detail: {detail}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": exc.status_code,
            "detail": detail
        }
    )
    
    # 检查 detail 是否包含自定义错误码（格式：code|message）
    if "|" in detail:
        try:
            code_str, msg = detail.split("|", 1)
            custom_code = int(code_str)
            
            # 尝试从枚举中获取对应的错误码
            response_code = ResponseCode.get_by_code(custom_code)
            if response_code:
                logger.debug(f"Using custom response code: {response_code.name} ({custom_code})")
                return error(code=response_code, msg=msg)
            else:
                # 自定义错误码，直接使用
                logger.debug(f"Using direct custom code: {custom_code}")
                return JSONResponse(
                    status_code=200,
                    content={"code": custom_code, "msg": msg, "data": None}
                )
        except (ValueError, AttributeError) as e:
            logger.warning(f"⚠️  Failed to parse custom error code from detail: {e}")
    
    # 默认根据 HTTP 状态码映射
    status_code_map = {
        400: ResponseCode.BAD_REQUEST,
        401: ResponseCode.UNAUTHORIZED,
        403: ResponseCode.FORBIDDEN,
        404: ResponseCode.NOT_FOUND,
        405: ResponseCode.METHOD_NOT_ALLOWED,
    }
    
    response_code = status_code_map.get(exc.status_code, ResponseCode.E_SYSTEM_BUSY)
    logger.debug(f"Mapped HTTP {exc.status_code} to response code: {response_code.name}")
    
    return error(code=response_code, msg=detail)

