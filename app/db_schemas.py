from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class TaskDBSchema(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String)
    creation_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    status = Column(String)
