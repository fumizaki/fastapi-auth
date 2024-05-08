from typing import Optional
from sqlalchemy import select
from sqlalchemy.engine.row import Row, Tuple
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.entity.AccountSecretEntity import AccountSecretEntity
from src.domain.v1.type.AccountValueType import AccountId, AccountSecretId
from src.domain.v1.repository.AccountSecretRepository import AccountSecretRepository
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.exception.RdbException import (
    RdbContraintError, RdbRecordNotFoundError
)
from src.infrastructure.postgresql.model.v1.AccountSecretTable import AccountSecretTable


class AccountSecretRepositoryImpl(AccountSecretRepository):

    def __init__(self, rdb: RdbSessionClient) -> None:
        self.rdb = rdb

    def insert(self, entity: AccountSecretEntity) -> None:
        self.rdb.session.add(AccountSecretTable.to_table(entity))
        self.rdb.session.flush()



    def find_by_id(self, id: RecordId) -> Optional[AccountSecretEntity]:
        result = self.rdb.session.execute(
            select(
                AccountSecretTable
            )
            .filter(
                AccountSecretTable.id == id
            )
        )
        row: Optional[Row[Tuple[AccountSecretTable]]] = result.one_or_none()
        
        if row is None:
            return
        
        _in_db: AccountSecretTable = row[0]

        return _in_db.to_entity()
    
    
    def find_by_account(self, account_id: AccountId) -> Optional[AccountSecretEntity]:
        result = self.rdb.session.execute(
            select(
                AccountSecretTable
            )
            .filter(
                AccountSecretTable.account_id == account_id
            )
        )
        row: Optional[Row[Tuple[AccountSecretTable]]] = result.one_or_none()
        
        if row is None:
            return
        
        _in_db: AccountSecretTable = row[0]

        return _in_db.to_entity()
    
    
    def update(self, entity: AccountSecretEntity) -> None:
        result = self.rdb.session.execute(
            select(
                AccountSecretTable
            )
            .filter(
                AccountSecretTable.id == entity.id
            )
        )
        row: Optional[Row[Tuple[AccountSecretTable]]] = result.first()
        if row is None:
            raise RdbRecordNotFoundError("Account secret not found")
        
        _in_db: AccountSecretTable = row[0]
        _in_db.password = entity.password
        _in_db.salt = entity.salt
        _in_db.stretching = entity.stretching
        
        self.rdb.session.flush()
        
        
    def delete(self, id: RecordId) -> None:
        result = self.rdb.session.execute(
            select(
                AccountSecretTable
            )
            .filter(
                AccountSecretTable.id == id
            )
        )
        row: Optional[Row[Tuple[AccountSecretTable]]] = result.first()
        if row is None:
            raise RdbRecordNotFoundError("Account secret not found")
        
        _in_db: AccountSecretTable = row[0]
        _in_db.deleted_at = _in_db.now()
        
        self.rdb.session.flush()