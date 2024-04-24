from database.db import session_factory
from .base import BaseUnitOfWork
from repositories.user import UserRepository
from repositories.company import CompanyRepository


class UnitOfWork(BaseUnitOfWork):

    def __init__(self):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.companies = CompanyRepository(self.session)
        return self

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
