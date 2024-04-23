from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgresql.util.PsqlSessionBuilder import build_session, build_async_session



def test_build_session():
    session = build_session()
    assert isinstance(session, Session)


def test_build_async_session():
    session = build_async_session()
    assert isinstance(session, AsyncSession)

