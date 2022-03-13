# Migrating

## From 2.x.x to 3.x.x

Support for Python 3.6 was dropped because it reached it's end of life.
Migrate by making sure you use a newer Python version.

## From 1.x.x to 2.x.x

The `GraphQLClient` constructor and how the client is used changed.
`GraphQLClient` does not longer create it's own aiohttp client session.
Instead, it takes a pre-configured sessions as an argument.

=== "1.x.x"

    ```Python
    from aiogqlc import GraphQLClient

    endpoint = "https://example.com/graphql/"
    headers = {}
    cookies = {}

    async with GraphQLClient(endpoint, headers=headers, cookies=cookies) as client:
        response = await client.execute(document)
    ```

=== "2.x.x"

    ```python
    from aiogqlc import GraphQLClient
    from aiohttp import ClientSession

    endpoint = "https://example.com/graphql/"
    headers = {}
    cookies = {}

    async with ClientSession(headers=headers, cookies=cookies) as session:
        client = GraphQLClient(endpoint, session=session)
        response = await client.execute(document)
    ```
