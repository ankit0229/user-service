from fastapi import HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from starlette import status

from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Set up password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    :param plain_password: The plain text password provided by the user.
    :param hashed_password: The hashed password stored in the database.
    :return: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain password for secure storage.

    :param password: The plain text password to be hashed.
    :return: The hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token.

    :param data: The data to encode in the token, typically user information.
    :param expires_delta: The time duration after which the token expires. If not provided, a default is used.
    :return: The encoded JWT token as a string.
    """
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create access token."
        )


def decode_jwt(token: str) -> dict | None:
    """
    Decode a JWT access token.

    :param token: The JWT token to decode.
    :return: The decoded token payload as a dictionary, or None if decoding fails.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        logger.error(f"JWT Error: {e}")
        return None
