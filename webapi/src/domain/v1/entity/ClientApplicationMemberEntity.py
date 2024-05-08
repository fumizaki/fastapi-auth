from src.domain.core.entity.CoreEntity import CoreEntity
from src.domain.v1.type.AccountValueType import AccountId
from src.domain.v1.type.ClientValueType import (
    ApplicationId, ApplicationRoleType
)


class ClientApplicationMemberEntity(CoreEntity):
    application_id: ApplicationId
    account_id: AccountId
    role: ApplicationRoleType
    is_banned: bool = False