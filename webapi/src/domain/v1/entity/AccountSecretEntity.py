from src.domain.core.entity.CoreEntity import CoreEntity
from src.domain.v1.type.AccountValueType import (
    AccountId, AccountPassword,
    AccountPasswordSalt, AccountPasswordStretching
)

class AccountSecretEntity(CoreEntity):
    account_id: AccountId
    password: AccountPassword
    salt: AccountPasswordSalt
    stretching: AccountPasswordStretching