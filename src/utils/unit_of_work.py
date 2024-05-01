from abc import ABC, abstractmethod

from utils.repository import AbstractRepository, AbstractDelRepository
from database.db import async_session_factory
from repositories import UserRepository, CompanyRepository, DepartmentRepository


class AbstractUnitOfWork(ABC):
    users: AbstractRepository
    companies: AbstractRepository
    departments: AbstractDelRepository

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):

    def __init__(self):
        self.session_factory = async_session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.companies = CompanyRepository(self.session)
        self.departments = DepartmentRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
