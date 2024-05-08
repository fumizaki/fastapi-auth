from typing import Optional, Sequence
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
        
        
    def find_list(self) -> list[ClientApplicationEntity]:
        result = self.rdb.session.execute(
            select(
                ClientApplicationTable
            )
        )
        rows: Sequence[Row[Tuple[ClientApplicationTable]]] = result.all()
        
        if len(rows) == 0:
            return []

        return [row[0].to_entity() for row in rows]


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
    
    
    def update(self, entity: ClientApplicationEntity) -> None:
        result = self.rdb.session.execute(
            select(
                ClientApplicationTable
            )
            .filter(
                ClientApplicationTable.id == entity.id
            )
        )
        row: Optional[Row[Tuple[ClientApplicationTable]]] = result.first()
        if row is None:
            raise RdbRecordNotFoundError("Client application not found")
        
        _in_db: ClientApplicationTable = row[0]
        _in_db.title = entity.title
        _in_db.scope = entity.scope
        _in_db.redirect_uri = entity.redirect_uri
        
        self.rdb.session.flush()
        
        
    def delete(self, id: RecordId) -> None:
        result = self.rdb.session.execute(
            select(
                ClientApplicationTable
            )
            .filter(
                ClientApplicationTable.id == id
            )
        )
        row: Optional[Row[Tuple[ClientApplicationTable]]] = result.first()
        if row is None:
            raise RdbRecordNotFoundError("Client application not found")
        
        _in_db: ClientApplicationTable = row[0]
        _in_db.deleted_at = _in_db.now()
        
        self.rdb.session.flush()
        