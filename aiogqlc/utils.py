def serialize_payload(
    query: str, variables: dict = None, operation: str = None
) -> dict:
    data = {"query": query}
    if variables:
        data["variables"] = variables
    if operation:
        data["operationName"] = operation
    return data
