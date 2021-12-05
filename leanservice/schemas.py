from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Extra
from pydantic.networks import HttpUrl


class RedditPost(BaseModel):
    class Config:
        extra = Extra.ignore

    permalink: str
    url: Optional[HttpUrl] = None

    @property
    def is_picture(self):
        return self.url and self.url.host == "i.redd.it"

    @property
    def post_url(self):
        return f"https://www.reddit.com/{self.permalink}"


class RedditPicture(BaseModel):
    url: HttpUrl
    post_url: HttpUrl
    time: datetime
    picture_id: UUID

