from src.application.usecase.AuthenticationUsecase import AuthenticationUsecase
from src.infrastructure.core.rdb.AsyncRdbSessionClient import AsyncRdbSessionClient
from src.infrastructure.postgresql.util.PsqlSessionBuilder import build_async_session
from src.infrastructure.postgresql.repository.v1.AccountRepositoryImpl import AccountRepositoryImpl

class AuthenticationDependency:
    
    @staticmethod
    def _inject(rdb: AsyncRdbSessionClient) -> AuthenticationUsecase:
        account_repository = AccountRepositoryImpl(rdb)
        return AuthenticationUsecase(rdb, account_repository)
    

    @staticmethod
    def depends() -> AuthenticationUsecase:
        rdb = AsyncRdbSessionClient(session = build_async_session())
        return AuthenticationDependency._inject(rdb)