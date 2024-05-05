from pydantic import Field, field_validator
from src.domain.core.schema.CoreSchema import CoreSchema
from src.domain.v1.type.AccountValueType import AccountEmail, AccountPassword
from src.domain.v1.type.ClientValueType import ApplicationId, SecretValue

class CredentialSchema(CoreSchema):
    client_id: ApplicationId
    client_secret: SecretValue
    email: AccountEmail
    password: AccountPassword = Field(..., min_length = 8, max_length = 128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not "@" in value:
            raise ValueError("Invalid email format")
        return value
    
    
class SignInSchema(CredentialSchema):
    pass

class SignUpSchema(CredentialSchema):
    pass
    