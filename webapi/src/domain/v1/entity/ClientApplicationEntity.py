from src.domain.core.entity.CoreEntity import CoreEntity
from src.domain.v1.type.ClientValueType import (
    ApplicationId, ApplicationName,
    ApplicationScope, ApplicationRedirectUri
)


class ClientApplicationEntity(CoreEntity):
    id: ApplicationId
    name: ApplicationName
    scope: ApplicationScope
    redirect_uri: ApplicationRedirectUri