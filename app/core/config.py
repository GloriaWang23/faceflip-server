"""Application configuration settings"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Face Flip Server"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS
    cors_origins: list[str] = ["*"]
    cors_credentials: bool = True
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]
    
    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_role_key: Optional[str] = None
    supabase_storage_bucket: str = "faceflip-images"
    
    # JWT
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: Optional[str] = None
    
    # File Upload
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    upload_folder: str = "uploads"
    
    # Logging
    log_level: str = "INFO"
    
    # ARK API
    ark_api_key: Optional[str] = None
    
    # ARK Image Generation
    ark_default_prompt: str = "生成3张女孩和奶牛玩偶在游乐园开心地坐过山车的图片，涵盖早晨、中午、晚上"
    ark_model: str = "doubao-seedream-4-0-250828"
    ark_image_size: str = "2K"
    ark_max_images: int = 3
    
    # SSE 超时设置（Vercel兼容）
    sse_timeout_seconds: int = 60  # SSE连接超时时间（60秒，Vercel限制）
    sse_keep_alive_interval: int = 15  # SSE心跳间隔（15秒）
    ark_api_timeout_seconds: int = 45  # ARK API调用超时时间（45秒）
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()

