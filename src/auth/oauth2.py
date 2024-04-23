from typing import Annotated, Optional

from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import HTTPException, Form
from pydantic import BaseModel


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


class OAuth2PasswordRequestForm:

    def __init__(self, *,
                 email: Annotated[str, Form()],
                 password: Annotated[str, Form()],
                 ):
        self.email = email
        self.password = password


class AuthBody(BaseModel):
    email: str
    password: str
