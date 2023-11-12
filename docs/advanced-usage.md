# Advanced usage

## Passing request options to `aiohttp`

While you can set various default options on your `aiohttp.ClientSession` instance,
there's sometimes the need to pass extra options to the underlying request made by `aiohttp`.

For this purpose, any additional keyword argument passed to `GraphQLClient.execute` will be passed to `aiohttp.ClientSession.request`.

```python
import aiohttp
from aiogqlc import GraphQLClient

async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient("https://example.com/graphql/", session=session)

        response = await client.execute(
            document="query { someField }",
            headers={"Authorization": "Bearer SomeToken"},
            timeout=aiohttp.ClientTimeout(total=10),
        )
```
