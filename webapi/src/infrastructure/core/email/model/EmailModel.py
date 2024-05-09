from typing import Optional
from pydantic import BaseModel
from src.domain.v1.type.AccountValueType import (
    AccountEmail
)

class SendEmailProps(BaseModel):
    to: list[AccountEmail]
    subject: str
    cc: Optional[list[AccountEmail]] = None
    bcc: Optional[list[AccountEmail]] = None
    reply_to: Optional[list[AccountEmail]] = None
    headers: Optional[dict[str, str]] = None
    attachiments: Optional[list[str]] = None
    


class SendHTMLEmailProps(SendEmailProps):
    html: str
    
    
class SendTextEmailProps(SendEmailProps):
    text: str