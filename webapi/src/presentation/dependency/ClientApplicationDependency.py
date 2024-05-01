from fastapi import Security
from src.application.usecase.ClientApplicationUsecase import ClientApplicationUsecase
from src.infrastructure.core.middleware.util.HttpRequestHeaderMiddleware import HttpRequestHeaderMiddleware
from src.infrastructure.core.middleware.model.MiddlewareModel import Authorization
from src.infrastructure.core.auth.util.OAuth2Client import OAuth2Client
from src.infrastructure.core.auth.model.OAuth2Model import Credential
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.postgresql.util.PsqlSessionBuilder import build_session
from src.infrastructure.postgresql.repository.v1.ClientApplicationRepositoryImpl import ClientApplicationRepositoryImpl

class ClientApplicationDependency:
    
    @staticmethod
    def _inject(authorization: Authorization, rdb: RdbSessionClient) -> ClientApplicationUsecase:
        credential: Credential = OAuth2Client.verify(authorization.required_scopes)
        client_application_repository = ClientApplicationRepositoryImpl(rdb)
        return ClientApplicationUsecase(credential, rdb, client_application_repository)
    

    @staticmethod
    def depends(
        authorization: Authorization = Security(
            HttpRequestHeaderMiddleware.extract_authorization,
            scopes=[
                "auth/client",
            ]
        )
    ) -> ClientApplicationUsecase:
        rdb = RdbSessionClient(session = build_session())
        return ClientApplicationDependency._inject(authorization, rdb)