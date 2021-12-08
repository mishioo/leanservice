import re
from unittest import mock

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


# pattern used to define which http calls to mock
ANY_REDDIT_CRE = re.compile(r"^http(s?)://www.reddit.com.*$")


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
def sub_redirect_to_search(mockresp):
    mockresp.get(
        ANY_REDDIT_CRE,
        payload={
            "kind": "Listing",
            "data": {"dist": 1, "children": [{"kind": "t5", "data": {}}]},
        },
    )
    path = "https://www.reddit.com/subreddits/search.json?q=sub"
    with mock.patch("yarl.URL.path", path):
        # can't mock `response.url` with aioresponses
        yield


@pytest.fixture
def sub_does_not_exist(mockresp):
    mockresp.get(
        ANY_REDDIT_CRE, payload={"message": "Not Found", "error": 404}, status=404
    )


# just a few, ap tests for any >500
@pytest.fixture(params=list(range(500, 505)))
def reddit_down(mockresp, request):
    mockresp.get(
        ANY_REDDIT_CRE,
        payload={"message": "Server-side error", "error": request.param},
        status=request.param,
    )


@pytest.fixture
def sub_is_private(mockresp):
    mockresp.get(
        ANY_REDDIT_CRE,
        payload={"reason": "private", "message": "Forbidden", "error": 403},
        status=403,
    )


@pytest.mark.usefixtures("sub_with_pics")
async def test_sub_with_pics(client, picture_post):
    resp = client.get("/random")
    assert resp.status_code == 200
    assert resp.json()["url"] == picture_post["data"]["url"]


@pytest.mark.usefixtures("sub_with_pics")
async def test_query_sub(client):
    sub = "someothersub"
    resp = client.get("/random", params={"sub": sub})
    assert resp.status_code == 200
    assert sub in resp.url


@pytest.mark.usefixtures("sub_with_pics")
@pytest.mark.parametrize("listing,status", [("best", 200), ("invalid", 422)])
async def test_query_listing(client, listing, status):
    resp = client.get("/random", params={"listing": listing})
    assert resp.status_code == status
    assert listing in resp.url


@pytest.mark.usefixtures("sub_without_pics")
async def test_random_query_sub(client):
    resp = client.get("/random")
    assert resp.status_code == 404


@pytest.mark.usefixtures("sub_redirect_to_search")
async def test_sub_redirect_to_search(client):
    resp = client.get("/random")
    assert resp.status_code == 404


@pytest.mark.usefixtures("sub_does_not_exist")
async def test_sub_does_not_exist(client):
    resp = client.get("/random")
    assert resp.status_code == 404


@pytest.mark.usefixtures("reddit_down")
async def test_reddit_down(client):
    resp = client.get("/random")
    assert resp.status_code == 503


@pytest.mark.usefixtures("sub_is_private")
async def test_sub_is_private(client):
    resp = client.get("/random")
    assert resp.status_code == 403


async def test_history_empty(client):
    resp = client.get("/history")
    assert resp.status_code == 200
    assert resp.json() == []
