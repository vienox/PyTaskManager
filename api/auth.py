"""
Authentication utilities for JWT token management and password hashing.

This module implements a critical security pattern: SHA256 pre-hashing before bcrypt.
This approach bypasses bcrypt's 72-byte input limitation while maintaining security.

Security Notes:
    - NEVER use passlib.hash.bcrypt - it's incompatible with this pattern
    - ALWAYS use direct bcrypt imports
    - The SHA256 pre-hash is applied to ALL password operations
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
import bcrypt
import hashlib

# JWT Configuration
SECRET_KEY = "super-secret-change-me"  # TODO: Move to environment variables in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def _prepare_password(password: str) -> bytes:
    """
    Prepare password for bcrypt hashing using SHA256 pre-hash.
    
    This function applies SHA256 hashing before bcrypt to handle passwords
    longer than bcrypt's 72-byte limit. This is a critical security pattern
    that must be consistently applied to all password operations.
    
    Args:
        password: Plain text password string
        
    Returns:
        bytes: SHA256 hexdigest as bytes, ready for bcrypt hashing
        
    Note:
        This pattern is incompatible with passlib. Always use direct bcrypt imports.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest().encode('utf-8')


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with SHA256 pre-hashing.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        str: Bcrypt hashed password (UTF-8 decoded)
        
    Example:
        >>> hashed = hash_password("user_password_123")
        >>> verify_password("user_password_123", hashed)
        True
    """
    prepared = _prepare_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(prepared, salt)
    return hashed.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    
    Args:
        plain: Plain text password to verify
        hashed: Bcrypt hashed password (from database)
        
    Returns:
        bool: True if password matches, False otherwise
        
    Example:
        >>> stored_hash = hash_password("secret123")
        >>> verify_password("secret123", stored_hash)
        True
        >>> verify_password("wrong", stored_hash)
        False
    """
    prepared = _prepare_password(plain)
    return bcrypt.checkpw(prepared, hashed.encode('utf-8'))


def create_access_token(sub: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """
    Create a JWT access token for a user.
    
    Args:
        sub: Subject (usually username) to encode in the token
        expires_minutes: Token expiration time in minutes (default: 60)
        
    Returns:
        str: Encoded JWT token
        
    Example:
        >>> token = create_access_token("john_doe")
        >>> # Token valid for 60 minutes
    """
    to_encode = {"sub": sub, "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[str]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string to decode
        
    Returns:
        Optional[str]: Username (subject) if token is valid, None if invalid/expired
        
    Example:
        >>> token = create_access_token("john_doe")
        >>> decode_token(token)
        'john_doe'
        >>> decode_token("invalid_token")
        None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
