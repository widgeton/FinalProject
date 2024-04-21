from datetime import timedelta
import re

from sqlalchemy.exc import NoResultFound

from repositories.uow import BaseUnitOfWork, UnitOfWork
from auth.schemas.register import CompanyRegister
from database.models.user import User
from database.models.company import Company
from . import jwt
from . import email_message as em
from . import hash


def is_email(line: str):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.match(pattern, line)


def is_email_in_db(email: str, uow: BaseUnitOfWork = UnitOfWork()) -> bool:
    with uow:
        try:
            uow.users.get(reference=email)
            return True
        except NoResultFound:
            return False


def send_jwt_token(email: str, expire: timedelta = timedelta(days=1)) -> None:
    data = {"sub": email}
    token = jwt.get_jwt_token(data, expire)
    email_message = em.get_email_message("Register Token", f"<h1>{token}</h1>", email)
    em.send_email(email_message)


def save_company_and_its_admin(reg: CompanyRegister, uow: BaseUnitOfWork = UnitOfWork()):
    with uow:
        company = Company(name=reg.company_name)
        admin = User(email=reg.email,
                     hashed_pass=hash.get_password_hash(reg.password),
                     first_name=reg.first_name,
                     last_name=reg.last_name,
                     role="admin",
                     company=company)
        uow.users.add(admin)
        uow.commit()
