import logging
from random import choice
from typing import List, Optional

import aiohttp
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from ..crud import add_to_history
from ..database import get_database
from ..schemas import RedditPicture, RedditPost
from ..settings import Settings, get_settings

logger = logging.getLogger(__name__)

router = APIRouter()


async def fetch_subreddit(subreddit: str, listing: str):
    listing_url = f"http://www.reddit.com/r/{subreddit}/{listing}.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(listing_url) as response:
            if response.status == 200:
                return await response.json()


def get_picture_posts(response: dict) -> List[RedditPost]:
    listing = response["data"]["children"]
    posts_fetched = (RedditPost(**item["data"]) for item in listing)
    picture_posts = [post for post in posts_fetched if post.is_picture]
    logger.debug(f"Fetched {len(picture_posts)} picture posts.")
    return picture_posts


@router.get("/random", response_model=RedditPicture)
async def random(
    sub: Optional[str] = None,
    listing: Optional[str] = None,
    db: Session = Depends(get_database),
    config: Settings = Depends(get_settings),
):
    fetched = await fetch_subreddit(
        subreddit=sub or config.DEFAULT_SUBREDDIT,
        listing=listing or config.DEFAULT_LISTING,
    )
    posts = get_picture_posts(fetched)
    post = choice(posts)
    return await add_to_history(db, post)
