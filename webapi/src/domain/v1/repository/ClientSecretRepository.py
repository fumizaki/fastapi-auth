from abc import ABC, abstractmethod
from typing import Optional
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.entity.ClientSecretEntity import ClientSecretEntity
from src.domain.v1.type.ClientValueType import ApplicationId, SecretValue

class ClientSecretRepository(ABC):

    @abstractmethod
    def insert(entity: ClientSecretEntity) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(id: RecordId) -> Optional[ClientSecretEntity]:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_secret(secret: SecretValue) -> Optional[ClientSecretEntity]:
        raise NotImplementedError

    @abstractmethod
    def find_list_by_application(application_id: ApplicationId) -> list[Optional[ClientSecretEntity]]:
        raise NotImplementedError

    
    