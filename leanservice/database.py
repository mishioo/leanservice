from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import get_settings

DATABASE_URL = get_settings().DATABASE_URL

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)

Base = declarative_base()


async def get_database():
    async with SessionLocal() as session:
        async with session.begin():
            yield session
