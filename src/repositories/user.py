from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from .base import BaseRepository
from database.models.user import User


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, item: User):
        self.session.add(item)

    def get(self, reference) -> User | None:
        try:
            query = select(User).filter_by(email=reference)
            result = self.session.execute(query)
            return result.scalar_one()
        except NoResultFound:
            return None
