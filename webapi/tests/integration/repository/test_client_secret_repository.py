import pytest
from src.domain.v1.repository.ClientSecretRepository import ClientSecretRepository
from src.domain.v1.entity.ClientSecretEntity import ClientSecretEntity
# from src.infrastructure.postgresql.repository.v1.ClientSecretRepositoryImpl import ClientSecretRepositoryImpl

class NotImplementedRepository(ClientSecretRepository):
    pass


def test_repository_not_implemented():
    with pytest.raises(TypeError):
        NotImplementedRepository()


def test_repository_abstract_method():
    
    with pytest.raises(NotImplementedError):
        ClientSecretRepository.insert(ClientSecretEntity(application_id = "", title = "", secret = "", expires_in = 0))

    with pytest.raises(NotImplementedError):
        ClientSecretRepository.find_by_id("")

    with pytest.raises(NotImplementedError):
        ClientSecretRepository.find_list_by_application("")

    with pytest.raises(NotImplementedError):
        ClientSecretRepository.update(ClientSecretEntity(application_id = "", title = "", secret = "", expires_in = 0))
    
    with pytest.raises(NotImplementedError):
        ClientSecretRepository.delete("")
  

