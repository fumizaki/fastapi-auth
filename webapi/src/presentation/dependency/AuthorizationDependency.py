from src.application.usecase.AuthorizationUsecase import AuthorizationUsecase
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.postgresql.util.PsqlSessionBuilder import build_session
from src.infrastructure.postgresql.repository.v1.AuthorizationCodeRepositoryImpl import AuthorizationCodeRepositoryImpl
from src.infrastructure.postgresql.repository.v1.ClientApplicationRepositoryImpl import ClientApplicationRepositoryImpl
from src.infrastructure.postgresql.repository.v1.ClientApplicationMemberRepositoryImpl import ClientApplicationMemberRepositoryImpl
from src.infrastructure.postgresql.repository.v1.ClientSecretRepositoryImpl import ClientSecretRepositoryImpl


class AuthorizationDependency:
    
    @staticmethod
    def _inject(rdb: RdbSessionClient) -> AuthorizationUsecase:
        authorization_code_repository = AuthorizationCodeRepositoryImpl(rdb)
        client_application_repository = ClientApplicationRepositoryImpl(rdb)
        client_application_member_repository = ClientApplicationMemberRepositoryImpl(rdb)
        client_secret_repository = ClientSecretRepositoryImpl(rdb)
        return AuthorizationUsecase(
            rdb,
            authorization_code_repository,
            client_application_repository,
            client_secret_repository,
            client_application_member_repository
            )
    

    @staticmethod
    def depends() -> AuthorizationUsecase:
        rdb = RdbSessionClient(session = build_session())
        return AuthorizationDependency._inject(rdb)