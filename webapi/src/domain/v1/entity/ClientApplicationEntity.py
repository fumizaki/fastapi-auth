from src.domain.core.entity.CoreEntity import CoreEntity
from src.domain.v1.type.ClientValueType import (
    ApplicationTitle,
    ApplicationScope, ApplicationRedirectUri
)


class ClientApplicationEntity(CoreEntity):
    title: ApplicationTitle
    scope: ApplicationScope
    redirect_uri: ApplicationRedirectUri