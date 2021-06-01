import aiohttp
import pytest
from aiogqlc import GraphQLClient
from aiogqlc.tests import TEST_ENDPOINT


@pytest.mark.asyncio
async def test_mutation_with_flat_response():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        query = """
            mutation {
                createUser(id: 7, name: "John Smith") {
                    id
                    name
                }
            }
        """
        response = await client.execute(query)
        expected = {"data": {"createUser": {"id": "7", "name": "John Smith"}}}
        assert await response.json() == expected


@pytest.mark.asyncio
async def test_mutation_with_nested_fields_in_response():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        query = """
            mutation {
                createTodo(id: 7, title: "TODO", priority: 10, creator: 1) {
                    id
                    title
                    priority
                    creator {
                        id
                        name
                    }
                }
            }
        """
        response = await client.execute(query)
        expected = {
            "data": {
                "createTodo": {
                    "id": "7",
                    "title": "TODO",
                    "priority": 10,
                    "creator": {"id": "1", "name": "Amelia"},
                }
            }
        }
        assert await response.json() == expected
