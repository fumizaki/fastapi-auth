from typing import Optional
from sqlalchemy import select
from sqlalchemy.engine.row import Row, Tuple
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.entity.AuthorizationCodeEntity import AuthorizationCodeEntity
from src.domain.v1.repository.AuthorizationCodeRepository import AuthorizationCodeRepository
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.exception.RdbException import (
    RdbContraintError, RdbRecordNotFoundError
)
from src.infrastructure.postgresql.model.v1.AuthorizationCodeTable import AuthorizationCodeTable


class AuthorizationCodeRepositoryImpl(AuthorizationCodeRepository):

    def __init__(self, rdb: RdbSessionClient) -> None:
        self.rdb = rdb

    def insert(self, entity: AuthorizationCodeEntity) -> None:
        self.rdb.session.add(AuthorizationCodeTable.to_table(entity))
        self.rdb.session.flush()


    def find_by_id(self, id: RecordId) -> Optional[AuthorizationCodeEntity]:
        result = self.rdb.session.execute(
            select(
                AuthorizationCodeTable
            )
            .filter(
                AuthorizationCodeTable.id == id
            )
        )
        row: Optional[Row[Tuple[AuthorizationCodeTable]]] = result.one_or_none()
        
        if row is None:
            return
        
        _in_db: AuthorizationCodeTable = row[0]

        return _in_db.to_entity()
    
    