# Getting started

## Installation

Run the following [pip](https://pip.pypa.io/en/stable/getting-started/) command in a terminal:

`pip install aiogqlc`

## Try it out

```python
import asyncio
import aiohttp
from aiogqlc import GraphQLClient

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
        endpoint = "https://swapi-graphql.netlify.app/.netlify/functions/index"
        client = GraphQLClient(endpoint, session=session)
        response = await client.execute(document)
        print(await response.json())


if __name__ == "__main__":
    asyncio.run(main())
```

## Learn more

Take a look at the navigation too learn more about
[queries](queries.md), [mutations](mutations.md), [subscriptions](subscriptions.md) and other operations.
