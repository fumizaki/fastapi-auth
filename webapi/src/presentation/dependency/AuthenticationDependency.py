from src.application.usecase.AuthenticationUsecase import AuthenticationUsecase
from src.application.usecase.v1.AuthenticationUsecaseImpl import AuthenticationUsecaseImpl as V1AuthenticationUsecaseImpl


class AuthenticationDependency:
    
    @staticmethod
    def v1_injection() -> AuthenticationUsecase:
        return V1AuthenticationUsecaseImpl()
    
    @staticmethod
    def v1() -> AuthenticationUsecase:
        return AuthenticationDependency.v1_injection()