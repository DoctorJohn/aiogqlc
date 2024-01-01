class GraphQLWSError(Exception):
    pass


class GraphQLWSConnectionError(GraphQLWSError):
    def __init__(self, payload: object):
        self.payload = payload
        super().__init__(payload)


class GraphQLWSProtocolError(GraphQLWSConnectionError):
    pass


class GraphQLWSOperationError(GraphQLWSConnectionError):
    pass
