import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from .database import Base, engine
from .routers import history, random

logging_level = (
    logging.DEBUG if os.environ.get("ENV", None) == "PROD" else logging.WARNING
)
logging.basicConfig(level=logging_level)

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


app.include_router(history.router)
app.include_router(random.router)
