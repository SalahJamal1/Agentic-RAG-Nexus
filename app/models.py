from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped,mapped_column
from app.database import Base




class Notes(Base):
    __tablename__="notes"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    content:Mapped[str]=mapped_column(String(255),nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc)
    )

