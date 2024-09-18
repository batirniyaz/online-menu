import datetime
from typing import List

from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.auth.database import Base
from app.models.product import Product


class SubCategory(Base):
    __tablename__ = "sub_category"

    id: Mapped[int]= mapped_column(Integer, unique=True, index=True, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    products: Mapped[List["Product"]] = relationship(back_populates="sub_category", lazy="selectin")

    category = relationship("Category", back_populates="sub_categories")

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
