# Testing

There is no need to mock `aiogqlc` in your tests.
Instead you might want to mock your GraphQL backend.
This can be done by providing a `aiohttp.web.Application`.

The following example shows an example based on `pytest`, `pytest-asyncio`, and `pytest-aiohttp` using a mock GraphQL backend:

```python
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
```

In fact, the `aiogqlc` test suite itself is based on this approach.
Take a look at [the aiogqlc tests directory](https://github.com/DoctorJohn/aiogqlc/tree/main/tests) for more advanced examples.
