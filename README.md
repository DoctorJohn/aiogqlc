# Asynchronous/IO GraphQL client

[![Versions][versions-image]][versions-url]
[![PyPI][pypi-image]][pypi-url]
[![Downloads][downloads-image]][downloads-url]
[![Codecov][codecov-image]][codecov-url]
[![License][license-image]][license-url]

[versions-image]: https://img.shields.io/pypi/pyversions/aiogqlc
[versions-url]: https://github.com/DoctorJohn/aiogqlc/blob/master/setup.py
[pypi-image]: https://img.shields.io/pypi/v/aiogqlc
[pypi-url]: https://pypi.org/project/aiogqlc/
[downloads-image]: https://img.shields.io/pypi/dm/aiogqlc
[downloads-url]: https://pypi.org/project/aiogqlc/
[codecov-image]: https://codecov.io/gh/DoctorJohn/aiogqlc/branch/main/graph/badge.svg?token=63WRUHG8SW
[codecov-url]: https://codecov.io/gh/DoctorJohn/aiogqlc
[license-image]: https://img.shields.io/pypi/l/aiogqlc
[license-url]: https://github.com/DoctorJohn/aiogqlc/blob/master/LICENSE

A Python asynchronous/IO GraphQL client based on [aiohttp][aiohttp-url].

In addition to standard HTTP POST `queries` and `mutations` this client fully supports
the [GraphQL multipart form requests spec][multipart-specs-url] for file uploads
and the [graphql-ws subprotocol][graphql-ws-url] for WebSocket based `subscriptions`.

**[Read the documentation][docs-url]**

## Installation

`pip install aiogqlc`

## Basic usage

```python
import asyncio
import aiohttp
from aiogqlc import GraphQLClient

ENDPOINT = "https://swapi-graphql.netlify.app/.netlify/functions/index"

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
        client = GraphQLClient(document, session=session)
        response = await client.execute(document)
        print(await response.json())


if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation

[Read the documentation][docs-url] to learn more about queries, mutations, subscriptions, file uploads and even authorization.

[aiohttp-url]: https://github.com/aio-libs/aiohttp
[multipart-specs-url]: https://github.com/jaydenseric/graphql-multipart-request-spec
[graphql-ws-url]: https://github.com/apollographql/subscriptions-transport-ws
[docs-url]: https://doctorjohn.github.io/aiogqlc/
