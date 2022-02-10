# Mutations

Mutations work just like [queries](queries.md).
If you want to upload files via mutations, take a look at the [file uploads documentation](file-uploads.md).

## Executing a simple mutation

```python
import aiohttp
from aiogqlc import GraphQLClient

document = """
    mutation ($userId: ID!) {
        deleteUser (id: $userId) {
            id
        }
    }
"""

variables = {
    "userId": "42",
}


async def main():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient("https://example.com/graphql/", session=session)
        response = await client.execute(document, variables=variables)
        print(await response.json())
```

### Selecting an operation

```python
import aiohttp
from aiogqlc import GraphQLClient

document = """
    mutation Operation1 {
        doSomething
    }
    mutation Operation2 {
        doSomethingElse
    }
"""


async def main():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient("https://example.com/graphql/", session=session)
        response = await client.execute(document, operation="Operation2")
        print(await response.json())
```
