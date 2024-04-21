from sqlalchemy.orm import DeclarativeBase, mapped_column, sessionmaker
from sqlalchemy import create_engine
from typing import Annotated

from config import settings

engine = create_engine(url=settings.DB_URL)
session_factory = sessionmaker(bind=engine, autoflush=False)

pk = Annotated[int, mapped_column(primary_key=True, nullable=False, unique=True, autoincrement=True)]


class Base(DeclarativeBase):
    pass
