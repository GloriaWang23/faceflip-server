"""Vercel serverless handler for FastAPI"""

import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

