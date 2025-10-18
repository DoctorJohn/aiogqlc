import aiohttp
import aiohttp.web
import pytest

from aiogqlc import GraphQLClient


class DemoGraphQLView(aiohttp.web.View):
    async def post(self):
        return aiohttp.web.json_response({"data": {"ping": "pong"}})


@pytest.fixture
async def graphql_client(aiohttp_client):
    app = aiohttp.web.Application()
    app.router.add_route("*", "/graphql", DemoGraphQLView)

    graphql_session = await aiohttp_client(app)
    return GraphQLClient(endpoint="/graphql", session=graphql_session)


@pytest.mark.asyncio
async def test_ping_query(graphql_client):
    response = await graphql_client.execute("query { ping }")
    assert await response.json() == {"data": {"ping": "pong"}}
