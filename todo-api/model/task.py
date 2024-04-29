from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from .base import Base


class Task(Base):
    __tablename__ = "Task"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[str] = mapped_column(nullable=False)

    def __init__(self, content: str):
        self.content = content
        self.timestamp = datetime.now().isoformat()
