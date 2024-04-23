import pytest
from sqlalchemy.orm import Session



@pytest.fixture
def session():
    mock_session = Session()
    mock_session.commit = lambda: None
    mock_session.rollback = lambda: None
    mock_session.close = lambda: None
    return mock_session



