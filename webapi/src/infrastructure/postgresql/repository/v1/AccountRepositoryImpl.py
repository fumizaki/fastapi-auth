from typing import Optional
from sqlalchemy import select
from sqlalchemy.engine.row import Row, Tuple
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.entity.AccountEntity import AccountEntity
from src.domain.v1.type.AccountValueType import AccountId
from src.domain.v1.repository.AccountRepository import AccountRepository
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.exception.RdbException import (
    RdbContraintError, RdbRecordNotFoundError
)
from src.infrastructure.postgresql.model.v1.AccountTable import AccountTable
from src.domain.v1.type.AccountValueType import AccountEmail


class AccountRepositoryImpl(AccountRepository):

    def __init__(self, rdb: RdbSessionClient) -> None:
        self.rdb = rdb

    def insert(self, entity: AccountEntity) -> None:
        self.rdb.session.add(AccountTable.to_table(entity))
        self.rdb.session.flush()


    def find_by_id(self, id: RecordId) -> Optional[AccountEntity]:
        result = self.rdb.session.execute(
            select(
                AccountTable
            )
            .filter(
                AccountTable.id == id
            )
        )
        row: Optional[Row[Tuple[AccountTable]]] = result.one_or_none()
        
        if row is None:
            return
        
        _in_db: AccountTable = row[0]

        return _in_db.to_entity()
    
    
    def find_by_email(self, email: AccountEmail) -> Optional[AccountEntity]:
        result = self.rdb.session.execute(
            select(
                AccountTable
            )
            .filter(
                AccountTable.email == email
            )
        )
        row: Optional[Row[Tuple[AccountTable]]] = result.one_or_none()
        
        if row is None:
            return
        
        _in_db: AccountTable = row[0]

        return _in_db.to_entity()
    
    
    def update(self, entity: AccountEntity) -> None:
        result = self.rdb.session.execute(
            select(
                AccountTable
            )
            .filter(
                AccountTable.id == entity.id
            )
        )
        row: Optional[Row[Tuple[AccountTable]]] = result.first()
        if row is None:
            raise RdbRecordNotFoundError("Account not found")
        
        _in_db: AccountTable = row[0]
        _in_db.email = entity.email

        self.rdb.session.flush()
        
        
    def delete(self, id: RecordId) -> None:
        result = self.rdb.session.execute(
            select(
                AccountTable
            )
            .filter(
                AccountTable.id == id
            )
        )
        row: Optional[Row[Tuple[AccountTable]]] = result.first()
        if row is None:
            raise RdbRecordNotFoundError("Account not found")
        
        _in_db: AccountTable = row[0]
        _in_db.deleted_at = _in_db.now()
        
        self.rdb.session.flush()