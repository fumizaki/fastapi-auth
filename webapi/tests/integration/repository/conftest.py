import pytest
from src.infrastructure.core.rdb.AsyncRdbSessionClient import AsyncRdbSessionClient
from src.infrastructure.postgresql.util.PsqlSessionBuilder import build_async_session


@pytest.fixture
def rdb() -> AsyncRdbSessionClient:
    return AsyncRdbSessionClient(session = build_async_session())