from typing import NewType
from enum import Enum

ApplicationId = NewType('ApplicationId', str)
ApplicationName = NewType('ApplicationName', str)
ApplicationScope = NewType('ApplicationScope', str)
ApplicationRedirectUri = NewType('ApplicationRedirectUri', str)


SecretId = NewType('SecretId', str)
SecretTitle = NewType('SecretTitle', str)
SecretValue = NewType('SecretValue', str)
SecretExpiresIn = NewType('SecretExpiresIn', int)


class SecretExpiresDaysType(int, Enum):
    ONE_MONTH = 30
    QUATER = 90
    SIX_MONTH = 180
    YEAR = 365
    NO_EXPIRATION = 999999999