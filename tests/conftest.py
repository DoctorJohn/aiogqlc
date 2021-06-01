import pytest
from tests.app import create_app


@pytest.fixture
def graphql_session(loop, aiohttp_client):
    app = create_app()
    loop.set_debug(True)
    return loop.run_until_complete(aiohttp_client(app))
