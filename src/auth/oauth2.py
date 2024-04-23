from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import HTTPException
from pydantic import BaseModel, Field


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


class OAuth2Body(BaseModel):
    email: str = Field(pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
                       examples=["user@gmail.com"])
    password: str = Field(min_length=6, examples=["NjuyT56Yu/U%g"])
