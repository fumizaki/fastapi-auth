from abc import ABC, abstractmethod
from typing import Optional
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.entity.ClientApplicationMemberEntity import ClientApplicationMemberEntity
from src.domain.v1.type.ClientValueType import ApplicationId
from src.domain.v1.type.AccountValueType import AccountId

class ClientApplicationMemberRepository(ABC):

    @abstractmethod
    def insert(entity: ClientApplicationMemberEntity) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(id: RecordId) -> Optional[ClientApplicationMemberEntity]:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_application_and_account(application_id: ApplicationId, account_id: AccountId) -> Optional[ClientApplicationMemberEntity]:
        raise NotImplementedError
    
    
    @abstractmethod
    def find_list_by_account(account_id: AccountId) -> list[Optional[ClientApplicationMemberEntity]]:
        raise NotImplementedError

    @abstractmethod
    def find_list_by_application(application_id: ApplicationId) -> list[Optional[ClientApplicationMemberEntity]]:
        raise NotImplementedError

    
    