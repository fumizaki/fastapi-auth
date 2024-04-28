from enum import Enum
from typing import NewType


AccountId = NewType('AccountId', str)
AccountSecretId = NewType('AccountSecretId', str)
AccountEmail = NewType('AccountEmail', str)
AccountPassword = NewType('AccountPassword', str)
AccountPasswordSalt = NewType('AccountPasswordSalt', str)
AccountPasswordStretching = NewType('AccountPasswordStretching', int)

class AccountCategoryType(str, Enum):
    APP = 'app'
    OAUTH = 'oauth'

class AccountRoleType(str, Enum):
    ADMIN = 'admin'
    GENERAL = 'general'
    
    
    