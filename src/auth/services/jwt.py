from datetime import timedelta, datetime, timezone

from jose import jwt, JWTError
from pydantic import ValidationError

from config import settings
from auth.schemas.token import TokenData
from auth.exceptions import TokenDataException


def generate_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise TokenDataException
        token_scopes = payload.get("scopes", [])
        return TokenData(scopes=token_scopes, email=email)
    except (JWTError, ValidationError):
        raise TokenDataException
