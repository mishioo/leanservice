"""Endpoint that loads a random picture from reddit."""
import logging
from random import choice
from typing import List, Optional

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from ..crud import add_to_history
from ..database import get_database
from ..schemas import RedditPicture, RedditPost
from ..settings import Listing, Settings, get_settings

logger = logging.getLogger(__name__)

router = APIRouter()


async def fetch_subreddit(subreddit: str, listing: str) -> dict:
    """Fetches 100 posts from given listing, from given subreddit.

    Parameters
    ----------
    subreddit : str
        Subreddit's name. This subreddit will be fetched for random picture post.
    listing : str
        Type of reddit's listing (how posts should be sorted): new, hot, and so on.

    Returns
    -------
    dict
        Reddit's response in JSON format, converted to Python's dict.
    """
    listing_url = f"http://www.reddit.com/r/{subreddit}/{listing}.json"
    params = {"limit": "100"}  # reddit's default is only 25, 100 is max
    logger.debug(f"Sending request to {listing_url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(listing_url, params=params) as response:
            logger.debug(f"Reddit's response: {response}")
            if not "X-Moose" in response.headers:
                logger.info("Where is the majestic Moose? :(")
            if response.status == 404 or "subreddits/search" in response.url.path:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    {"reason": f"no such subreddit: {subreddit}", "error": 404},
                )
            elif response.status == 403:
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    {"reason": f"this subreddit is private: {subreddit}", "error": 403},
                )
            elif response.status >= 500:
                # for such a simple app we will just say its unavailable,
                # if reddit responses with server error
                raise HTTPException(
                    status.HTTP_503_SERVICE_UNAVAILABLE,
                    {"reason": {"reddit_error": response.status}, "error": 503},
                )
            fetched = await response.json()
            return fetched


def get_picture_posts(response: dict) -> List[RedditPost]:
    """Filter posts fetched to keep only those with a picture.

    Parameters
    ----------
    response : dict
        Reddit's response in JSON format, converted to Python's dict.

    Returns
    -------
    list of RedditPost
        Posts that contain a picture.
    """
    listing = response["data"]["children"]  # location of actual list of posts
    # convert all posts to `RedditPost` instances
    # not particularly efficient, but convenient
    posts_fetched = (RedditPost(**item["data"]) for item in listing)
    picture_posts = [post for post in posts_fetched if post.is_picture]
    logger.debug(f"Fetched {len(picture_posts)} picture posts.")
    return picture_posts


@router.get("/random", response_model=Optional[RedditPicture])
async def random(
    sub: Optional[str] = None,
    listing: Optional[Listing] = None,
    db: Session = Depends(get_database),
    config: Settings = Depends(get_settings),
):
    """/random endpoint's GET method.
    Returns a JSON representation of random picture from reddit.
    """
    subreddit = sub or config.DEFAULT_SUBREDDIT
    listing = listing or config.DEFAULT_LISTING
    fetched = await fetch_subreddit(subreddit, listing)
    posts = get_picture_posts(fetched)
    if not posts:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            {
                "reason": f"no picture posts found in {subreddit}/{listing}",
                "error": 404,
            },
        )
    post = choice(posts)  # chose at random
    return await add_to_history(db, post)
