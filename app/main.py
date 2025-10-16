"""FastAPI main application"""

import logging
from contextlib import asynccontextmanager
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

# 初始化日志系统
setup_logging(
    log_level="DEBUG" if settings.debug else "INFO",
    enable_file_logging=True  # 可以改为 True 启用文件日志
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"📝 Debug mode: {settings.debug}")
    logger.info(f"🌐 Server: {settings.host}:{settings.port}")
    logger.info(f"🔐 Global auth: enabled")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("=" * 60)
    logger.info(f"👋 Shutting down {settings.app_name}")
    logger.info("=" * 60)


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
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
app.add_middleware(AuthMiddleware, enable=True)  # 启用全局认证，类似 Spring 拦截器
app.middleware("http")(error_handler_middleware)

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
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return success(data={
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version
    })

