from io import IOBase
from typing import Any, Dict, List, Literal, Mapping, Sequence, TypedDict, Union

from typing_extensions import NotRequired, Required, TypeAlias

VariableValue: TypeAlias = Union[
    str,
    int,
    None,
    float,
    IOBase,
    Sequence["VariableValue"],
    Mapping[str, "VariableValue"],
]

Variables: TypeAlias = Mapping[str, VariableValue]

ConnectionInitParamValue: TypeAlias = Union[
    None,
    str,
    int,
    float,
    Sequence["ConnectionInitParamValue"],
    Mapping[str, "ConnectionInitParamValue"],
]

ConnectionInitParams: TypeAlias = Mapping[str, ConnectionInitParamValue]

FilesToPathsMapping: TypeAlias = Dict[IOBase, List[str]]


class Payload(TypedDict):
    query: Required[str]
    variables: NotRequired[Variables]
    operationName: NotRequired[str]


# graphql-ws protocol types:


class GraphQLWSConnectionInitMessage(TypedDict):
    type: Literal["connection_init"]
    payload: Mapping[str, Any]


class GraphQLWSStartMessage(TypedDict):
    type: Literal["start"]
    id: str
    payload: Payload


class GraphQLWSStopMessage(TypedDict):
    type: Literal["stop"]
    id: str


class GraphQLWSConnectionTerminateMessage(TypedDict):
    type: Literal["connection_terminate"]


GraphQLWSClientOperationMessage: TypeAlias = Union[
    GraphQLWSConnectionInitMessage,
    GraphQLWSStartMessage,
    GraphQLWSStopMessage,
    GraphQLWSConnectionTerminateMessage,
]


class GraphQLWSErrorLocations(TypedDict):
    line: int
    column: int


class GraphQLWSError(TypedDict, total=False):
    message: Required[str]
    locations: NotRequired[List[GraphQLWSErrorLocations]]
    path: NotRequired[List[Union[str, int]]]
    extensions: NotRequired[Dict[str, Any]]


class GraphQLWSConnectionErrorMessage(TypedDict):
    type: Literal["connection_error"]
    payload: Dict[str, Any]


class GraphQLWSConnectionAckMessage(TypedDict):
    type: Literal["connection_ack"]


class GraphQLWSDataMessagePayload(TypedDict, total=False):
    data: Required[Any]
    errors: NotRequired[List[GraphQLWSError]]


class GraphQLWSDataMessage(TypedDict):
    type: Literal["data"]
    id: str
    payload: GraphQLWSDataMessagePayload


class GraphQLWSErrorMessage(TypedDict):
    type: Literal["error"]
    id: str
    payload: GraphQLWSError


class GraphQLWSCompleteMessage(TypedDict, total=True):
    type: Literal["complete"]
    id: str


class GraphQLWSConnectionKeepAliveMesssage(TypedDict, total=True):
    type: Literal["ka"]


GraphQLWSServerConnectionOperationMessage: TypeAlias = Union[
    GraphQLWSConnectionErrorMessage,
    GraphQLWSConnectionAckMessage,
    GraphQLWSConnectionKeepAliveMesssage,
]

GraphQLWSServerExecutionOperationMessage: TypeAlias = Union[
    GraphQLWSDataMessage,
    GraphQLWSErrorMessage,
    GraphQLWSCompleteMessage,
]

GraphQLWSServerOperationMessage: TypeAlias = Union[
    GraphQLWSServerConnectionOperationMessage,
    GraphQLWSServerExecutionOperationMessage,
]
