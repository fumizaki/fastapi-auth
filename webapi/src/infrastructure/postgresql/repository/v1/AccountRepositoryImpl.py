from typing import Optional
from sqlalchemy import select
from sqlalchemy.engine.row import Row, Tuple
from src.domain.v1.entity.AccountEntity import AccountEntity
from src.domain.v1.type.AccountValueType import AccountId
from src.domain.v1.repository.AccountRepository import AccountRepository
from src.infrastructure.core.rdb.RdbSessionClient import RdbSessionClient
from src.infrastructure.postgresql.model.v1.AccountTable import AccountTable


class AccountRepositoryImpl(AccountRepository):

    def __init__(self, rdb: RdbSessionClient) -> None:
        self.rdb = rdb

    def insert(self, entity: AccountEntity) -> AccountEntity:
        self.rdb.session.add(AccountTable.to_table(entity))
        self.rdb.session.flush()

        _in_db: Optional[AccountEntity] = self.find_by_id(entity.id)
        if _in_db is None:
            raise

        return _in_db


    def find_by_id(self, id: AccountId) -> Optional[AccountEntity]:
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