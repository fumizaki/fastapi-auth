import uuid
from src.domain.core.entity.CoreEntity import CoreEntity
from src.domain.v1.type.AccountValueType import AccountId, AccountCategoryType, AccountRoleType


class AccountEntity(CoreEntity):
    id: AccountId = str(uuid.uuid4())
    category: AccountCategoryType
    role: AccountRoleType
    email: str
    password: str
    