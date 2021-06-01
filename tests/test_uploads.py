import aiohttp
import pytest
from aiogqlc import GraphQLClient
from tests import TEST_ENDPOINT


def create_test_file(tmp_path, filename):
    test_file_content = "hello world"
    test_file = tmp_path / filename
    test_file.write_text(test_file_content)
    return test_file


@pytest.mark.asyncio
async def test_single_file_upload(tmp_path):
    async with aiohttp.ClientSession() as session:
        filename = "file1.txt"
        test_file = create_test_file(tmp_path, filename)

        query = """
            mutation($file: Upload!) {
                uploadFile(file: $file) {
                    filename
                    mimetype
                    encoding
                }
            }
        """
        variables = {"file": test_file.open()}

        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        response = await client.execute(query, variables=variables)

        assert await response.json() == {
            "data": {
                "uploadFile": {
                    "filename": filename,
                    "mimetype": "text/plain",
                    "encoding": "7bit",
                }
            }
        }


@pytest.mark.asyncio
async def test_file_list_upload(tmp_path):
    async with aiohttp.ClientSession() as session:
        filename1 = "file1.txt"
        filename2 = "file2.txt"
        test_file1 = create_test_file(tmp_path, filename1).open()
        test_file2 = create_test_file(tmp_path, filename2).open()

        query = """
            mutation($files: [Upload!]!) {
                uploadFiles(files: $files) {
                    filename
                    mimetype
                    encoding
                }
            }
        """
        variables = {"files": [test_file1, test_file2]}

        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        response = await client.execute(query, variables=variables)

        assert await response.json() == {
            "data": {
                "uploadFiles": [
                    {
                        "filename": filename1,
                        "mimetype": "text/plain",
                        "encoding": "7bit",
                    },
                    {
                        "filename": filename2,
                        "mimetype": "text/plain",
                        "encoding": "7bit",
                    },
                ]
            }
        }


@pytest.mark.asyncio
async def test_using_in_single_file_under_multiple_paths(tmp_path):
    async with aiohttp.ClientSession() as session:
        filename1 = "file1.txt"
        test_file1 = create_test_file(tmp_path, filename1).open()

        query = """
            mutation($files: [Upload!]!) {
                uploadFiles(files: $files) {
                    filename
                    mimetype
                    encoding
                }
            }
        """
        variables = {"files": [test_file1, test_file1]}

        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        response = await client.execute(query, variables=variables)

        assert await response.json() == {
            "data": {
                "uploadFiles": [
                    {
                        "filename": filename1,
                        "mimetype": "text/plain",
                        "encoding": "7bit",
                    },
                    {
                        "filename": filename1,
                        "mimetype": "text/plain",
                        "encoding": "7bit",
                    },
                ]
            }
        }
