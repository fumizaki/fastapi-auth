import uuid
from src.domain.core.entity.CoreEntity import CoreEntity
from src.domain.v1.type.AccountValueType import AccountId, AccountEmail, AccountCategoryType, AccountRoleType


class AccountEntity(CoreEntity):
    id: AccountId = str(uuid.uuid4())
    category: AccountCategoryType = AccountCategoryType.APP
    role: AccountRoleType = AccountRoleType.GENERAL
    email: AccountEmail
    