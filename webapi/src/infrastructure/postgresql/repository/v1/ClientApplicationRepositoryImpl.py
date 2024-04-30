from typing import Optional
from sqlalchemy import select
from sqlalchemy.engine.row import Row, Tuple
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.entity.ClientApplicationEntity import ClientApplicationEntity
from src.domain.v1.repository.ClientApplicationRepository import ClientApplicationRepository
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.exception.RdbException import (
    RdbContraintError, RdbRecordNotFoundError
)
from src.infrastructure.postgresql.model.v1.ClientApplicationTable import ClientApplicationTable


class ClientApplicationRepositoryImpl(ClientApplicationRepository):

    def __init__(self, rdb: RdbSessionClient) -> None:
        self.rdb = rdb

    def insert(self, entity: ClientApplicationEntity) -> None:
        self.rdb.session.add(ClientApplicationTable.to_table(entity))
        self.rdb.session.flush()


    def find_by_id(self, id: RecordId) -> Optional[ClientApplicationEntity]:
        result = self.rdb.session.execute(
            select(
                ClientApplicationTable
            )
            .filter(
                ClientApplicationTable.id == id
            )
        )
        row: Optional[Row[Tuple[ClientApplicationTable]]] = result.one_or_none()
        
        if row is None:
            return
        
        _in_db: ClientApplicationTable = row[0]

        return _in_db.to_entity()