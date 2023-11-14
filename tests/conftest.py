import pytest_asyncio

from tests.app import create_app


@pytest_asyncio.fixture
async def graphql_session(event_loop, aiohttp_client):
    app = create_app()
    event_loop.set_debug(True)
    return await aiohttp_client(app)
