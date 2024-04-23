from sqlalchemy import DateTime, Column
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.sql import func

class TimestampMixin:
    
    @declared_attr
    def created_at(cls):
        return Column(
            DateTime,
            default = func.now(),
            nullable = False
        )
    
    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            default = func.now(),
            onupdate = func.now(),
            nullable = False
        )


class CoreTable(DeclarativeBase, TimestampMixin):
    pass
