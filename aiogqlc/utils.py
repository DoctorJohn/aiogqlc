from typing import Any, Dict, Optional


def serialize_payload(
    query: str,
    variables: Optional[Dict[str, Any]] = None,
    operation: Optional[str] = None,
) -> dict:
    data: Dict[str, Any] = {"query": query}
    if variables:
        data["variables"] = variables
    if operation:
        data["operationName"] = operation
    return data
