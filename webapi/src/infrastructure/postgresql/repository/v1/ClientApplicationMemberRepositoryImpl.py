from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.engine.row import Row, Tuple
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.type.ClientValueType import ApplicationId
from src.domain.v1.type.AccountValueType import AccountId
from src.domain.v1.entity.ClientApplicationMemberEntity import ClientApplicationMemberEntity
from src.domain.v1.repository.ClientApplicationMemberRepository import ClientApplicationMemberRepository
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.exception.RdbException import (
    RdbContraintError, RdbRecordNotFoundError
)
from src.infrastructure.postgresql.model.v1.ClientApplicationMemberTable import ClientApplicationMemberTable


class ClientApplicationMemberRepositoryImpl(ClientApplicationMemberRepository):

    def __init__(self, rdb: RdbSessionClient) -> None:
        self.rdb = rdb

    def insert(self, entity: ClientApplicationMemberEntity) -> None:
        self.rdb.session.add(ClientApplicationMemberTable.to_table(entity))
        self.rdb.session.flush()


    def find_by_id(self, id: RecordId) -> Optional[ClientApplicationMemberEntity]:
        result = self.rdb.session.execute(
            select(
                ClientApplicationMemberTable
            )
            .filter(
                ClientApplicationMemberTable.id == id
            )
        )
        row: Optional[Row[Tuple[ClientApplicationMemberTable]]] = result.one_or_none()
        
        if row is None:
            return
        
        _in_db: ClientApplicationMemberTable = row[0]

        return _in_db.to_entity()
    
    
    def find_by_application_and_account(self, application_id: ApplicationId, account_id: AccountId) -> Optional[ClientApplicationMemberEntity]:
        result = self.rdb.session.execute(
            select(
                ClientApplicationMemberTable
            )
            .filter(
                ClientApplicationMemberTable.application_id == application_id,
                ClientApplicationMemberTable.account_id == account_id
            )
        )
        row: Optional[Row[Tuple[ClientApplicationMemberTable]]] = result.one_or_none()
        
        if row is None:
            return
        
        _in_db: ClientApplicationMemberTable = row[0]

        return _in_db.to_entity()
    
    
    def find_list_by_account(self, account_id: AccountId) -> list[Optional[ClientApplicationMemberEntity]]:
        result = self.rdb.session.execute(
            select(
                ClientApplicationMemberTable
            )
            .filter(
                ClientApplicationMemberTable.account_id == account_id
            )
        )
        rows: Sequence[Row[Tuple[ClientApplicationMemberTable]]] = result.all()
        
        if len(rows) == 0:
            return []
        

        return [row[0].to_entity() for row in rows]
    
    
    def find_list_by_application(self, application_id: ApplicationId) -> list[Optional[ClientApplicationMemberEntity]]:
        result = self.rdb.session.execute(
            select(
                ClientApplicationMemberTable
            )
            .filter(
                ClientApplicationMemberTable.application_id == application_id
            )
        )
        rows: Sequence[Row[Tuple[ClientApplicationMemberTable]]] = result.all()
        
        if len(rows) == 0:
            return []
        

        return [row[0].to_entity() for row in rows]
    
    
    def delete(self, id: RecordId) -> None:
        result = self.rdb.session.execute(
            select(
                ClientApplicationMemberTable
            )
            .filter(
                ClientApplicationMemberTable.id == id
            )
        )
        row: Optional[Row[Tuple[ClientApplicationMemberTable]]] = result.first()
        if row is None:
            raise RdbRecordNotFoundError("Client application member not found")
        
        _in_db: ClientApplicationMemberTable = row[0]
        _in_db.deleted_at = _in_db.now()
        
        self.rdb.session.flush()