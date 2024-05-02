from typing import Optional
from src.domain.core.entity.CoreEntity import CoreEntity
from src.domain.v1.type.AuthValueType import AuthorizationCode, AuthorizationState
from src.domain.v1.type.ClientValueType import ApplicationId, ApplicationScope


class AuthorizationCodeEntity(CoreEntity):
    client_id: ApplicationId
    scope: Optional[ApplicationScope]
    state: Optional[AuthorizationState] = None
    