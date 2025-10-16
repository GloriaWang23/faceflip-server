"""Error handling middleware"""

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.response_code import ResponseCode
from app.core.response import error


async def error_handler_middleware(request: Request, call_next):
    """全局错误处理中间件 - 捕获所有异常"""
    try:
        return await call_next(request)
    except Exception as exc:
        print(f"❌ Unhandled error: {exc}")
        import traceback
        traceback.print_exc()
        
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
    
    return error(
        code=ResponseCode.E_INVALID_PARAM,
        msg="param invalid",
        data={"errors": errors, "messages": error_messages}
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """处理 HTTP 异常"""
    detail = str(exc.detail)
    
    # 检查 detail 是否包含自定义错误码（格式：code|message）
    if "|" in detail:
        try:
            code_str, msg = detail.split("|", 1)
            custom_code = int(code_str)
            
            # 尝试从枚举中获取对应的错误码
            response_code = ResponseCode.get_by_code(custom_code)
            if response_code:
                return error(code=response_code, msg=msg)
            else:
                # 自定义错误码，直接使用
                return JSONResponse(
                    status_code=200,
                    content={"code": custom_code, "msg": msg, "data": None}
                )
        except (ValueError, AttributeError):
            pass
    
    # 默认根据 HTTP 状态码映射
    status_code_map = {
        400: ResponseCode.BAD_REQUEST,
        401: ResponseCode.UNAUTHORIZED,
        403: ResponseCode.FORBIDDEN,
        404: ResponseCode.NOT_FOUND,
        405: ResponseCode.METHOD_NOT_ALLOWED,
    }
    
    response_code = status_code_map.get(exc.status_code, ResponseCode.INTERNAL_ERROR)
    
    return error(code=response_code, msg=detail)

