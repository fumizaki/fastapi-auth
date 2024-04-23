from __future__ import annotations
from sqlalchemy import Column, String
from src.domain.v1.entity.AccountEntity import AccountEntity
from src.infrastructure.postgresql.model.core.CoreTable import CoreTable



class AccountTable(CoreTable):
    __tablename__ = 'account'
    id = Column(String, primary_key=True)
    category = Column(String, nullable=False)
    role = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    @staticmethod
    def to_table(o: AccountEntity) -> AccountTable:
        return AccountTable(**o.model_dump())
    
    def to_entity(self) -> AccountEntity:
        return AccountEntity(**self.__dict__)