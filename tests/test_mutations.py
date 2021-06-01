from aiogqlc import GraphQLClient


async def test_mutation_with_flat_response(graphql_session):
    query = """
        mutation {
            fakeUser(id: 7, name: "John Smith") {
                id
                name
            }
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    response = await client.execute(query)

    assert await response.json() == {
        "data": {"fakeUser": {"id": "7", "name": "John Smith"}}
    }


async def test_mutation_with_nested_fields_in_response(graphql_session):
    query = """
        mutation {
            fakeTodo(id: 7, title: "TODO", priority: 10, creator: 1) {
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

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    response = await client.execute(query)

    assert await response.json() == {
        "data": {
            "fakeTodo": {
                "id": "7",
                "title": "TODO",
                "priority": 10,
                "creator": {"id": "1", "name": "Bill"},
            }
        }
    }
