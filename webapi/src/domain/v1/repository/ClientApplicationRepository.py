from abc import ABC, abstractmethod
from typing import Optional
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.entity.ClientApplicationEntity import ClientApplicationEntity
from src.domain.v1.type.ClientValueType import ApplicationId

class ClientApplicationRepository(ABC):

    @abstractmethod
    def insert(entity: ClientApplicationEntity) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def find_list() -> list[Optional[ClientApplicationEntity]]:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(id: RecordId) -> Optional[ClientApplicationEntity]:
        raise NotImplementedError

    
    