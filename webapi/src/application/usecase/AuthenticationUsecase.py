from abc import ABC, abstractmethod
from src.domain.v1.schema.AuthenticationSchema import SignUpSchema
from src.domain.v1.entity.AccountEntity import AccountEntity

class AuthenticationUsecase(ABC):
    
    @abstractmethod
    def signup_exec(param: SignUpSchema) -> AccountEntity:
        raise NotImplementedError()