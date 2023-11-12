# Authentication

## Authenticate queries and mutations

HTTP based requests can be authenticated using HTTP headers.
Take a look at the [aiohttp documentation][aiohttp-headers-url] to learn more.

[aiohttp-headers-url]: https://docs.aiohttp.org/en/stable/client_advanced.html#custom-request-headers

The following example shows how to set a default `Authorization` header for the whole session.

```python
import aiohttp
from aiogqlc import GraphQLClient

headers = {
    "Authorization": "Token <your-token-here>"
}

async def foo():
    async with aiohttp.ClientSession(headers=headers) as session:
        client = GraphQLClient("https://example.com/graphql/", session=session)
```

Instead of setting a default header for the whole session, you can also set a header for a single request.

```python
import aiohttp
from aiogqlc import GraphQLClient

headers = {
    "Authorization": "Token <your-token-here>"
}

async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient("https://example.com/graphql/", session=session)
        response = await client.execute("query { someField }", headers=headers)
```

## Authenticate `graphql-ws` connections

GraphQL servers _usualy_ don't support the authentication of WebSocket connections via
HTTP headers. The reason for this is that the [WebSocket specification][ws-spec] does
not cover the usage of HTTP headers via WebSockets.

Instead of HTTP headers, so called _connection parameters_ are used to authenticate
a `graphql-ws` WebSocket connections.
Keep in mind that connection parameters are a subprotocol specific feature
and not an universal standard.

```python
import aiohttp
from aiogqlc import GraphQLClient


async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient("https://example.com/graphql/", session=session)

        connection_params = {
            "username": "john",
            "password": "1234",
        }

        async with client.connect(params=connection_params) as connection:
            pass
```

[ws-spec]: https://websockets.spec.whatwg.org/
