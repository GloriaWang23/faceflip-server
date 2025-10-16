"""File handling utilities"""

import os
import uuid
from typing import Optional
from pathlib import Path
from fastapi import UploadFile, HTTPException, status

from app.core.config import settings


async def save_upload_file(file: UploadFile, folder: str = "uploads") -> str:
    """Save uploaded file to disk"""
    # Validate file size
    file_size = 0
    chunk_size = 1024 * 1024  # 1MB chunks
    
    # Create upload folder if not exists
    upload_path = Path(settings.upload_folder) / folder
    upload_path.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_ext = Path(file.filename or "").suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = upload_path / unique_filename
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(chunk_size):
                file_size += len(chunk)
                
                # Check file size
                if file_size > settings.max_upload_size:
                    # Delete partial file
                    buffer.close()
                    os.remove(file_path)
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File too large. Max size: {settings.max_upload_size} bytes"
                    )
                
                buffer.write(chunk)
        
        return str(file_path)
    except Exception as e:
        # Clean up on error
        if file_path.exists():
            os.remove(file_path)
        raise e


def delete_file(file_path: str) -> bool:
    """Delete a file from disk"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False


def get_file_extension(filename: str) -> str:
    """Get file extension"""
    return Path(filename).suffix.lower()


def is_valid_image(filename: str) -> bool:
    """Check if file is a valid image"""
    valid_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
    return get_file_extension(filename) in valid_extensions


def is_valid_video(filename: str) -> bool:
    """Check if file is a valid video"""
    valid_extensions = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
    return get_file_extension(filename) in valid_extensions

