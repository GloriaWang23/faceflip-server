"""Validation utilities"""

import re
from typing import Optional


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """Validate password strength
    
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, None


def validate_username(username: str) -> tuple[bool, Optional[str]]:
    """Validate username format
    
    Requirements:
    - 3-20 characters
    - Only alphanumeric characters and underscores
    - Must start with a letter
    """
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be 3-20 characters long"
    
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        return False, "Username must start with a letter and contain only letters, numbers, and underscores"
    
    return True, None


def validate_phone_number(phone: str) -> tuple[bool, Optional[str]]:
    """Validate phone number format"""
    # Basic international phone number validation
    pattern = r'^\+?[1-9]\d{1,14}$'
    
    if not re.match(pattern, phone):
        return False, "Invalid phone number format"
    
    return True, None

