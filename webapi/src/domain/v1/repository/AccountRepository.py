from abc import ABC, abstractmethod
from typing import Optional
from src.domain.v1.entity.AccountEntity import AccountEntity
from src.domain.v1.type.AccountValueType import AccountId

class AccountRepository(ABC):

    @abstractmethod
    def insert(entity: AccountEntity) -> AccountEntity:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(id: AccountId) -> Optional[AccountEntity]:
        raise NotImplementedError