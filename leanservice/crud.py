"""Database operatons.

This application does not need many database interactions, so all are defined in the
single module. As in standard CRUD module, functions defied here are responsible for
reading and modifying database state for persistent storage. Two typer of operations are
supported: adding a record to history and retriving whole history.
"""
from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from . import models, schemas


async def add_to_history(db: Session, post: schemas.RedditPost) -> models.RedditPicture:
    """Adds given picture post to history of picks."""
    db_entry = models.RedditPicture(url=post.url, post_url=post.post_url)
    db.add(db_entry)
    # above is an equivalent of
    # 'INSERT INTO history (id, url, post_url, created_at) VALUES (?, ?, ?, ?)'
    # where "url" and "post_url" values are provided by `RedditPost` schema
    # and "id" and "created_at" are auto-generated by model
    await db.commit()
    return db_entry


async def get_history(db: Session) -> List[models.RedditPicture]:
    """Retrieves a whole history of picks."""
    query = select(
        models.RedditPicture.url,
        models.RedditPicture.post_url,
        models.RedditPicture.created_at,
    )  # equivalent of:
    # 'SELECT history.url, history.post_url, history.created_at FROM history'
    result = await db.execute(query)
    return result.all()
