from typing import List

from sqlalchemy.orm import Session

from . import models, schemas


def add_to_history(db: Session, post: schemas.RedditPost) -> models.RedditPicture:
    db_entry = models.RedditPicture(url=post.url, post_url=post.post_url)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def get_history(db: Session) -> List[models.RedditPicture]:
    return db.query(models.RedditPicture).all()
