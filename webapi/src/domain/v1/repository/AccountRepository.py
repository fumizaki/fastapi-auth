from abc import ABC, abstractmethod
from typing import Optional
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.entity.AccountEntity import AccountEntity
from src.domain.v1.type.AccountValueType import AccountEmail

class AccountRepository(ABC):

    @abstractmethod
    def insert(entity: AccountEntity) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(id: RecordId) -> Optional[AccountEntity]:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_email(email: AccountEmail) -> Optional[AccountEntity]:
        raise NotImplementedError