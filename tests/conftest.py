"""Provides pytest fixtures and configuration available for all tests in current module.
"""

import pathlib

import pytest
from leanservice.database import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
async def database(tmp_path: pathlib.Path):
    # configure database for tests
    # pytest.fixture assures that new db is created for each test
    path = "sqlite+aiosqlite:///" + str(tmp_path / "test.db")
    engine = create_async_engine(path, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=engine,
        class_=AsyncSession,
    )
    async with engine.begin() as connection:
        # create all tables
        await connection.run_sync(Base.metadata.create_all)
    return SessionLocal


@pytest.fixture
async def connection(database):
    async with database() as session:
        async with session.begin():
            yield session


@pytest.fixture(scope="module")
def picture_post():
    return {
        "kind": "t3",
        "data": {
            "url": "https://i.redd.it/address.jpg",
            "permalink": "/r/subreddit/comments/code/title/",
        },
    }


@pytest.fixture(scope="module")
def no_picture_post():
    return {
        "kind": "t3",
        "data": {
            "url": "https://www.reddit.com/address/to/post",
            "permalink": "/r/subreddit/comments/code/title/",
        },
    }
