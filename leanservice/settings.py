"""Defines and exposes app's configuration."""
from enum import Enum
from functools import lru_cache

from pydantic import BaseSettings


class Env(Enum):
    """Possible environments this app may be runned in."""

    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"


class Listing(Enum):
    """Listing types provided by reddit's API."""

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
    """Defines app's configuration.

    Attributes
    ----------
    DEFAULT_SUBREDDIT : str
            Default subreddit, from which app should draw a picture post.
    DEFAULT_LISTING : Listing
        Default listing, from which app should draw a picture post.
        Should be a member of `Listing` enumeration, but string will also be accepted
        if it can be converted to `Listing`'s member.
    DATABASE_URL : str
        Address of the database used by app.
    ENV : Env
        Defines type of environment that app runs in.
        Should be a member of `Env` enumeration, but string will also be accepted
        if it can be converted to `Env`'s member.

    Notes
    -----
    Loads ".env" file with variables declaration, it should be located in working
    directory. Actual environment variables are also fetched, in fact they take
    precedence over ".env" file declarations.
    Also, variables in ".env" or environment variables that are not defined as this
    class' attribute will be ignored.
    """

    DEFAULT_SUBREDDIT: str = "dankmemes"
    DEFAULT_LISTING: Listing = Listing.NEW
    DATABASE_URL: str
    ENV: Env = Env.PROD

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    """Returns application's settings as `pydantic.BaseSettings` instance.

    Notes
    -----
    This function is available for FastAPI's dependency injection.
    Decorated with `functools.lru_cache`, always returns original object.
    """
    return Settings()
