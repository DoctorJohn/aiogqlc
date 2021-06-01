import aiohttp
import pytest
from aiogqlc import GraphQLClient
from tests import TEST_ENDPOINT


@pytest.mark.asyncio
async def test_query_flat_list():
    async with aiohttp.ClientSession() as session:
        query = """
            query {
                todos {
                    id
                    title
                    priority
                }
            }
        """

        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        response = await client.execute(query)

        assert await response.json() == {
            "data": {
                "todos": [
                    {"id": "1", "title": "Clean kitchen", "priority": 1},
                    {"id": "2", "title": "Buy food", "priority": 2},
                    {"id": "3", "title": "Stay hydrated", "priority": 3},
                ]
            }
        }


@pytest.mark.asyncio
async def test_query_list_with_nested_fields():
    async with aiohttp.ClientSession() as session:
        query = """
            query {
                todos {
                    id
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
                "todos": [
                    {"id": "1", "creator": {"id": "1", "name": "Amelia"}},
                    {"id": "2", "creator": {"id": "2", "name": "Bill"}},
                    {"id": "3", "creator": {"id": "3", "name": "Clara"}},
                ]
            }
        }


@pytest.mark.asyncio
async def test_query_flat_object():
    async with aiohttp.ClientSession() as session:
        query = """
            query {
                todo(id: 1) {
                    id
                    title
                    priority
                }
            }
        """

        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        response = await client.execute(query)

        assert await response.json() == {
            "data": {"todo": {"id": "1", "title": "Clean kitchen", "priority": 1}}
        }


@pytest.mark.asyncio
async def test_query_object_with_nested_fields():
    async with aiohttp.ClientSession() as session:
        query = """
            query {
                todo(id: 1) {
                    id
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
            "data": {"todo": {"id": "1", "creator": {"id": "1", "name": "Amelia"}}}
        }


@pytest.mark.asyncio
async def test_selecting_an_operation():
    async with aiohttp.ClientSession() as session:
        query = """
            query Operation1 {
                todos {
                    id
                }
            }
            query Operation2 {
                todo(id: 1) {
                    id
                }
            }
        """

        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        response = await client.execute(query, operation="Operation2")

        assert await response.json() == {"data": {"todo": {"id": "1"}}}
