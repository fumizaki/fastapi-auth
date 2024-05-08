import pytest
from src.domain.v1.repository.ClientApplicationMemberRepository import ClientApplicationMemberRepository
from src.domain.v1.entity.ClientApplicationMemberEntity import ClientApplicationMemberEntity
# from src.infrastructure.postgresql.repository.v1.ClientApplicationRepositoryImpl import ClientApplicationRepositoryImpl

class NotImplementedRepository(ClientApplicationMemberRepository):
    pass


def test_repository_not_implemented():
    with pytest.raises(TypeError):
        NotImplementedRepository()


def test_repository_abstract_method():
    
    with pytest.raises(NotImplementedError):
        ClientApplicationMemberRepository.insert(ClientApplicationMemberEntity(application_id = "", account_id = ""))

    with pytest.raises(NotImplementedError):
        ClientApplicationMemberRepository.find_by_id("")

    with pytest.raises(NotImplementedError):
        ClientApplicationMemberRepository.find_by_application_and_account("", "")

    with pytest.raises(NotImplementedError):
        ClientApplicationMemberRepository.find_list_by_account("")

    with pytest.raises(NotImplementedError):
        ClientApplicationMemberRepository.find_list_by_application("")

    with pytest.raises(NotImplementedError):
        ClientApplicationMemberRepository.delete("")

    
    

    

    

  

