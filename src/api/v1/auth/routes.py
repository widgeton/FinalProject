from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Response

import api.v1.auth.services.common as srv
from api.v1.auth.exceptions import SendEmailMessageException
import api.v1.auth.dependencies as dep
from api.v1.auth.services.jwt import generate_token
import api.v1.auth.schemas as sch
from models.field_types import Roles
from utils.unit_of_work import UnitOfWork
from config import settings

ACCESS_TOKEN_EXPIRE_DAYS = 30

router = APIRouter()


@router.get("/invite_compony")
async def invite_compony(email: Annotated[str, Depends(dep.EmailInDBChecker())]):
    try:
        data = {"sub": email}
        token = srv.send_token(email, data, title="Register Token")
        return {"token": token}
    except SendEmailMessageException:
        raise HTTPException(status_code=400, detail="Failed to send email")


@router.post("/register-company/{token}")
async def complete_register_company(body: sch.CompanyRegister,
                                    token_data: Annotated[sch.TokenData, Depends(dep.validate_token)],
                                    uow: Annotated[UnitOfWork, Depends()]):
    company = sch.Company(name=body.company_name)
    admin = sch.UserCreate(role=Roles.admin,
                           email=token_data.email,
                           **body.model_dump(exclude={"company_name"}))
    new_admin_with_company = await srv.save_company_and_its_admin(company, admin, uow)
    return new_admin_with_company


@router.post("/login")
async def login(response: Response, body: sch.OAuth2Body,
                uow: Annotated[UnitOfWork, Depends()]):
    user = await srv.authenticate_user(body.email, body.password, uow)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = generate_token(
        data={"sub": user.email, "scopes": [user.role.value]},
        secret_key=settings.JWT_SECRET_KEY,
        expires_delta=timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
    )
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return sch.Token(access_token=access_token, token_type="bearer")


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")


@router.get("/invite-worker")
async def invite_worker(email: Annotated[str, Depends(dep.EmailInDBChecker())],
                        admin: Annotated[sch.UserInDB, Depends(dep.get_current_admin)]):
    try:
        data = {"sub": email, "company_id": admin.company_id}
        token = srv.send_token(email, data, title="Invite Token")
        return {"token": token}
    except SendEmailMessageException:
        raise HTTPException(status_code=400, detail="Failed to send email")


@router.post("/register-user/{token}")
async def register_user(body: sch.UserRegister,
                        token_data: Annotated[sch.TokenData, Depends(dep.validate_token)],
                        uow: Annotated[UnitOfWork, Depends()]):
    user = sch.UserCreate(role=Roles.worker,
                          **token_data.model_dump(exclude={"scopes"}),
                          **body.model_dump())
    new_user = await srv.save_new_user(user, uow)
    return new_user


@router.put("/update-user")
async def update_user(email: Annotated[str, Depends(dep.EmailInDBChecker(versa=True))],
                      data: sch.UserUpdate,
                      admin: Annotated[sch.UserInDB, Depends(dep.get_current_admin)],
                      uow: Annotated[UnitOfWork, Depends()]):
    user = await srv.get_user(email, uow)
    if admin.company_id != user.company_id:
        raise HTTPException(status_code=400, detail="Could not update another company user.")
    updated_user = await srv.update_user(user.id, data, uow)
    return updated_user
