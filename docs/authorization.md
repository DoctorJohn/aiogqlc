# Authorization

## Authorizing queries and mutations

HTTP based requests can be authenticated using HTTP headers.
Take a look at the [aiohttp documentation][aiohttp-headers-url] to learn more.

[aiohttp-headers-url]: https://docs.aiohttp.org/en/stable/client_advanced.html#custom-request-headers

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

## Authorizing `graphql-ws` subscriptions

WebSocket based subscriptions cannot be authorized via HTTP headers.
Instead, subscription subprotocol specific *connection parameters* are used.

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
