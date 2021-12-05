from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Extra
from pydantic.networks import HttpUrl


class RedditPost(BaseModel):
    permalink: str
    url: Optional[HttpUrl] = None

    class Config:
        extra = Extra.ignore

    @property
    def is_picture(self):
        return self.url and self.url.host == "i.redd.it"

    @property
    def post_url(self):
        return f"https://www.reddit.com/{self.permalink}"


class RedditPicture(BaseModel):
    url: HttpUrl
    post_url: HttpUrl
    created_at: datetime

    class Config:
        orm_mode = True
