from pydantic import Field, field_validator
from src.domain.core.schema.CoreSchema import CoreSchema
from src.domain.v1.type.ClientValueType import (
    ApplicationRoleType,
    ApplicationId, ApplicationTitle,
    ApplicationScope, ApplicationRedirectUri
)
from src.domain.v1.type.AccountValueType import AccountEmail

class CreateClientApplicationSchema(CoreSchema):
    title: ApplicationTitle = Field(..., min_length = 1, max_length = 64)
    scope: ApplicationScope
    redirect_uri: ApplicationRedirectUri
    
    @field_validator("redirect_uri")
    @classmethod
    def validate_redirect_uri(cls, value: ApplicationRedirectUri) -> ApplicationRedirectUri:
        if not value.startswith("http://") and not value.startswith("https://"):
            raise ValueError("Invalid redirect_uri format")
        return value
    

class InviteMemberSchema(CoreSchema):
    client_id: ApplicationId
    role: ApplicationRoleType
    emails: list[AccountEmail]