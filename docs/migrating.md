# Migrating

## From 4.x.x to 5.x.x

The connection initialization parameters of the legacy `graphql-ws`
protocol now default to an empty JSON object `{}` instead of `null`.
This is to be more aligned with the reference implementation.

Furthermore, various constants have been removed from `aiogqlc.constants`.
They were not considered part of the public API, but in case you used them,
you might need to update your code.

## From 3.x.x to 4.x.x

Support for Python 3.7 was dropped because it reached its end of life.
Migrate by making sure you use a newer Python version.

## From 2.x.x to 3.x.x

Support for Python 3.6 was dropped because it reached its end of life.
Migrate by making sure you use a newer Python version.

## From 1.x.x to 2.x.x

The `GraphQLClient` constructor and how the client is used changed.
`GraphQLClient` does not longer create its own aiohttp client session.
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
