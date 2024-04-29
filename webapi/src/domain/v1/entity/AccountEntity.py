import uuid
from src.domain.core.entity.CoreEntity import CoreEntity
from src.domain.v1.type.AccountValueType import AccountEmail, AccountCategoryType, AccountRoleType


class AccountEntity(CoreEntity):
    category: AccountCategoryType = AccountCategoryType.APP
    role: AccountRoleType = AccountRoleType.GENERAL
    email: AccountEmail
    