from typing import Optional
from src.domain.core.schema.CoreSchema import CoreSchema
from src.domain.v1.type.AuthValueType import (
    AuthGrantType, AuthResponseType, TokenType,
    AuthorizationState, AuthorizationCode,
    AuthorizationToken, AuthorizationCodeChallenge
)
from src.domain.v1.type.ClientValueType import (
    ApplicationId, ApplicationScope, ApplicationRedirectUri,
    SecretValue, SecretExpiresIn
)


class AuthorizeRequestSchema(CoreSchema):
    client_id: ApplicationId
    redirect_uri: ApplicationRedirectUri
    response_type: AuthResponseType
    scope: Optional[ApplicationScope] = None
    state: Optional[AuthorizationState] = None
    code_challenge: Optional[AuthorizationCodeChallenge] = None
    
    
class AuthorizeResponseSchema(CoreSchema):
    code: AuthorizationCode
    state: AuthorizationState
    
    
class TokenRequestSchema(CoreSchema):
    client_id: ApplicationId
    client_secret: SecretValue
    grant_type: AuthGrantType
    code: AuthorizationCode
    scope: Optional[ApplicationScope] = None
    
    
class TokenResponseSchema(CoreSchema):
    access_token: AuthorizationToken
    expires_in: SecretExpiresIn
    refresh_token: AuthorizationToken
    token_type: TokenType
    scope: Optional[ApplicationScope] = None
    