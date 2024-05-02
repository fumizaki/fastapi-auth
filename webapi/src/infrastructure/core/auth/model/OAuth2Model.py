from typing import Optional
from pydantic import BaseModel
from src.domain.v1.type.AccountValueType import (
    AccountId
)


class AuthorizationTokenProps(BaseModel):
    sub: str
    iss: str
    aud: str
    exp: int
    iat: int
    scope: Optional[str] = None
    jti: Optional[str] = None
    nonce: Optional[str] = None


class AuthorizationCodeProps(BaseModel):
    code: str
    client_id: str
    state: Optional[str] = None
    scope: Optional[str] = None


class Credential(BaseModel):
    account_id: AccountId
    scope: Optional[str] = None
    token: str