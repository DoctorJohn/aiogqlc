import asyncio
import json
from io import IOBase
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple

import aiohttp
import aiohttp.client
from aiogqlc.constants import (
    GQL_COMPLETE,
    GQL_CONNECTION_ACK,
    GQL_CONNECTION_ERROR,
    GQL_CONNECTION_INIT,
    GQL_CONNECTION_KEEP_ALIVE,
    GQL_CONNECTION_TERMINATE,
    GQL_DATA,
    GQL_ERROR,
    GQL_START,
    GQL_STOP,
    GRAPHQL_WS,
)
from aiogqlc.errors import (
    GraphQLWSConnectionError,
    GraphQLWSOperationError,
    GraphQLWSProtocolError,
)
from aiogqlc.utils import serialize_payload


class GraphQLWSManager:
    def __init__(
        self,
        endpoint: str,
        session: aiohttp.ClientSession,
        connection_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._endpoint = endpoint
        self._session = session
        self._connection_params = connection_params
        self._last_operation_id = 0
        self._ws_context: aiohttp.client._WSRequestContextManager
        self._ws: aiohttp.ClientWebSocketResponse
        self._operations_message_queues: Dict[str, asyncio.Queue] = {}
        self._connection_handler_task: asyncio.Task

    async def __aenter__(self) -> "GraphQLWSManager":
        self._ws_context = self._session.ws_connect(
            self._endpoint, protocols=[GRAPHQL_WS]
        )
        self._ws = await self._ws_context.__aenter__()
        await self.init_connection(self._connection_params)
        self._connection_handler_task = asyncio.create_task(self.handle_connection())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.terminate_connection()
        await self._connection_handler_task
        await self._ws_context.__aexit__(exc_type, exc_val, exc_tb)

    async def subscribe(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation: Optional[str] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        operation_id = self.get_next_operation_id()
        self._operations_message_queues[operation_id] = asyncio.Queue()

        await self.start_operation(operation_id, query, variables, operation)
        operation_handler = self.handle_operation(operation_id)

        try:
            while True:
                payload = await operation_handler.__anext__()
                yield payload
        except StopAsyncIteration:
            await self.stop_operation(operation_id)
        except GraphQLWSOperationError as exc:
            raise exc

    def get_next_operation_id(self) -> str:
        self._last_operation_id += 1
        return str(self._last_operation_id)

    async def init_connection(self, params: Optional[Dict[str, Any]]) -> None:
        await self._ws.send_json({"type": GQL_CONNECTION_INIT, "payload": params})
        message = await self._ws.receive_json()

        if message["type"] == GQL_CONNECTION_ACK:
            return
        elif message["type"] == GQL_CONNECTION_ERROR:
            raise GraphQLWSConnectionError(message.get("payload"))
        else:
            raise GraphQLWSProtocolError(message.get("payload"))

    async def start_operation(
        self,
        operation_id: str,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation: Optional[str] = None,
    ) -> None:
        payload = serialize_payload(query, variables, operation)
        await self._ws.send_json(
            {
                "type": GQL_START,
                "id": operation_id,
                "payload": payload,
            }
        )

    async def handle_connection(self) -> None:
        async for message in self._ws:  # type: aiohttp.WSMessage
            if message.type != aiohttp.WSMsgType.TEXT:
                continue

            operation_message = message.json()

            if operation_message.get("type") == GQL_CONNECTION_KEEP_ALIVE:
                continue

            if "id" in operation_message:
                self.yield_operation_message(operation_message)
                continue

    async def handle_operation(
        self, operation_id: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        while True:
            operation_message = await self._operations_message_queues[
                operation_id
            ].get()
            payload = operation_message.get("payload")

            if operation_message["type"] == GQL_DATA:
                yield payload
                continue

            if operation_message["type"] == GQL_ERROR:
                raise GraphQLWSOperationError(payload)

            if operation_message["type"] == GQL_COMPLETE:
                return

    def yield_operation_message(self, operation_message: dict) -> None:
        operation_id = operation_message["id"]
        self._operations_message_queues[operation_id].put_nowait(operation_message)

    async def stop_operation(self, operation_id: str) -> None:
        await self._ws.send_json({"type": GQL_STOP, "id": operation_id})

    async def terminate_connection(self) -> None:
        await self._ws.send_json({"type": GQL_CONNECTION_TERMINATE})


class GraphQLClient:
    def __init__(self, endpoint: str, session: aiohttp.ClientSession) -> None:
        self.endpoint = endpoint
        self.session = session

    def connect(
        self, protocol: str = GRAPHQL_WS, params: Optional[Dict[str, Any]] = None
    ) -> GraphQLWSManager:
        if protocol == GRAPHQL_WS:
            return GraphQLWSManager(self.endpoint, self.session, params)
        raise ValueError(protocol)

    async def execute(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation: Optional[str] = None,
    ) -> aiohttp.ClientResponse:
        nulled_variables, files_to_paths_mapping = self.prepare(variables)
        data_param: Dict[str, Any]

        if files_to_paths_mapping:
            form_data = self.prepare_multipart(
                query, nulled_variables, files_to_paths_mapping, operation
            )
            data_param = {"data": form_data}
        else:
            json_data = serialize_payload(query, variables, operation)
            data_param = {"json": json_data}

        async with self.session.post(self.endpoint, **data_param) as response:
            await response.read()
            return response

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
