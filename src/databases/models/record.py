import uuid
import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from databases.settings.database import Base


class Record(Base):
    __tablename__ = 'records'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    started_at = Column(DateTime)
    stopped_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
