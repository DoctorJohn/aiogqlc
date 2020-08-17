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
from aiogqlc import GraphQLClient


query = '''
    query {
        allFilms {
            title
        }
    }
'''

async def foo():
    client = GraphQLClient('https://swapi.graph.cool/')
    response = await client.execute(query)
    print(await response.json())

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(foo())
```

### Adding authorization headers

```python
from aiogqlc import GraphQLClient

headers = {
    'Authorization': 'Token <your-token-here>'
}

client = GraphQLClient('https://example.com/graphql/', headers=headers)
```

### Single file upload

```python
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
    client = GraphQLClient('https://example.com/graphql/')
    response = await client.execute(query, variables=variables)
    print(await response.json())
```

### Multiple file upload

```python
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
    client = GraphQLClient('https://example.com/graphql/')
    response = await client.execute(query, variables=variables)
    print(await response.json())
```

## Contributing

After cloning the repo and creating/entering an dedicated virtual environment, you may run `pip install -e ".[dev]"` to install development dependencies.

Make sure to run `black aiogqlc setup.py` and `flake8 aiogqlc setup.py` before commiting your changes.

Note that if you have `make` installed, you may run the following recipes instead of the commands named above: `make install-dev`, `make format`, `make lint`.
