import asyncio

import aiohttp
from aiogqlc import GraphQLClient

ENDPOINT = "https://swapi-graphql.netlify.app/.netlify/functions/index"


async def main():
    query = """
        query {
            allFilms {
                films {
                    title
                }
            }
        }
    """

    async with aiohttp.ClientSession() as session:
        client = GraphQLClient(ENDPOINT, session=session)
        response = await client.execute(query)
        print(await response.json())


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
