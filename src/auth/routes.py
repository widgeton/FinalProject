from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Response

import auth.services.common as srv
from . import exceptions as exc
from . import dependencies as dep
from .services import jwt
from .schemas.register import CompleteCompanyRegister, CompanyRegister
from .schemas.token import Token
from .oauth2 import AuthBody

ACCESS_TOKEN_EXPIRE_DAYS = 30

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/check-email/{email}")
async def check_email(email: Annotated[str, Depends(dep.check_email_in_db)]):
    try:
        srv.send_jwt_token(email)
    except exc.SendEmailMessageException:
        raise HTTPException(status_code=400, detail="Failed to send email")


@router.post("/register-company")
async def register_company(body: CompanyRegister):
    try:
        token_data = jwt.decode_token(body.token)
    except exc.TokenDataException:
        raise HTTPException(status_code=400, detail="Could not validate token")
    if token_data.email != body.email:
        raise HTTPException(status_code=400, detail="Email does not match with token")


@router.post("/complete-register-company")
async def complete_register_company(body: CompleteCompanyRegister):
    srv.save_company_and_its_admin(body)


@router.post("/login")
async def login(response: Response, body: AuthBody):
    user = srv.authenticate_user(body.email, body.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = jwt.generate_token(
        data={"sub": user.email, "scopes": [user.role.value]},
        expires_delta=timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
    )
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
