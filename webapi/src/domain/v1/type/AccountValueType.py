from enum import Enum
from typing import NewType


AccountId = NewType('AccountId', str)
AccountEmail = NewType('AccountEmail', str)
AccountPassword = NewType('AccountPassword', str)

class AccountCategoryType(str, Enum):
    APP = 'app'
    OAUTH = 'oauth'

class AccountRoleType(str, Enum):
    ADMIN = 'admin'
    GENERAL = 'general'
    
    
    