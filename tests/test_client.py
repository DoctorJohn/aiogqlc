import aiohttp
from pytest_aiohttp import AiohttpClient

from aiogqlc import GraphQLClient
from tests.app import create_app


async def test_execute_extra_kwargs_are_passed_to_aiohttp(
    graphql_session: aiohttp.ClientSession,
):
    query = """
        query {
            authorizationHeader
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    response = await client.execute(query, headers={"Authorization": "Bearer Token123"})

    assert await response.json() == {"data": {"authorizationHeader": "Bearer Token123"}}


async def test_default_headers_can_be_overridden(aiohttp_client: AiohttpClient):
    app = create_app()
    graphql_session = await aiohttp_client(
        app, headers={"Authorization": "Bearer DefaultToken"}
    )

    query = """
        query {
            authorizationHeader
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    response = await client.execute(
        query, headers={"Authorization": "Bearer SpecialToken"}
    )

    result = await response.json()
    assert result["data"]["authorizationHeader"] != "Bearer DefaultToken"
    assert result["data"]["authorizationHeader"] == "Bearer SpecialToken"
