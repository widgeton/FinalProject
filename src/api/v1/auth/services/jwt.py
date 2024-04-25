from datetime import timedelta, datetime, timezone

from jose import jwt, JWTError
from pydantic import ValidationError

from api.v1.auth.schemas.token import TokenData
from api.v1.auth.exceptions import TokenDataException

ALGORITHM = "HS256"


def generate_token(data: dict, secret_key: str,
                   expires_delta: timedelta | None = None,
                   algorithm: str = ALGORITHM) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_token(token: str, secret_key: str, algorithm: str = ALGORITHM) -> TokenData:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email = payload.get("sub")
        if email is None:
            raise TokenDataException
        company_id = payload.get("company_id")
        token_scopes = payload.get("scopes", [])
        return TokenData(scopes=token_scopes, email=email, company_id=company_id)
    except (JWTError, ValidationError):
        raise TokenDataException
