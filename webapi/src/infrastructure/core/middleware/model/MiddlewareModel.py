from pydantic import BaseModel
    
class Authorization(BaseModel):
    access_token: str
    required_scopes: list[str]