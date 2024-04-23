from sqlalchemy.orm import Session
from src.infrastructure.postgresql.util.PsqlSessionBuilder import build_session

def test_build_session():
    session = build_session()
    assert isinstance(session, Session)

