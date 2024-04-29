from abc import ABC, abstractmethod
from typing import Optional
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.entity.AccountSecretEntity import AccountSecretEntity
from src.domain.v1.type.AccountValueType import AccountId, AccountSecretId

class AccountSecretRepository(ABC):

    @abstractmethod
    def insert(entity: AccountSecretEntity) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(id: RecordId) -> Optional[AccountSecretEntity]:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_account(account_id: AccountId) -> Optional[AccountSecretEntity]:
        raise NotImplementedError
    
    