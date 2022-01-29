from typing import Any, Dict, Optional

import aiohttp.client
from aiogqlc.constants import GRAPHQL_WS
from aiogqlc.http import GraphQLHTTPManager
from aiogqlc.ws import GraphQLWSManager


class GraphQLClient:
    def __init__(self, endpoint: str, session: aiohttp.ClientSession) -> None:
        self.endpoint = endpoint
        self.session = session

    def connect(
        self,
        protocol: str = GRAPHQL_WS,
        connection_params: Optional[Dict[str, Any]] = None,
    ) -> GraphQLWSManager:
        if protocol == GRAPHQL_WS:
            return GraphQLWSManager(
                endpoint=self.endpoint,
                session=self.session,
                connection_params=connection_params,
            )
        raise ValueError(protocol)

    def execute(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation: Optional[str] = None,
    ) -> GraphQLHTTPManager:
        return GraphQLHTTPManager(
            endpoint=self.endpoint,
            session=self.session,
            query=query,
            variables=variables,
            operation=operation,
        )
