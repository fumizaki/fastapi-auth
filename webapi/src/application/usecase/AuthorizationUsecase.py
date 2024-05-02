from typing import Optional
from src.domain.v1.schema.AuthorizationSchema import (
    AuthorizeRequestSchema, AuthorizeResponseSchema,
    TokenRequestSchema, TokenRefreshRequestSchema, TokenResponseSchema,
    TokenIntrospectRequestSchema, TokenIntrospectResponseSchema,
    AuthResponseType
)
from src.domain.v1.entity.AuthorizationCodeEntity import AuthorizationCodeEntity
from src.domain.v1.entity.ClientApplicationEntity import ClientApplicationEntity 
from src.domain.v1.repository.ClientApplicationRepository import ClientApplicationRepository
from src.domain.v1.repository.ClientApplicationMemberRepository import ClientApplicationMemberRepository
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.exception.RdbException import RdbContraintError
from src.infrastructure.core.auth.util.OAuth2Client import OAuth2Client
from src.infrastructure.core.auth.model.OAuth2Model import AuthorizationCodeProps

class AuthorizationUsecase:
    
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
        rdb: RdbSessionClient,
        client_application_repository: ClientApplicationRepository,
        client_application_member_repository: ClientApplicationMemberRepository
    ) -> None:
        self.uow = self.UnitOfWork(
            rdb,
            client_application_repository,
            client_application_member_repository
        )
        
        
    def v1_authorize_exec(self, param: AuthorizeRequestSchema) -> AuthorizeResponseSchema:
        try:
            if param.response_type != AuthResponseType.CODE:
                raise
            
            client_application_in_db: Optional[ClientApplicationEntity] = self.uow.client_application_repository.find_by_id(param.client_id)
            if client_application_in_db is None:
                raise ValueError("client application is not found")
            
            if param.scope:
                required_scopes = client_application_in_db.scope.split(",")
                if not OAuth2Client.has_required_scope(param.scope, required_scopes):
                    raise ValueError("scope is not valid")
                
            if param.redirect_uri != client_application_in_db.redirect_uri:
                raise ValueError("redirect_uri is not valid")
            
            
            authorization_code: AuthorizationCodeEntity = AuthorizationCodeEntity(
                client_id=param.client_id,
                scope=param.scope,
                state=param.state
            )
            
            return AuthorizeResponseSchema(
                code=authorization_code.id,
                state=param.state
            )
        
        finally:
            self.uow.rdb.close()
    
    
    def v1_token_exec(self, param: TokenRequestSchema) -> TokenResponseSchema:
        try:
            pass
        
        finally:
            self.uow.rdb.close()
    
    
    def v1_token_refresh_exec(self, param: TokenRefreshRequestSchema) -> TokenResponseSchema:
        try:
            pass
        
        finally:
            self.uow.rdb.close()
    
    
    def v1_token_introspect_exec(self, param: TokenIntrospectRequestSchema) -> TokenIntrospectResponseSchema:
        try:
            pass
        
        finally:
            self.uow.rdb.close()