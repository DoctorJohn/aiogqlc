# Asynchronous/IO GraphQL client

![PyPI](https://img.shields.io/pypi/v/aiogqlc)
![PyPI - Downloads](https://img.shields.io/pypi/dm/aiogqlc)
![PyPI - License](https://img.shields.io/pypi/l/aiogqlc)

A Python asynchronous/IO GraphQL client based on `aiohttp` that supports the [GraphQL multipart form requests spec](https://github.com/jaydenseric/graphql-multipart-request-spec) for file uploads.

## Requirements

- Python 3
- [aiohttp](https://pypi.org/project/aiohttp/)

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
3. Run `make install-dev` to install dev dependencies and a formatting pre-commit hook.

### Individual commands

Run `pip install -r ".[dev]"` to install dev dependencies.

Run `black aiogqlc setup.py` or `make format` to format the code.

Run `flake8 aiogqlc setup.py` or `make lint` to lint the code.

Run `pre-commit install` to install a formatting pre-commit hook.

