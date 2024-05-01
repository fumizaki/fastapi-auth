import pytest
from src.domain.v1.repository.ClientApplicationRepository import ClientApplicationRepository
from src.domain.v1.entity.ClientApplicationEntity import ClientApplicationEntity
# from src.infrastructure.postgresql.repository.v1.ClientApplicationRepositoryImpl import ClientApplicationRepositoryImpl

class NotImplementedRepository(ClientApplicationRepository):
    pass


def test_repository_not_implemented():
    with pytest.raises(TypeError):
        NotImplementedRepository()


def test_repository_abstract_method():
    
    with pytest.raises(NotImplementedError):
        ClientApplicationRepository.insert(ClientApplicationEntity(name = "", scope = "", redirect_uri = ""))

    with pytest.raises(NotImplementedError):
        ClientApplicationRepository.find_list()

    with pytest.raises(NotImplementedError):
        ClientApplicationRepository.find_by_id("")

  

