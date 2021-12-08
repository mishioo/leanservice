from collections import namedtuple
from datetime import datetime
from random import shuffle

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from leanservice import crud
from leanservice.models import RedditPicture
from leanservice.routers.random import get_picture_posts
from leanservice.settings import Listing
from sqlalchemy.future import select

# run all tests with async backend
pytestmark = pytest.mark.asyncio


@pytest.fixture
def post_schema():
    # very simple mock for `RedditPost` schema
    post = namedtuple("RedditPost", ["url", "post_url"])
    return post("/picture_url", "/permalink/to/post")


async def test_get_history_empty(connection):
    # we should allways get empty db if setup is ok
    assert await crud.get_history(connection) == []


async def test_add_to_history(database, post_schema):
    pre_time = datetime.now()
    async with database() as session:
        async with session.begin():
            result = await crud.add_to_history(session, post_schema)
    assert result.url == post_schema.url
    assert result.post_url == post_schema.post_url
    assert pre_time <= result.created_at <= datetime.now()
    async with database() as session:
        async with session.begin():
            # need to open a new connection after commit in crud.add_to_history
            db_state = await session.execute(select(RedditPicture))
    assert len(db_state.all()) == 1


# hypothesis allows for easy property-based testing
@given(st.integers(min_value=0, max_value=100), st.integers(min_value=0, max_value=100))
async def test_get_picture_posts(picture_post, no_picture_post, num_pp, num_npp):
    # num_pp and num_npp are given by hypothesis
    assume(num_pp <= num_npp)  # can't have more pic posts than total posts
    children = [picture_post] * num_pp + [no_picture_post] * num_npp
    shuffle(children)  # shuffles in-place, randomization controlled by hypothesis
    listing = {"kind": "Listing", "data": {"children": children}}
    assert len(get_picture_posts(listing)) == num_pp


@pytest.mark.parametrize("member", Listing)
def test_listing_str(member):
    assert str(member) == member.value


@pytest.mark.parametrize("member", Listing)
def test_listing_lower(member):
    assert Listing(member.value.upper()) == member
