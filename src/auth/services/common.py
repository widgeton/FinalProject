from datetime import timedelta
import re

from repositories.uow import BaseUnitOfWork, UnitOfWork
import auth.schemas.register as reg
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


def send_jwt_token(email: str, expire: timedelta = timedelta(days=1)) -> None:
    data = {"sub": email}
    token = jwt.generate_token(data, expire)
    email_message = em.get_email_message("Register Token", f"<h1>{token}</h1>", email)
    em.send_email(email_message)


def save_company_and_its_admin(body: reg.CompleteCompanyRegister, uow: BaseUnitOfWork = UnitOfWork()):
    with uow:
        company = Company(name=body.company_name)
        admin = User(email=body.email,
                     hashed_pass=hash.get_password_hash(body.password),
                     first_name=body.first_name,
                     last_name=body.last_name,
                     role="admin",
                     company=company)
        uow.users.add(admin)
        uow.commit()


def get_user(email: str, uow: BaseUnitOfWork = UnitOfWork()) -> UserInDB | None:
    with uow:
        user = uow.users.get(email)
        if user:
            return UserInDB.model_validate(user, from_attributes=True)


def authenticate_user(email: str, password: str):
    user = get_user(email)
    if hash.verify_password(password, user.hashed_pass):
        return user
