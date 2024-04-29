from sqlalchemy import Column, Integer, String, Base
from datetime import datetime
from .base import Base


class Task(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)

    def __init__(self, content: str):
        self.content = content
        self.timestamp = datetime.now().isoformat()
