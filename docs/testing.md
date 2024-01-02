# Testing

There is no need to mock `aiogqlc` in your tests.
Instead you might want to mock your GraphQL backend.
This can be done by providing a `aiohttp.web.Application`.

The following example shows a `pytest` and `pytest-aiohttp` based test using a mock GraphQL backend:

```python
import aiohttp
import aiohttp.web
from aiogqlc import GraphQLClient


class TestGraphQLView(aiohttp.web.View):
    async def post(self):
        return aiohttp.web.json_response({"data": {"ping": "pong"}})


async def test_ping_query(aiohttp_client):
    app = aiohttp.web.Application()
    app.router.add_route("*", "/graphql", TestGraphQLView)

    graphql_session = await aiohttp_client(app)
    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    response = await client.execute("query { ping }")
    assert await response.json() == {"data": {"ping": "pong"}}
```

In fact, the `aiogqlc` test suite itself is based on this approach.
Take a look at [the aiogqlc tests directory](https://github.com/DoctorJohn/aiogqlc/tree/main/tests) for more advanced examples.
