from datetime import timedelta
import re

from config import settings
from repositories.uow import BaseUnitOfWork, UnitOfWork
from auth import schemas as sch
from database.models.user import User
from database.models.company import Company
from schemas.user import UserInDB
from . import jwt
from . import email_message as em
from . import hash


def is_email(line: str):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.match(email_pattern, line)


def is_email_in_db(email: str, uow: BaseUnitOfWork = UnitOfWork()) -> bool:
    with uow:
        user = uow.users.get(reference=email)
        return user is not None


def send_token(email: str, data: dict, title: str = "Token",
               expire: timedelta = timedelta(days=1)) -> None:
    token = jwt.generate_token(data, settings.JWT_SECRET_KEY, expire)
    email_message = em.get_email_message(title, f"<h1>{token}</h1>", email)
    em.send_email(email_message)


def save_company_and_its_admin(company: sch.Company, admin: sch.User, password: str,
                               uow: BaseUnitOfWork = UnitOfWork()) -> None:
    with uow:
        company = Company(**company.model_dump())
        admin = User(hashed_pass=hash.get_password_hash(password),
                     company=company,
                     **admin.model_dump(exclude_unset=True))
        uow.users.add(admin)
        uow.commit()


def get_user(email: str, uow: BaseUnitOfWork = UnitOfWork()) -> UserInDB | None:
    with uow:
        user = uow.users.get(email)
        if user:
            return UserInDB.model_validate(user, from_attributes=True)


def authenticate_user(email: str, password: str) -> UserInDB | None:
    user = get_user(email)
    if hash.verify_password(password, user.hashed_pass):
        return user


def save_new_user(new_user: sch.User, password: str,
                  uow: BaseUnitOfWork = UnitOfWork()) -> None:
    with uow:
        user = User(hashed_pass=hash.get_password_hash(password),
                    **new_user.model_dump())
        uow.users.add(user)
        uow.commit()


def update_user(user: sch.UserInDB, new_user: sch.UserUpdate, uow: BaseUnitOfWork) -> None:
    with uow:
        uow.users.update(user.id, **new_user.model_dump(exclude_unset=True))
        uow.commit()
