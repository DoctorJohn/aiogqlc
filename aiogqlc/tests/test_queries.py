import aiohttp
import pytest
from aiogqlc import GraphQLClient
from aiogqlc.tests import TEST_ENDPOINT


@pytest.mark.asyncio
async def test_query_flat_list():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        query = """
            query {
                todos {
                    id
                    title
                    priority
                }
            }
        """
        response = await client.execute(query)
        expected = {
            "data": {
                "todos": [
                    {"id": "1", "title": "Clean kitchen", "priority": 1},
                    {"id": "2", "title": "Buy food", "priority": 2},
                    {"id": "3", "title": "Stay hydrated", "priority": 3},
                ]
            }
        }
        assert await response.json() == expected


@pytest.mark.asyncio
async def test_query_list_with_nested_fields():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
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
        response = await client.execute(query)
        expected = {
            "data": {
                "todos": [
                    {"id": "1", "creator": {"id": "1", "name": "Amelia"}},
                    {"id": "2", "creator": {"id": "2", "name": "Bill"}},
                    {"id": "3", "creator": {"id": "3", "name": "Clara"}},
                ]
            }
        }
        assert await response.json() == expected


@pytest.mark.asyncio
async def test_query_flat_object():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        query = """
            query {
                todo(id: 1) {
                    id
                    title
                    priority
                }
            }
        """
        response = await client.execute(query)
        expected = {
            "data": {"todo": {"id": "1", "title": "Clean kitchen", "priority": 1}}
        }
        assert await response.json() == expected


@pytest.mark.asyncio
async def test_query_object_with_nested_fields():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
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
        response = await client.execute(query)
        expected = {
            "data": {"todo": {"id": "1", "creator": {"id": "1", "name": "Amelia"}}}
        }
        assert await response.json() == expected
