from src.domain.v1.schema.AuthenticationSchema import SignUpSchema
from src.domain.v1.entity.AccountEntity import AccountEntity
from src.domain.v1.type.AccountValueType import AccountEmail, AccountPassword
from src.domain.v1.repository.AccountRepository import AccountRepository
from src.infrastructure.core.rdb.RdbSessionClient import RdbSessionClient

class AuthenticationUsecase:

    class UnitOfWork:
        def __init__(
            self,
            rdb: RdbSessionClient,
            account_repository: AccountRepository
        ) -> None:
            self.rdb = rdb
            self.account_repository = account_repository


    def __init__(
        self,
        rdb: RdbSessionClient,
        account_repository: AccountRepository
    ) -> None:
        self.uow = self.UnitOfWork(
            rdb,
            account_repository
        )
    
    def v1_signup_exec(self, param: SignUpSchema) -> AccountEntity:
        try:
            account = AccountEntity(
                email=AccountEmail(param.email),
                password=AccountPassword(param.password)
            )
            account_in_db = self.uow.account_repository.insert(account)
            self.uow.rdb.commit()
            return account_in_db
        
        finally:
            self.uow.rdb.close()