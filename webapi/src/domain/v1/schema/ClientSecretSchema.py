from pydantic import Field
from src.domain.core.schema.CoreSchema import CoreSchema
from src.domain.v1.type.ClientValueType import ApplicationId, SecretTitle, SecretExpiresDaysType

class CreateClientSecretSchema(CoreSchema):
    application_id: ApplicationId
    title: SecretTitle = Field(..., min_length = 1, max_length = 64)
    expiration: SecretExpiresDaysType