import aiohttp
import json
from typing import Tuple
from aiogqlc.utils import is_file_like


class GraphQLClient:
    def __init__(self, endpoint: str, session: aiohttp.ClientSession) -> None:
        self.endpoint = endpoint
        self.session = session

    @classmethod
    def prepare_json_data(
        cls, query: str, variables: dict = None, operation: str = None
    ) -> dict:
        '''
        variables must be serializable; in particular,
        it should have already been run through prepare() in case
        it had filestreams in it.
        '''
        data = {'query': query}
        if variables:
            data['variables'] = variables
        if operation:
            data['operationName'] = operation
        return data

    @classmethod
    def prepare(cls, variables: dict) -> Tuple[dict, dict, list]:
        files = {}

        def extract_files(path, obj):
            '''
            recursively traverse obj, doing a deepcopy, but
            replacing any file-like objects with nulls and
            shunting the originals off to the side.
            '''
            nonlocal files
            if type(obj) is list:
                nulled_obj = []
                for key, value in enumerate(obj):
                    value = extract_files(f'{path}.{key}', value)
                    nulled_obj.append(value)
                # TODO: merge this with dict case below. somehow.
                return nulled_obj
            elif type(obj) is dict:
                nulled_obj = {}
                for key, value in obj.items():
                    value = extract_files(f'{path}.{key}', value)
                    nulled_obj[key] = value
                return nulled_obj
            elif is_file_like(obj):
                # extract obj from its parent and put it into files instead.
                files[path] = obj
                return None
            else:
                # base case: pass through unchanged
                return obj

        nulled_variables = extract_files('variables', variables)

        return nulled_variables, files

    @classmethod
    def prepare_multipart(
        cls, query: str, variables: dict, files: dict, operation: str = None
    ) -> aiohttp.FormData:
        data = aiohttp.FormData()
        operations_json = json.dumps(cls.prepare_json_data(query, variables, operation))

        # separate files[path]=stream into two parts: a header and the content, with.
        # an extra ID -- the *index* of the file in the *ordered* dict -- to link them.
        # (the reason the spec adds the extra indirection is to allow multiple pointers
        # to the same file. To save bandwidth):
        file_map = {str(i): [path] for i, path in enumerate(files)}  # header
        # path is nested in a list because the spec allows multiple pointers to the same file.
        # But we don't use that.
        file_streams = {str(i): files[path] for i, path in enumerate(files)}  # payload

        data.add_field('operations', operations_json, content_type='application/json')
        data.add_field('map', json.dumps(file_map), content_type='application/json')
        data.add_fields(*file_streams.items())
        return data

    async def execute(
        self, query: str, variables: dict = None, operation: str = None
    ) -> aiohttp.ClientResponse:
        nulled_variables, files = self.prepare(variables)

        if files:
            # file-uploading extension case:
            # send the query as JSON inside the first multipart form upload
            # followed by a header for the files, then the files themselves.
            data = self.prepare_multipart(query, nulled_variables, files, operation)
            data_param = {'data': data}
        else:
            # normal GraphQL case: just send the query as JSON.
            # nulled_variables should == variables here
            data = self.prepare_json_data(query, variables, operation)
            data_param = {'json': data}

        async with self.session.post(self.endpoint, **data_param) as response:
            await response.read()
            return response
