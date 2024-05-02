from enum import Enum
from typing import NewType
from src.domain.core.type.CoreValueType import RecordId


AccountId = NewType('AccountId', RecordId)
AccountSecretId = NewType('AccountSecretId', RecordId)
AccountEmail = NewType('AccountEmail', str)
AccountPassword = NewType('AccountPassword', str)
AccountPasswordSalt = NewType('AccountPasswordSalt', str)
AccountPasswordStretching = NewType('AccountPasswordStretching', int)

class AccountCategoryType(str, Enum):
    APP = 'application'
    ACCOUNT = 'account'
    OAUTH = 'oauth' # GoogleやGitHubなどのOAuth認証を利用しているアカウント

class AccountRoleType(str, Enum):
    ADMIN = 'admin'
    GENERAL = 'general'
    
    
    