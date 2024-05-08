from src.domain.core.schema.CoreSchema import CoreSchema
from src.domain.v1.type.ClientValueType import (
    ApplicationRoleType, ApplicationId
    )
from src.domain.v1.type.AccountValueType import AccountEmail

    

class InviteMemberSchema(CoreSchema):
    client_id: ApplicationId
    role: ApplicationRoleType
    emails: list[AccountEmail]