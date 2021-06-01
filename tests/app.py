import typing

import strawberry
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView
from strawberry.file_uploads import Upload


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
    def users(self) -> typing.List[User]:
        return users

    @strawberry.field
    def user(self, id: strawberry.ID) -> User:
        return users[int(id)]

    @strawberry.field
    def todos(self) -> typing.List[Todo]:
        return todos

    @strawberry.field
    def todo(self, id: strawberry.ID) -> Todo:
        return todos[int(id)]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def read_file(self, file: Upload) -> str:
        return file.read().decode()

    @strawberry.mutation
    def read_files(self, files: typing.List[Upload]) -> typing.List[str]:
        contents = []
        for file in files:
            content = file.read().decode()
            contents.append(content)

            # If the list contains the same file multiple times, the read cursor needs
            # to be reset to enable the file to be read again.
            file.seek(0)
        return contents

    @strawberry.mutation
    def fake_user(self, id: strawberry.ID, name: str) -> User:
        return User(id=id, name=name)

    @strawberry.mutation
    def fake_todo(
        self, id: strawberry.ID, title: str, priority: int, creator: strawberry.ID
    ) -> Todo:
        return Todo(id=id, title=title, priority=priority, creator=users[int(creator)])


schema = strawberry.Schema(query=Query, mutation=Mutation)


def create_app(**kwargs):
    app = web.Application()
    app.router.add_route("*", "/graphql", GraphQLView(schema=schema, **kwargs))
    return app
