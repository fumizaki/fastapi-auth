from typing import Optional
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.type.ClientValueType import ApplicationId
from src.domain.v1.entity.ClientSecretEntity import ClientSecretEntity
from src.domain.v1.schema.ClientSecretSchema import CreateClientSecretSchema
from src.domain.v1.repository.ClientSecretRepository import ClientSecretRepository
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.exception.RdbException import RdbContraintError



class ClientSecretUsecase:

    class UnitOfWork:
        def __init__(
            self,
            rdb: RdbSessionClient,
            client_secret_repository: ClientSecretRepository
        ) -> None:
            self.rdb = rdb
            self.client_secret_repository = client_secret_repository

    def __init__(
        self,
        rdb: RdbSessionClient,
        client_secret_repository: ClientSecretRepository
    ) -> None:
        self.uow = self.UnitOfWork(
            rdb,
            client_secret_repository
        )
            
            
    def v1_list_client_secret_linked_to_application_exec(self, application_id: ApplicationId) -> list[Optional[ClientSecretEntity]]:
        try:
            client_secret_in_db: list[Optional[ClientSecretEntity]] = self.uow.client_secret_repository.find_list_by_application(application_id)
            return client_secret_in_db
        
        finally:
            self.uow.rdb.close()
        
    
    def v1_create_client_secret_exec(self, param: CreateClientSecretSchema) -> ClientSecretEntity:
        
        def _insert_client_secret(client_secret: ClientSecretEntity) -> RecordId:
            try:
                self.uow.client_secret_repository.insert(client_secret)
                return client_secret.id
            
            # TODO: PK重複エラーとその他のエラーを分ける
            except RdbContraintError as e:
                # TODO: PK重複エラーの場合、EntityのIDを再生成して再挿入
                client_secret.reset_id()
                _insert_client_secret(client_secret)


        def _get_client_secret(id: RecordId) -> ClientSecretEntity:
            client_secret_in_db: Optional[ClientSecretEntity] = self.uow.client_secret_repository.find_by_id(id)
            if client_secret_in_db is None:
                raise ValueError("Client secret not found")
            return client_secret_in_db
        
        try:
            client_secret = ClientSecretEntity(
                application_id=param.application_id,
                title=param.title,
                
            )
            
            client_secret_id = _insert_client_secret(client_secret)
              
            self.uow.rdb.commit()
            return _get_client_secret(client_secret_id)
        
        
        finally:
            self.uow.rdb.close()
            
            
    