from pydantic import BaseModel


class CoreSchema(BaseModel):
    class ConfigDict:
        frozen = True
        from_attributes = True
        arbitrary_types_allowed = True
        validate_assignment = True
