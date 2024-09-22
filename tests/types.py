from typing import Any, Awaitable, Protocol

from aiohttp import web
from aiohttp.test_utils import TestClient


class AiohttpClient(Protocol):
    def __call__(
        self, app: web.Application, **kwargs: Any
    ) -> Awaitable[TestClient]: ...
