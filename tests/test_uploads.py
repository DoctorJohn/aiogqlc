from io import BytesIO

from aiogqlc import GraphQLClient


async def test_single_file_upload(graphql_session):
    file1 = BytesIO(b"Hello, World!")

    query = """
        mutation($file: Upload!) {
            readFile(file: $file)
        }
    """
    variables = {"file": file1}

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    async with client.execute(query, variables=variables) as response:
        assert await response.json() == {"data": {"readFile": "Hello, World!"}}


async def test_file_list_upload(graphql_session):
    file1 = BytesIO(b"Hello, Foo!")
    file2 = BytesIO(b"Hello, Bar!")

    query = """
        mutation($files: [Upload!]!) {
            readFiles(files: $files)
        }
    """
    variables = {"files": [file1, file2]}

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    async with client.execute(query, variables=variables) as response:
        assert await response.json() == {
            "data": {
                "readFiles": [
                    "Hello, Foo!",
                    "Hello, Bar!",
                ]
            }
        }


async def test_using_in_single_file_under_multiple_paths(graphql_session, tmp_path):
    file1 = BytesIO(b"Hello, World!")

    query = """
        mutation($files: [Upload!]!) {
            readFiles(files: $files)
        }
    """
    variables = {"files": [file1, file1]}

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    async with client.execute(query, variables=variables) as response:
        assert await response.json() == {
            "data": {
                "readFiles": [
                    "Hello, World!",
                    "Hello, World!",
                ]
            }
        }
