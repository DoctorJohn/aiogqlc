import asyncio
import aiohttp
from aiogqlc import GraphQLClient

query = '''
    query {
        allFilms {
            title
        }
    }
'''


async def main():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient('https://swapi.graph.cool', session=session)
        response = await client.execute(query)
        print(await response.json())


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
