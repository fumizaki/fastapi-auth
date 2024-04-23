from enum import Enum


class AuthResponseType(str, Enum):
    CODE = 'code'
    TOKEN = 'token'
    ID_TOKEN = 'id_token'


class AuthGrantType(str, Enum):
    AUTHORIZATION_CODE = 'authorization_code'
    PASSWORD = 'password'
    CLIENT_CREDENTIALS = 'client_credentials'
    REFRESH_TOKEN = 'refresh_token'
    

class TokenType(str, Enum):
    BEARER = 'Bearer'
    MAC = 'MAC'
    JWT = 'JWT'

