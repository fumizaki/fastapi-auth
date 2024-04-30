from typing import Optional
from sqlalchemy import select
from sqlalchemy.engine.row import Row, Tuple
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.type.ClientValueType import ApplicationId
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
    
    
    
    def find_by_application(self, application_id: ApplicationId) -> Optional[ClientSecretEntity]:
        result = self.rdb.session.execute(
            select(
                ClientSecretTable
            )
            .filter(
                ClientSecretTable.application_id == application_id
            )
        )
        row: Optional[Row[Tuple[ClientSecretTable]]] = result.one_or_none()
        
        if row is None:
            return
        
        _in_db: ClientSecretTable = row[0]

        return _in_db.to_entity()