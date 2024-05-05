from typing import Optional
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.type.AccountValueType import AccountEmail, AccountPassword, AccountCategoryType
from src.domain.v1.type.ClientValueType import ApplicationRoleType
from src.domain.v1.schema.AuthenticationSchema import SignUpSchema, SignInSchema
from src.domain.v1.entity.AccountEntity import AccountEntity
from src.domain.v1.entity.AccountSecretEntity import AccountSecretEntity
from src.domain.v1.entity.ClientApplicationEntity import ClientApplicationEntity
from src.domain.v1.entity.ClientApplicationMemberEntity import ClientApplicationMemberEntity
from src.domain.v1.entity.ClientSecretEntity import ClientSecretEntity
from src.domain.v1.repository.ClientApplicationRepository import ClientApplicationRepository
from src.domain.v1.repository.ClientSecretRepository import ClientSecretRepository
from src.domain.v1.repository.ClientApplicationMemberRepository import ClientApplicationMemberRepository
from src.domain.v1.repository.AccountRepository import AccountRepository
from src.domain.v1.repository.AccountSecretRepository import AccountSecretRepository
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.exception.RdbException import RdbContraintError
from src.infrastructure.core.auth.util.OAuth2Client import OAuth2Client
from src.infrastructure.core.hash.util.HashClient import HashClient


class AuthenticationUsecase:

    class UnitOfWork:
        def __init__(
            self,
            rdb: RdbSessionClient,
            account_repository: AccountRepository,
            account_secret_repository: AccountSecretRepository,
            client_application_repository: ClientApplicationRepository,
            client_secret_repository: ClientSecretRepository,
            client_application_member_repository: ClientApplicationMemberRepository
        ) -> None:
            self.rdb = rdb
            self.account_repository = account_repository
            self.account_secret_repository = account_secret_repository
            self.client_application_repository = client_application_repository
            self.client_secret_repository = client_secret_repository
            self.client_application_member_repository = client_application_member_repository


    def __init__(
        self,
        rdb: RdbSessionClient,
        account_repository: AccountRepository,
        account_secret_repository: AccountSecretRepository,
        client_application_repository: ClientApplicationRepository,
        client_secret_repository: ClientSecretRepository,
        client_application_member_repository: ClientApplicationMemberRepository
    ) -> None:
        self.uow = self.UnitOfWork(
            rdb,
            account_repository,
            account_secret_repository,
            client_application_repository,
            client_secret_repository,
            client_application_member_repository
        )
    
    def v1_signup_exec(self, param: SignUpSchema) -> AccountEntity:
        
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

        def _insert_client_application_member(client_application_member: ClientApplicationMemberEntity) -> RecordId:
            try:
                self.uow.client_application_member_repository.insert(client_application_member)
                return client_application_member.id    
            
            # TODO: PK重複エラーとその他のエラーを分ける
            except RdbContraintError as e:
                # TODO: PK重複エラーの場合、EntityのIDを再生成して再挿入
                client_application_member.reset_id()
                _insert_client_application_member(client_application_member)

        
        try:
            client_application_in_db: Optional[ClientApplicationEntity] = self.uow.client_application_repository.find_by_id(param.client_id)
            if client_application_in_db is None:
                raise

            client_secret_in_db: Optional[ClientSecretEntity] = self.uow.client_secret_repository.find_by_secret(param.client_secret)
            if client_secret_in_db is None:
                raise

            if not OAuth2Client.is_effective(client_secret_in_db.expires_in):
                raise

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

            client_application_member = ClientApplicationMemberEntity(
                application_id=param.client_id,
                account_id=account_id,
                role=ApplicationRoleType.GUEST
            )
            _insert_client_application_member(client_application_member)
                
            self.uow.rdb.commit()
            
            account_in_db: Optional[AccountEntity] = self.uow.account_repository.find_by_id(id)
            if account_in_db is None:
                raise ValueError("Account not found")
            
            return account_in_db
        
        finally:
            self.uow.rdb.close()
            
            
    def v1_signin_exec(self, param: SignInSchema) -> AccountEntity:
        try:
            client_application_in_db: Optional[ClientApplicationEntity] = self.uow.client_application_repository.find_by_id(param.client_id)
            if client_application_in_db is None:
                raise

            client_secret_in_db: Optional[ClientSecretEntity] = self.uow.client_secret_repository.find_by_secret(param.client_secret)
            if client_secret_in_db is None:
                raise

            if not OAuth2Client.is_effective(client_secret_in_db.expires_in):
                raise

            account_in_db: Optional[AccountEntity] = self.uow.account_repository.find_by_email(param.email)
            if account_in_db is None:
                raise Exception("Account not found")
            

            client_application_member_in_db: Optional[ClientApplicationMemberEntity] = self.uow.client_application_member_repository.find_by_application_and_account(param.client_id, account_in_db.id)
            if client_application_member_in_db is None:
                raise
            
            if account_in_db.category == AccountCategoryType.OAUTH:
                raise Exception(f"Account is {AccountCategoryType.OAUTH}")
            
            account_secret_in_db: Optional[AccountSecretEntity] = self.uow.account_secret_repository.find_by_account(account_in_db.id)
            if account_secret_in_db is None:
                raise Exception("AccountSecret not found")
        
            if HashClient.verify(param.password, account_secret_in_db.salt, account_secret_in_db.stretching, account_secret_in_db.password):
                raise Exception("Password is incorrect")
            
            return account_in_db
        
        finally:
            self.uow.rdb.close()