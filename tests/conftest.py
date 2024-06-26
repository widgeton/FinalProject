import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)

from config import settings
from models import BaseModel
from main import app


@pytest.fixture(scope="session")
def async_engine() -> AsyncEngine:
    _async_engine = create_async_engine(
        url=settings.DB_URL,
        echo=False,
        future=True
    )
    return _async_engine


@pytest.fixture(scope="session")
def async_session_maker(async_engine):
    _async_session_maker = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    return _async_session_maker


@pytest.fixture(scope="session", autouse=True)
async def setup_db(async_engine):
    assert settings.MODE == "TEST"
    async with async_engine.begin() as db_conn:
        await db_conn.run_sync(BaseModel.metadata.drop_all)
        await db_conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
        await db_conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with async_engine.begin() as db_conn:
        await db_conn.run_sync(BaseModel.metadata.drop_all)


@pytest.fixture
async def async_session(async_session_maker) -> AsyncSession:
    async with async_session_maker() as _async_session:
        yield _async_session


@pytest.fixture(scope="session")
def client() -> TestClient:
    with TestClient(app) as c:
        yield c
