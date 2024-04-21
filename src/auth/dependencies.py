from typing import Annotated

from fastapi import HTTPException, Depends

from .services import jwt
from . import exceptions as exc
from .services import common as srvs


def check_string_on_email(email: str):
    if not srvs.is_email(email):
        raise HTTPException(status_code=400, detail="Wrong email format")
    return email


def check_email_in_db(email: Annotated[str, Depends(check_string_on_email)]):
    if srvs.is_email_in_db(email):
        raise HTTPException(status_code=400, detail="Email already exists in system")
    return email


def check_token(token: str):
    try:
        token_data = jwt.get_jwt_token_data(token)
        return token_data
    except exc.TokenDataException:
        raise HTTPException(status_code=400, detail="Could not validate token")
