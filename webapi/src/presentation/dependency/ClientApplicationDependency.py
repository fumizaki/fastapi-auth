from src.application.usecase.ClientApplicationUsecase import ClientApplicationUsecase
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.postgresql.util.PsqlSessionBuilder import build_session
from src.infrastructure.postgresql.repository.v1.ClientApplicationRepositoryImpl import ClientApplicationRepositoryImpl

class ClientApplicationDependency:
    
    @staticmethod
    def _inject(rdb: RdbSessionClient) -> ClientApplicationUsecase:
        client_application_repository = ClientApplicationRepositoryImpl(rdb)
        return ClientApplicationUsecase(rdb, client_application_repository)
    

    @staticmethod
    def depends() -> ClientApplicationUsecase:
        rdb = RdbSessionClient(session = build_session())
        return ClientApplicationDependency._inject(rdb)