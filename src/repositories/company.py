from sqlalchemy.orm import Session
from sqlalchemy import select

from .base import BaseRepository
from database.models.company import Company


class CompanyRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, item: Company):
        self.session.add(item)

    def get(self, reference) -> Company:
        query = select(Company).filter_by(id=reference)
        result = self.session.execute(query)
        return result.scalar_one()
