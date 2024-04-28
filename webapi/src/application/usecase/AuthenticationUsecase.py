from src.domain.v1.schema.AuthenticationSchema import SignUpSchema
from src.domain.v1.entity.AccountEntity import AccountEntity
from src.domain.v1.entity.AccountSecretEntity import AccountSecretEntity
from src.domain.v1.type.AccountValueType import AccountEmail, AccountPassword
from src.domain.v1.repository.AccountRepository import AccountRepository
from src.domain.v1.repository.AccountSecretRepository import AccountSecretRepository
from src.infrastructure.core.rdb.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.hash.HashClient import HashClient


class AuthenticationUsecase:

    class UnitOfWork:
        def __init__(
            self,
            rdb: RdbSessionClient,
            account_repository: AccountRepository,
            account_secret_repository: AccountSecretRepository
        ) -> None:
            self.rdb = rdb
            self.account_repository = account_repository
            self.account_secret_repository = account_secret_repository


    def __init__(
        self,
        rdb: RdbSessionClient,
        account_repository: AccountRepository,
        account_secret_repository: AccountSecretRepository
    ) -> None:
        self.uow = self.UnitOfWork(
            rdb,
            account_repository,
            account_secret_repository
        )
    
    def v1_signup_exec(self, param: SignUpSchema) -> AccountEntity:
        try:
            account = AccountEntity(
                email=AccountEmail(param.email),
                password=AccountPassword(param.password)
            )
            account_in_db: AccountEntity = self.uow.account_repository.insert(account)
            
            salt = HashClient.salt()
            stretching = HashClient.stretching()
            account_secret = AccountSecretEntity(
                account_id=account_in_db.id,
                password=HashClient.hash(param.password, salt, stretching),
                salt=salt,
                stretching=stretching
            )
            
            account_secret_in_db: AccountSecretEntity = self.uow.account_secret_repository.insert(account_secret)
            
            
            self.uow.rdb.commit()
            return account_in_db
        
        finally:
            self.uow.rdb.close()