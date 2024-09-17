import datetime
from typing import List, Dict
import uuid

from sqlalchemy import Integer, TIMESTAMP, JSON, Column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.auth.database import Base


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False, primary_key=True)
    uuid = Column(PG_UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    products: Mapped[List[Dict]] = mapped_column(JSON, default=[])

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                            default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                            onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

