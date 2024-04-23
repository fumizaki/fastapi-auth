from typing import Optional
from datetime import datetime
from src.domain.core.schema.CoreSchema import CoreSchema


class CoreEntity(CoreSchema):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None