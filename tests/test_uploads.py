from io import BytesIO

import aiohttp

from aiogqlc import GraphQLClient
from aiogqlc.types import Variables


async def test_single_file_upload(graphql_session: aiohttp.ClientSession):
    file1 = BytesIO(b"Hello, World!")

    query = """
        mutation($file: Upload!) {
            readFile(file: $file)
        }
    """
    variables = {"file": file1}

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    response = await client.execute(query, variables=variables)

    assert await response.json() == {"data": {"readFile": "Hello, World!"}}


async def test_file_list_upload(graphql_session: aiohttp.ClientSession):
    file1 = BytesIO(b"Hello, Foo!")
    file2 = BytesIO(b"Hello, Bar!")

    query = """
        mutation($files: [Upload!]!) {
            readFiles(files: $files)
        }
    """
    variables = {"files": [file1, file2]}

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    response = await client.execute(query, variables=variables)

    assert await response.json() == {
        "data": {
            "readFiles": [
                "Hello, Foo!",
                "Hello, Bar!",
            ]
        }
    }


async def test_using_in_single_file_under_multiple_paths(
    graphql_session: aiohttp.ClientSession,
):
    file1 = BytesIO(b"Hello, World!")

    query = """
        mutation($files: [Upload!]!) {
            readFiles(files: $files)
        }
    """
    variables = {"files": [file1, file1]}

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    response = await client.execute(query, variables=variables)

    assert await response.json() == {
        "data": {
            "readFiles": [
                "Hello, World!",
                "Hello, World!",
            ]
        }
    }


async def test_separation_of_files_from_an_object(
    graphql_session: aiohttp.ClientSession,
):
    file1 = BytesIO(b"Hello, World!")

    query = """
        mutation($document: DocumentInput!) {
            readDocument(document: $document) {
                title
                length
            }
        }
    """

    variables: Variables = {
        "document": {
            "file": file1,
            "title": "Some Title",
        }
    }

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    response = await client.execute(query, variables=variables)

    assert await response.json() == {
        "data": {
            "readDocument": {
                "title": "Some Title",
                "length": 13,
            }
        }
    }
