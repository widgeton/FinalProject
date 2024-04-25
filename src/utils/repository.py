from abc import ABC, abstractmethod

from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: Session):
        self.session = session

    def add(self, **kwargs) -> type(model):
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        res = self.session.execute(stmt)
        return res.scalar_one()

    def get(self, reference: dict) -> type(model) | None:
        query = select(self.model).filter_by(**reference)
        result = self.session.execute(query)
        return result.unique().scalar_one_or_none()

    def update(self, id_, **fields) -> type(model):
        stmt = (
            update(self.model)
            .filter_by(id=id_)
            .values(**fields)
            .returning(self.model)
        )
        res = self.session.execute(stmt)
        return res.scalar_one()
