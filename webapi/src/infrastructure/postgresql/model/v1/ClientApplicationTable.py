from __future__ import annotations
from sqlalchemy import Column, String
from src.domain.v1.entity.ClientApplicationEntity import ClientApplicationEntity
from src.infrastructure.postgresql.model.core.CoreTable import CoreTable



class ClientApplicationTable(CoreTable):
    __tablename__ = 'client_application'
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    scope = Column(String, nullable=False)
    redirect_uri = Column(String, nullable=False)

    @staticmethod
    def to_table(entity: ClientApplicationEntity) -> ClientApplicationTable:
        return ClientApplicationTable(**entity.model_dump())
    
    def to_entity(self) -> ClientApplicationEntity:
        return ClientApplicationEntity(**self.__dict__)