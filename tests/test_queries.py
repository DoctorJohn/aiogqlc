from aiogqlc import GraphQLClient


async def test_query_flat_list(graphql_session):
    query = """
        query {
            todos {
                id
                title
                priority
            }
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    response = await client.execute(query)

    assert await response.json() == {
        "data": {
            "todos": [
                {"id": "0", "title": "Clean kitchen", "priority": 0},
                {"id": "1", "title": "Buy groceries", "priority": 1},
                {"id": "2", "title": "Stay hydrated", "priority": 2},
            ]
        }
    }


async def test_query_list_with_nested_fields(graphql_session):
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

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    response = await client.execute(query)

    assert await response.json() == {
        "data": {
            "todos": [
                {"id": "0", "creator": {"id": "0", "name": "Amelia"}},
                {"id": "1", "creator": {"id": "1", "name": "Bill"}},
                {"id": "2", "creator": {"id": "2", "name": "Clara"}},
            ]
        }
    }


async def test_query_flat_object(graphql_session):
    query = """
        query {
            todo(id: 1) {
                id
                title
                priority
            }
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    response = await client.execute(query)

    assert await response.json() == {
        "data": {"todo": {"id": "1", "title": "Buy groceries", "priority": 1}}
    }


async def test_query_object_with_nested_fields(graphql_session):
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

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    response = await client.execute(query)

    assert await response.json() == {
        "data": {"todo": {"id": "1", "creator": {"id": "1", "name": "Bill"}}}
    }


async def test_selecting_an_operation(graphql_session):
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

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    response = await client.execute(query, operation="Operation2")

    assert await response.json() == {"data": {"todo": {"id": "1"}}}
