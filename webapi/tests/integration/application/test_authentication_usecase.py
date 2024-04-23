import pytest
from src.application.usecase.AuthenticationUsecase import AuthenticationUsecase


class NotImplementedUsecase(AuthenticationUsecase):
    pass


def test_authentication_usecase_not_impl():
    with pytest.raises(TypeError):
        NotImplementedUsecase()
        


def test_abstract_signup():
    param = {"email": "test@test.com", "password": "testtesttest"}
    with pytest.raises(NotImplementedError):
        AuthenticationUsecase.signup_exec(param)

    
    

        