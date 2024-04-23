import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession
from src.infrastructure.postgresql.util.PsqlConstant import *


PSQL_URL = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(PSQL_USER, PSQL_PASSWORD, PSQL_HOST, PSQL_PORT, PSQL_DB)
ASYNC_PSQL_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(PSQL_USER, PSQL_PASSWORD, PSQL_HOST, PSQL_PORT, PSQL_DB)

ENGINE = create_engine(PSQL_URL, echo = False)
ASYNC_ENGINE = create_async_engine(ASYNC_PSQL_URL, echo = False)

def build_session() -> Session:
    session = scoped_session(
        sessionmaker(
            autocommit = False,
            expire_on_commit = False,
            autoflush = True,
            bind = ENGINE
            )
        )
    return session()


# 要調査
def async_scopefunc():
    return f"coroutine-{uuid.uuid4()}"

def build_async_session() -> AsyncSession:
    session = async_scoped_session(
        async_sessionmaker(
            autocommit = False,
            expire_on_commit = False,
            autoflush = True,
            bind = ASYNC_ENGINE,
            class_ = AsyncSession
            ),
        scopefunc=async_scopefunc # 要調査
        )
    return session()