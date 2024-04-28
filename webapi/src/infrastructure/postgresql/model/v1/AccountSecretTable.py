from __future__ import annotations
from sqlalchemy import Column, String, Integer
from src.domain.v1.entity.AccountSecretEntity import AccountSecretEntity
from src.infrastructure.postgresql.model.core.CoreTable import CoreTable



class AccountSecretTable(CoreTable):
    __tablename__ = 'account_secret'
    id = Column(String, primary_key=True)
    account_id = Column(String, nullable=False)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    stretching = Column(Integer, nullable=False)

    @staticmethod
    def to_table(entity: AccountSecretEntity) -> AccountSecretTable:
        return AccountSecretTable(**entity.model_dump())
    
    def to_entity(self) -> AccountSecretEntity:
        return AccountSecretEntity(**self.__dict__)