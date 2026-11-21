from aiogqlc.types import Payload, Variables


def serialize_payload(
    query: str,
    variables: Variables | None = None,
    operation: str | None = None,
) -> Payload:
    data: Payload = {"query": query}
    if variables:
        data["variables"] = variables
    if operation:
        data["operationName"] = operation
    return data
