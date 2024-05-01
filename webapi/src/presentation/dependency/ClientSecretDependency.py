from src.application.usecase.ClientSecretUsecase import ClientSecretUsecase
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.postgresql.util.PsqlSessionBuilder import build_session
from src.infrastructure.postgresql.repository.v1.ClientSecretRepositoryImpl import ClientSecretRepositoryImpl

class ClientSecretDependency:
    
    @staticmethod
    def _inject(rdb: RdbSessionClient) -> ClientSecretUsecase:
        client_secret_repository = ClientSecretRepositoryImpl(rdb)
        return ClientSecretUsecase(rdb, client_secret_repository)
    

    @staticmethod
    def depends() -> ClientSecretUsecase:
        rdb = RdbSessionClient(session = build_session())
        return ClientSecretDependency._inject(rdb)