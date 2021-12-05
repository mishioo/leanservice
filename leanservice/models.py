import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String

from .database import Base


class RedditPicture(Base):
    __tablename__ = "history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(String)
    post_url = Column(String)
    created_at = Column(DateTime, default=datetime.now)
