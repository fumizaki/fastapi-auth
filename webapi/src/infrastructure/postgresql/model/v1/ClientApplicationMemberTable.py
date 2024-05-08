from __future__ import annotations
from sqlalchemy import Column, String, Boolean
from src.domain.v1.entity.ClientApplicationMemberEntity import ClientApplicationMemberEntity
from src.infrastructure.postgresql.model.core.CoreTable import CoreTable



class ClientApplicationMemberTable(CoreTable):
    __tablename__ = 'client_application_member'
    id = Column(String, primary_key=True)
    application_id = Column(String, unique=True, nullable=False)
    account_id = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    is_banned = Column(Boolean, nullable=False)

    @staticmethod
    def to_table(entity: ClientApplicationMemberEntity) -> ClientApplicationMemberTable:
        return ClientApplicationMemberTable(**entity.model_dump())
    
    def to_entity(self) -> ClientApplicationMemberEntity:
        return ClientApplicationMemberEntity(**self.__dict__)