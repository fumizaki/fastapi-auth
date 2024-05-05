from typing import Optional
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.schema.AuthorizationSchema import (
    AuthorizeRequestSchema, AuthorizeResponseSchema,
    TokenRequestSchema, TokenRefreshRequestSchema, TokenResponseSchema,
    TokenIntrospectRequestSchema, TokenIntrospectResponseSchema,
    AuthResponseType, AuthGrantType, TokenType
)
from src.domain.v1.entity.AuthorizationCodeEntity import AuthorizationCodeEntity
from src.domain.v1.entity.ClientApplicationEntity import ClientApplicationEntity
from src.domain.v1.entity.ClientApplicationMemberEntity import ClientApplicationMemberEntity
from src.domain.v1.entity.ClientSecretEntity import ClientSecretEntity
from src.domain.v1.repository.AuthorizationCodeRepository import AuthorizationCodeRepository
from src.domain.v1.repository.ClientApplicationRepository import ClientApplicationRepository
from src.domain.v1.repository.ClientSecretRepository import ClientSecretRepository
from src.domain.v1.repository.ClientApplicationMemberRepository import ClientApplicationMemberRepository
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.exception.RdbException import RdbContraintError
from src.infrastructure.core.auth.util.OAuth2Client import OAuth2Client
from src.infrastructure.core.auth.util.OAuth2Constant import *
from src.infrastructure.core.auth.model.OAuth2Model import AuthorizationTokenProps

