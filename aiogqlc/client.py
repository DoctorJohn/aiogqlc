import asyncio
import json
from io import IOBase
from types import TracebackType
from typing import (
    AsyncContextManager,
    AsyncGenerator,
    Dict,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    Union,
)

import aiohttp
import aiohttp.client
import aiohttp.test_utils

from aiogqlc.constants import GRAPHQL_WS
from aiogqlc.errors import (
    GraphQLWSConnectionError,
    GraphQLWSOperationError,
    GraphQLWSProtocolError,
)
from aiogqlc.types import (
    ConnectionInitParams,
    FilesToPathsMapping,
    GraphQLWSConnectionInitMessage,
    GraphQLWSConnectionTerminateMessage,
    GraphQLWSDataMessagePayload,
    GraphQLWSServerConnectionOperationMessage,
    GraphQLWSServerExecutionOperationMessage,
    GraphQLWSServerOperationMessage,
    GraphQLWSStartMessage,
    GraphQLWSStopMessage,
    Payload,
    Variables,
    VariableValue,
)
from aiogqlc.utils import serialize_payload


class GraphQLWSManager:
    def __init__(
        self,
        endpoint: str,
        session: Union[aiohttp.ClientSession, aiohttp.test_utils.TestClient],
        connection_params: Optional[ConnectionInitParams] = None,
    ) -> None:
        self._endpoint = endpoint
        self._session = session
        self._connection_params = connection_params
        self._last_operation_id = 0
        self._ws_context: AsyncContextManager[aiohttp.ClientWebSocketResponse]
        self._ws: aiohttp.ClientWebSocketResponse
        self._operations_message_queues: Dict[
            str, asyncio.Queue[GraphQLWSServerOperationMessage]
        ] = {}
        self._connection_handler_task: asyncio.Task[None]

    async def __aenter__(self) -> "GraphQLWSManager":
        self._ws_context = self._session.ws_connect(
            self._endpoint, protocols=[GRAPHQL_WS]
        )
        self._ws = await self._ws_context.__aenter__()
        await self.init_connection(self._connection_params)
        self._connection_handler_task = asyncio.create_task(self.handle_connection())
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.terminate_connection()
        await self._connection_handler_task
        await self._ws_context.__aexit__(exc_type, exc_val, exc_tb)

    async def subscribe(
        self,
        query: str,
        variables: Optional[Variables] = None,
        operation: Optional[str] = None,
    ) -> AsyncGenerator[GraphQLWSDataMessagePayload, None]:
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

    async def init_connection(self, params: Optional[ConnectionInitParams]) -> None:
        connection_init_message: GraphQLWSConnectionInitMessage = {
            "type": "connection_init",
            "payload": params or {},
        }
        await self._ws.send_json(connection_init_message)

        message: GraphQLWSServerConnectionOperationMessage = (
            await self._ws.receive_json()
        )

        if message["type"] == "connection_ack":
            return

        if message["type"] == "connection_error":
            raise GraphQLWSConnectionError(message["payload"])

        raise GraphQLWSProtocolError(message.get("payload"))

    async def start_operation(
        self,
        operation_id: str,
        query: str,
        variables: Optional[Variables] = None,
        operation: Optional[str] = None,
    ) -> None:
        payload = serialize_payload(query, variables, operation)
        start_message: GraphQLWSStartMessage = {
            "type": "start",
            "id": operation_id,
            "payload": payload,
        }
        await self._ws.send_json(start_message)

    async def handle_connection(self) -> None:
        async for ws_message in self._ws:
            if ws_message.type != aiohttp.WSMsgType.TEXT:
                continue

            message: GraphQLWSServerOperationMessage = ws_message.json()

            if message["type"] == "ka":
                continue

            if (
                message["type"] == "data"
                or message["type"] == "error"
                or message["type"] == "complete"
            ):
                self.yield_operation_message(message)
                continue

    async def handle_operation(
        self, operation_id: str
    ) -> AsyncGenerator[GraphQLWSDataMessagePayload, None]:
        while True:
            operation_message = await self._operations_message_queues[
                operation_id
            ].get()

            if operation_message["type"] == "data":
                yield operation_message["payload"]
                continue

            if operation_message["type"] == "error":
                raise GraphQLWSOperationError(operation_message["payload"])

            if operation_message["type"] == "complete":
                return

    def yield_operation_message(
        self, operation_message: GraphQLWSServerExecutionOperationMessage
    ) -> None:
        operation_id = operation_message["id"]
        self._operations_message_queues[operation_id].put_nowait(operation_message)

    async def stop_operation(self, operation_id: str) -> None:
        stop_message: GraphQLWSStopMessage = {
            "type": "stop",
            "id": operation_id,
        }
        await self._ws.send_json(stop_message)

    async def terminate_connection(self) -> None:
        terminate_message: GraphQLWSConnectionTerminateMessage = {
            "type": "connection_terminate"
        }
        await self._ws.send_json(terminate_message)


class GraphQLClient:
    def __init__(
        self,
        endpoint: str,
        session: Union[aiohttp.ClientSession, aiohttp.test_utils.TestClient],
    ) -> None:
        self.endpoint = endpoint
        self.session = session

    def connect(
        self, protocol: str = GRAPHQL_WS, params: Optional[ConnectionInitParams] = None
    ) -> GraphQLWSManager:
        if protocol == GRAPHQL_WS:
            return GraphQLWSManager(self.endpoint, self.session, params)
        raise ValueError(protocol)

    async def execute(
        self,
        query: str,
        variables: Optional[Variables] = None,
        operation: Optional[str] = None,
        **kwargs: Mapping[str, object],
    ) -> aiohttp.ClientResponse:
        nulled_variables, files_to_paths_mapping = self.prepare(variables)
        data_param: Dict[str, Union[aiohttp.FormData, Payload]]

        if files_to_paths_mapping:
            form_data = self.prepare_multipart(
                query=query,
                nulled_variables=nulled_variables,
                files_to_paths_mapping=files_to_paths_mapping,
                operation=operation,
            )
            data_param = {"data": form_data}
        else:
            json_data = serialize_payload(query, variables, operation)
            data_param = {"json": json_data}

        async with self.session.post(self.endpoint, **kwargs, **data_param) as response:
            await response.read()
            return response

    @classmethod
    def prepare(
        cls, variables: Optional[Variables]
    ) -> Tuple[Optional[Variables], FilesToPathsMapping]:
        files_to_paths_mapping: FilesToPathsMapping = {}

        def separate_files(path: str, obj: VariableValue) -> VariableValue:
            if isinstance(obj, list):
                nulled_list: List[VariableValue] = []
                for index, value in enumerate(obj):
                    value = separate_files(f"{path}.{index}", value)
                    nulled_list.append(value)
                return nulled_list

            elif isinstance(obj, dict):
                nulled_dict: Dict[str, VariableValue] = {}
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

        if variables is None:
            return None, files_to_paths_mapping

        nulled_variables: Variables = dict(
            (key, separate_files(f"variables.{key}", value))
            for key, value in variables.items()
        )

        return nulled_variables, files_to_paths_mapping

    @classmethod
    def prepare_multipart(
        cls,
        query: str,
        nulled_variables: Optional[Variables],
        files_to_paths_mapping: FilesToPathsMapping,
        operation: Optional[str] = None,
    ) -> aiohttp.FormData:
        form_data = aiohttp.FormData()
        operations = serialize_payload(query, nulled_variables, operation)

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
