import uuid
from typing import Optional
from datetime import datetime
from src.domain.core.type.CoreValueType import RecordId
from src.domain.core.schema.CoreSchema import CoreSchema


class CoreEntity(CoreSchema):
    id: RecordId = str(uuid.uuid4())
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None