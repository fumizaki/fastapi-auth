import pytest
from src.domain.v1.repository.AccountRepository import AccountRepository
from src.domain.v1.entity.AccountEntity import AccountEntity

class NotImplementedRepository(AccountRepository):
    pass


def test_account_repository_not_implemented():
    with pytest.raises(TypeError):
        NotImplementedRepository()


def test_account_repository_abstract_method():
    
    with pytest.raises(NotImplementedError):
        AccountRepository.insert(AccountEntity(email = "", password = ""))

    with pytest.raises(NotImplementedError):
        AccountRepository.find_by_id("")




