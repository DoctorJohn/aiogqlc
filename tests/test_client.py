import aiohttp
import pytest
from aiogqlc import GraphQLClient
from tests import TEST_ENDPOINT


@pytest.mark.asyncio
async def test_client_init():
    headers = {"x-foo": "bar"}
    async with aiohttp.ClientSession(headers=headers) as session:
        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        assert client.session is session
        assert client.session._default_headers["x-foo"] == "bar"
        assert client.endpoint == TEST_ENDPOINT
