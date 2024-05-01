import pytest
from src.domain.v1.repository.AccountRepository import AccountRepository
from src.domain.v1.entity.AccountEntity import AccountEntity
from src.infrastructure.postgresql.repository.v1.AccountRepositoryImpl import AccountRepositoryImpl

class NotImplementedRepository(AccountRepository):
    pass


def test_repository_not_implemented():
    with pytest.raises(TypeError):
        NotImplementedRepository()


def test_repository_abstract_method():
    
    with pytest.raises(NotImplementedError):
        AccountRepository.insert(AccountEntity(email = "", password = ""))

    with pytest.raises(NotImplementedError):
        AccountRepository.find_by_id("")

    with pytest.raises(NotImplementedError):
        AccountRepository.find_by_email("")


def test_repository_insert(rdb):
    _repository = AccountRepositoryImpl(rdb)
    result = _repository.insert(AccountEntity(email = "", password = ""))
    assert isinstance(result, None.__class__)    


@pytest.mark.parametrize(
    "expected, id",
    [
        (None.__class__, ""),
    ]
)
def test_repository_find_by_id(rdb, expected, id):
    _repository = AccountRepositoryImpl(rdb)
    result = _repository.find_by_id(id)
    assert isinstance(result, expected)    

