"""Pydantic schemes for input validation anf input/output formatting."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra
from pydantic.networks import HttpUrl


class RedditPost(BaseModel):
    """Represents a post loaded from reddit.

    The actual post's JSON representation fetched from reddit provides much more fields
    that defined here, but most are not important for this simple app, so they are
    simply ignpred.
    """

    permalink: str  # link to post without host
    url: Optional[HttpUrl] = None  # file location on reddit's server

    class Config:
        extra = Extra.ignore

    @property
    def is_picture(self) -> bool:
        """Returns `True` if post contains a picture."""
        # pictures on reddit are stored on the "i.redd.it" host
        return self.url and self.url.host == "i.redd.it"

    @property
    def post_url(self) -> str:
        """Full permanent link to the post."""
        return f"https://www.reddit.com{self.permalink}"


class RedditPicture(BaseModel):
    """Scheme for picture picked from reddit."""

    url: HttpUrl
    post_url: HttpUrl
    created_at: datetime

    class Config:
        orm_mode = True
