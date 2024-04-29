from abc import ABC, abstractmethod
from typing import Optional
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.entity.ClientSecretEntity import ClientSecretEntity
from src.domain.v1.type.ClientValueType import ApplicationId, SecretId

class ClientSecretRepository(ABC):

    @abstractmethod
    def insert(entity: ClientSecretEntity) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(id: RecordId) -> Optional[ClientSecretEntity]:
        raise NotImplementedError

    @abstractmethod
    def find_by_application(application_id: ApplicationId) -> Optional[ClientSecretEntity]:
        raise NotImplementedError

    
    