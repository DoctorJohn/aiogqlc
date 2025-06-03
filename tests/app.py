import asyncio
from io import BytesIO
from typing import Any, AsyncGenerator, List, TypedDict, Union

import strawberry
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView
from strawberry.file_uploads import Upload
from strawberry.types import Info


class CustomContext(TypedDict):
    request: web.Request
    response: Union[web.Response, web.WebSocketResponse]


@strawberry.type
class User:
    id: strawberry.ID
    name: str


@strawberry.type
class Todo:
    id: strawberry.ID
    title: str
    priority: int
    creator: User


@strawberry.input
class DocumentInput:
    file: BytesIO
    title: str


@strawberry.type
class Document:
    title: str
    length: int


users = [
    User(id=strawberry.ID("0"), name="Amelia"),
    User(id=strawberry.ID("1"), name="Bill"),
    User(id=strawberry.ID("2"), name="Clara"),
]

todos = [
    Todo(id=strawberry.ID("0"), title="Clean kitchen", priority=0, creator=users[0]),
    Todo(id=strawberry.ID("1"), title="Buy groceries", priority=1, creator=users[1]),
    Todo(id=strawberry.ID("2"), title="Stay hydrated", priority=2, creator=users[2]),
]


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[User]:
        return users

    @strawberry.field
    def user(self, id: strawberry.ID) -> User:
        return users[int(id)]

    @strawberry.field
    def todos(self) -> List[Todo]:
        return todos

    @strawberry.field
    def todo(self, id: strawberry.ID) -> Todo:
        return todos[int(id)]

    @strawberry.field
    def authorization_header(self, info: Info) -> str:
        return info.context["request"].headers["Authorization"]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def read_file(self, file: BytesIO) -> str:
        return file.read().decode()

    @strawberry.mutation
    def read_files(self, files: List[BytesIO]) -> List[str]:
        contents = []
        for file in files:
            content = file.read().decode()
            contents.append(content)

            # If the list contains the same file multiple times, the read cursor needs
            # to be reset to enable the file to be read again.
            file.seek(0)
        return contents

    @strawberry.mutation
    def read_document(self, document: DocumentInput) -> Document:
        length = len(document.file.read().decode())
        return Document(title=document.title, length=length)

    @strawberry.mutation
    def fake_user(self, id: strawberry.ID, name: str) -> User:
        return User(id=id, name=name)

    @strawberry.mutation
    def fake_todo(
        self, id: strawberry.ID, title: str, priority: int, creator: strawberry.ID
    ) -> Todo:
        return Todo(id=id, title=title, priority=priority, creator=users[int(creator)])


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, to: int, interval: float = 0) -> AsyncGenerator[int, None]:
        for i in range(to):
            yield i + 1
            await asyncio.sleep(interval)

    @strawberry.subscription
    async def infinity(self, interval: float = 1) -> AsyncGenerator[str, None]:
        yield "For ever"
        while True:
            await asyncio.sleep(interval)
            yield "and ever..."

    @strawberry.subscription
    async def todo_added(self) -> AsyncGenerator[Todo, None]:
        yield todos[0]

    @strawberry.subscription
    async def binary_message(
        self, info: Info[CustomContext, None]
    ) -> AsyncGenerator[int, None]:
        ws = info.context["response"]
        assert isinstance(ws, web.WebSocketResponse)
        yield 1
        await ws.send_bytes(b"\n\0")
        yield 2

    @strawberry.subscription
    async def message_without_id(
        self, info: Info[CustomContext, None]
    ) -> AsyncGenerator[int, None]:
        ws = info.context["response"]
        assert isinstance(ws, web.WebSocketResponse)
        yield 1
        await ws.send_json({"type": "message-without-id"})
        yield 2

    @strawberry.subscription
    async def message_with_invalid_type(
        self, info: Info[CustomContext, None]
    ) -> AsyncGenerator[int, None]:
        ws = info.context["response"]
        assert isinstance(ws, web.WebSocketResponse)

        yield 1
        await ws.send_json({"type": "invalid-type", "id": "1"})
        yield 2


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    scalar_overrides={BytesIO: Upload},
)


def create_app(**kwargs: Any):
    view = GraphQLView(schema=schema, multipart_uploads_enabled=True, **kwargs)
    app = web.Application()
    app.router.add_route("*", "/graphql", view)
    return app
