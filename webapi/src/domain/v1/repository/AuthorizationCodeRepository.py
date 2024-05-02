from abc import ABC, abstractmethod
from typing import Optional
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.entity.AuthorizationCodeEntity import AuthorizationCodeEntity

class AuthorizationCodeRepository(ABC):

    @abstractmethod
    def insert(entity: AuthorizationCodeEntity) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(id: RecordId) -> Optional[AuthorizationCodeEntity]:
        raise NotImplementedError
    
