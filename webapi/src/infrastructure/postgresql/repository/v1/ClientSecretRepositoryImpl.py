from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.engine.row import Row, Tuple
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.type.ClientValueType import ApplicationId, SecretValue
from src.domain.v1.entity.ClientSecretEntity import ClientSecretEntity
from src.domain.v1.repository.ClientSecretRepository import ClientSecretRepository
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.exception.RdbException import (
    RdbContraintError, RdbRecordNotFoundError
)
from src.infrastructure.postgresql.model.v1.ClientSecretTable import ClientSecretTable


class ClientSecretRepositoryImpl(ClientSecretRepository):

    def __init__(self, rdb: RdbSessionClient) -> None:
        self.rdb = rdb

    def insert(self, entity: ClientSecretEntity) -> None:
        self.rdb.session.add(ClientSecretTable.to_table(entity))
        self.rdb.session.flush()


    def find_by_id(self, id: RecordId) -> Optional[ClientSecretEntity]:
        result = self.rdb.session.execute(
            select(
                ClientSecretTable
            )
            .filter(
                ClientSecretTable.id == id
            )
        )
        row: Optional[Row[Tuple[ClientSecretTable]]] = result.one_or_none()
        
        if row is None:
            return
        
        _in_db: ClientSecretTable = row[0]

        return _in_db.to_entity()
    

    def find_by_secret(self, secret: SecretValue) -> Optional[ClientSecretEntity]:
        result = self.rdb.session.execute(
            select(
                ClientSecretTable
            )
            .filter(
                ClientSecretTable.secret == secret
            )
        )
        row: Optional[Row[Tuple[ClientSecretTable]]] = result.one_or_none()
        
        if row is None:
            return
        
        _in_db: ClientSecretTable = row[0]

        return _in_db.to_entity()
    
    
    
    def find_list_by_application(self, application_id: ApplicationId) -> list[Optional[ClientSecretEntity]]:
        result = self.rdb.session.execute(
            select(
                ClientSecretTable
            )
            .filter(
                ClientSecretTable.application_id == application_id
            )
        )
        rows: Sequence[Row[Tuple[ClientSecretTable]]] = result.all()
        
        if len(rows) == 0:
            return []
        

        return [row[0].to_entity() for row in rows]
    
    
    def update(self, entity: ClientSecretEntity) -> None:
        result = self.rdb.session.execute(
            select(
                ClientSecretTable
            )
            .filter(
                ClientSecretTable.id == entity.id
            )
        )
        row: Optional[Row[Tuple[ClientSecretTable]]] = result.first()
        if row is None:
            raise RdbRecordNotFoundError("Client secret not found")
        
        _in_db: ClientSecretTable = row[0]
        _in_db.title = entity.title
        
        self.rdb.session.flush()
        
        
    def delete(self, id: RecordId) -> None:
        result = self.rdb.session.execute(
            select(
                ClientSecretTable
            )
            .filter(
                ClientSecretTable.id == id
            )
        )
        row: Optional[Row[Tuple[ClientSecretTable]]] = result.first()
        if row is None:
            raise RdbRecordNotFoundError("Client secret not found")
        
        _in_db: ClientSecretTable = row[0]
        _in_db.deleted_at = _in_db.now()
        
        self.rdb.session.flush()
        