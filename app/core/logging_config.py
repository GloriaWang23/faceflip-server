"""日志配置模块"""

import logging
import sys
from pathlib import Path
from typing import Optional

from app.core.config import settings


def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None,
    enable_file_logging: bool = False
):
    """
    配置应用日志系统
    
    Args:
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 日志文件路径（可选）
        enable_file_logging: 是否启用文件日志
    """
    # 确定日志级别
    if log_level is None:
        log_level = "DEBUG" if settings.debug else "INFO"
    
    # 转换为大写
    log_level = log_level.upper()
    
    # 日志格式
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - "
        "%(message)s"
    )
    
    # 详细日志格式（包含文件名和行号）
    detailed_format = (
        "%(asctime)s - %(name)s - %(levelname)s - "
        "[%(filename)s:%(lineno)d] - %(message)s"
    )
    
    # 使用详细格式如果是 DEBUG 模式
    format_string = detailed_format if log_level == "DEBUG" else log_format
    
    # 创建格式化器
    formatter = logging.Formatter(
        format_string,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # 清除现有的处理器
    root_logger.handlers.clear()
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 文件处理器（如果启用）
    if enable_file_logging:
        if log_file is None:
            # 默认日志文件路径
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / "app.log"
        
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        
        # 错误日志单独记录
        error_log_file = Path(log_file).parent / "error.log"
        error_handler = logging.FileHandler(error_log_file, encoding="utf-8")
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        root_logger.addHandler(error_handler)
    
    # 配置第三方库的日志级别
    # 避免第三方库的日志过多
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("supabase").setLevel(logging.WARNING)
    
    # 记录日志配置完成
    logger = logging.getLogger(__name__)
    logger.info(f"📋 Logging configured - Level: {log_level}")
    if enable_file_logging:
        logger.info(f"📁 Log file: {log_file}")
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称（通常使用 __name__）
    
    Returns:
        logging.Logger: 日志记录器实例
    """
    return logging.getLogger(name)

