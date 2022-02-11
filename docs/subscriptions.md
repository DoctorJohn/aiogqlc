# Subscriptions

WebSocket based subscriptions are not part of the official GraphQL specification (yet).
Fortunately, there are third-party specifications such as
[graphql-ws][graphql-ws-url] and [graphql-transport-ws][graphql-transport-ws-url].

AIOGQLC currently only supports the legacy `graphql-ws` subprotocol.

!!! warning "Subprotocol names are confusing!"

    Note that the legacy `graphql-ws` subprotocol is hosted in a repository called `graphql-ws-transport`,
    while the newer `graphql-transport-ws` subprotocol is hosted in a repository called `graphql-ws`.
    *This documentation always refers to the subprotocol names, not the repository names.*

[graphql-ws-url]: https://github.com/apollographql/subscriptions-transport-ws/blob/master/PROTOCOL.md
[graphql-transport-ws-url]: https://github.com/enisdenjo/graphql-ws/blob/master/PROTOCOL.md

## Using the `graphql-ws` subprotocol

### Starting a subscription

```python
import aiohttp
from aiogqlc import GraphQLClient

document = """
    subscription ($postId: ID!) {
        likeAdded(postId: $postId)
    }
"""

variables = {
    "postId": "42"
}


async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient("https://example.com/graphql/", session=session)

        async with client.connect() as connection:
            async for payload in connection.subscribe(document, variables=variables):
                print(payload)
```

### Start multiple subscriptions using a single connection

The `graphql-ws` protocol allows us to reuse a single WebSocket connection for multiple subscriptions.

```python
import aiohttp
from aiogqlc import GraphQLClient

document = """
    subscription ($postId: ID!) {
        likeAdded(postId: $postId)
    }
"""


async def watch_likes(connection, post_id):
    variables = {
        "postId": post_id
    }

    async for payload in connection.subscribe(document, variables=variables):
        print(payload)


async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient("https://example.com/graphql/", session=session)

        async with client.connect() as connection:
            asyncio.create_task(watch_likes(connection, post_id="1"))
            asyncio.create_task(watch_likes(connection, post_id="2"))
```

### Selecting an operation

```python
import aiohttp
from aiogqlc import GraphQLClient

document = """
    subscription Subscription1 {
        count(to: 11)
    }
    subscription Subscription2 {
        count(to: 22)
    }
"""


async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient("https://example.com/graphql/", session=session)

        async with client.connect() as connection:
            async for payload in connection.subscribe(document, operation="Subscription2"):
                print(payload)
```

### Using connection params

Some servers allow clients to specify connection params.
These are particular useful for authentication and other connection settings.

```python
import aiohttp
from aiogqlc import GraphQLClient

document = """
    subscription {
        newTemperature
    }
"""


async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient("https://example.com/graphql/", session=session)
        
        connection_params = {
            "username": "john",
            "password": "1234",
            "keep_alive_interval": 20,
        }

        async with client.connect(params=connection_params) as connection:
            async for payload in connection.subscribe(document):
                print(payload)
```
