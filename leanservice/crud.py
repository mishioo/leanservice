from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from . import models, schemas


async def add_to_history(db: Session, post: schemas.RedditPost) -> models.RedditPicture:
    db_entry = models.RedditPicture(url=post.url, post_url=post.post_url)
    db.add(db_entry)
    await db.commit()
    return db_entry


async def get_history(db: Session) -> List[models.RedditPicture]:
    query = select(
        models.RedditPicture.url,
        models.RedditPicture.post_url,
        models.RedditPicture.created_at,
    )
    result = await db.execute(query)
    return result.all()
