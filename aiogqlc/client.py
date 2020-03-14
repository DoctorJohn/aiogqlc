import aiohttp
import json
from typing import Tuple
from aiogqlc.utils import is_file_like, is_file_list_like, contains_file_variable, null_file_variables


class GraphQLClient:
    def __init__(self, endpoint: str, headers: dict = None) -> None:
        self.endpoint = endpoint
        self.headers = headers or {}

    def prepare_headers(self):
        headers = self.headers
        if aiohttp.hdrs.ACCEPT not in headers:
            headers[aiohttp.hdrs.ACCEPT] = 'application/json'
        return headers

    @classmethod
    def prepare_json_data(cls, query: str, variables: dict = None, operation: str = None) -> dict:
        data = {'query': query}
        if variables:
            data['variables'] = null_file_variables(variables)
        if operation:
            data['operationName'] = operation
        return data

    @classmethod
    def prepare_files(cls, variables: dict) -> Tuple[dict, list]:
        file_map = dict()
        file_fields = list()
        map_index = 0
        for key, value in variables.items():
            if is_file_like(value):
                file_map[str(map_index)] = ['variables.{}'.format(key)]
                file_fields.append([str(map_index), value])
                map_index += 1
            elif is_file_list_like(value):
                file_list_index = 0
                for item in value:
                    file_map[str(map_index)] = ['variables.{}.{}'.format(key, file_list_index)]
                    file_fields.append([str(map_index), item])
                    file_list_index += 1
                    map_index += 1
        return file_map, file_fields

    @classmethod
    def prepare_multipart(cls, query: str, variables: dict, operation: str = None) -> aiohttp.FormData:
        data = aiohttp.FormData()
        operations_json = json.dumps(cls.prepare_json_data(query, variables, operation))
        file_map, file_fields = cls.prepare_files(variables)
        data.add_field('operations', operations_json, content_type='application/json')
        data.add_field('map', json.dumps(file_map), content_type='application/json')
        data.add_fields(*file_fields)
        return data

    async def execute(self, query: str, variables: dict = None, operation: str = None) -> aiohttp.ClientResponse:
        async with aiohttp.ClientSession() as session:
            if variables and contains_file_variable(variables):
                data = self.prepare_multipart(query, variables, operation)
                headers = self.prepare_headers()
            else:
                data = json.dumps(self.prepare_json_data(query, variables, operation))
                headers = self.prepare_headers()
                headers[aiohttp.hdrs.CONTENT_TYPE] = 'application/json'
            async with session.post(self.endpoint, data=data, headers=headers) as response:
                await response.json()
                return response
