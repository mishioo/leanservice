import logging

from fastapi import FastAPI

from .database import Base, engine
from .routers import history, random
from .settings import Env, get_settings

config = get_settings()
if config.ENV is Env.DEV:
    logging.basicConfig(level=logging.DEBUG)


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


app.include_router(history.router)
app.include_router(random.router)
