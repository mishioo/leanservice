"""Configuration of the database.

This app uses SQLAlchemy ORM to comunicate with the database. Starting from the latest
version (1.4) SQLAlchemy provides an asynchronous interface by `sqlalchemy.ext.asyncio`
extension, which is great for use with an asynchronous framework like FastAPI.
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import get_settings

DATABASE_URL = get_settings().DATABASE_URL

# engine picked by SQLAlchemy based on the url
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# creates a configured Session class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)

Base = declarative_base()


async def get_database():
    """Provides an opened connection with the database, available for FastAPI's
    dependency injection."""
    async with SessionLocal() as session:
        async with session.begin():
            yield session
