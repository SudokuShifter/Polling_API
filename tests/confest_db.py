import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.db_models import Base
from repository.session_db.session import get_db


TEST_DB_URL = 'sqlite+aiosqlite:///:memory:'
test_engine = create_async_engine(TEST_DB_URL, future=True)
TestingSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope='function', autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture()
def override_get_db(db_session):
    async def _override_get_db():
        yield db_session
    return _override_get_db

