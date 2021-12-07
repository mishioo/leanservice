import re

import pytest
from aioresponses import aioresponses
from fastapi.testclient import TestClient
from leanservice.database import get_database
from leanservice.main import app

# run all tests with async backend
pytestmark = pytest.mark.asyncio


@pytest.fixture
def client(database):

    # connection fixture is not designed to be used as regular function
    # so this must be reimplemented
    async def mocked_connection():
        async with database() as session:
            async with session.begin():
                yield session

    # injects a testing database dependency
    app.dependency_overrides[get_database] = mocked_connection
    return TestClient(app)


@pytest.fixture
def mockresp():
    # allows to easily mock effects of aiohttp requests
    with aioresponses() as mocked_response:
        yield mocked_response


ANY_REDDIT_CRE = re.compile(r"^http://www.reddit.com.*$")


@pytest.fixture
def sub_with_pics(mockresp, picture_post):
    mockresp.get(
        ANY_REDDIT_CRE,
        payload={"kind": "Listing", "data": {"dist": 1, "children": [picture_post]}},
    )


@pytest.fixture
def sub_without_pics(mockresp, no_picture_post):
    mockresp.get(
        ANY_REDDIT_CRE,
        payload={"kind": "Listing", "data": {"dist": 1, "children": [no_picture_post]}},
    )


@pytest.fixture
def sub_does_not_exist(mockresp):
    mockresp.get(
        ANY_REDDIT_CRE,
        payload={"kind": "Listing", "data": {"dist": 0, "children": []}},
    )


@pytest.mark.usefixtures("sub_with_pics")
async def test_sub_with_pics(client, picture_post):
    resp = client.get("/random")
    assert resp.json()["url"] == picture_post["data"]["url"]


@pytest.mark.usefixtures("sub_without_pics")
async def test_sub_without_pics(client):
    resp = client.get("/random")
    assert resp.code == 204


@pytest.mark.usefixtures("sub_does_not_exist")
async def test_sub_does_not_exist(client):
    resp = client.get("/random")
    assert resp.code == 404


async def test_history_empty(client):
    resp = client.get("/history")
    assert resp.code == 200
    assert resp.json() == []
