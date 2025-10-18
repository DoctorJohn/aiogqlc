# Queries

All examples on this page are runnable. Be encouraged to copy and run them.

### Executing simple queries

```python
import asyncio
import aiohttp
from aiogqlc import GraphQLClient

endpoint = "https://swapi-graphql.netlify.app/graphql"

document = """
    query {
        allFilms {
            films {
                title
            }
        }
    }
"""


async def main():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient(endpoint, session=session)
        response = await client.execute(document)
        print(await response.json())


if __name__ == "__main__":
    asyncio.run(main())
```

### Passing variables

```python
import aiohttp
from aiogqlc import GraphQLClient

endpoint = "https://swapi-graphql.netlify.app/graphql"

document = """
    query ($count: Int!) {
        allFilms (first: $count) {
            films {
                title
            }
        }
    }
"""

variables = {
    "count": 3,
}


async def main():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient(endpoint, session=session)
        response = await client.execute(document, variables=variables)
        print(await response.json())


if __name__ == "__main__":
    asyncio.run(main())
```

### Selecting an operation

```python
import aiohttp
from aiogqlc import GraphQLClient

endpoint = "https://swapi-graphql.netlify.app/graphql"

document = """
    query Operation1 {
        allPlanets {
            totalCount
        }
    }

    query Operation2 {
        allFilms {
            totalCount
        }
    }
"""

async def main():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient(endpoint, session=session)
        response = await client.execute(document, operation="Operation2")
        print(await response.json())


if __name__ == "__main__":
    asyncio.run(main())
```