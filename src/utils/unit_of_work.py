from abc import ABC, abstractmethod

from utils.repository import AbstractRepository, AbstractDelRepository
from database.db import async_session_factory
import repositories as repo


class AbstractUnitOfWork(ABC):
    users: AbstractRepository
    companies: AbstractRepository
    departments: AbstractDelRepository
    positions: AbstractDelRepository
    tasks: AbstractDelRepository

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
        self.users = repo.UserRepository(self.session)
        self.companies = repo.CompanyRepository(self.session)
        self.departments = repo.DepartmentRepository(self.session)
        self.positions = repo.PositionRepository(self.session)
        self.tasks = repo.TaskRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
