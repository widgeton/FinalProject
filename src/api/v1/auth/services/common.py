from datetime import timedelta
import re

from config import settings
from utils.unit_of_work import AbstractUnitOfWork
from schemas import Company, UserCreate, UserWithCompany
from schemas.user import UserInDB
from api.v1.auth import schemas as sch
from api.v1.auth.services.jwt import generate_token
from api.v1.auth.services.email_message import get_email_message, send_email
from api.v1.auth.services.hash import get_password_hash, verify_password


def is_email(line: str):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.match(email_pattern, line)


def is_email_in_db(email: str, uow: AbstractUnitOfWork) -> bool:
    with uow:
        user = uow.users.get(reference={"email": email})
        return user is not None


def send_token(email: str, data: dict, title: str = "Token",
               expire: timedelta = timedelta(days=1)) -> str:
    token = generate_token(data, settings.JWT_SECRET_KEY, expire)
    if settings.MODE == "PROD":
        email_message = get_email_message(title, f"<h1>{token}</h1>", email)
        send_email(email_message)
    return token


def save_company_and_its_admin(company: Company, admin: UserCreate,
                               uow: AbstractUnitOfWork) -> UserWithCompany:
    with uow:
        company = uow.companies.add(**company.model_dump())
        admin = uow.users.add(hashed_pass=get_password_hash(admin.password),
                              company_id=company.id,
                              **admin.model_dump(exclude={"password", "company_id"}))
        user = admin.to_pydantic_schema()
        uow.commit()
        return user


def get_user(email: str, uow: AbstractUnitOfWork) -> UserInDB | None:
    with uow:
        user = uow.users.get({"email": email})
        if user:
            return UserInDB.model_validate(user, from_attributes=True)


def authenticate_user(email: str, password: str,
                      uow: AbstractUnitOfWork) -> UserInDB | None:
    user = get_user(email, uow)
    if verify_password(password, user.hashed_pass):
        return user


def save_new_user(new_user: sch.UserCreate,
                  uow: AbstractUnitOfWork) -> UserWithCompany:
    with uow:
        new_user = uow.users.add(hashed_pass=get_password_hash(new_user.password),
                                 **new_user.model_dump(exclude={"password"}))
        user = new_user.to_pydantic_schema()
        uow.commit()
        return user


def update_user(user_id: int,
                new_user: sch.UserUpdate,
                uow: AbstractUnitOfWork) -> UserWithCompany:
    with uow:
        new_user = uow.users.update(user_id, **new_user.model_dump(exclude_unset=True))
        user = new_user.to_pydantic_schema()
        uow.commit()
        return user
