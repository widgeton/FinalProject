from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from config import settings

engine = create_engine(
    url=settings.DB_URL,
    echo=False,
    future=True,
    pool_size=50,
    max_overflow=100
)

session_factory = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)
