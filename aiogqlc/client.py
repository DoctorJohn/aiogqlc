import json
from io import IOBase
from typing import Any, Tuple

import aiohttp


class GraphQLClient:
    def __init__(self, endpoint: str, session: aiohttp.ClientSession) -> None:
        self.endpoint = endpoint
        self.session = session

    async def execute(
        self, query: str, variables: dict = None, operation: str = None
    ) -> aiohttp.ClientResponse:
        nulled_variables, files = self.prepare(variables)

        if files:
            data = self.prepare_multipart(query, nulled_variables, files, operation)
            data_param = {"data": data}
        else:
            data = self.prepare_json_data(query, variables, operation)
            data_param = {"json": data}

        async with self.session.post(self.endpoint, **data_param) as response:
            await response.read()
            return response

    @classmethod
    def prepare(cls, variables: dict) -> Tuple[dict, dict]:
        files = {}

        def separate_files(path: str, obj: object) -> Any:
            if isinstance(obj, list):
                nulled_list = []
                for key, value in enumerate(obj):
                    value = separate_files(f"{path}.{key}", value)
                    nulled_list.append(value)
                return nulled_list

            elif isinstance(obj, dict):
                nulled_dict = {}
                for key, value in obj.items():
                    value = separate_files(f"{path}.{key}", value)
                    nulled_dict[key] = value
                return nulled_dict

            elif isinstance(obj, IOBase):
                files[path] = obj
                return None

            else:
                return obj

        nulled_variables = separate_files("variables", variables)
        return nulled_variables, files

    @classmethod
    def prepare_multipart(
        cls, query: str, variables: dict, files: dict, operation: str = None
    ) -> aiohttp.FormData:
        form_data = aiohttp.FormData()
        operations = cls.prepare_json_data(query, variables, operation)

        file_map = {str(i): [path] for i, path in enumerate(files)}
        file_streams = {str(i): files[path] for i, path in enumerate(files)}

        form_data.add_field(
            "operations", json.dumps(operations), content_type="application/json"
        )
        form_data.add_field(
            "map", json.dumps(file_map), content_type="application/json"
        )
        form_data.add_fields(*file_streams.items())

        return form_data

    @classmethod
    def prepare_json_data(
        cls, query: str, variables: dict = None, operation: str = None
    ) -> dict:
        data = {"query": query}
        if variables:
            data["variables"] = variables
        if operation:
            data["operationName"] = operation
        return data
