import logging

from dotenv import dotenv_values
from fastapi import FastAPI

from .routers import history, random

config = dotenv_values()
logging_level = logging.DEBUG if config.get("ENV", None) == "PROD" else logging.WARNING
logging.basicConfig(level=logging_level)

app = FastAPI()

app.include_router(history.router)
app.include_router(random.router)
