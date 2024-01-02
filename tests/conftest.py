import asyncio

import pytest_asyncio

from tests.app import create_app
from tests.types import AiohttpClient


@pytest_asyncio.fixture
async def graphql_session(aiohttp_client: AiohttpClient):
    app = create_app()
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    return await aiohttp_client(app)
