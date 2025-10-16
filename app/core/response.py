"""统一响应封装"""

from typing import Any, Optional, TypeVar, Generic
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.response_code import ResponseCode


T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    """统一响应模型"""
    code: int
    msg: str
    data: Optional[T] = None
    
    class Config:
        from_attributes = True


class ResponseUtil:
    """响应工具类"""
    
    @staticmethod
    def success(data: Any = None, msg: str = "success") -> JSONResponse:
        """成功响应"""
        return JSONResponse(
            status_code=200,
            content={
                "code": ResponseCode.SUCCESS.code,
                "msg": msg,
                "data": data
            }
        )
    
    @staticmethod
    def error(
        code: ResponseCode = ResponseCode.E_SYSTEM_BUSY,
        msg: Optional[str] = None,
        data: Any = None
    ) -> JSONResponse:
        """错误响应"""
        return JSONResponse(
            status_code=200,  # HTTP 状态码始终返回 200
            content={
                "code": code.code,
                "msg": msg or code.message,
                "data": data
            }
        )
    
    @staticmethod
    def custom(code: int, msg: str, data: Any = None) -> JSONResponse:
        """自定义响应"""
        return JSONResponse(
            status_code=200,
            content={
                "code": code,
                "msg": msg,
                "data": data
            }
        )


# 便捷方法
def success(data: Any = None, msg: str = "success") -> JSONResponse:
    """成功响应"""
    return ResponseUtil.success(data, msg)


def error(
    code: ResponseCode = ResponseCode.E_SYSTEM_BUSY,
    msg: Optional[str] = None,
    data: Any = None
) -> JSONResponse:
    """错误响应"""
    return ResponseUtil.error(code, msg, data)

