from typing import Optional
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.type.ClientValueType import ApplicationRoleType
from src.domain.v1.entity.ClientApplicationEntity import ClientApplicationEntity
from src.domain.v1.entity.ClientApplicationMemberEntity import ClientApplicationMemberEntity
from src.domain.v1.schema.ClientApplicationSchema import (
    CreateClientApplicationSchema,
)
from src.domain.v1.repository.ClientApplicationRepository import ClientApplicationRepository
from src.domain.v1.repository.ClientApplicationMemberRepository import ClientApplicationMemberRepository
from src.infrastructure.core.auth.model.OAuth2Model import Credential
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.exception.RdbException import RdbContraintError



class ClientApplicationUsecase:

    class UnitOfWork:
        def __init__(
            self,
            rdb: RdbSessionClient,
            client_application_repository: ClientApplicationRepository,
            client_application_member_repository: ClientApplicationMemberRepository
        ) -> None:
            self.rdb = rdb
            self.client_application_repository = client_application_repository
            self.client_application_member_repository = client_application_member_repository

    def __init__(
        self,
        credential: Credential,
        rdb: RdbSessionClient,
        client_application_repository: ClientApplicationRepository,
        client_application_member_repository: ClientApplicationMemberRepository
    ) -> None:
        self.credential = credential
        self.uow = self.UnitOfWork(
            rdb,
            client_application_repository,
            client_application_member_repository
        )
        
    def v1_list_client_application_exec(self) -> list[Optional[ClientApplicationEntity]]:
        try:
            client_application_in_db: list[Optional[ClientApplicationEntity]] = self.uow.client_application_repository.find_list()
            return client_application_in_db
        
        finally:
            self.uow.rdb.close()
        
        
    def v1_get_client_application_exec(self, id: RecordId) -> ClientApplicationEntity:
        try:
            client_application_in_db: Optional[ClientApplicationEntity] = self.uow.client_application_repository.find_by_id(id)
            if client_application_in_db is None:
                raise ValueError("Client application not found")
            return client_application_in_db
        
        finally:
            self.uow.rdb.close()
        
        
    def v1_create_client_application_exec(self, param: CreateClientApplicationSchema) -> ClientApplicationEntity:
        
        def _insert_client_application(client_application: ClientApplicationEntity) -> RecordId:
            try:
                self.uow.client_application_repository.insert(client_application)
                return client_application.id
            
            # TODO: PK重複エラーとその他のエラーを分ける
            except RdbContraintError as e:
                # TODO: PK重複エラーの場合、EntityのIDを再生成して再挿入
                client_application.reset_id()
                _insert_client_application(client_application) 
                
                
        def _insert_client_application_member(client_application_member: ClientApplicationMemberEntity) -> None:
            try:
                self.uow.client_application_member_repository.insert(client_application_member)
                return client_application_member.id
                
            # TODO: PK重複エラーとその他のエラーを分ける
            except RdbContraintError as e:
                # TODO: PK重複エラーの場合、EntityのIDを再生成して再挿入
                client_application_member.reset_id()
                _insert_client_application_member(client_application_member) 
        
        try:
            client_application = ClientApplicationEntity(
                title=param.title,
                scope=param.scope,
                redirect_uri=param.redirect_uri
            )
            
            client_application_id = _insert_client_application(client_application)
            
            client_application_member = ClientApplicationMemberEntity(
                application_id=client_application_id,
                account_id=self.credential.account_id,
                role=ApplicationRoleType.OWNER
            )
            
            client_application_member_id = _insert_client_application_member(client_application_member)
            
            self.uow.rdb.commit()
            
            # TODO: sessionのcloseが必要かどうか確認
            return self.v1_get_client_application_exec(client_application_id)
        
        
        finally:
            self.uow.rdb.close()
            