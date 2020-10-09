# Asynchronous/IO GraphQL client

![PyPI](https://img.shields.io/pypi/v/aiogqlc)
![PyPI - Downloads](https://img.shields.io/pypi/dm/aiogqlc)
![PyPI - License](https://img.shields.io/pypi/l/aiogqlc)

A Python asynchronous/IO GraphQL client based on `aiohttp` that supports the [GraphQL multipart form requests spec](https://github.com/jaydenseric/graphql-multipart-request-spec) for file uploads.

## Requirements

- Python (>=3.6)
- [aiohttp](https://pypi.org/project/aiohttp/) (>=3.6.0)

## Installation

```pip install aiogqlc```

## Usage

### Executing simple queries

```python
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

async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient('https://swapi.graph.cool/', session=session)
        response = await client.execute(query)
        print(await response.json())

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(foo())
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

### Multiple file upload

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

## Contributing

### Quickstart

1. Clone the repo
2. Create and enter a dedicated virtual environment
3. Run `make install-dev` to install dev dependencies and a pre-commit hook that automatically formats code.

If you do not have `make` installed, either install it or take a look at the `Makefile` to find out how to run individual commands manually.

### Formatting and linting

- Run `make format` to format the code.
- Run `make lint` to lint the code.

### Testing
- Run `make test` to run all tests in your local environment.
- Run `make test-with-tox` to run all tests with all supported python versions.

