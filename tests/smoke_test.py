import asyncio

import aiohttp

from aiogqlc import GraphQLClient

ENDPOINT = "https://swapi-graphql.netlify.app/graphql"
DOCUMENT = """
    query TestQuery {
        allFilms {
            films {
                title
            }
        }
    }
"""


async def main():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient(ENDPOINT, session=session)
        response = await client.execute(DOCUMENT)
        print(await response.json())


if __name__ == "__main__":
    asyncio.run(main())
