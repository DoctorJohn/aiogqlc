import json
from io import IOBase
from typing import Any, Dict, List, Tuple

import aiohttp


class GraphQLClient:
    def __init__(self, endpoint: str, session: aiohttp.ClientSession) -> None:
        self.endpoint = endpoint
        self.session = session

    async def execute(
        self, query: str, variables: dict = None, operation: str = None
    ) -> aiohttp.ClientResponse:
        nulled_variables, files_to_paths_mapping = self.prepare(variables)

        if files_to_paths_mapping:
            data = self.prepare_multipart(
                query, nulled_variables, files_to_paths_mapping, operation
            )
            data_param = {"data": data}
        else:
            data = self.prepare_json_data(query, variables, operation)
            data_param = {"json": data}

        async with self.session.post(self.endpoint, **data_param) as response:
            await response.read()
            return response

    @classmethod
    def prepare(cls, variables: dict) -> Tuple[dict, Dict[IOBase, List[str]]]:
        files_to_paths_mapping: Dict[IOBase, List[str]] = {}

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
                if obj in files_to_paths_mapping:
                    files_to_paths_mapping[obj].append(path)
                else:
                    files_to_paths_mapping[obj] = [path]
                return None

            else:
                return obj

        nulled_variables = separate_files("variables", variables)
        return nulled_variables, files_to_paths_mapping

    @classmethod
    def prepare_multipart(
        cls,
        query: str,
        variables: dict,
        files_to_paths_mapping: Dict[IOBase, List[str]],
        operation: str = None,
    ) -> aiohttp.FormData:
        form_data = aiohttp.FormData()
        operations = cls.prepare_json_data(query, variables, operation)

        file_map = {
            str(i): files_to_paths_mapping[file]
            for i, file in enumerate(files_to_paths_mapping)
        }
        file_streams = {str(i): file for i, file in enumerate(files_to_paths_mapping)}

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
