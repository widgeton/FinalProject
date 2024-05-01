from typing import Annotated

from fastapi import HTTPException, Depends, Security, status
from fastapi.security import SecurityScopes

from config import settings
from utils.unit_of_work import UnitOfWork
from schemas import UserInDB
from models.field_types import Roles
from api.v1.auth.oauth2 import OAuth2PasswordBearerWithCookie
from api.v1.auth.services.jwt import decode_token
from api.v1.auth.exceptions import TokenDataException
from api.v1.auth.services.common import is_email, get_user


def check_string_on_email(email: str):
    if not is_email(email):
        raise HTTPException(status_code=400, detail="Wrong email format")
    return email


class EmailInDBChecker:
    def __init__(self, versa: bool = False):
        self.versa = versa

    async def __call__(self, email: Annotated[str, Depends(check_string_on_email)],
                       uow: Annotated[UnitOfWork, Depends()]):
        user = await get_user(email, uow)
        if not self.versa and user:
            raise HTTPException(status_code=400, detail="Email already exists in system")
        if self.versa and not user:
            raise HTTPException(status_code=400, detail="Email does not exists in system")
        return email


def validate_token(token: str):
    try:
        token = decode_token(token, settings.JWT_SECRET_KEY)
        return token
    except TokenDataException:
        raise HTTPException(status_code=400, detail="Could not validate token")


oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl="/auth/login",
    scopes={
        "admin": "Rights for admin.",
        "chief": "Rights for chief.",
        "worker": "Rights for worker."
    },
)


async def get_current_user(security_scopes: SecurityScopes,
                           token: Annotated[str, Depends(oauth2_scheme)],
                           uow: Annotated[UnitOfWork, Depends()]):
    authenticate_value = "Bearer"
    if security_scopes.scopes:
        authenticate_value += f' scope="{security_scopes.scope_str}"'

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        token_data = decode_token(token, settings.JWT_SECRET_KEY)
    except TokenDataException:
        raise credentials_exception

    user = await get_user(token_data.email, uow)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            credentials_exception.detail = "Not enough permissions"
            raise credentials_exception
    return user


async def get_current_admin(
        current_user: Annotated[UserInDB, Security(get_current_user, scopes=["admin"])],
):
    if current_user.role != Roles.admin:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