class AuthorizationUsecase:
    
    class UnitOfWork:
        def __init__(
            self,
            rdb: RdbSessionClient,
            authorization_code_repository: AuthorizationCodeRepository,
            client_application_repository: ClientApplicationRepository,
            client_secret_repository: ClientSecretRepository,
            client_application_member_repository: ClientApplicationMemberRepository
        ) -> None:
            self.rdb = rdb
            self.authorization_code_repository = authorization_code_repository
            self.client_application_repository = client_application_repository
            self.client_secret_repository = client_secret_repository
            self.client_application_member_repository = client_application_member_repository

    def __init__(
        self,
        rdb: RdbSessionClient,
        authorization_code_repository: AuthorizationCodeRepository,
        client_application_repository: ClientApplicationRepository,
        client_secret_repository: ClientSecretRepository,
        client_application_member_repository: ClientApplicationMemberRepository
    ) -> None:
        self.uow = self.UnitOfWork(
            rdb,
            authorization_code_repository,
            client_application_repository,
            client_secret_repository,
            client_application_member_repository
        )
        
        
    def v1_authorize_exec(self, param: AuthorizeRequestSchema) -> AuthorizeResponseSchema:
        
        def _insert_authorization_code(authorization_code: AuthorizationCodeEntity) -> RecordId:
            try:
                self.uow.authorization_code_repository.insert(authorization_code)
                return authorization_code.id
            
            # TODO: PK重複エラーとその他のエラーを分ける
            except RdbContraintError as e:
                # TODO: PK重複エラーの場合、EntityのIDを再生成して再挿入
                authorization_code.reset_id()
                _insert_authorization_code(authorization_code) 
        
        try:
            if param.response_type != AuthResponseType.CODE:
                raise ValueError("response type is not valid")
            
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

            authorization_code_id = _insert_authorization_code(authorization_code)
            
            return AuthorizeResponseSchema(
                code=authorization_code_id,
                state=param.state
            )
        
        finally:
            self.uow.rdb.close()
    
    
    def v1_token_exec(self, param: TokenRequestSchema) -> TokenResponseSchema:
        try:
            if param.grant_type != AuthGrantType.AUTHORIZATION_CODE:
                raise

            client_secret_in_db: Optional[ClientSecretEntity] = self.uow.client_secret_repository.find_by_secret(param.client_secret)
            if client_secret_in_db is None:
                raise

            authorization_code_in_db: Optional[AuthorizationCodeEntity] = self.uow.authorization_code_repository.find_by_id(param.code)
            if authorization_code_in_db is None:
                raise

            if param.client_id != authorization_code_in_db:
                raise

            client_application_member_in_db: Optional[ClientApplicationMemberEntity] = self.uow.client_application_member_repository.find_by_application_and_account(param.client_id, param.account_id)
            if client_application_member_in_db is None:
                raise
            
            expires_in = OAuth2Client.exp()
            access_token: str = OAuth2Client.create_authorization_token(
                AuthorizationTokenProps(
                    sub=client_application_member_in_db.account_id,
                    iss=OAuth2Client.iss(),
                    aud=OAuth2Client.aud(),
                    iat=OAuth2Client.iat(),
                    exp=expires_in,
                    scope=authorization_code_in_db.scope
                )
            )
            refresh_expires_in = OAuth2Client.exp(30)
            refresh_token: str = OAuth2Client.create_authorization_token(
                AuthorizationTokenProps(
                    sub=client_application_member_in_db.account_id,
                    iss=OAuth2Client.iss(),
                    aud=OAuth2Client.aud(),
                    iat=OAuth2Client.iat(),
                    exp=refresh_expires_in,
                    scope=authorization_code_in_db.scope
                ),
                OAUTH2_TOKEN_REFRESH_SECRET,
                OAUTH2_TOKEN_REFRESH_ALGORITHM
            )

            return TokenResponseSchema(
                access_token=access_token,
                expires_in=expires_in,
                refresh_token=refresh_token,
                token_type=TokenType.BEARER,
                scope=authorization_code_in_db.scope
            )


        
        finally:
            self.uow.rdb.close()
    
    
    def v1_token_refresh_exec(self, param: TokenRefreshRequestSchema) -> TokenResponseSchema:
        try:
            if param.grant_type != AuthGrantType.REFRESH_TOKEN:
                raise

            client_application_in_db: Optional[ClientApplicationEntity] = self.uow.client_application_repository.find_by_id(param.client_id)
            if client_application_in_db is None:
                raise

            client_secret_in_db: Optional[ClientSecretEntity] = self.uow.client_secret_repository.find_by_secret(param.client_secret)
            if client_secret_in_db is None:
                raise

            if not OAuth2Client.is_effective(client_secret_in_db.expires_in):
                raise

            payload: AuthorizationTokenProps = OAuth2Client.decode_authorization_token(
                param.refresh_token,
                OAUTH2_TOKEN_REFRESH_SECRET,
                OAUTH2_TOKEN_REFRESH_ALGORITHM
                )

            if not OAuth2Client.is_effective(payload.exp):
                raise

            if payload.scope:
                scopes: list[str] = payload.scope.split(",")
                if not OAuth2Client.has_required_scope(scopes, client_application_in_db.scope):
                    raise

            client_application_member_in_db: Optional[ClientApplicationMemberEntity] = self.uow.client_application_member_repository.find_by_application_and_account(param.client_id, payload.sub)
            if client_application_member_in_db is None:
                raise

            expires_in = OAuth2Client.exp()
            access_token: str = OAuth2Client.create_authorization_token(
                AuthorizationTokenProps(
                    sub=client_application_member_in_db.account_id,
                    iss=OAuth2Client.iss(),
                    aud=OAuth2Client.aud(),
                    iat=OAuth2Client.iat(),
                    exp=expires_in,
                    scope=payload.scope
                )
            )
            refresh_expires_in = OAuth2Client.exp(30)
            refresh_token: str = OAuth2Client.create_authorization_token(
                AuthorizationTokenProps(
                    sub=client_application_member_in_db.account_id,
                    iss=OAuth2Client.iss(),
                    aud=OAuth2Client.aud(),
                    iat=OAuth2Client.iat(),
                    exp=refresh_expires_in,
                    scope=payload.scope
                ),
                OAUTH2_TOKEN_REFRESH_SECRET,
                OAUTH2_TOKEN_REFRESH_ALGORITHM
            )

            return TokenResponseSchema(
                access_token=access_token,
                expires_in=expires_in,
                refresh_token=refresh_token,
                token_type=TokenType.BEARER,
                scope=payload.scope
            )

        finally:
            self.uow.rdb.close()
    
    
    def v1_token_introspect_exec(self, param: TokenIntrospectRequestSchema) -> TokenIntrospectResponseSchema:
        try:
            if param.grant_type != AuthGrantType.AUTHORIZATION_CODE:
                raise ValueError("grant type is not authorization_code")
            
            if param.token_type != TokenType.BEARER:
                raise ValueError("token type hint is not bearer")
        
            client_application_in_db: Optional[ClientApplicationEntity] = self.uow.client_application_repository.find_by_id(param.client_id)
            if client_application_in_db is None:
                raise

            client_secret_in_db: Optional[ClientSecretEntity] = self.uow.client_secret_repository.find_by_secret(param.client_secret)
            if client_secret_in_db is None:
                raise

            if not OAuth2Client.is_effective(client_secret_in_db.expires_in):
                raise

            payload: AuthorizationTokenProps = OAuth2Client.decode_authorization_token(param.token)

            if not OAuth2Client.is_effective(payload.exp):
                raise

            client_application_member_in_db: Optional[ClientApplicationMemberEntity] = self.uow.client_application_member_repository.find_by_application_and_account(param.client_id, payload.sub)
            if client_application_member_in_db is None:
                raise

            return TokenIntrospectResponseSchema(
                subject=payload.sub,
                client_id=param.client_id,
                token_type=param.token_type,
                scope=payload.scope
            )

        finally:
            self.uow.rdb.close()