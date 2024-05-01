from fastapi import Depends, Request
from fastapi.security import SecurityScopes
from src.infrastructure.core.middleware.util.MiddlewareConstant import *
from src.infrastructure.core.middleware.model.MiddlewareModel import Authorization
from src.infrastructure.core.auth.util.OAuth2AuthorizationCodeFlow import OAuth2AuthorizationCodeGrantFlow



class HttpRequestHeaderMiddleware:

    def _authorization_code_flow() -> OAuth2AuthorizationCodeGrantFlow:
        return OAuth2AuthorizationCodeGrantFlow(
                authorizationUrl="{}/v1/oauth/authorize/".format(WEBAPI_AUTH_URL),
                tokenUrl="{}/v1/oauth/token/".format(WEBAPI_AUTH_URL),
                refreshUrl="{}/v1/oauth/token/refresh/".format(WEBAPI_AUTH_URL),
                # 設定可能なスコープ
                scopes={
                    "auth/account": "アカウント情報のスコープ",
                    "auth/member": "会員情報のスコープ",
                    "auth/client": "クライアント情報のスコープ",
                },
                description="OAuth2 Authorization Code Flow"
            )

    def extract_authorization(
        security_scopes: SecurityScopes,
        access_token: str = Depends(_authorization_code_flow())
    ):
        return Authorization(
            access_token=access_token,
            required_scopes=security_scopes.scopes
        )

