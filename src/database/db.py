from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine, text

from config import settings

sync_engine = create_engine(
    url=settings.DB_URL,
    echo=False,
    future=True,
    pool_size=50,
    max_overflow=100
)

with sync_engine.begin() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS ltree;"))

async_engine = create_async_engine(
    url=settings.DB_URL,
    echo=False,
    future=True,
    pool_size=50,
    max_overflow=100
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)
