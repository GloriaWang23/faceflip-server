"""Common schemas"""

from typing import Optional, Generic, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    """Generic response wrapper"""
    success: bool = True
    message: str = "Success"
    data: Optional[T] = None
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = False
    message: str
    detail: Optional[str] = None
    
    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema"""
    items: list[T]
    total: int
    page: int = 1
    page_size: int = 10
    total_pages: int
    
    class Config:
        from_attributes = True

