from src.application.usecase.AuthenticationUsecase import AuthenticationUsecase
from src.infrastructure.core.rdb.RdbSessionClient import RdbSessionClient
from src.infrastructure.postgresql.util.PsqlSessionBuilder import build_session
from src.infrastructure.postgresql.repository.v1.AccountRepositoryImpl import AccountRepositoryImpl
from src.infrastructure.postgresql.repository.v1.AccountSecretRepositoryImpl import AccountSecretRepositoryImpl

class AuthenticationDependency:
    
    @staticmethod
    def _inject(rdb: RdbSessionClient) -> AuthenticationUsecase:
        account_repository = AccountRepositoryImpl(rdb)
        account_secret_repository = AccountSecretRepositoryImpl(rdb)
        return AuthenticationUsecase(rdb, account_repository, account_secret_repository)
    

    @staticmethod
    def depends() -> AuthenticationUsecase:
        rdb = RdbSessionClient(session = build_session())
        return AuthenticationDependency._inject(rdb)