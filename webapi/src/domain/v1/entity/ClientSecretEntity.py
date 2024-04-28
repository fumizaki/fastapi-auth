from src.domain.core.entity.CoreEntity import CoreEntity
from src.domain.v1.type.ClientValueType import (
    ApplicationId, SecretId,
    SecretTitle, SecretValue, SecretExpiresIn
)


class ClientApplicationEntity(CoreEntity):
    id: SecretId
    application_id: ApplicationId
    title: SecretTitle
    secret: SecretValue
    expires_in: SecretExpiresIn