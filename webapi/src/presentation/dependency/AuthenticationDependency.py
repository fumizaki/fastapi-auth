from src.application.usecase.AuthenticationUsecase import AuthenticationUsecase
from src.infrastructure.core.rdb.RdbSessionClient import RdbSessionClient
from src.infrastructure.postgresql.util.PsqlSessionBuilder import build_session
from src.infrastructure.postgresql.repository.v1.AccountRepositoryImpl import AccountRepositoryImpl

class AuthenticationDependency:
    
    @staticmethod
    def _inject(rdb: RdbSessionClient) -> AuthenticationUsecase:
        account_repository = AccountRepositoryImpl(rdb)
        return AuthenticationUsecase(rdb, account_repository)
    

    @staticmethod
    def depends() -> AuthenticationUsecase:
        rdb = RdbSessionClient(session = build_session())
        return AuthenticationDependency._inject(rdb)