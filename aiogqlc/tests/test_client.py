# Local libraries
from aiogqlc import GraphQLClient

# Third party libraries
import aiohttp
from aioextensions import run_decorator


@run_decorator
async def test_client() -> None:
    async with aiohttp.ClientSession(headers={"x-foo": "bar"}) as session:
        client = GraphQLClient(endpoint="https://swapi.graph.cool", session=session,)

        assert client.endpoint == "https://swapi.graph.cool"
        assert client.session is session
        assert client.session._default_headers["x-foo"] == "bar"

        response: aiohttp.ClientResponse = await client.execute(
            """
            query {
                allFilms {
                    title
                }
            }
        """
        )

        assert await response.json() == {
            "data": {
                "allFilms": [
                    {"title": "A New Hope"},
                    {"title": "Attack of the Clones"},
                    {"title": "The Phantom Menace"},
                    {"title": "Revenge of the Sith"},
                    {"title": "Return of the Jedi"},
                    {"title": "The Empire Strikes Back"},
                    {"title": "The Force Awakens"},
                ],
            },
        }
