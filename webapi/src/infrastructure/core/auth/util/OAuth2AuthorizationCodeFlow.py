from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.security import utils, OAuth2
from fastapi.openapi.models import OAuthFlows


class OAuth2AuthorizationCodeGrantFlow(OAuth2):
    def __init__(
        self,
        authorizationUrl: str,
        tokenUrl: str,
        refreshUrl: Optional[str] = None,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict[str, str]] = {},
        description: Optional[str] = None,
        auto_error: bool = True,
        header_key: str = 'Authorization'
    ):
        super().__init__(
            flows=OAuthFlows(
                authorizationCode={
                    "authorizationUrl": authorizationUrl,
                    "tokenUrl": tokenUrl,
                    "refreshUrl": refreshUrl,
                    "scopes": scopes
                    }
                ),
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error
            )
        self.header_key = header_key
    
    async def __call__(self, request: Request) -> str:
        try:
            authorization: str = request.headers.get(self.header_key)
            scheme, param = utils.get_authorization_scheme_param(authorization)
            if not authorization or scheme.lower() != "bearer":
                raise ValueError
            return param
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not Authenticated: {}'.format(e),
                headers={"WWW-Authenticate": "Bearer realm='auth_required'"}
            )