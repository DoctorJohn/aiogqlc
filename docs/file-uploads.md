# File uploads

File uploads are not part of the official GraphQL spec (yet).
To fill the gap AIOGQLC supports the widely adopted
[GraphQL multipart request specification][multipart-specs-url].

File upload variables work just like other variables.
Just remember to **open files in a readable `mode`**.
Otherwise they can't be read and uploaded.

## Upload a single file

```python
import aiohttp
from aiogqlc import GraphQLClient

document = """
    mutation($file: Upload!) {
        uploadFile(file: $file) {
            size
        }
    }
"""

variables = {
    "file": open("test.txt", "rb")
}


async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient("https://example.com/graphql/", session=session)
        response = await client.execute(document, variables=variables)
        print(await response.json())
```

## Uploading a list of files

```python
import aiohttp
from aiogqlc import GraphQLClient

document = """
    mutation($files: [Upload!]!) {
        uploadFiles(files: $files) {
            id
        }
    }
"""

variables = {
    "files": [
        open("foo.zip", "rb"),
        open("bar.zip", "rb"),
    ],
}


async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient("https://example.com/graphql/", session=session)
        response = await client.execute(document, variables=variables)
        print(await response.json())
```

## Prevent unnecessary uploads

A file can be referenced multiple times but will only be uploaded once.

```python
import aiohttp
from aiogqlc import GraphQLClient

document = """
    mutation($files: [Upload!]!) {
        combineFiles(files: $files) {
            id
        }
    }
"""

blank_file = open("blank.pdf", "rb")
content_file = open("content.pdf", "rb")

variables = {
    "files": [
        blank_file,
        content_file,
        blank_file,
    ],
}


async def foo():
    async with aiohttp.ClientSession() as session:
        client = GraphQLClient("https://example.com/graphql/", session=session)
        response = await client.execute(document, variables=variables)
        print(await response.json())
```

[multipart-specs-url]: https://github.com/jaydenseric/graphql-multipart-request-spec
