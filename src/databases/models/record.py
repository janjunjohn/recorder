import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from databases.settings.database import Base

class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True, index=True)
    started_time = Column(DateTime)
    stopped_time = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
