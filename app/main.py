"""FastAPI main application"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.core.config import settings
from app.core.response import success
from app.api.routes import api_router
from app.middleware.logging import LoggingMiddleware
from app.middleware.error_handler import (
    error_handler_middleware,
    validation_exception_handler,
    http_exception_handler
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"📝 Debug mode: {settings.debug}")
    print(f"🌐 Server: {settings.host}:{settings.port}")
    
    yield
    
    # Shutdown
    print(f"👋 Shutting down {settings.app_name}")


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
app.add_middleware(LoggingMiddleware)
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

