import aiohttp
import pytest
from aiogqlc import GraphQLClient
from tests import TEST_ENDPOINT


@pytest.mark.asyncio
async def test_mutation_with_flat_response():
    async with aiohttp.ClientSession() as session:
        query = """
            mutation {
                createUser(id: 7, name: "John Smith") {
                    id
                    name
                }
            }
        """

        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        response = await client.execute(query)

        assert await response.json() == {
            "data": {"createUser": {"id": "7", "name": "John Smith"}}
        }


@pytest.mark.asyncio
async def test_mutation_with_nested_fields_in_response():
    async with aiohttp.ClientSession() as session:
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

        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        response = await client.execute(query)

        assert await response.json() == {
            "data": {
                "createTodo": {
                    "id": "7",
                    "title": "TODO",
                    "priority": 10,
                    "creator": {"id": "1", "name": "Amelia"},
                }
            }
        }
