import pytest
from src.domain.v1.repository.AccountSecretRepository import AccountSecretRepository
from src.domain.v1.entity.AccountSecretEntity import AccountSecretEntity
from src.infrastructure.postgresql.repository.v1.AccountSecretRepositoryImpl import AccountSecretRepositoryImpl

class NotImplementedRepository(AccountSecretRepository):
    pass


def test_repository_not_implemented():
    with pytest.raises(TypeError):
        NotImplementedRepository()


def test_repository_abstract_method():
    
    with pytest.raises(NotImplementedError):
        AccountSecretRepository.insert(AccountSecretEntity(account_id = "", password = "", salt="", stretching=10))

    with pytest.raises(NotImplementedError):
        AccountSecretRepository.find_by_id("")


def test_repository_insert(rdb):
    _repository = AccountSecretRepositoryImpl(rdb)
    result = _repository.insert(AccountSecretEntity(account_id = "", password = "", salt="", stretching=10))
    assert isinstance(result, None.__class__)    


@pytest.mark.parametrize(
    "expected, id",
    [
        (None.__class__, ""),
    ]
)
def test_repository_find_by_id(rdb, expected, id):
    _repository = AccountSecretRepositoryImpl(rdb)
    result = _repository.find_by_id(id)
    assert isinstance(result, expected)  
    
    
@pytest.mark.parametrize(
    "expected, account_id",
    [
        (None.__class__, ""),
    ]
)
def test_repository_find_by_account(rdb, expected, account_id):
    _repository = AccountSecretRepositoryImpl(rdb)
    result = _repository.find_by_account(account_id)
    assert isinstance(result, expected)    

