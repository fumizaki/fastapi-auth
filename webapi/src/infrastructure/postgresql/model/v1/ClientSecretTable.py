from __future__ import annotations
from sqlalchemy import Column, String, Integer
from src.domain.v1.entity.ClientSecretEntity import ClientSecretEntity
from src.infrastructure.postgresql.model.core.CoreTable import CoreTable



class ClientSecretTable(CoreTable):
    __tablename__ = 'client_secret'
    id = Column(String, primary_key=True)
    application_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    expires_in = Column(Integer, nullable=False)

    @staticmethod
    def to_table(entity: ClientSecretEntity) -> ClientSecretTable:
        return ClientSecretTable(**entity.model_dump())
    
    def to_entity(self) -> ClientSecretEntity:
        return ClientSecretEntity(**self.__dict__)