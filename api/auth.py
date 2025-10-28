from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
import bcrypt
import hashlib

SECRET_KEY = "super-secret-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def _prepare_password(password: str) -> bytes:
    """
    Przygotowuje hasło do hashowania bcrypt.
    Używa SHA256 aby obsłużyć długie hasła (bcrypt ma limit 72 bajtów).
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest().encode('utf-8')

def hash_password(password: str) -> str:
    """Hashuje hasło używając bcrypt z pre-hash SHA256"""
    prepared = _prepare_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(prepared, salt)
    return hashed.decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    """Weryfikuje hasło"""
    prepared = _prepare_password(plain)
    return bcrypt.checkpw(prepared, hashed.encode('utf-8'))

def create_access_token(sub: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = {"sub": sub, "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
