import aiohttp
import pytest
from aiogqlc import GraphQLClient
from aiogqlc.tests import TEST_ENDPOINT


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
        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
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
        response = await client.execute(query, variables=variables)
        expected = {
            "data": {
                "uploadFile": {
                    "filename": filename,
                    "mimetype": "text/plain",
                    "encoding": "7bit",
                }
            }
        }
        assert await response.json() == expected


@pytest.mark.asyncio
async def test_multiple_file_upload(tmp_path):
    async with aiohttp.ClientSession() as session:
        filename1 = "file1.txt"
        filename2 = "file2.txt"
        test_file1 = create_test_file(tmp_path, filename1)
        test_file2 = create_test_file(tmp_path, filename2)
        client = GraphQLClient(endpoint=TEST_ENDPOINT, session=session)
        query = """
            mutation($files: [Upload!]!) {
                uploadFiles(files: $files) {
                    filename
                    mimetype
                    encoding
                }
            }
        """
        variables = {"files": [test_file1.open(), test_file2.open()]}
        response = await client.execute(query, variables=variables)
        expected = {
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
        assert await response.json() == expected
