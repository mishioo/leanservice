from enum import Enum
from functools import lru_cache

from pydantic import BaseSettings


class Env(Enum):
    """Possible environments this app may be runned in."""

    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"


class Listing(Enum):
    """Provides listing types provided by reddit's API."""

    NEW = "new"
    HOT = "hot"
    BEST = "best"
    RISING = "rising"
    TOP = "top"
    CONTROVERSIAL = "controversial"

    def __str__(self):
        # print as just a value to easily insert in url
        return self.value

    @classmethod
    def _missing_(cls, value):
        # make instantiation case-insensitive
        # will only impact instantiation with `Enum(value)` syntax
        # but that's exactly what we need for validation with pydantic
        for member in cls:
            if member.value == value.upper():
                return member


class Settings(BaseSettings):
    DEFAULT_SUBREDDIT: str = "dankmemes"
    DEFAULT_LISTING: Listing = Listing.NEW
    DATABASE_URL: str
    ENV: Env = Env.PROD

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
