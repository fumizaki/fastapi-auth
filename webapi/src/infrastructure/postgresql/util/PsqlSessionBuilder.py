from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from src.infrastructure.postgresql.util.PsqlConstant import *


PSQL_URL = "postgresql://{}:{}@{}:{}/{}".format(PSQL_USER, PSQL_PASSWORD, PSQL_HOST, PSQL_PORT, PSQL_DB)
ENGINE = create_engine(PSQL_URL, echo=False)


def build_session() -> Session:
    session = scoped_session(
        sessionmaker(
            autocommit=False,
            expire_on_commit=False,
            autoflush=True,
            bind=ENGINE
            )
        )
    return session()