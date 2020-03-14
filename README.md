# Asynchronous/IO GraphQL client

![PyPI](https://img.shields.io/pypi/v/aiogqlc)
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
