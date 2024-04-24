from typing import Annotated

from fastapi import HTTPException, Depends, Security, status
from fastapi.security import SecurityScopes

from config import settings
from .schemas import User, Roles
from .oauth2 import OAuth2PasswordBearerWithCookie
from .services import jwt
from . import exceptions as exc
from .services import common as srv


def check_string_on_email(email: str):
    if not srv.is_email(email):
        raise HTTPException(status_code=400, detail="Wrong email format")
    return email


class EmailInDBChecker:
    def __init__(self, versa: bool = False):
        self.versa = versa

    def __call__(self, email: Annotated[str, Depends(check_string_on_email)]):
        if not self.versa and srv.is_email_in_db(email):
            raise HTTPException(status_code=400, detail="Email already exists in system")
        if self.versa and not srv.is_email_in_db(email):
            raise HTTPException(status_code=400, detail="Email does not exists in system")
        return email


def validate_token(token: str):
    try:
        token = jwt.decode_token(token, settings.JWT_SECRET_KEY)
        return token
    except exc.TokenDataException:
        raise HTTPException(status_code=400, detail="Could not validate token")


oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl="/auth/login",
    scopes={
        "admin": "Rights for admin.",
        "chief": "Rights for chief.",
        "worker": "Rights for worker."
    },
)


def get_current_user(
        security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    authenticate_value = "Bearer"
    if security_scopes.scopes:
        authenticate_value += f' scope="{security_scopes.scope_str}"'

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        token_data = jwt.decode_token(token, settings.JWT_SECRET_KEY)
    except exc.TokenDataException:
        raise credentials_exception

    user = srv.get_user(token_data.email)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            credentials_exception.detail = "Not enough permissions"
            raise credentials_exception
    return user


def get_current_admin(
        current_user: Annotated[User, Security(get_current_user, scopes=["admin"])],
):
    if current_user.role != Roles.admin:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
