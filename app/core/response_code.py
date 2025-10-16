"""统一响应码定义"""

from enum import Enum


class ResponseCode(Enum):
    """响应码枚举 - 与 Java ResultCode 保持一致"""
    
    # 成功
    SUCCESS = (200, "success")
    
    # 系统错误 (500, 11xxx)
    E_SYSTEM_BUSY = (500, "system busy")
    E_SYSTEM_UNAVAILABLE = (11002, "service is unavailable")
    
    # 参数错误 (12xxx)
    E_INVALID_PARAM = (12001, "param invalid")
    
    # 认证/用户错误 (13xxx)
    E_USER_NOT_FOUND = (13001, "user not found")
    E_TOKEN_EXPIRED = (13002, "token expired")
    E_TOKEN_NOT_VALID = (13003, "token not valid")
    
    # 资源/项目错误 (14xxx)
    E_ITEM_NOT_EXIST = (14001, "item not exist")
    E_ITEM_FORBIDDEN = (14002, "item forbidden")
    
    # ===== 扩展错误码 =====
    
    # 客户端错误 (400-499)
    BAD_REQUEST = (400, "bad request")
    UNAUTHORIZED = (401, "unauthorized")
    FORBIDDEN = (403, "forbidden")
    NOT_FOUND = (404, "not found")
    METHOD_NOT_ALLOWED = (405, "method not allowed")
    VALIDATION_ERROR = (422, "validation error")
    
    # 认证相关扩展 (13xxx 继续)
    TOKEN_MISSING = (13004, "token missing")
    AUTH_FAILED = (13005, "authentication failed")
    
    # 用户相关扩展 (13xxx 继续)
    USER_ALREADY_EXISTS = (13006, "user already exists")
    USER_DISABLED = (13007, "user disabled")
    
    # 业务错误 (15xxx)
    BUSINESS_ERROR = (15000, "business error")
    
    # 文件相关错误 (16xxx)
    FILE_TOO_LARGE = (16001, "file too large")
    FILE_TYPE_NOT_ALLOWED = (16002, "file type not allowed")
    FILE_UPLOAD_FAILED = (16003, "file upload failed")
    
    # 数据库错误 (17xxx)
    DATABASE_ERROR = (17001, "database error")
    
    # 第三方服务错误 (18xxx)
    THIRD_PARTY_ERROR = (18001, "third party service error")
    
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        self.msg = message  # 兼容 Java 的 msg 字段
    
    @classmethod
    def get_by_code(cls, code: int):
        """根据 code 获取枚举"""
        for item in cls:
            if item.code == code:
                return item
        return None
    
    def get_code(self) -> int:
        """获取状态码（兼容 Java 的 getCode 方法）"""
        return self.code
    
    def get_msg(self) -> str:
        """获取消息（兼容 Java 的 getMsg 方法）"""
        return self.message

