from __future__ import annotations
from sqlalchemy import Column, String
from src.domain.v1.entity.AuthorizationCodeEntity import AuthorizationCodeEntity
from src.infrastructure.postgresql.model.core.CoreTable import CoreTable



class AuthorizationCodeTable(CoreTable):
    __tablename__ = 'authorization_code'
    id = Column(String, primary_key=True)
    client_id = Column(String, nullable=False)
    scope = Column(String, nullable=True)
    state = Column(String, nullable=True)

    @staticmethod
    def to_table(entity: AuthorizationCodeEntity) -> AuthorizationCodeTable:
        return AuthorizationCodeTable(**entity.model_dump())
    
    def to_entity(self) -> AuthorizationCodeEntity:
        return AuthorizationCodeEntity(**self.__dict__)