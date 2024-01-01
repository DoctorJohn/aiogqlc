import typing
from io import IOBase

from typing_extensions import NotRequired, Required, TypeAlias

VariableValue: TypeAlias = typing.Union[
    str,
    int,
    None,
    float,
    IOBase,
    typing.List["VariableValue"],
    typing.Dict[str, "VariableValue"],
]

Variables: TypeAlias = typing.Dict[str, VariableValue]

FilesToPathsMapping: TypeAlias = typing.Dict[IOBase, typing.List[str]]

ConnectionInitParamValue: TypeAlias = typing.Union[
    None,
    str,
    int,
    float,
    typing.List["ConnectionInitParamValue"],
    typing.Dict[str, "ConnectionInitParamValue"],
]

ConnectionInitParams: TypeAlias = typing.Dict[str, ConnectionInitParamValue]


class Payload(typing.TypedDict):
    query: Required[str]
    variables: NotRequired[Variables]
    operationName: NotRequired[str]


# graphql-ws protocol types:


class GraphQLWSConnectionInitMessage(typing.TypedDict):
    type: typing.Literal["connection_init"]
    payload: typing.Dict[str, typing.Any]


class GraphQLWSStartMessage(typing.TypedDict):
    type: typing.Literal["start"]
    id: str
    payload: Payload


class GraphQLWSStopMessage(typing.TypedDict):
    type: typing.Literal["stop"]
    id: str


class GraphQLWSConnectionTerminateMessage(typing.TypedDict):
    type: typing.Literal["connection_terminate"]


GraphQLWSClientOperationMessage: TypeAlias = typing.Union[
    GraphQLWSConnectionInitMessage,
    GraphQLWSStartMessage,
    GraphQLWSStopMessage,
    GraphQLWSConnectionTerminateMessage,
]


class GraphQLWSErrorLocations(typing.TypedDict):
    line: int
    column: int


class GraphQLWSError(typing.TypedDict, total=False):
    message: typing.Required[str]
    locations: typing.NotRequired[typing.List[GraphQLWSErrorLocations]]
    path: typing.NotRequired[typing.List[typing.Union[str, int]]]
    extensions: typing.NotRequired[typing.Dict[str, typing.Any]]


class GraphQLWSConnectionErrorMessage(typing.TypedDict):
    type: typing.Literal["connection_error"]
    payload: typing.Dict[str, typing.Any]


class GraphQLWSConnectionAckMessage(typing.TypedDict):
    type: typing.Literal["connection_ack"]


class GraphQLWSDataMessagePayload(typing.TypedDict, total=False):
    data: Required[typing.Any]
    errors: NotRequired[typing.List[GraphQLWSError]]


class GraphQLWSDataMessage(typing.TypedDict):
    type: typing.Literal["data"]
    id: str
    payload: GraphQLWSDataMessagePayload


class GraphQLWSErrorMessage(typing.TypedDict):
    type: typing.Literal["error"]
    id: str
    payload: GraphQLWSError


class GraphQLWSCompleteMessage(typing.TypedDict, total=True):
    type: typing.Literal["complete"]
    id: str


class GraphQLWSConnectionKeepAliveMesssage(typing.TypedDict, total=True):
    type: typing.Literal["ka"]


GraphQLWSServerConnectionOperationMessage: TypeAlias = typing.Union[
    GraphQLWSConnectionErrorMessage,
    GraphQLWSConnectionAckMessage,
    GraphQLWSConnectionKeepAliveMesssage,
]

GraphQLWSServerExecutionOperationMessage: TypeAlias = typing.Union[
    GraphQLWSDataMessage,
    GraphQLWSErrorMessage,
    GraphQLWSCompleteMessage,
]

GraphQLWSServerOperationMessage: TypeAlias = typing.Union[
    GraphQLWSServerConnectionOperationMessage,
    GraphQLWSServerExecutionOperationMessage,
]
