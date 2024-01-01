import typing

from aiogqlc.types import Payload, Variables


def serialize_payload(
    query: str,
    variables: typing.Optional[Variables] = None,
    operation: typing.Optional[str] = None,
) -> Payload:
    data: Payload = {"query": query}
    if variables:
        data["variables"] = variables
    if operation:
        data["operationName"] = operation
    return data
