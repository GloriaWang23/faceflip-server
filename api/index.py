"""Vercel serverless handler for FastAPI"""

import sys
import os
import logging

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.response import success
from app.api.routes import api_router
from app.middleware.auth import AuthMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.error_handler import (
    error_handler_middleware,
    validation_exception_handler,
    http_exception_handler
)

# 初始化日志系统（Vercel 环境）
setup_logging(
    log_level="INFO",  # Vercel 环境使用 INFO 级别
    enable_file_logging=False  # Vercel 不需要文件日志，使用 CloudWatch
)

logger = logging.getLogger(__name__)

# Create FastAPI application without lifespan for serverless
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Custom middlewares
# 注意：中间件的添加顺序很重要，执行顺序是反向的（后添加的先执行）
# 执行顺序：Logging -> Auth -> Error Handler
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware, enable=False)  # 启用全局认证
app.middleware("http")(error_handler_middleware)

logger.info("🚀 Vercel serverless function initialized")

# Exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# Include API routes
app.include_router(api_router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return success(data={
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "status": "running"
    })

# Health check endpoint
@app.get("/health/check")
async def health_check():
    """Health check endpoint"""
    return success(data={
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version
    })

