from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, delete


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, **kwargs) -> type(model):
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get(self, reference: dict) -> type(model) | None:
        query = select(self.model).filter_by(**reference)
        result = await self.session.execute(query)
        return result.unique().scalar_one_or_none()

    async def update(self, id_, **fields) -> type(model):
        stmt = (
            update(self.model)
            .filter_by(id=id_)
            .values(**fields)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()


class AbstractDelRepository(AbstractRepository):
    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyDelRepository(SQLAlchemyRepository, AbstractDelRepository):
    async def delete(self, id_: int):
        stmt = delete(self.model).filter_by(id=id_)
        await self.session.execute(stmt)
