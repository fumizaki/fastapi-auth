import uuid
from src.domain.core.entity.CoreEntity import CoreEntity
from src.domain.v1.type.AccountValueType import AccountEmail, AccountCategoryType, AccountRoleType


class AccountEntity(CoreEntity):
    category: AccountCategoryType = AccountCategoryType.ACCOUNT
    role: AccountRoleType = AccountRoleType.GENERAL
    email: AccountEmail
    