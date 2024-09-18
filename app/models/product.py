import datetime
from typing import List

from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.auth.database import Base
from app.models.option import Option


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(length=255), nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    image: Mapped[str] = mapped_column(String(length=255), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    sub_category_id: Mapped[int] = mapped_column(ForeignKey("sub_category.id"), nullable=False)
    options: Mapped[List["Option"]] = relationship(back_populates="product", lazy="selectin")

    sub_category = relationship("SubCategory", back_populates="products")

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))