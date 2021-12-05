import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from . import models
from .database import engine
from .routers import history, random

models.Base.metadata.create_all(bind=engine)


logging_level = (
    logging.DEBUG if os.environ.get("ENV", None) == "PROD" else logging.WARNING
)
logging.basicConfig(level=logging_level)

app = FastAPI()

app.include_router(history.router)
app.include_router(random.router)
