from typing import Optional
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, status
from src.infrastructure.core.auth.util.OAuth2Constant import *
from src.infrastructure.core.auth.model.OAuth2Model import AuthorizationToken, AuthorizationCode, Credential

def _get_current_unixtime() -> int:
    """
    現在時刻のunixtime
    """
    return int(datetime.now().timestamp())


def _get_future_unixtime(days: int = 1) -> int:
    """
    現在時刻からdaysで指定した日数を追加したunixtime
    """
    return int((datetime.now() + timedelta(days = days)).timestamp())



class OAuth2Client:

    @staticmethod
    def iat() -> int:
        return _get_current_unixtime()
    
    @staticmethod
    def exp(days: int = 1) -> int:
        return _get_future_unixtime(days = days)
    
    @staticmethod
    def iss() -> str:
        return OAUTH2_ISSUER
    
    @staticmethod
    def aud() -> str:
        return OAUTH2_AUDIENCE
    
    @staticmethod
    def is_effective(exp: int) -> bool:
        return exp > _get_current_unixtime()
    

    @staticmethod
    def has_required_scope(scopes: list[str], required_scopes: list[str]) -> bool:
        """
        `required_scopes`に格納されている値が1つでも`scopes`に含まれていれば`True`
        """
        is_valid = False
        for scope in scopes:
            if scope in required_scopes:
                is_valid = True
                break            
        return is_valid
    

    @staticmethod
    def create_authorization_token(
        param: AuthorizationToken,
        key: str = OAUTH2_TOKEN_SECRET,
        alg: str = OAUTH2_TOKEN_ALGORITHM
    ) -> str:
        try:
            return jwt.encode(
                payload=param.model_dump(),
                key=key,
                algorithm=alg
            )
            
        except:
            raise
    

    @staticmethod
    def decode_authorization_token(
        token: str,
        key: str = OAUTH2_TOKEN_SECRET,
        alg: str = OAUTH2_TOKEN_ALGORITHM
    ) -> AuthorizationToken:
        try:
            param = jwt.decode(
                token,
                key,
                audience=OAuth2Client.aud(),
                issuer=OAuth2Client.iss(),
                algorithms=[alg]
            )

            return AuthorizationToken(
                sub=param['sub'],
                iss=param['iss'],
                aud=param['aud'],
                exp=param['exp'],
                iat=param['iat'],
                scope=param['scope'],
                jti=param['jti'],
                nonce=param['nonce']
            )

        except:
            raise
    

    @staticmethod
    def create_authorization_code(
        param: AuthorizationCode,
        key: str = OAUTH2_CODE_SECRET,
        alg: str = OAUTH2_CODE_ALGORITHM
    ) -> str:
        try:
            return jwt.encode(
                payload=param.model_dump(),
                key=key,
                algorithm=alg
            )

        except:
            raise
    

    @staticmethod
    def decode_authorization_code(
        code: str,
        key: str = OAUTH2_CODE_SECRET,
        alg: str = OAUTH2_CODE_ALGORITHM
    ) -> AuthorizationCode:
        try:
            param = jwt.decode(
                code,
                key,
                algorithms=[alg]
            )
            return AuthorizationCode(
                code=param['code'],
                client_id=param['client_id'],
                state=param['state'],
                scope=param['scope']
            )
        except:
            raise

    
    @staticmethod
    def verify(required_scopes: Optional[list[str]], token: str) -> Credential:
        payload: AuthorizationToken = OAuth2Client.decode_authorization_token(token)

        if payload.iss != OAuth2Client.iss():
            raise


        if payload.aud != OAuth2Client.aud():
            raise


        if not OAuth2Client.is_effective(payload.exp):
            raise


        if required_scopes and payload.scope:
            scopes = payload.scope.split(",")
            if not OAuth2Client.has_required_scope(scopes, required_scopes):
                raise

        return Credential(
            account_id=payload.sub,
            scope=payload.scope,
            token=token
        )

        