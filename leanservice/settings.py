from enum import Enum
from functools import lru_cache

from pydantic import BaseSettings


class Env(Enum):
    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"


class Settings(BaseSettings):
    DEFAULT_SUBREDDIT: str = "dankmemes"
    DEFAULT_LISTING: str = "new"
    DATABASE_URL: str
    ENV: Env = Env.PROD

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
