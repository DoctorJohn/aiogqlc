# Asynchronous/IO GraphQL client

[![PyPI][pypi-image]][pypi-url]
[![Downloads][downloads-image]][downloads-url]
[![License][license-image]][license-url]
[![Tests][tests-image]][tests-url]
[![codecov][codecov-image]][codecov-url]

[pypi-image]: https://img.shields.io/pypi/v/aiogqlc
[pypi-url]: https://pypi.org/project/aiogqlc/
[downloads-image]: https://img.shields.io/pypi/dm/aiogqlc
[downloads-url]: https://pypi.org/project/aiogqlc/
[license-image]: https://img.shields.io/pypi/l/aiogqlc
[license-url]: https://github.com/DoctorJohn/aiogqlc/blob/master/LICENSE
[tests-image]: https://github.com/DoctorJohn/aiogqlc/workflows/Tests/badge.svg
[tests-url]: https://github.com/DoctorJohn/aiogqlc/actions
[codecov-image]: https://codecov.io/gh/DoctorJohn/aiogqlc/branch/main/graph/badge.svg?token=63WRUHG8SW
[codecov-url]: https://codecov.io/gh/DoctorJohn/aiogqlc

A Python asynchronous/IO GraphQL client based on [aiohttp][aiohttp-url].
In addition to standard HTTP POST `queries` and `mutations` this client fully supports
the [GraphQL multipart form requests spec][multipart-specs-url] for file uploads
and the [graphql-ws protocol][graphql-ws-url] for WebSocket based `subscriptions`.

[aiohttp-url]: https://github.com/aio-libs/aiohttp
[multipart-specs-url]: https://github.com/jaydenseric/graphql-multipart-request-spec
[graphql-ws-url]: https://github.com/apollographql/subscriptions-transport-ws

## Requirements

- Python (>=3.7)
- [aiohttp](https://pypi.org/project/aiohttp/) (>=3.6.0)

## Installation

`pip install aiogqlc`

## Usage

### Executing simple queries

```python
import asyncio
import aiohttp
from aiogqlc import GraphQLClient

ENDPOINT = "https://swapi-graphql.netlify.app/.netlify/functions/index"

query = """
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
        client = GraphQLClient(ENDPOINT, session=session)
        response = await client.execute(query)
        print(await response.json())


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
```

### Adding authorization headers

```python
import aiohttp
from aiogqlc import GraphQLClient

headers = {
    'Authorization': 'Token <your-token-here>'
}

async def foo():
    async with aiohttp.ClientSession(headers=headers) as session:
        client = GraphQLClient('https://example.com/graphql/', session=session)
```

### Single file upload

```python
import aiohttp
from aiogqlc import GraphQLClient

query = '''
    mutation($file: Upload!) {
        yourSingleUploadMutation(file: $file) {
            errors {
                field
                messages
            }
        }
    }
'''

variables = {
    'file': open('test.zip', 'rb'),
}

async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient('https://example.com/graphql/', session=session)
        response = await client.execute(query, variables=variables)
        print(await response.json())
```

### File list upload

```python
import aiohttp
from aiogqlc import GraphQLClient

query = '''
    mutation($files: [Upload!]!) {
        yourMultiUploadMutation(files: $files) {
            errors {
                field
                messages
            }
        }
    }
'''

variables = {
    'files': [
        open('foo.zip', 'rb'),
        open('var.zip', 'rb'),
    ],
}

async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient('https://example.com/graphql/', session=session)
        response = await client.execute(query, variables=variables)
        print(await response.json())
```

### Selecting an operation

```python
import aiohttp
from aiogqlc import GraphQLClient

query = '''
    query Operation1 {
        allFilms {
            id
        }
    }
    query Operation2 {
        film(id: 1) {
            id
        }
    }
'''

async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient('https://example.com/graphql/', session=session)
        response = await client.execute(query, operation='Operation2')
        print(await response.json())
```

### Starting a subscription

```python
import aiohttp
from aiogqlc import GraphQLClient


query = """
    subscription CommentAdded($article: ID!) {
        commentAdded(article: $article) {
            id
            content
        }
    }
"""

variables = {
    "article": "42"
}


async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient('https://example.com/graphql/', session=session)

        async with client.connect() as connection:
            async for payload in connection.subscribe(query, variables=variables):
                print(payload)
```

### Start multiple subscriptions using a single connection

The `graphql-ws` protocol allows us to reuse a single WebSocket connection for multiple
subscriptions. While the example below shows running two subscriptions sequential,
running multiple subscriptions over one connection in parallel works as well.

```python
import aiohttp
from aiogqlc import GraphQLClient


query = """
    subscription ItemAdded($list: ID!) {
        itemAdded(list: $list) {
            id
            content
        }
    }
"""


async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient('https://example.com/graphql/', session=session)

        async with client.connect() as connection:
            async for payload in connection.subscribe(query, variables={"list": "1"}):
                print(payload)

            async for payload in connection.subscribe(query, variables={"list": "2"}):
                print(payload)
```

### Selecting a subscription operating

```python
import aiohttp
from aiogqlc import GraphQLClient


query = """
    subscription Subscription1 {
        count(to: 11)
    }
    subscription Subscription2 {
        count(to: 22)
    }
"""


async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient('https://example.com/graphql/', session=session)

        async with client.connect() as connection:
            async for payload in connection.subscribe(query, operation="Subscription2"):
                print(payload)
```

### Using connection params

Some servers supporting `graphql-ws` allow clients to specify connection params.

```python
import aiohttp
from aiogqlc import GraphQLClient


query = """
    subscription {
        userCreated
    }
"""


async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient('https://example.com/graphql/', session=session)
        
        connection_params = {
            "username": "john",
            "password": "1234",
            "keep_alive_interval": 20,
        }

        async with client.connect(params=connection_params) as connection:
            async for payload in connection.subscribe(query):
                print(payload)
```

## Contributing

### Quickstart

1. Clone the repo
2. Create and enter a dedicated virtual environment
3. Run `make dev` to install dev dependencies and a pre-commit hook that automatically formats code.

If you do not have `make` installed, either install it or take a look at the `Makefile` to find out how to run individual commands manually.

### Formatting and linting

- Run `make format` to format the code.
- Run `make lint` to lint the code.

### Testing

- Run `make test` to run all tests in your local environment.
- Run `make tox` to run all tests with all supported python versions.
