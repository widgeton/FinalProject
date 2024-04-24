from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Response

from config import settings
import auth.services.common as srv
from . import exceptions as exc
from . import dependencies as dep
from .services import jwt
from . import schemas as sch
from repositories.base import BaseUnitOfWork
from repositories.uow import UnitOfWork

ACCESS_TOKEN_EXPIRE_DAYS = 30

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/check-email/{email}")
async def check_email(email: Annotated[str, Depends(dep.EmailInDBChecker())]):
    try:
        data = {"sub": email}
        srv.send_token(email, data, title="Register Token")
    except exc.SendEmailMessageException:
        raise HTTPException(status_code=400, detail="Failed to send email")


@router.post("/register-company")
async def register_company(body: sch.CompanyRegister,
                           token_data: Annotated[sch.TokenData, Depends(dep.validate_token)]):
    if token_data.email != body.email:
        raise HTTPException(status_code=400, detail="Email does not match with token")


@router.post("/complete-register-company")
async def complete_register_company(body: sch.CompleteCompanyRegister):
    company = sch.Company(name=body.company_name)
    admin = sch.User(email=body.email,
                     first_name=body.first_name,
                     last_name=body.last_name,
                     role=sch.Roles.admin)
    srv.save_company_and_its_admin(company, admin, body.password)


@router.post("/login")
async def login(response: Response, body: sch.OAuth2Body):
    user = srv.authenticate_user(body.email, body.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = jwt.generate_token(
        data={"sub": user.email, "scopes": [user.role.value]},
        secret_key=settings.JWT_SECRET_KEY,
        expires_delta=timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
    )
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return sch.Token(access_token=access_token, token_type="bearer")


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")


@router.get("/invite")
async def invite(email: Annotated[str, Depends(dep.EmailInDBChecker())],
                 admin: Annotated[sch.UserInDB, Depends(dep.get_current_admin)]):
    try:
        data = {"sub": email, "company_id": admin.company_id}
        srv.send_token(email, data, title="Invite Token")
    except exc.SendEmailMessageException:
        raise HTTPException(status_code=400, detail="Failed to send email")


@router.post("/register-user/{token}")
async def register_user(body: sch.UserRegister,
                        token_data: Annotated[sch.TokenData, Depends(dep.validate_token)]):
    user = sch.User(role=sch.Roles.worker,
                    **token_data.model_dump(exclude={"scopes"}),
                    **body.model_dump(exclude={"password"}))
    srv.save_new_user(user, body.password)


@router.put("/update-user")
async def update_user(email: Annotated[str, Depends(dep.EmailInDBChecker(versa=True))],
                      admin: Annotated[sch.UserInDB, Depends(dep.get_current_admin)],
                      uow: Annotated[BaseUnitOfWork, Depends(UnitOfWork)],
                      data: sch.UserUpdate):
    user = srv.get_user(email)
    if admin.company_id != user.company_id:
        raise HTTPException(status_code=400, detail="Could not update another company user.")
    srv.update_user(user, data, uow)

