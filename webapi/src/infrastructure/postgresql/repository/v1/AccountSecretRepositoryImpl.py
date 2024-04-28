from typing import Optional
from sqlalchemy import select
from sqlalchemy.engine.row import Row, Tuple
from src.domain.v1.entity.AccountSecretEntity import AccountSecretEntity
from src.domain.v1.type.AccountValueType import AccountId, AccountSecretId
from src.domain.v1.repository.AccountSecretRepository import AccountSecretRepository
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.postgresql.model.v1.AccountSecretTable import AccountSecretTable


class AccountSecretRepositoryImpl(AccountSecretRepository):

    def __init__(self, rdb: RdbSessionClient) -> None:
        self.rdb = rdb

    def insert(self, entity: AccountSecretEntity) -> None:
        self.rdb.session.add(AccountSecretTable.to_table(entity))
        self.rdb.session.flush()



    def find_by_id(self, id: AccountSecretId) -> Optional[AccountSecretEntity]:
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