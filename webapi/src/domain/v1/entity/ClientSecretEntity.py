from src.domain.core.entity.CoreEntity import CoreEntity
from src.domain.v1.type.ClientValueType import (
    ApplicationId,
    SecretTitle, SecretValue, SecretExpiresIn
)


class ClientSecretEntity(CoreEntity):
    application_id: ApplicationId
    title: SecretTitle
    secret: SecretValue
    expires_in: SecretExpiresIn
    
    
    def mask_secret(self) -> None:
        self.secret = "******************************"