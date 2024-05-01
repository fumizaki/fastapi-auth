from fastapi import Security
from src.application.usecase.ClientSecretUsecase import ClientSecretUsecase
from src.infrastructure.core.middleware.util.HttpRequestHeaderMiddleware import HttpRequestHeaderMiddleware
from src.infrastructure.core.middleware.model.MiddlewareModel import Authorization
from src.infrastructure.core.auth.util.OAuth2Client import OAuth2Client
from src.infrastructure.core.auth.model.OAuth2Model import Credential
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.postgresql.util.PsqlSessionBuilder import build_session
from src.infrastructure.postgresql.repository.v1.ClientSecretRepositoryImpl import ClientSecretRepositoryImpl

class ClientSecretDependency:
    
    @staticmethod
    def _inject(authorization: Authorization, rdb: RdbSessionClient) -> ClientSecretUsecase:
        credential: Credential = OAuth2Client.verify(authorization.required_scopes)
        client_secret_repository = ClientSecretRepositoryImpl(rdb)
        return ClientSecretUsecase(credential, rdb, client_secret_repository)
    

    @staticmethod
    def depends(
        authorization: Authorization = Security(
            HttpRequestHeaderMiddleware.extract_authorization,
            scopes=[
                "auth/client",
            ]
        )
    ) -> ClientSecretUsecase:
        rdb = RdbSessionClient(session = build_session())
        return ClientSecretDependency._inject(authorization, rdb)