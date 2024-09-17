import datetime
from typing import List, Dict
from uuid import uuid4 as uuid

from sqlalchemy import Integer, TIMESTAMP, JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.auth.database import Base


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False, primary_key=True)
    uuid: Mapped[uuid] = mapped_column(UUID(as_uuid=True), default=uuid, nullable=False)
    products: Mapped[List[Dict]] = mapped_column(JSON, default=[])

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                            default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                            default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                            onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

