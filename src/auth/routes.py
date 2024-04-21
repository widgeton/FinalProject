from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

import auth.services.common as srv
from . import exceptions as exc
from . import dependencies as dep
from .schemas.register import CompanyRegister
from .schemas.token import TokenData

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/check-email/{email}")
async def check_email(email: Annotated[str, Depends(dep.check_email_in_db)]):
    try:
        srv.send_jwt_token(email)
    except exc.SendEmailMessageException:
        raise HTTPException(status_code=400, detail="Failed to send email")


@router.post("/register-company")
async def register_company(email: Annotated[str, Depends(dep.check_string_on_email)],
                           token_data: Annotated[TokenData, Depends(dep.check_token)]):
    if token_data.email != email:
        raise HTTPException(status_code=400, detail="Email does not match with token")


@router.post("/complete-register-company")
async def complete_register_company(reg: CompanyRegister):
    srv.save_company_and_its_admin(reg)
