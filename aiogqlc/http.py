import json
from io import IOBase
from typing import Any, Dict, List, Optional, Tuple

import aiohttp
import aiohttp.client
from aiogqlc.utils import serialize_payload


class GraphQLHTTPManager:
    def __init__(
        self,
        endpoint: str,
        session: aiohttp.ClientSession,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation: Optional[str] = None,
    ) -> None:
        self._endpoint = endpoint
        self._session = session
        self._query = query
        self._variables = variables
        self._operation = operation
        self._context: aiohttp.client._RequestContextManager

    async def __aenter__(self) -> aiohttp.ClientResponse:
        nulled_variables, files_to_paths_mapping = self.prepare(self._variables)
        data_param: Dict[str, Any]

        if files_to_paths_mapping:
            form_data = self.prepare_multipart(
                self._query, nulled_variables, files_to_paths_mapping, self._operation
            )
            data_param = {"data": form_data}
        else:
            json_data = serialize_payload(self._query, self._variables, self._operation)
            data_param = {"json": json_data}

        self._context = self._session.post(self._endpoint, **data_param)
        return await self._context.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._context.__aexit__(exc_type, exc_val, exc_tb)

    @classmethod
    def prepare(
        cls, variables: Optional[Dict[str, Any]]
    ) -> Tuple[dict, Dict[IOBase, List[str]]]:
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
        variables: Dict[str, Any],
        files_to_paths_mapping: Dict[IOBase, List[str]],
        operation: Optional[str] = None,
    ) -> aiohttp.FormData:
        form_data = aiohttp.FormData()
        operations = serialize_payload(query, variables, operation)

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
