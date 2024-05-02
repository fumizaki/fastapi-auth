from typing import Optional
from src.domain.v1.schema.AuthenticationSchema import SignUpSchema, SignInSchema
from src.domain.v1.entity.AccountEntity import AccountEntity
from src.domain.v1.entity.AccountSecretEntity import AccountSecretEntity
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.type.AccountValueType import AccountEmail, AccountPassword, AccountCategoryType
from src.domain.v1.repository.AccountRepository import AccountRepository
from src.domain.v1.repository.AccountSecretRepository import AccountSecretRepository
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.exception.RdbException import RdbContraintError
from src.infrastructure.core.hash.util.HashClient import HashClient


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
        
        def _get_account(id: RecordId) -> AccountEntity:
            account_in_db: Optional[AccountEntity] = self.uow.account_repository.find_by_id(id)
            if account_in_db is None:
                raise ValueError("Account not found")
            return account_in_db
        
        def _insert_account(account: AccountEntity) -> RecordId:
            try:
                self.uow.account_repository.insert(account)
                return account.id
            
            # TODO: PK重複エラーとその他のエラーを分ける
            except RdbContraintError as e:
                # TODO: PK重複エラーの場合、EntityのIDを再生成して再挿入
                account.reset_id()
                _insert_account(account)
            
        def _insert_account_secret(account_secret: AccountSecretEntity) -> RecordId:
            try:
                self.uow.account_secret_repository.insert(account_secret)
                return account_secret.id    
            
            # TODO: PK重複エラーとその他のエラーを分ける
            except RdbContraintError as e:
                # TODO: PK重複エラーの場合、EntityのIDを再生成して再挿入
                account_secret.reset_id()
                _insert_account_secret(account_secret)

        
        try:
            account = AccountEntity(
                email=AccountEmail(param.email),
                password=AccountPassword(param.password)
            )
            account_id = _insert_account(account)
            
            salt = HashClient.salt()
            stretching = HashClient.stretching()
            account_secret = AccountSecretEntity(
                account_id=account_id,
                password=HashClient.hash(param.password, salt, stretching),
                salt=salt,
                stretching=stretching
            )

            _insert_account_secret(account_secret)
                
            self.uow.rdb.commit()
            return _get_account(account_id)
        
        finally:
            self.uow.rdb.close()
            
            
    def v1_signin_exec(self, param: SignInSchema) -> AccountEntity:
        try:
            account_in_db: Optional[AccountEntity] = self.uow.account_repository.find_by_email(param.email)
            if account_in_db is None:
                raise Exception("Account not found")
            
            if account_in_db.category == AccountCategoryType.OAUTH:
                raise Exception(f"Account is {AccountCategoryType.OAUTH}")
            
            account_secret: Optional[AccountSecretEntity] = self.uow.account_secret_repository.find_by_account(account_in_db.id)
        
            if account_secret is None:
                raise Exception("AccountSecret not found")
        
            if HashClient.verify(param.password, account_secret.salt, account_secret.stretching, account_secret.password):
                raise Exception("Password is incorrect")
            
            return account_in_db
        
        finally:
            self.uow.rdb.close()