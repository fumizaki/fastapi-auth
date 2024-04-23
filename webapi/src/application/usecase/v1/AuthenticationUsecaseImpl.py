from src.application.usecase.AuthenticationUsecase import AuthenticationUsecase
from src.domain.v1.schema.AuthenticationSchema import SignUpSchema
from src.domain.v1.entity.AccountEntity import AccountEntity
from src.domain.v1.type.AccountValueType import AccountEmail, AccountPassword, AccountCategoryType, AccountRoleType


class AuthenticationUsecaseImpl(AuthenticationUsecase):
    
    def signup_exec(self, param: SignUpSchema) -> AccountEntity:
        account = AccountEntity(
            category=AccountCategoryType.APP,
            role=AccountRoleType.GENERAL,
            email=AccountEmail(param.email),
            password=AccountPassword(param.password)
        )
        return account
