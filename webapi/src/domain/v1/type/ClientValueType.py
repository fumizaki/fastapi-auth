from typing import NewType
from enum import Enum
from src.domain.core.type.CoreValueType import RecordId


ApplicationId = NewType('ApplicationId', RecordId)
ApplicationTitle = NewType('ApplicationTitle', str)
ApplicationScope = NewType('ApplicationScope', str)
ApplicationRedirectUri = NewType('ApplicationRedirectUri', str)


SecretId = NewType('SecretId', RecordId)
SecretTitle = NewType('SecretTitle', str)
SecretValue = NewType('SecretValue', str)
SecretExpiresIn = NewType('SecretExpiresIn', int)


class SecretExpiresDaysType(int, Enum):
    ONE_MONTH = 30
    QUATER = 90
    SIX_MONTH = 180
    ONE_YEAR = 365
    NO_EXPIRATION = 99999999999
    
    
class ApplicationRoleType(str, Enum):
    OWNER = 'owner'
    ADMIN = 'admin'
    DEVELOPER = 'developer'
    TESTER = 'tester'
    VIEWER = 'viewer'
    GUEST = 'guest'