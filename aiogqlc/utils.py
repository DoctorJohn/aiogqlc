from typing import Optional

from aiogqlc.types import Payload, Variables


def serialize_payload(
    query: str,
    variables: Optional[Variables] = None,
    operation: Optional[str] = None,
) -> Payload:
    data: Payload = {"query": query}
    if variables:
        data["variables"] = variables
    if operation:
        data["operationName"] = operation
    return data
