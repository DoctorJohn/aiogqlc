from typing import Any, List

import aiohttp
import pytest
from aiohttp import web
from strawberry.aiohttp.handlers.graphql_ws_handler import GraphQLWSHandler
from strawberry.aiohttp.views import GraphQLView

from aiogqlc import GraphQLClient
from aiogqlc.errors import (
    GraphQLWSConnectionError,
    GraphQLWSOperationError,
    GraphQLWSProtocolError,
)
from tests.app import create_app, schema
from tests.types import AiohttpClient


async def test_choosing_unsupported_protocol(graphql_session: aiohttp.ClientSession):
    client = GraphQLClient(endpoint="/graphql", session=graphql_session)
    unsupported_protocol = "imaginary-protocol"

    with pytest.raises(ValueError) as exc_info:
        client.connect(protocol=unsupported_protocol)

    assert unsupported_protocol in str(exc_info.value)


async def test_server_completed_subscription(graphql_session: aiohttp.ClientSession):
    query = """
        subscription {
            count(to: 3)
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    data: List[int] = []

    async with client.connect() as connection:
        async for payload in connection.subscribe(query):
            data.append(payload["data"]["count"])

    assert data == [1, 2, 3]


async def test_subscribing_nested_fields(graphql_session: aiohttp.ClientSession):
    query = """
        subscription {
            todoAdded {
                id
                title
                priority
                creator {
                    id
                    name
                }
            }
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    async with client.connect() as connection:
        async for payload in connection.subscribe(query):
            assert payload["data"]["todoAdded"] == {
                "id": "0",
                "title": "Clean kitchen",
                "priority": 0,
                "creator": {
                    "id": "0",
                    "name": "Amelia",
                },
            }


async def test_passing_variables(graphql_session: aiohttp.ClientSession):
    query = """
        subscription ($to: Int!) {
            count(to: $to)
        }
    """

    variables = {"to": 3}

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    data: List[int] = []

    async with client.connect() as connection:
        async for payload in connection.subscribe(query, variables=variables):
            data.append(payload["data"]["count"])

    assert data == [1, 2, 3]


async def test_missing_variables(graphql_session: aiohttp.ClientSession):
    query = """
        subscription ($to: Int!) {
            count(to: $to)
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    with pytest.raises(GraphQLWSOperationError) as exc_info:
        async with client.connect() as connection:
            async for _ in connection.subscribe(query):
                assert False, "Unreachable"

    payload = exc_info.value.payload
    expectation = "Variable '$to' of required type 'Int!' was not provided."
    assert isinstance(payload, dict)
    assert payload["message"] == expectation


async def test_operation_selection(graphql_session: aiohttp.ClientSession):
    query = """
        subscription Subscription1 {
            count(to: 1)
        }
        subscription Subscription2 {
            count(to: 2)
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    data: List[int] = []

    async with client.connect() as connection:
        async for payload in connection.subscribe(query, operation="Subscription2"):
            data.append(payload["data"]["count"])

    assert data == [1, 2]


async def test_unknown_operation_selection(graphql_session: aiohttp.ClientSession):
    query = """
        subscription Subscription1 {
            count(to: 1)
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    with pytest.raises(GraphQLWSOperationError) as exc_info:
        async with client.connect() as connection:
            async for _ in connection.subscribe(query, operation="Subscription2"):
                assert False, "Unreachable"

    payload = exc_info.value.payload
    expectation = "Unknown operation named 'Subscription2'."
    assert isinstance(payload, dict)
    assert payload["message"] == expectation


async def test_missing_operation_selection(graphql_session: aiohttp.ClientSession):
    query = """
        subscription Subscription1 {
            count(to: 1)
        }
        subscription Subscription2 {
            count(to: 2)
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    with pytest.raises(GraphQLWSOperationError) as exc_info:
        async with client.connect() as connection:
            async for _ in connection.subscribe(query):
                assert False, "Unreachable"

    payload = exc_info.value.payload
    expectation = "Must provide operation name if query contains multiple operations."
    assert isinstance(payload, dict)
    assert payload["message"] == expectation


async def test_unsubscribing(graphql_session: aiohttp.ClientSession):
    query = """
        subscription {
            count(to: 3)
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    async with client.connect() as connection:
        async for _ in connection.subscribe(query):
            break


async def test_operation_id_counter(graphql_session: aiohttp.ClientSession):
    query = """
        subscription {
            count(to: 3)
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    async with client.connect() as connection:
        async for _ in connection.subscribe(query):
            break
        assert connection._last_operation_id == 1  # pyright: ignore[reportPrivateUsage]

        async for _ in connection.subscribe(query):
            break
        assert connection._last_operation_id == 2  # pyright: ignore[reportPrivateUsage]

    async with client.connect() as connection:
        async for _ in connection.subscribe(query):
            break
        assert connection._last_operation_id == 1  # pyright: ignore[reportPrivateUsage]

        async for _ in connection.subscribe(query):
            break
        assert connection._last_operation_id == 2  # pyright: ignore[reportPrivateUsage]


async def test_sequential_subscriptions_using_one_connection(
    graphql_session: aiohttp.ClientSession,
):
    query = """
        subscription {
            count(to: 3)
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    data1: List[int] = []
    data2: List[int] = []

    async with client.connect() as connection:
        async for payload in connection.subscribe(query):
            data1.append(payload["data"]["count"])

        async for payload in connection.subscribe(query):
            data2.append(payload["data"]["count"])

    assert data1 == [1, 2, 3]
    assert data2 == [1, 2, 3]


async def test_parallel_subscriptions_using_one_connection(
    graphql_session: aiohttp.ClientSession,
):
    query = """
        subscription {
            count(to: 3)
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    data1: List[int] = []
    data2: List[int] = []

    async with client.connect() as connection:
        subscription1 = connection.subscribe(query)
        subscription2 = connection.subscribe(query)

        try:
            while True:
                payload1 = await subscription1.__anext__()
                payload2 = await subscription2.__anext__()
                data1.append(payload1["data"]["count"])
                data2.append(payload2["data"]["count"])
        except StopAsyncIteration:
            pass

    assert data1 == [1, 2, 3]
    assert data2 == [1, 2, 3]


async def test_reusing_a_connection_after_cancelling_a_subscription(
    graphql_session: aiohttp.ClientSession,
):
    query = """
        subscription {
            count(to: 3)
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    data1: List[int] = []
    data2: List[int] = []

    async with client.connect() as connection:
        async for payload in connection.subscribe(query):
            data1.append(payload["data"]["count"])
            break

        async for payload in connection.subscribe(query):
            data2.append(payload["data"]["count"])

    assert data1 == [1]
    assert data2 == [1, 2, 3]


async def test_server_connection_rejection(aiohttp_client: AiohttpClient):
    class ConnectingRejectingHandler(GraphQLWSHandler):
        async def handle_connection_init(self, message: Any) -> None:
            await self.send_json(
                {"type": "connection_error", "payload": {"message": "TEST"}}
            )

    class ConnectionRejectingGraphQLView(GraphQLView[Any, None]):
        graphql_ws_handler_class = ConnectingRejectingHandler

    app = web.Application()
    app.router.add_route("*", "/graphql", ConnectionRejectingGraphQLView(schema=schema))

    graphql_session = await aiohttp_client(app)
    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    with pytest.raises(GraphQLWSConnectionError) as exc_info:
        async with client.connect() as _:
            pass

    payload = exc_info.value.payload
    assert isinstance(payload, dict)
    assert payload["message"] == "TEST"


async def test_server_connection_protocol_violation(aiohttp_client: AiohttpClient):
    class ProtocolViolatingHandler(GraphQLWSHandler):
        async def handle_connection_init(self, message: Any) -> None:
            await self.send_json({"type": "data", "payload": {"data": "TEST"}})

    class ProtocolViolatingGraphQLView(GraphQLView[Any, None]):
        graphql_ws_handler_class = ProtocolViolatingHandler

    app = web.Application()
    app.router.add_route("*", "/graphql", ProtocolViolatingGraphQLView(schema=schema))

    graphql_session = await aiohttp_client(app)
    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    with pytest.raises(GraphQLWSProtocolError):
        async with client.connect() as _:
            pass


async def test_keep_alive_message_handling(aiohttp_client: AiohttpClient):
    app = create_app(keep_alive_interval=0.1)

    graphql_session = await aiohttp_client(app)
    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    query = """
        subscription {
            count(to: 3, interval: 0.1)
        }
    """

    data: List[int] = []

    async with client.connect() as connection:
        async for payload in connection.subscribe(query):
            data.append(payload["data"]["count"])

    assert data == [1, 2, 3]


async def test_client_ignores_non_text_messages(graphql_session: aiohttp.ClientSession):
    query = """
        subscription {
            binaryMessage
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    data: List[int] = []

    async with client.connect() as connection:
        async for payload in connection.subscribe(query):
            data.append(payload["data"]["binaryMessage"])

    assert data == [1, 2]


async def test_client_ignores_messages_without_id(
    graphql_session: aiohttp.ClientSession,
):
    query = """
        subscription {
            messageWithoutId
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    data: List[int] = []

    async with client.connect() as connection:
        async for payload in connection.subscribe(query):
            data.append(payload["data"]["messageWithoutId"])

    assert data == [1, 2]


async def test_client_ignores_messages_with_invalid_type(
    graphql_session: aiohttp.ClientSession,
):
    query = """
        subscription {
            messageWithInvalidType
        }
    """

    client = GraphQLClient(endpoint="/graphql", session=graphql_session)

    data: List[int] = []

    async with client.connect() as connection:
        async for payload in connection.subscribe(query):
            data.append(payload["data"]["messageWithInvalidType"])

    assert data == [1, 2]
