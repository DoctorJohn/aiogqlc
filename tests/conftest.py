import pytest
from tests.app import create_app


@pytest.fixture
def graphql_session(event_loop, aiohttp_client):
    app = create_app()
    event_loop.set_debug(True)
    return event_loop.run_until_complete(aiohttp_client(app))
