import pytest
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.postgresql.util.PsqlSessionBuilder import build_session


@pytest.fixture
def rdb() -> RdbSessionClient:
    return RdbSessionClient(session = build_session())